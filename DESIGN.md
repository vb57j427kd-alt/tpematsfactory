# tpematsfactory.com — visual system

Implemented 2026-09-21. **Source of truth: `theme.css`.** `generate.py` reads it and
inlines it into every generated page at build time, so the deployed site still ships
self-contained HTML with no extra request.

> The stylesheet used to live as a 163-line string literal inside `generate.py`.
> It was moved to `theme.css` because editing CSS inside a Python string literal is
> where this repo has previously corrupted a file (an edit tool wrote a closing quote
> as a literal `\"`). A real `.css` file removes that failure mode and makes visual
> iteration cheap.

---

## 1. Why this system — evidence, not taste

The category's actual designers were sampled by loading their sites in a browser and
reading **computed styles off the rendered DOM**, not by eyeballing screenshots.
Raw JSON + screenshots live in the workspace `design-ref/` folder (outside this repo).

| Reference | Canvas | Ink | The one accent | Container | Card treatment |
|---|---|---|---|---|---|
| Husky Liners | `#FFFFFF` | `#1C1C1E` | `#FFC600`, CTA only | 1280px | radius 4px, no shadow |
| 3D MAXpider | `#FFFFFF` | `#000000` | `#C8A684` champagne | full-bleed, 40px pad | radius 0, no shadow, no border |
| TuxMat | `#FFFFFF` | `#171717` | `#B9975B` gold, CTA/links/icons only | 1600px | radius 16px + 1px hairline, shadow tokens all `0` |
| Porsche Tequipment | `#FFFFFF` | `#000000` | `#D5001C`, hover only | 1600px | hero radius 12px |

**Not obtained (recorded, not guessed):** WeatherTech is behind Cloudflare;
Petex and Rezaw-Plast are blocked by the corporate network gateway. No substitute
values were invented for them.

### What the category does — therefore what we do

1. **White canvas, near-black ink.** All four references. We were dark.
2. **Exactly one accent, spent only on interactive points.** Never headings, never
   prices, never card borders.
3. **One type family; hierarchy from weight and size.** 3D MAXpider sets `h1` at
   **weight 400**. We now load Inter alone.
4. **Fitment/vehicle selection is a dark band near the top.** (See §6 for what we did
   and did not change here.)
5. **Cards are undecorated** — hairline borders, shadow ≈ 0.
6. **Geometry is small and crisp** — 0–4px, or a full pill. Never the 8–16px middle
   ground that reads as "template".

### What none of them do — therefore what we removed

- **Orange `#FF6A1F` on near-black doing every job at once** — heading colour, price
  colour, tag fill, link colour and hover-border colour. This was the loudest
  "discount" signal in the old build.
- Condensed display headings (Oswald).
- Cards that lift `-4px` and glow on hover.
- Gradients (radial hero, linear CTA band) and `backdrop-filter` glassmorphism.
- Uppercase + letterspaced "fake luxury" headings.

---

## 2. Colour tokens

| Token | Value | Role |
|---|---|---|
| `--bg` | `#FFFFFF` | canvas |
| `--surface` | `#F6F5F3` | faint warm inset: spec tables, image wells, finder panel |
| `--dark` | `#16181A` | dark bands only: hero, CTA, footer |
| `--dark-2` | `#24272B` | dark hover |
| `--ink` | `#16181A` | headings, primary values |
| `--ink2` | `#4C5157` | body copy |
| `--ink3` | `#83898F` | meta, captions, field labels |
| `--accent` | `#8A6636` | **links, active states, small marks only** |
| `--accent-2` | `#6F5228` | accent hover |
| `--wa` | `#25D366` | WhatsApp mark, rendered as an 8px dot only |
| `--line` | `#E4E2DE` | hairline |
| `--line-2` | `#CFCCC6` | stronger hairline (input borders) |

`#8A6636` is a deeper bronze than any reference uses, deliberately: TuxMat's
`#B9975B` and 3D's `#C8A684` are too light to clear 4.5:1 on white, so they cannot
carry an inline link. This one can.

## 3. Geometry

- Container `.wrap`: **1280px**, `0 28px` gutter.
- Radius: **3px** (`--r`) for buttons, inputs, cards and panels; 4px for the modal.
- Elevation: **none** on cards. The only shadows in the system are the dropdown
  (`0 18px 44px rgba(22,24,26,.10)`) and the modal (`0 30px 80px rgba(22,24,26,.22)`),
  i.e. only for genuinely floating layers.
- Section rhythm: **92px** block padding desktop, 64px ≤900px, 52px ≤560px.
- Hover on interactive surfaces changes **border or text colour only** — no
  `transform`, no glow.

## 4. Type

Single family: **Inter** `400/500/600/700` (Oswald removed — one fewer network font).

| Element | Size | Weight |
|---|---|---|
| Hero `h1` | 2.6rem | 500 |
| Section `h2` | 1.55rem | 500 |
| Page `h1` | 1.85rem | 500 |
| Product `h1` | 1.75rem | 500 |
| Card `h3` | .98rem | 500 |
| Body | 16px / 1.7 | 400 |
| Meta | .78rem | 400 |

`letter-spacing: normal` everywhere except the uppercase wordmark. Headings are
`--ink`; emphasis inside a heading is done with **weight, not colour**
(e.g. the `Factory Direct` span in the hero is 600, not orange).

## 5. Components

- **Buttons** — primary is solid `--ink`; secondary and WhatsApp are a single
  hairline. On dark surfaces (hero, CTA band) primary inverts to solid white and
  outlines switch to `rgba(255,255,255,.32)`.
- **Product card** — 1px hairline, radius 3px, image well on `--surface`; the price
  row sits under its own hairline. Price is `--ink` 600, **not** accent.
- **Tag** — a plain bronze label. No pill, no fill, no uppercase.
- **Vehicle finder** — `--surface` panel, hairline inputs; focus turns the border
  `--ink` (the old orange glow ring is gone).
- **Spec table** — hairlines, label column on `--surface`.
- **Modal** — plain `rgba(22,24,26,.62)` scrim, **no** backdrop blur.
- **Focus** — a real `:focus-visible` outline in `--accent`. The old build had none.

## 6. Deliberate deviations & trade-offs

- **WhatsApp is no longer a solid neon-green button.** It is a hairline button with a
  green dot, bringing it inside the one-accent rule while staying recognisable. If
  WhatsApp conversion matters more than the visual system, reverting this one rule
  (`.btn-wa` in `theme.css`) is a one-line change — flagged as a business trade-off,
  not a design one.
- **The vehicle finder was restyled in place, not moved.** All four references put
  fitment selection in a dark band directly under the nav; ours still sits further
  down the page. Moving it is the single highest-value remaining structural change but
  requires a section reorder, which was explicitly out of scope for this pass.
- **Footer is dark**, though TuxMat's is light. Deliberate: it brackets the light
  content between the dark hero and the dark CTA band.

## 7. Responsive behaviour, and two defects the first render caught

The system was verified by rendering it in a real browser at **1440×900** and
**375×812** rather than by reading the CSS. That caught three things that reading the
stylesheet would not have:

1. **12px horizontal overflow at 375px.** `.foot` used `1fr 1fr`; a long unbreakable
   string set a min-content floor (142 + 166 + gap 36 = 344px inside a 304px
   container), pushing `html.scrollWidth` to 372 against a 360 client width — a real
   horizontal scrollbar. Fixed with `repeat(2,minmax(0,1fr))`, `min-width:0` on the
   grid children and `overflow-wrap:anywhere` on footer links. All three mobile page
   types now measure `scrollWidth === clientWidth`.
2. **The primary CTA was unreachable on mobile.** The nav is a horizontally scrolling
   strip (deliberate — it keeps every link reachable without JS), but at 375px only
   129px of it was visible, so `Get Quote` sat off-screen. Below 900px the nav is now
   two rows: logo + a compact solid `Get Quote` on row one, the scrolling link strip
   on row two. No JavaScript added.
3. **Outlined buttons on the dark band** were `rgba(255,255,255,.32)`, which composites
   to only **2.9:1** against `#16181A` — under the 3:1 required for non-text UI.
   Raised to `.42` (measured 4.08:1).

## 8. Legacy token aliases — read before renaming any token

The page templates still carry inline styles using the **old dark-theme token names**
(`--t1/--t2/--t3`, `--bg2`, `--card`, `--card2`, `--accent2`). CSS reports no error for
an undefined variable: the declaration is simply dropped and the element inherits. A
renamed token therefore yields a page that looks *almost* right and is very hard to
debug — this happened during this redesign and was only caught by grepping.

`theme.css` defines those old names as aliases onto real roles. They are aliases, not a
second palette.

```
python ../tools/check_css_tokens.py
```

cross-checks every `var(--x)` referenced by the generator **and** by the generated
pages against the tokens defined in `theme.css`. It exits non-zero on anything
undefined. Run it after any token rename.

## 9. Rebuilding

```
python generate.py          # regenerates all 99 pages + sitemap
python _verify_generate.py  # 40+ structural assertions, must print ALL CHECKS PASSED
```
