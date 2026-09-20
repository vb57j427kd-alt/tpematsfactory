# -*- coding: utf-8 -*-
"""
Regression check for generate.py.

Builds the site twice:
  pass 1 - the real data layer (may be empty)
  pass 2 - a synthetic sample injected in memory only, so vehicle pages,
           fitment blocks and vehicles.json get exercised even while the real
           mould list is still pending.
The sample is NEVER written into products_data.py.

Run:  python _verify_generate.py
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import products_data as pd          # noqa: E402
import generate as g                # noqa: E402

SAMPLE_PRODUCTS = [
    {
        "slug": "sample-honda-cr-v-liner", "cat": "floor-liners",
        "name": "Sample 3D TPE Floor Liners for Honda CR-V 2017-2026 - Full Set",
        "badge": "Sample", "price": "$0.00 - $0.00 / set", "moq": "MOQ 0 sets",
        "img": "/images/sample-honda-cr-v-liner.jpg", "src": "",
        "fitment": {"make": "Honda", "model": "CR-V", "years": "2017-2026", "body": "SUV",
                    "hand": "LHD", "positions": ["Front Row", "2nd Row"]},
        "desc": "Sample description used only by the generator regression test. " * 3,
        "specs": [("Material", "TPE"), ("Thickness", "0 mm"), ("Coverage", "3D"),
                  ("Fixing", "OE posts"), ("Color", "Black"), ("MOQ", "0 sets")],
        "points": ["sample point one", "sample point two", "sample point three"],
        "related": [],
    },
    {
        "slug": "sample-model-y-cargo-liner", "cat": "trunk-mats",
        "name": "Sample TPE Cargo Liner for Tesla Model Y 2020-2026",
        "badge": "Sample", "price": "$0.00 - $0.00 / set", "moq": "MOQ 0 sets",
        "img": "/images/sample-model-y-cargo-liner.jpg", "src": "",
        "fitment": {"make": "Tesla", "model": "Model Y", "years": "2020-2026", "body": "SUV",
                    "hand": "Both", "positions": ["Trunk"]},
        "desc": "Sample description used only by the generator regression test. " * 3,
        "specs": [("Material", "TPE"), ("Thickness", "0 mm"), ("Coverage", "Cargo area"),
                  ("Fixing", "Anti-slip nibs"), ("Color", "Black"), ("MOQ", "0 sets")],
        "points": ["sample point one", "sample point two", "sample point three"],
        "related": ["sample-honda-cr-v-liner"],
    },
]
SAMPLE_VEHICLES = [
    {"slug": "sample-honda-cr-v", "make": "Honda", "model": "CR-V", "years": "2017-2026",
     "body": "SUV", "hand": "LHD", "positions": ["Front Row", "2nd Row"],
     "note": "sample note", "products": ["sample-honda-cr-v-liner"]},
    {"slug": "sample-tesla-model-y", "make": "Tesla", "model": "Model Y", "years": "2020-2026",
     "body": "SUV", "hand": "Both", "positions": ["Trunk"],
     "note": "", "products": ["sample-model-y-cargo-liner"]},
    # second Honda: exercises the "Other Honda Models" sibling block, and has
    # zero linked products so the empty-vehicle state is exercised too.
    {"slug": "sample-honda-civic", "make": "Honda", "model": "Civic", "years": "2016-2022",
     "body": "Sedan", "hand": "LHD", "positions": ["Front Row"],
     "note": "", "products": []},
]

fails = []


def check(label, ok, detail=""):
    print(("  PASS  " if ok else "  FAIL  ") + label + ((" -> " + str(detail)) if detail else ""))
    if not ok:
        fails.append(label)


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def build(with_sample):
    out = tempfile.mkdtemp(prefix="tmf_build_")
    if with_sample:
        pd.PRODUCTS[:] = []
        pd.VEHICLES[:] = []
        pd.PRODUCTS.extend(SAMPLE_PRODUCTS)
        pd.VEHICLES.extend(SAMPLE_VEHICLES)
        pd.RELATED_INDEX.clear()
        pd.RELATED_INDEX.update({p["slug"]: p for p in pd.PRODUCTS})
        pd.VEHICLE_INDEX.clear()
        pd.VEHICLE_INDEX.update({v["slug"]: v for v in pd.VEHICLES})
        g.PRODUCTS = pd.PRODUCTS
        g.VEHICLES = pd.VEHICLES
        g.RELATED_INDEX = pd.RELATED_INDEX
        g.VEHICLE_INDEX = pd.VEHICLE_INDEX
    g.BASE = out
    print("\n== building " + ("WITH sample data" if with_sample else "with the real data layer"))
    g.main()
    return out


def jsonld_blocks(html):
    return re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)


def inline_js_blocks(html):
    """Inline <script> bodies that are not JSON-LD and not external includes."""
    found = re.findall(r'<script(?![^>]*application/ld\+json)[^>]*>(.*?)</script>', html, re.S)
    return [b for b in found if b.strip()]


def check_inline_js(root, tmp):
    """Syntax-check every inline script with node --check.

    Added because a raw (unquoted) substitution into a JS string literal made
    the whole quote modal a SyntaxError on every page while the rest of the
    suite stayed green - a page can be structurally perfect and still dead.
    """
    node = shutil.which("node")
    if not node:
        return None
    bad = []
    for dirpath, _dirs, files in os.walk(root):
        for fn in files:
            if not fn.endswith(".html"):
                continue
            rel = os.path.relpath(os.path.join(dirpath, fn), root)
            for i, block in enumerate(inline_js_blocks(read(os.path.join(dirpath, fn)))):
                path = os.path.join(tmp, "chk.js")
                with open(path, "w", encoding="utf-8") as fh:
                    fh.write(block)
                res = subprocess.run([node, "--check", path], capture_output=True, text=True)
                if res.returncode != 0:
                    first = (res.stderr or "").strip().splitlines()
                    bad.append((rel, i, first[0] if first else "syntax error"))
    return bad


# ---------------------------------------------------------------- pass 1
real = build(False)
print("\n-- pass 1 checks (real data layer)")
check("index.html written", os.path.isfile(os.path.join(real, "index.html")))
check("products/ dir exists even with an empty catalogue", os.path.isdir(os.path.join(real, "products")))
check("shop-by-vehicle/index.html written", os.path.isfile(os.path.join(real, "shop-by-vehicle", "index.html")))
check("4 category dirs written", all(os.path.isfile(os.path.join(real, c["id"], "index.html")) for c in pd.CATEGORIES))
check("CNAME == domain", read(os.path.join(real, "CNAME")).strip() == pd.SITE["domain"])
check("robots.txt points at sitemap", "Sitemap: https://" + pd.SITE["domain"] + "/sitemap.xml" in read(os.path.join(real, "robots.txt")))
check("404.html written", os.path.isfile(os.path.join(real, "404.html")))
check("vehicles.json is valid JSON", isinstance(json.loads(read(os.path.join(real, "vehicles.json"))), list))
home = read(os.path.join(real, "index.html"))
check("home has finder select ids", all(x in home for x in ('id="fYear"', 'id="fMake"', 'id="fModel"')))
check("home loads vehicles.json", "fetch('https://" + pd.SITE["domain"] + "/vehicles.json')" in home)
check("no placeholder analytics injected", "googletagmanager" not in home and "clarity.ms" not in home)
check("no formspree id injected", "formspree.io" not in home)
check("og:image omitted when no product image", 'property="og:image"' not in home)
sm = read(os.path.join(real, "sitemap.xml"))
check("sitemap has home at 1.0", "<priority>1.0</priority>" in sm)
check("sitemap 0.9 tier = 4 categories + vehicle index + vehicle pages",
      sm.count("<priority>0.9</priority>") == 5 + len(pd.VEHICLES), sm.count("<priority>0.9</priority>"))

# ---------------------------------------------------------------- pass 2
sample = build(True)
print("\n-- pass 2 checks (synthetic sample)")
vpage = os.path.join(sample, "shop-by-vehicle", "honda", "cr-v", "index.html")
ppage = os.path.join(sample, "products", "sample-honda-cr-v-liner", "index.html")
check("vehicle page at /shop-by-vehicle/honda/cr-v/", os.path.isfile(vpage))
check("product page at /products/{slug}/", os.path.isfile(ppage))
home2 = read(os.path.join(sample, "index.html"))
vh = read(vpage)
ph = read(ppage)
check("vehicle page breadcrumb", "Shop by Vehicle" in vh and "&rsaquo;" in vh)
check("vehicle page H1 carries make+model+years", "Honda CR-V 2017-2026" in vh)
check("vehicle page lists its product", "/products/sample-honda-cr-v-liner/" in vh)
check("vehicle page cross-links its siblings", "Other Honda Models" in vh and "/shop-by-vehicle/honda/civic/" in vh)
check("home nav dropdown lists vehicle models", "/shop-by-vehicle/honda/cr-v/" in home2)
civic = read(os.path.join(sample, "shop-by-vehicle", "honda", "civic", "index.html"))
check("vehicle with 0 linked products shows the ask-for-quote state",
      "Send us your model and year" in civic and "Tooling confirmed" not in civic)
check("vehicle URL slugifies safely", os.path.isfile(os.path.join(sample, "shop-by-vehicle", "honda", "civic", "index.html")))
check("reserved characters are neutralised in URLs",
      g.slugify("Mercedes-Benz: V-Class") == "mercedes-benz-v-class", g.slugify("Mercedes-Benz: V-Class"))
check("degenerate make/model cannot collapse to ///",
      g.vurl({"make": "日本", "model": "..."}) == "/shop-by-vehicle/vehicle/model/",
      g.vurl({"make": "日本", "model": "..."}))
_saved_v = g.VEHICLES
g.VEHICLES = [{"make": "Honda", "model": "CR-V", "years": "2020"},
              {"make": "Honda", "model": "CR V", "years": "2021"}]
try:
    g.check_unique_vehicle_urls()
    dup_ok = False
except ValueError:
    dup_ok = True
g.VEHICLES = _saved_v
check("colliding vehicle URLs raise instead of overwriting silently", dup_ok)
check("brand is quoted inside the emitted JS (no bare identifier)", "+TPE Mats Factory+" not in read(os.path.join(sample, "index.html")))
check("product page has Vehicle Fitment block", "Vehicle Fitment" in ph)
check("product page fitment shows years", "2017-2026" in ph)
check("product page links back to vehicle page", "/shop-by-vehicle/honda/cr-v/" in ph)
check("product page has both CTAs", "openQuote(" in ph and "wa.me" in ph)
check("sitemap vehicle URL at 0.9", "<priority>0.9</priority>" in sm)
sm2 = read(os.path.join(sample, "sitemap.xml"))
check("sitemap contains vehicle URL", "/shop-by-vehicle/honda/cr-v/" in sm2)
check("sitemap product URL at 0.8", re.search(r'/products/sample-honda-cr-v-liner/</loc><lastmod>[^<]+</lastmod><priority>0\.8<', sm2) is not None)
check("vehicle 0.9 ranks above product 0.8",
      sm2.index("/shop-by-vehicle/honda/cr-v/") < sm2.index("/products/sample-honda-cr-v-liner/"))
vj = json.loads(read(os.path.join(sample, "vehicles.json")))
check(f"vehicles.json has {len(SAMPLE_VEHICLES)} entries", len(vj) == len(SAMPLE_VEHICLES), len(vj))
check("vehicles.json entry carries card payload",
      vj[0]["products"] and vj[0]["products"][0]["url"] == "/products/sample-honda-cr-v-liner/")
check("vehicles.json years parseable", vj[0]["years"] == "2017-2026")
check("og:image absent while the referenced image is missing", 'property="og:image"' not in vh)
os.makedirs(os.path.join(sample, "images"), exist_ok=True)
with open(os.path.join(sample, "images", "sample-honda-cr-v-liner.jpg"), "wb") as fh:
    fh.write(b"\xff\xd8\xff\xd9")
g.BASE = sample
check("og:image appears once the image file exists",
      'property="og:image"' in g.product_page(SAMPLE_PRODUCTS[0]))

bad_ld = []
for root, _dirs, files in os.walk(sample):
    for fn in files:
        if fn.endswith(".html"):
            for blk in jsonld_blocks(read(os.path.join(root, fn))):
                try:
                    json.loads(blk)
                except Exception as exc:                      # noqa: BLE001
                    bad_ld.append((os.path.relpath(os.path.join(root, fn), sample), str(exc)))
check("all JSON-LD blocks parse", not bad_ld, bad_ld[:3])

js_bad = check_inline_js(sample, tempfile.mkdtemp(prefix="tmf_js_"))
if js_bad is None:
    print("  SKIP  node not found - inline JS syntax check did not run")
else:
    check("every inline <script> passes node --check", not js_bad, js_bad[:2])
check("quote modal handlers are defined in the emitted JS",
      all(f"function {fn}" in home2 for fn in ("openQuote", "closeQuote", "submitQuote")))

types = {}
for root, _dirs, files in os.walk(sample):
    for fn in files:
        if fn.endswith(".html"):
            for blk in jsonld_blocks(read(os.path.join(root, fn))):
                types.setdefault(json.loads(blk).get("@type"), 0)
                types[json.loads(blk).get("@type")] += 1
check("Organization on home", "Organization" in types, types)
check("CollectionPage on category/vehicle pages", types.get("CollectionPage", 0) >= 3, types)
check("Product schema on product pages", types.get("Product", 0) >= 1, types)
check("BreadcrumbList present", types.get("BreadcrumbList", 0) >= 2, types)

print("\n" + ("ALL CHECKS PASSED" if not fails else "FAILED: " + ", ".join(fails)))
print("temp build dirs: " + real + " | " + sample)
sys.exit(1 if fails else 0)
