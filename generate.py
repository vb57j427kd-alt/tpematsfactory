# -*- coding: utf-8 -*-
"""
Generate the tpematsfactory.com static site.

Base: besthardwaretools.com generate.py. Five changes for the car-mat category
(see tpematsfactory-site-plan.md sections 3 and 5):
  1. every page is written as {dir}/index.html instead of a flat {name}.html
  2. vehicle_page(v)      -> /shop-by-vehicle/{make}/{model}/
  3. vehicle_index()      -> /shop-by-vehicle/
  4. vehicles.json        -> powers the home Year -> Make -> Model finder
  5. sitemap.xml          -> vehicle pages get priority 0.9 (above product 0.8)
"""
import os
import json
from datetime import datetime
from products_data import (SITE, CATEGORIES, PRODUCTS, VEHICLES, RELATED_INDEX,
                           VEHICLE_INDEX, products_for_vehicle,
                           vehicles_for_product, category_name)

try:
    from blog_data import ARTICLES, ARTICLE_INDEX
except ImportError:            # blog is optional while the catalogue is empty
    ARTICLES, ARTICLE_INDEX = [], {}

try:
    from products_data import CATEGORY_COPY
except ImportError:
    CATEGORY_COPY = {}

BASE = os.path.dirname(os.path.abspath(__file__))
DOMAIN = SITE["domain"]
URL = f"https://{DOMAIN}/"
YEAR = datetime.now().year
WA = SITE["whatsapp"]
BRAND = SITE["brand"]
IS_LIVE = bool(SITE.get("ga4"))          # used to warn about placeholder config

# IndexNow key (Bing / Yandex instant indexing). Not a secret - it only proves
# we control the domain, and it is served as /<key>.txt from the site root.
INDEXNOW_KEY = "9f2c7a41d68b4e53a1c0f7e29d34b856"

CSS = """
:root{--bg:#0A0C10;--bg2:#101419;--card:#151A21;--card2:#1B222B;--accent:#FF6A1F;--accent2:#D14E0D;--t1:#E9EEF4;--t2:#A6B2C0;--t3:#6C7987;--line:#212A34}
*{margin:0;padding:0;box-sizing:border-box}
a{text-decoration:none;color:inherit}
body{background:var(--bg);color:var(--t1);font-family:'Inter',system-ui,-apple-system,sans-serif;line-height:1.6}
.wrap{max-width:1200px;margin:0 auto;padding:0 24px}
h1,h2,h3,h4,h5,.logo{font-family:'Oswald',sans-serif;font-weight:600;letter-spacing:.02em}
nav{position:sticky;top:0;z-index:100;background:rgba(10,12,16,.93);backdrop-filter:blur(10px);border-bottom:1px solid var(--line)}
.nav-in{display:flex;align-items:center;justify-content:space-between;height:64px;gap:18px}
.logo{font-size:1.2rem;white-space:nowrap}.logo b{color:var(--accent)}
.nav-links{display:flex;gap:20px;font-size:.88rem;color:var(--t2);align-items:center}
.nav-links a:hover{color:var(--accent)}
.dd{position:relative}
.dd-t{cursor:pointer;color:var(--t2)}
.dd-menu{display:none;position:absolute;top:34px;left:50%;transform:translateX(-50%);background:var(--bg2);border:1px solid var(--line);border-radius:12px;padding:20px 22px;box-shadow:0 20px 50px rgba(0,0,0,.6);min-width:520px;max-height:70vh;overflow:auto;grid-template-columns:repeat(3,1fr);gap:18px 26px;z-index:120}
.dd:hover .dd-menu{display:grid}
.dd-col h6{font-family:'Oswald';color:var(--accent);font-size:.82rem;letter-spacing:.08em;text-transform:uppercase;margin-bottom:8px}
.dd-col a{display:block;color:var(--t2);font-size:.84rem;padding:3px 0}
.dd-col a:hover{color:var(--accent)}
.btn{display:inline-block;padding:11px 26px;border-radius:6px;font-weight:600;font-size:.92rem;transition:.2s;cursor:pointer;border:none;font-family:inherit}
.btn-p{background:var(--accent);color:#14181d}.btn-p:hover{background:var(--accent2);transform:translateY(-1px)}
.btn-o{border:1px solid var(--line);color:var(--t1)}.btn-o:hover{border-color:var(--accent);color:var(--accent)}
.btn-wa{background:#25D366;color:#0d1216}.btn-wa:hover{filter:brightness(1.08);transform:translateY(-1px)}
.hero{background:radial-gradient(ellipse at 72% 14%,#1C2635 0%,var(--bg) 62%);padding:78px 0 60px;border-bottom:1px solid var(--line)}
.hero h1{font-size:2.75rem;line-height:1.14;margin-bottom:16px}
.hero h1 span{color:var(--accent)}
.hero p{color:var(--t2);max-width:660px;font-size:1.05rem;margin-bottom:26px}
.cta-row{display:flex;gap:14px;flex-wrap:wrap}
.trust{display:flex;gap:40px;flex-wrap:wrap;margin-top:34px}
.trust div b{font-size:1.55rem;color:var(--accent);font-family:'Oswald';display:block}
.trust div span{font-size:.8rem;color:var(--t3)}
section{padding:60px 0;border-bottom:1px solid var(--line)}
.sec-head{display:flex;align-items:baseline;justify-content:space-between;margin-bottom:26px;gap:20px;flex-wrap:wrap}
.sec-head h2{font-size:1.75rem}.sec-head h1{font-size:2rem}
.sec-head a{color:var(--t3);font-size:.85rem}.sec-head a:hover{color:var(--accent)}
.tag{display:inline-block;background:rgba(255,106,31,.12);color:var(--accent);border:1px solid rgba(255,106,31,.3);padding:3px 12px;border-radius:20px;font-size:.73rem;letter-spacing:.08em;text-transform:uppercase;margin-bottom:12px}
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:22px}
.grid-4{display:grid;grid-template-columns:repeat(4,1fr);gap:20px}
.pc{background:var(--card);border:1px solid var(--line);border-radius:10px;overflow:hidden;transition:.25s;display:block}
.pc:hover{transform:translateY(-4px);border-color:rgba(255,106,31,.5);box-shadow:0 12px 34px rgba(0,0,0,.45)}
.pc-img{position:relative;background:#0c1015;overflow:hidden}
.pc-img img{width:100%;height:225px;object-fit:cover;display:block}
.badge{position:absolute;top:12px;left:12px;background:var(--accent);color:#14181d;font-size:.68rem;font-weight:700;padding:3px 10px;border-radius:4px;letter-spacing:.06em}
.pc-body{padding:17px}
.pc-body h3{font-size:1rem;margin-bottom:6px;line-height:1.35}
.pc-body p{color:var(--t3);font-size:.83rem;margin-bottom:10px}
.price-row{display:flex;justify-content:space-between;align-items:baseline;gap:10px}
.price{color:var(--accent);font-weight:700;font-size:1rem}
.moq{color:var(--t3);font-size:.76rem}
.feats{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}
.feat{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:20px}
.feat h4{color:var(--accent);font-size:1rem;margin-bottom:8px}
.feat p{color:var(--t2);font-size:.85rem}
.feat a{color:var(--accent);font-size:.85rem;display:block;margin-top:10px}
/* vehicle finder */
.finder{background:var(--bg2);border:1px solid var(--line);border-radius:14px;padding:26px}
.finder-row{display:grid;grid-template-columns:repeat(3,1fr) auto;gap:14px;align-items:end}
.finder-row label{display:block;color:var(--t3);font-size:.78rem;margin-bottom:6px}
.finder-row select{width:100%;padding:12px 14px;border-radius:8px;border:1px solid var(--line);background:var(--card);color:var(--t1);font-size:.92rem;font-family:inherit;outline:none}
.finder-row select:focus{border-color:var(--accent)}
.finder-note{color:var(--t3);font-size:.82rem;margin-top:16px}
.finder-note a{color:var(--accent)}
.finder-res{margin-top:22px}
.vgrid{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}
.vcard{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:16px;transition:.2s;display:block}
.vcard:hover{border-color:rgba(255,106,31,.5);transform:translateY(-3px)}
.vcard b{display:block;font-size:1rem;font-family:'Oswald'}
.vcard span{color:var(--t3);font-size:.79rem;display:block;margin-top:4px}
.vcard em{color:var(--accent);font-style:normal;font-size:.76rem;display:block;margin-top:8px}
.vhero{background:var(--card);border:1px solid var(--line);border-radius:12px;overflow:hidden;margin-bottom:20px}
.vhero img{width:100%;display:block}
.empty{background:var(--card);border:1px dashed var(--line);border-radius:10px;padding:26px;color:var(--t2);font-size:.92rem}
.empty b{color:var(--t1)}
/* breadcrumb */
/* longhand padding on purpose: the shorthand reset the 24px gutter from .wrap,
   leaving breadcrumbs and product text flush against the screen on mobile */
.crumb{color:var(--t3);font-size:.82rem;padding-top:18px;padding-bottom:18px}
.crumb a:hover{color:var(--accent)}
/* product page */
.pd{display:grid;grid-template-columns:1.05fr 1fr;gap:42px;padding-top:26px;padding-bottom:56px}
.pd-img{background:var(--card);border:1px solid var(--line);border-radius:12px;overflow:hidden;align-self:start}
.pd-img img{width:100%;display:block}
.pd-info h1{font-size:1.85rem;line-height:1.2;margin-bottom:12px}
.pd-price{font-size:1.45rem;color:var(--accent);font-weight:700;margin-bottom:4px}
.pd-moq{color:var(--t3);font-size:.88rem;margin-bottom:16px}
.pd-desc{color:var(--t2);font-size:.94rem;margin-bottom:20px}
.block{margin-bottom:22px}
.block h4{font-size:1.02rem;color:var(--accent);margin-bottom:10px}
.block ul{margin-left:18px}
.block li{color:var(--t2);font-size:.88rem;margin:6px 0}
.fit{display:grid;grid-template-columns:repeat(2,1fr);gap:1px;background:var(--line);border:1px solid var(--line);border-radius:8px;overflow:hidden}
.fit div{background:var(--bg2);padding:10px 14px;font-size:.86rem;display:flex;justify-content:space-between;gap:12px}
.fit span{color:var(--t3)}
/* the 4-column comparison table cannot fit 375px: scroll it instead of
   letting it push the whole page 57px wide */
.tbl{overflow-x:auto;-webkit-overflow-scrolling:touch;padding-bottom:2px}
.specs{width:100%;border-collapse:collapse;margin-bottom:22px}
.tbl .specs{margin-bottom:0;min-width:420px}
.specs td{border:1px solid var(--line);padding:10px 14px;font-size:.87rem}
.specs td:first-child{color:var(--t3);width:36%;background:var(--bg2)}
/* category buyer's guide + FAQ (rankable on-page content) */
.guide{max-width:900px;margin-bottom:32px}
.guide h2{font-size:1.22rem;color:var(--accent);margin:24px 0 10px}
.guide h3{font-size:1.02rem;margin:18px 0 8px}
.guide p{color:var(--t2);font-size:.94rem;margin-bottom:12px}
.guide li{color:var(--t2);font-size:.92rem;margin:6px 0 6px 18px}
.guide a,.post a{color:var(--accent)}
.faq{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:14px 18px;margin-bottom:10px}
.faq summary{cursor:pointer;font-weight:600;font-size:.95rem;color:var(--t1)}
.faq summary:hover{color:var(--accent)}
.faq-a{color:var(--t2);font-size:.9rem;margin-top:10px;line-height:1.65}
.sm-col{margin-bottom:30px}
.sm-col h3{font-size:1.05rem;color:var(--accent);margin-bottom:10px}
.sm-col a{display:inline-block;color:var(--t2);font-size:.86rem;margin:0 14px 7px 0}
.sm-col a:hover{color:var(--accent)}
.pts{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:20px}
.pts h4{color:var(--accent);margin-bottom:12px;font-size:1.02rem}
.related{padding:50px 0}
/* modal */
.modal{display:none;position:fixed;inset:0;z-index:200;background:rgba(5,7,10,.8);backdrop-filter:blur(4px)}
.modal.open{display:flex;align-items:center;justify-content:center}
.mbox{background:var(--bg2);border:1px solid var(--line);border-radius:18px;max-width:560px;width:93%;max-height:92vh;overflow:auto;padding:28px;box-shadow:0 24px 80px rgba(0,0,0,.65)}
.mbox h3{font-size:1.25rem;margin-bottom:6px}
.mbox .prod-line{color:var(--accent);font-size:.84rem;margin-bottom:16px}
.fg{margin-bottom:13px}
.fg label{display:block;color:var(--t3);font-size:.79rem;margin-bottom:6px}
.fg input,.fg textarea{width:100%;padding:11px 14px;border-radius:8px;border:1px solid var(--line);background:var(--card);color:var(--t1);font-size:.91rem;outline:none;font-family:inherit}
.fg input:focus,.fg textarea:focus{border-color:var(--accent);box-shadow:0 0 0 3px rgba(255,106,31,.14)}
.fg2{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.mbtn{width:100%;padding:13px;border:none;border-radius:8px;background:var(--accent);color:#14181d;font-weight:700;font-size:.94rem;cursor:pointer;font-family:inherit}
.mbtn:hover{background:var(--accent2)}
.mclose{position:sticky;float:right;background:none;border:none;color:var(--t3);font-size:1.4rem;cursor:pointer;line-height:1}
.bank{margin-top:16px;border-top:1px solid var(--line);padding-top:14px}
.bank h5{color:var(--t1);margin-bottom:10px;font-size:.93rem}
.bank-row{display:flex;justify-content:space-between;gap:16px;padding:7px 0;border-bottom:1px dashed var(--line);font-size:.84rem}
.blabel{color:var(--t3)}
.bvalue{color:var(--t1);font-weight:600;text-align:right;word-break:break-all}
.bvalue.hl{color:var(--accent)}
.bank-note{color:var(--t3);font-size:.75rem;line-height:1.5;margin-top:10px}
.success{display:none;text-align:center;padding:20px 0}
.success h4{color:#25D366;font-size:1.15rem;margin-bottom:10px}
.success p{color:var(--t2);font-size:.9rem}
/* blog */
.post{max-width:820px}
.post h1{font-size:2rem;margin-bottom:14px}
.post h2{font-size:1.3rem;margin:26px 0 10px;color:var(--accent)}
.post p{color:var(--t2);margin-bottom:14px;font-size:.96rem}
.post ul{margin:0 0 16px 20px}.post li{color:var(--t2);font-size:.94rem;margin:6px 0}
.cta{background:linear-gradient(135deg,#141A22,#1B2634);text-align:center;padding:64px 24px;border-bottom:1px solid var(--line)}
.cta h2{font-size:1.9rem;margin-bottom:12px}
.cta p{color:var(--t2);max-width:580px;margin:0 auto 26px}
footer{background:var(--bg2);padding:46px 0 28px;border-top:1px solid var(--line)}
.foot{display:grid;grid-template-columns:1.6fr 1fr 1fr 1fr;gap:30px}
.foot h5{font-size:.93rem;margin-bottom:12px;color:var(--t1)}
.foot a{display:block;color:var(--t3);font-size:.84rem;margin-bottom:7px}
.foot a:hover{color:var(--accent)}
.copy{text-align:center;color:var(--t3);font-size:.77rem;margin-top:34px;border-top:1px solid var(--line);padding-top:18px}
@media(max-width:900px){.grid,.feats{grid-template-columns:repeat(2,1fr)}.grid-4,.vgrid{grid-template-columns:repeat(2,1fr)}.pd{grid-template-columns:1fr}.foot{grid-template-columns:1fr 1fr}.hero h1{font-size:2.1rem}.finder-row{grid-template-columns:1fr 1fr}
/* keep every nav link reachable on touch devices: scroll horizontally instead of hiding */
.nav-in{height:60px;gap:12px}.nav-links{display:flex;overflow-x:auto;gap:15px;font-size:.82rem;white-space:nowrap;-webkit-overflow-scrolling:touch;padding-bottom:2px}.nav-links::-webkit-scrollbar{display:none}
.dd-menu{display:none!important}}
@media(max-width:560px){.grid,.grid-4,.vgrid{grid-template-columns:1fr}.finder-row{grid-template-columns:1fr}.fit{grid-template-columns:1fr}.nav-links{gap:12px}.logo{font-size:1.05rem}.trust{gap:22px}.specs td{padding:8px 10px;font-size:.82rem}.tbl .specs{min-width:380px}}
"""

JS = """
var currentProduct='';
function openQuote(name){currentProduct=name||'';document.getElementById('quoteProduct').textContent=currentProduct||'General enquiry';document.getElementById('modal').classList.add('open');document.getElementById('quoteSuccess').style.display='none';document.getElementById('quoteFormWrap').style.display='block'}
function closeQuote(){document.getElementById('modal').classList.remove('open')}
function submitQuote(e){
  e.preventDefault();
  var g=function(id){return (document.getElementById(id).value||'').trim()};
  var msg='Quote request - '+__BRAND__+'\\nProduct / Vehicle: '+(currentProduct||g('qVehicle'))+'\\nName: '+g('qName')+'\\nEmail: '+g('qEmail')+'\\nCountry: '+g('qCountry')+'\\nWhatsApp: '+g('qPhone')+'\\nCompany: '+g('qCompany')+'\\nVehicle model: '+g('qVehicle')+'\\nQuantity: '+g('qQty')+'\\nMessage: '+g('qMsg');
  window.open('https://wa.me/__WA__?text='+encodeURIComponent(msg),'_blank');
  __FORMSPREE__
  document.getElementById('quoteFormWrap').style.display='none';
  document.getElementById('quoteSuccess').style.display='block';
}
document.addEventListener('DOMContentLoaded',function(){
  var m=document.getElementById('modal');
  if(!m)return;
  document.addEventListener('keydown',function(e){if(e.key==='Escape')closeQuote()});
  m.addEventListener('click',function(e){if(e.target===m)closeQuote()});
});
"""

FINDER_JS = """
(function(){
  var y=document.getElementById('fYear');
  if(!y)return;
  var mk=document.getElementById('fMake'),md=document.getElementById('fModel'),
      out=document.getElementById('fResult'),st=document.getElementById('fStatus'),DATA=[];
  function esc(s){return String(s==null?'':s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
  function yearsOf(str){
    var set=[],re=/(\\d{4})\\s*-\\s*(\\d{4})/g,m;
    str=str||'';
    while((m=re.exec(str))){var a=+m[1],b=+m[2];if(b-a>40)b=a+40;for(var i=a;i<=b;i++)set.push(i)}
    if(!set.length){var s=/(\\d{4})/.exec(str);if(s)set.push(+s[1])}
    return set;
  }
  function fill(sel,list,ph){
    var h='<option value="">'+ph+'</option>';
    for(var i=0;i<list.length;i++)h+='<option value="'+esc(list[i])+'">'+esc(list[i])+'</option>';
    sel.innerHTML=h;sel.disabled=(list.length===0);
  }
  function uniq(a){var o=[],s={};for(var i=0;i<a.length;i++){if(!s[a[i]]){s[a[i]]=1;o.push(a[i])}}return o}
  function card(p){
    var src=(p.imgw?'<source srcset="'+esc(p.imgw)+'" type="image/webp">':'');
    return '<a class="pc" href="'+esc(p.url)+'"><div class="pc-img"><picture>'+src+'<img src="'+esc(p.imgc||p.img)+'" alt="'+esc(p.name)+'" width="400" height="280" loading="lazy" decoding="async"></picture>'+(p.badge?'<span class="badge">'+esc(p.badge)+'</span>':'')+'</div><div class="pc-body"><h3>'+esc(p.name)+'</h3><p>'+esc(p.desc)+'</p><div class="price-row"><span class="price">'+esc(p.price)+'</span><span class="moq">'+esc(p.moq)+'</span></div></div></a>';
  }
  function sync(){
    var Y=y.value,M=mk.value,pool=DATA;
    // A vehicle whose year range is unknown must NOT be filtered out by the
    // year selector - most of this catalogue has no stated years, and hiding
    // them makes e.g. Honda unreachable for anyone who picks a year first.
    if(Y)pool=pool.filter(function(v){return !v.years || yearsOf(v.years).indexOf(+Y)>=0});
    var makes=uniq(pool.map(function(v){return v.make}));
    if(makes.indexOf(M)<0){fill(mk,makes,'Select make');md.value='';fill(md,[],'Select model')}
    else{fill(mk,makes,'Select make');mk.value=M}
    if(mk.value){
      syncModels();
    }else{
      fill(md,[],'Select model');
    }
    render();
  }
  function syncModels(){
    var Y=y.value,M=mk.value;
    var pool=DATA.filter(function(v){
      if(M&&v.make!==M)return false;
      if(Y&&v.years&&yearsOf(v.years).indexOf(+Y)<0)return false;
      return true;
    });
    var models=uniq(pool.map(function(v){return v.model}));
    var keep=md.value;
    fill(md,models,'Select model');
    if(models.indexOf(keep)>=0)md.value=keep;
  }
  function render(){
    var Y=y.value,M=mk.value,MO=md.value;
    if(!M&&!MO&&!Y){out.innerHTML='';if(st)st.textContent='';return}
    var hits=DATA.filter(function(v){
      if(Y&&v.years&&yearsOf(v.years).indexOf(+Y)<0)return false;
      if(M&&v.make!==M)return false;
      if(MO&&v.model!==MO)return false;
      return true;
    });
    if(!hits.length){
      out.innerHTML='<div class="empty"><b>No listing for that combination yet.</b> Send us the make, model and year - we check tooling and come back with a price and sample lead time, or tell you plainly that we cannot make it. <a href="javascript:void(0)" onclick="openQuote(\\'New vehicle request\\')" style="color:var(--accent)">request this vehicle</a>.</div>';
      if(st)st.textContent='';return;
    }
    var cards='',n=0,vlist='';
    for(var i=0;i<hits.length;i++){
      var v=hits[i];
      vlist+='<a class="vcard" href="'+esc(v.url)+'"><b>'+esc(v.make)+' '+esc(v.model)+'</b><span>'+esc(v.years||'year range on request')+(v.body?' &middot; '+esc(v.body):'')+'</span><em>View liners &rarr;</em></a>';
      var ps=v.products||[];
      for(var j=0;j<ps.length;j++){cards+=card(ps[j]);n++}
    }
    out.innerHTML='<div class="vgrid">'+vlist+'</div>'+(n?'<div class="grid" style="margin-top:22px">'+cards+'</div>':'');
    if(st)st.textContent=hits.length+' vehicle'+(hits.length>1?'s':'')+' matched'+(n?', '+n+' product'+(n>1?'s':''):' - no product page yet, ask us for a quote');
  }
  y.addEventListener('change',function(){md.value='';sync()});
  mk.addEventListener('change',function(){md.value='';sync()});
  md.addEventListener('change',function(){render()});
  fetch('__VJSON__').then(function(r){return r.json()}).then(function(d){
    DATA=d||[];
    if(st)st.textContent=DATA.length?(DATA.length+' vehicle models indexed'):'Fitment index is being compiled - send us your make, model and year.';
    var ys=[];
    for(var i=0;i<DATA.length;i++)ys=ys.concat(yearsOf(DATA[i].years));
    ys=uniq(ys).sort(function(a,b){return b-a});
    fill(y,ys,'Select year');
    fill(mk,uniq(DATA.map(function(v){return v.make})).sort(),'Select make');
    fill(md,[],'Select model');
    render();
  }).catch(function(){if(st)st.textContent='Vehicle index unavailable.'});
})();
"""


def analytics():
    """GA4 / Clarity are injected only when configured - never paste BHT ids."""
    out = []
    g = SITE.get("ga4")
    if g:
        out.append(f'<script async src="https://www.googletagmanager.com/gtag/js?id={g}"></script>')
        out.append("<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments)}"
                   f"gtag('js',new Date());gtag('config','{g}');</script>")
    c = SITE.get("clarity")
    if c:
        out.append('<script type="text/javascript">(function(c,l,a,r,i,t,y){c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};'
                   't=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;'
                   'y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y)})(window,document,"clarity","script","' + c + '")</script>')
    return "\n".join(out)


def js():
    fs = ""
    if SITE.get("formspree"):
        fs = ("var fd=new FormData();fd.append('product',currentProduct);fd.append('name',g('qName'));"
              "fd.append('email',g('qEmail'));fd.append('country',g('qCountry'));fd.append('phone',g('qPhone'));"
              "fd.append('company',g('qCompany'));fd.append('vehicle',g('qVehicle'));fd.append('quantity',g('qQty'));"
              "fd.append('message',g('qMsg'));"
              f"fetch('https://formspree.io/f/{SITE['formspree']}',{{method:'POST',body:fd,headers:{{Accept:'application/json'}}}}).catch(function(){{}});")
    # json.dumps, not a raw substitution: the brand lands inside a JS string
    # literal, so an unquoted name would be a SyntaxError on every page.
    return (JS.replace("__BRAND__", json.dumps(BRAND))
              .replace("__WA__", WA)
              .replace("__FORMSPREE__", fs))


def finder_js():
    # Root-relative, NOT the absolute https://domain/... URL: the absolute form
    # works in production but makes the finder dead on any local preview or
    # staging host, which is exactly when you need to test it.
    return FINDER_JS.replace("__VJSON__", "/vehicles.json")


def img_exists(rel):
    if not rel:
        return False
    return os.path.isfile(os.path.join(BASE, rel.lstrip("/").replace("/", os.sep)))


def picture(jpg, alt, w, h, card=False, loading="lazy"):
    """<picture> with a WebP source plus a JPEG fallback.

    The <source> is only emitted when the WebP file is really on disk, so a
    build without the WebP step silently degrades to plain JPEG rather than
    404ing every image."""
    if not jpg:
        return ""
    base = jpg[:-4] if jpg.lower().endswith(".jpg") else jpg
    webp = base + ("-card.webp" if card else ".webp")
    src = (jpg[:-4] + "-card.jpg") if (card and jpg.lower().endswith(".jpg")) else jpg
    srcs = f'<source srcset="{webp}" type="image/webp">' if img_exists(webp) else ""
    return (f'<picture>{srcs}<img src="{src}" alt="{alt}" width="{w}" height="{h}" '
            f'loading="{loading}" decoding="async"></picture>')


def og_image(rel):
    """Absolute og:image URL - emitted only when the file really exists in the
    repo, so a half-loaded catalogue never ships a 404 image reference."""
    if not rel:
        return ""
    path = os.path.join(BASE, rel.lstrip("/").replace("/", os.sep))
    return (URL.rstrip("/") + rel) if os.path.isfile(path) else ""


def head(title, desc, canonical, ogimg, ld="", schema_title=None):
    if ogimg:
        og_img = (f'<meta property="og:image" content="{ogimg}">\n'
                  f'<meta name="twitter:image" content="{ogimg}">')
    else:
        # No product image yet: omit rather than point og:image at a 404 file.
        og_img = ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
{og_img}
<meta name="theme-color" content="#0A0C10">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<!-- weights trimmed to the ones actually used: Oswald 600/700 for headings, Inter 400/600/700 for body -->
<link href="https://fonts.googleapis.com/css2?family=Oswald:wght@600;700&family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
{analytics()}
{ld}
<style>{CSS}</style>
</head>
"""


# ---------------------------------------------------------------------------
# shared chrome
# ---------------------------------------------------------------------------

def slugify(x):
    """URL and filesystem safe slug: lowercase, no reserved or non-ASCII chars.
    Matters because a mould list can contain 'V-Class', 'Mercedes-Benz: V' or
    an accented make - any of those would otherwise break makedirs() or ship an
    unencoded URL."""
    s = str(x).strip().lower()
    for bad in ("/", "\\", ":", "?", "*", '"', "<", ">", "|", ",", ".", "'", "&", "#", "+", "(", ")"):
        s = s.replace(bad, "-")
    s = "".join(ch if ((ch.isascii() and ch.isalnum()) or ch == "-") else "-" for ch in s)
    while "--" in s:
        s = s.replace("--", "-")
    return s.strip("-")


def vurl(v):
    """Vehicle landing-page URL: /shop-by-vehicle/{make}/{model}/

    Falls back to literal placeholders if a name slugifies to nothing, so a
    non-Latin or punctuation-only entry can never collapse to
    /shop-by-vehicle/// (which would overwrite the vehicle index page)."""
    make = slugify(v["make"]) or "vehicle"
    model = slugify(v["model"]) or "model"
    return f"/shop-by-vehicle/{make}/{model}/"


def vname(v):
    """'Make Model' with whitespace normalised (an empty years field used to
    leave a trailing space in titles and H1s)."""
    return " ".join(f'{v.get("make", "")} {v.get("model", "")}'.split())


def vfull(v):
    """'Make Model Years' - years omitted entirely when unknown."""
    return " ".join(f'{vname(v)} {v.get("years", "") or ""}'.split())


def check_unique_vehicle_urls():
    """Fail loudly on colliding vehicle URLs instead of silently overwriting.

    Two entries like 'CR-V' and 'CR V' (or a blank slug) would otherwise write
    to the same directory with no warning."""
    seen = {}
    for v in VEHICLES:
        u = vurl(v)
        label = f'{v.get("make")} {v.get("model")}'
        if u in seen:
            raise ValueError(
                f"Duplicate vehicle URL {u}: {seen[u]!r} and {label!r}. "
                "Fix the make/model spelling so each entry gets its own page.")
        seen[u] = label


def logo():
    words = BRAND.upper().split()
    if len(words) >= 2:
        return f"{words[0]} <b>{words[1]}</b> " + " ".join(words[2:])
    return f"<b>{BRAND.upper()}</b>"


def vehicle_dropdown():
    if not VEHICLES:
        return ('<div class="dd-col"><h6>Coverage</h6>'
                '<a href="/shop-by-vehicle/">Vehicle index</a>'
                '<a href="javascript:void(0)" onclick="openQuote(\'Vehicle request\')">Ask for your model</a></div>')
    makes = {}
    for v in VEHICLES:
        makes.setdefault(v["make"], []).append(v)
    cols = []
    for make in sorted(makes):
        items = sorted(makes[make], key=lambda x: x["model"])
        links = "".join(f'<a href="{vurl(v)}">{v["model"]}</a>' for v in items[:9])
        more = f'<a href="/shop-by-vehicle/"><em>All {len(items)} models</em></a>' if len(items) > 9 else ""
        cols.append(f'<div class="dd-col"><h6>{make}</h6>{links}{more}</div>')
    return "".join(cols)


def nav(active=""):
    cats = ""
    for c in CATEGORIES:
        hl = ' style="color:var(--accent)"' if active == c["id"] else ""
        cats += f'<a href="/{c["id"]}/"{hl}>{c["nav"]}</a>'
    blog = '<a href="/blog/">Blog</a>' if ARTICLES else ""
    return f"""<nav><div class="wrap nav-in">
<a href="/" class="logo">{logo()}</a>
<div class="nav-links"><a href="/">Home</a>{cats}
<div class="dd"><a href="/shop-by-vehicle/" class="dd-t">Shop by Vehicle &#9662;</a><div class="dd-menu">{vehicle_dropdown()}</div></div>
{blog}<a href="javascript:void(0)" onclick="openQuote('')" style="color:var(--accent)">Get Quote</a></div>
</div></nav>"""


def quote_modal():
    bank = ""
    if SITE.get("bank_account"):
        bank = f"""<div class="bank"><h5>Bank Transfer Details</h5>
<div class="bank-row"><span class="blabel">Beneficiary</span><span class="bvalue">{SITE['bank_beneficiary']}</span></div>
<div class="bank-row"><span class="blabel">Account No.</span><span class="bvalue hl">{SITE['bank_account']}</span></div>
<div class="bank-row"><span class="blabel">Swift Code</span><span class="bvalue">{SITE['bank_swift']}</span></div>
<p class="bank-note">{SITE['bank_note']}</p></div>"""
    mail = f'<a class="btn btn-o" style="margin-top:16px" href="mailto:{SITE["email"]}">Email {SITE["email"]}</a>' if SITE.get("email") else ""
    return f"""<div class="modal" id="modal"><div class="mbox">
<button class="mclose" onclick="closeQuote()">&times;</button>
<div id="quoteFormWrap">
<h3>Get a Wholesale Quote</h3>
<p class="prod-line">Product: <span id="quoteProduct"></span></p>
<form onsubmit="submitQuote(event)">
<div class="fg"><label>Name *</label><input type="text" id="qName" required></div>
<div class="fg2">
<div class="fg"><label>Email *</label><input type="email" id="qEmail" required></div>
<div class="fg"><label>Country *</label><input type="text" id="qCountry" required></div>
</div>
<div class="fg2">
<div class="fg"><label>WhatsApp / Phone</label><input type="tel" id="qPhone"></div>
<div class="fg"><label>Company</label><input type="text" id="qCompany"></div>
</div>
<div class="fg2">
<div class="fg"><label>Your Vehicle Model</label><input type="text" id="qVehicle" placeholder="e.g. Honda CR-V 2020"></div>
<div class="fg"><label>Quantity (sets)</label><input type="text" id="qQty"></div>
</div>
<div class="fg"><label>Message</label><textarea id="qMsg" rows="3"></textarea></div>
<button class="mbtn" type="submit">Send Quote Request</button>
</form>
{bank}
</div>
<div class="success" id="quoteSuccess"><h4>Request Received</h4><p>We have opened WhatsApp with your details and logged the enquiry. Our sales team replies within 24 hours on working days.</p>{mail}</div>
</div></div>"""


def footer():
    cat_links = "".join(f'<a href="/{c["id"]}/">{c["name"]}</a>' for c in CATEGORIES)
    if VEHICLES:
        top = sorted(VEHICLES, key=lambda v: (v["make"], v["model"]))[:6]
        veh_links = "".join(f'<a href="{vurl(v)}">{vname(v)}</a>' for v in top)
        veh_links += '<a href="/shop-by-vehicle/">All vehicles</a>'
    else:
        veh_links = '<a href="/shop-by-vehicle/">Shop by Vehicle</a>'
    veh_links += '<a href="/site-map/">Site map</a>'
    contact = f'<a href="mailto:{SITE["email"]}">{SITE["email"]}</a>' if SITE.get("email") else ""
    return f"""<footer><div class="wrap">
<div class="foot">
<div><a href="/" class="logo">{logo()}</a><p style="color:var(--t3);font-size:.84rem;margin-top:12px">{SITE['tagline']}. OEM/ODM welcome, worldwide shipping.</p></div>
<div><h5>Categories</h5>{cat_links}</div>
<div><h5>Shop by Vehicle</h5>{veh_links}</div>
<div><h5>Contact</h5><a href="https://wa.me/{WA}" target="_blank" rel="noopener">WhatsApp: +{WA}</a>{contact}<a href="javascript:void(0)" onclick="openQuote('')">Request a quote</a></div>
</div>
<div class="copy">&copy; {YEAR} {BRAND} ({DOMAIN}). All rights reserved. TPE floor liners, all-weather mats and cargo liners direct from the factory.</div>
</div></footer>
<script>var currentOrderProduct='';</script>
{quote_modal()}
<script>{js()}</script>
</body></html>"""


def shell(title, desc, canonical, ogimg, body, ld=""):
    return head(title, desc, canonical, ogimg, ld) + body


def product_card(p):
    d = p["desc"][:110] + ("..." if len(p["desc"]) > 110 else "")
    url = f'/products/{p["slug"]}/'
    alt = p["name"]
    return (f'<a href="{url}" class="pc"><div class="pc-img">{picture(p["img"], alt, 400, 280, card=True)}'
            f'<span class="badge">{p["badge"]}</span></div><div class="pc-body"><h3>{p["name"]}</h3>'
            f'<p>{d}</p><div class="price-row"><span class="price">{p["price"]}</span>'
            f'<span class="moq">{p["moq"]}</span></div></div></a>')


def vehicle_card(v):
    n = len(products_for_vehicle(v))
    meta = (v["years"] or "year range on request") + (f' &middot; {v["body"]}' if v.get("body") else "")
    tag = f'{n} product{"s" if n != 1 else ""}' if n else "Ask for quote"
    return (f'<a class="vcard" href="{vurl(v)}"><b>{vname(v)}</b>'
            f'<span>{meta}</span><em>{tag} &rarr;</em></a>')


def ld_org():
    cert = ""
    return json.dumps({
        "@context": "https://schema.org", "@type": "Organization",
        "name": BRAND, "url": URL,
        "contactPoint": {"@type": "ContactPoint", "contactType": "sales",
                         "telephone": "+" + WA},
        "areaServed": {"@type": "Place", "name": "Worldwide"},
        "knowsAbout": ["TPE car floor liners", "3D floor liners", "all-weather floor mats",
                       "cargo liners", "car mat OEM ODM"],
    }, ensure_ascii=False)


def ld_crumbs(trail):
    items = []
    for i, (name, url) in enumerate(trail, start=1):
        items.append({"@type": "ListItem", "position": i, "name": name,
                      "item": url if url.startswith("http") else URL.rstrip("/") + url})
    return json.dumps({"@context": "https://schema.org", "@type": "BreadcrumbList",
                       "itemListElement": items}, ensure_ascii=False)


def ld_collection(name, desc, canonical):
    return json.dumps({"@context": "https://schema.org", "@type": "CollectionPage",
                       "name": name, "description": desc, "url": canonical}, ensure_ascii=False)


def ld_product(p, canonical):
    props = []
    f = p.get("fitment") or {}
    if f.get("make"):
        props.append({"@type": "PropertyValue", "name": "Compatible Make", "value": f.get("make")})
    if f.get("model"):
        props.append({"@type": "PropertyValue", "name": "Compatible Model", "value": f.get("model")})
    if f.get("years"):
        props.append({"@type": "PropertyValue", "name": "Compatible Years", "value": f.get("years")})
    props.append({"@type": "PropertyValue", "name": "Material", "value": "TPE (Thermoplastic Elastomer)"})
    return json.dumps({
        "@context": "https://schema.org", "@type": "Product",
        "name": p["name"], "image": p["img"], "description": p["desc"],
        "brand": {"@type": "Brand", "name": BRAND},
        "additionalProperty": props,
        "offers": {"@type": "Offer", "priceCurrency": "USD",
                   "availability": "https://schema.org/InStock", "url": canonical},
    }, ensure_ascii=False)


def ld_script(payload):
    return f'<script type="application/ld+json">{payload}</script>'


def faq_block(items, title="Frequently Asked Questions"):
    rows = "".join(
        f'<details class="faq"><summary>{q}</summary><div class="faq-a">{a}</div></details>'
        for q, a in items)
    return (f'<section><div class="wrap"><div class="sec-head"><div>'
            f'<span class="tag">FAQ</span><h2>{title}</h2></div></div>{rows}</div></section>')


def ld_faq(items):
    """Same source as the visible FAQ, so the markup and the rich-result data
    can never drift apart."""
    return json.dumps({
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q,
                        "acceptedAnswer": {"@type": "Answer", "text": a}}
                       for q, a in items]}, ensure_ascii=False)


def vehicle_faq(v):
    """Answers restate only what the catalogue actually knows; where a fact is
    missing they ask for it instead of asserting it."""
    year_line = (f'These listings are moulded for the {vfull(v)}.'
                 if v.get("years") else
                 f'These listings are moulded for the {vname(v)}; the catalogue does not state a year range for it.')
    hand_line = (f'This vehicle is listed as {v["hand"]}.'
                 if v.get("hand") else
                 'Both left- and right-hand drive versions can be tooled.')
    return [
        ("Will these liners fit my exact year?", year_line +
         " Fitment changes between generations, so send us the model year and body type and we confirm before you order."),
        ("Do you make left-hand and right-hand drive versions?", hand_line +
         " Tell us which side the driver sits on when you place the order."),
        ("Can I put my own brand on the mats?",
         "Yes. OEM and ODM orders can carry your brand mark, colour and packaging, subject to a tooling check and sample approval."),
        ("What is the minimum order quantity?",
         "The MOQ printed on each listing is that listing's own minimum. Send your target quantity and destination country and we confirm what we can do."),
        ("How do I get a sample before ordering in bulk?",
         "Use the quote form or WhatsApp with your vehicle, quantity and destination. A first-article sample can be arranged before mass production."),
    ]


def product_faq(p):
    f = p.get("fitment") or {}
    veh = f'{f.get("make", "")} {f.get("model", "")}'.strip()
    lead = (f'This listing is for the {veh}. ' if veh
            else 'Tell us your vehicle and we confirm the fitment. ')
    return [
        ("How do I confirm this fits my car?", lead +
         "Send the year, body type and drive side; we check the tooling and confirm before production."),
        ("What is it made of?",
         "TPE, a thermoplastic elastomer. It contains no plasticiser, so it does not give off the chemical smell PVC mats develop in a hot cabin, and it stays flexible in cold weather."),
        ("How do I clean it?",
         "Shake out loose dirt, then hose it down or wipe with a damp cloth. Mild detergent is enough - no solvent and no machine washing."),
        ("Can it be branded for my shop?",
         "Yes, OEM and ODM branding is available. Send your artwork, colour and packaging requirements with the enquiry."),
    ]


def breadcrumb(trail):
    parts = []
    for i, (name, url) in enumerate(trail):
        if url and i < len(trail) - 1:
            parts.append(f'<a href="{url}">{name}</a>')
        else:
            parts.append(name)
    return '<div class="wrap crumb">' + " &rsaquo; ".join(parts) + "</div>"


# ---------------------------------------------------------------------------
# home
# ---------------------------------------------------------------------------

def finder_block():
    return f"""<div class="finder">
<div class="finder-row">
<div><label>Year</label><select id="fYear"></select></div>
<div><label>Make</label><select id="fMake"></select></div>
<div><label>Model</label><select id="fModel"></select></div>
<div><button class="btn btn-p" onclick="openQuote('Vehicle request')">Get Quote</button></div>
</div>
<p class="finder-note" style="margin-top:14px">Not in the list? Send us the make, model and year - we check the tooling and come back with price and sample lead time. <a href="javascript:void(0)" onclick="openQuote('Vehicle request')" style="color:var(--accent)">Request your vehicle</a></p>
<p class="finder-note" id="fStatus"></p>
<div class="finder-res" id="fResult"></div>
</div>"""


def tpe_table():
    rows = [
        ("Odour", "Odourless - no plasticiser to evaporate", "Smell from plasticiser release", "Strong rubber smell"),
        ("Cold weather", "Stays flexible at low temperature", "Hardens and can crack", "Stiffens when freezing"),
        ("Recycling", "100 percent recyclable", "Difficult to recycle", "Limited recyclability"),
        ("Halogen content", "Halogen-free", "Contains chlorine from PVC", "None"),
        ("Moulding accuracy", "Laser-measured 3D forms, deep trays", "Good but softer detail", "Limited shape complexity"),
        ("Feel and finish", "Matte, non-slip, low gloss", "Glossy, can feel slick", "Heavy, coarse grain"),
    ]
    body = "".join(f'<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td></tr>' for r in rows)
    return f"""<div class="tbl"><table class="specs">
<tr><td style="background:var(--card2);color:var(--t2)">Property</td><td style="background:var(--card2);color:var(--accent);font-weight:600">TPE</td><td style="background:var(--card2);color:var(--t2)">PVC</td><td style="background:var(--card2);color:var(--t2)">Rubber</td></tr>
{body}</table></div>
<p style="color:var(--t3);font-size:.78rem">Comparison based on general polymer properties. Ask for our own test reports for the compounds we mould.</p>"""


def index_html():
    nv = len(VEHICLES)
    np_ = len(PRODUCTS)
    stats = [(str(nv) if nv else "New", "Vehicle Models Covered"),
             (str(np_) if np_ else "Soon", "Products Online"),
             ("4", "Mat Categories"),
             ("LHD / RHD", "Tooling Options")]
    stats_html = "".join(f'<div><b>{n}</b><span>{l}</span></div>' for n, l in stats)

    cat_cards = "".join(
        f'<a href="/{c["id"]}/" class="feat"><h4>{c["name"]}</h4><p>{c["blurb"]}</p>'
        f'<span style="color:var(--accent);font-size:.85rem;display:block;margin-top:10px">Browse &rarr;</span></a>'
        for c in CATEGORIES)

    if PRODUCTS:
        cards = "".join(product_card(p) for p in PRODUCTS[:9])
        best = f'<div class="grid">{cards}</div>'
        best_more = f'<div style="text-align:center;margin-top:34px"><a href="/shop-by-vehicle/" class="btn btn-o">Browse by vehicle ({nv})</a></div>' if nv else ""
    else:
        best = ('<div class="empty"><b>Catalogue is being loaded.</b> Product pages go live as soon as the '
                'factory catalogue and fitment data are confirmed - every listing carries the exact year '
                'range, body type and drive side it fits. Tell us your vehicle and we will quote from '
                'existing tooling right away.</div>')
        best_more = ""

    if VEHICLES:
        vcards = "".join(vehicle_card(v) for v in sorted(VEHICLES, key=lambda x: (x["make"], x["model"]))[:12])
        veh_sec = f"""<section id="vehicles" style="background:var(--bg2)"><div class="wrap">
<div class="sec-head"><div><span class="tag">Fitment Index</span><h2>Vehicle Coverage</h2></div><a href="/shop-by-vehicle/">All vehicles &rarr;</a></div>
<div class="vgrid">{vcards}</div></div></section>"""
    else:
        veh_sec = """<section id="vehicles" style="background:var(--bg2)"><div class="wrap">
<div class="sec-head"><div><span class="tag">Fitment Index</span><h2>Vehicle Coverage</h2></div><a href="/shop-by-vehicle/">Vehicle index &rarr;</a></div>
<div class="empty"><b>The mould coverage list is being compiled.</b> Send us the make, model and year you need and our engineer checks the tooling list the same day - if we already have the mould we quote FOB price and sample lead time immediately.</div>
</div></section>"""

    cert_sec = ""
    certs = SITE.get("certificates") or []
    if certs:
        chips = "".join(f'<div class="feat"><h4>{c}</h4><p>Report available on request.</p></div>' for c in certs)
        cert_sec = f'<section id="trust"><div class="wrap"><div class="sec-head"><div><span class="tag">Compliance</span><h2>Testing &amp; Certificates</h2></div></div><div class="feats">{chips}</div></div></section>'

    feats = [
        ("Odourless TPE", "No plasticiser, so no smell in a hot car - the complaint buyers raise most often about cheap PVC mats."),
        ("Laser-Measured Fit", "Each liner is moulded to a measured floor pan: raised edges, OE fixing points and anti-slip nibs."),
        ("OEM / ODM", "Your brand on the mat, your packaging, your colour - tooling and artwork handled in-house."),
        ("Low MOQ", "Start with a sample order and scale the SKUs that sell in your market."),
        ("Container Consolidation", "Mix liners, mats and cargo liners into one container with one set of documents."),
        ("Reply Within 24h", "Fitment questions, FOB pricing and sample lead times answered on WhatsApp or email."),
    ]
    feat_html = "".join(f'<div class="feat"><h4>{t}</h4><p>{d}</p></div>' for t, d in feats)

    body = f"""<body>
{nav()}
<header class="hero"><div class="wrap">
<h1>3D TPE Car Floor Liners - <span>Factory Direct</span>, Custom Fit</h1>
<p>We mould TPE floor liners, all-weather mats and cargo liners for specific vehicles - not universal rubber sheets. Tell us the year, make and model and we quote from existing tooling.</p>
<div class="cta-row"><a href="#finder" class="btn btn-p">Find Mats for My Car</a>
<a href="javascript:void(0)" onclick="openQuote('')" class="btn btn-o">Get Wholesale Quote</a>
<a href="https://wa.me/{WA}" class="btn btn-wa" target="_blank" rel="noopener">WhatsApp</a></div>
<div class="trust">{stats_html}</div>
</div></header>
<section id="finder"><div class="wrap">
<div class="sec-head"><div><span class="tag">Fitment Finder</span><h2>Find Mats for Your Car</h2>
<p style="color:var(--t3);font-size:.88rem;margin-top:6px">Pick year, make and model - we show every TPE mat we can mould for that vehicle.</p></div><a href="/shop-by-vehicle/">Browse all vehicles &rarr;</a></div>
{finder_block()}
</div></section>
<section id="cats" style="background:var(--bg2)"><div class="wrap">
<div class="sec-head"><h2>Product Categories</h2></div>
<div class="feats">{cat_cards}</div></div></section>
{veh_sec}
<section id="bestsellers"><div class="wrap">
<div class="sec-head"><div><span class="tag">Catalogue</span><h2>Featured TPE Liners</h2></div></div>
{best}{best_more}</div></section>
<section id="why-tpe" style="background:var(--bg2)"><div class="wrap">
<div class="sec-head"><div><span class="tag">Material</span><h2>Why TPE - Not PVC or Rubber</h2></div></div>
{tpe_table()}</div></section>
<section id="oem"><div class="wrap">
<div class="sec-head"><div><span class="tag">OEM / ODM</span><h2>From Vehicle Scan to Container</h2></div></div>
<div class="feats">
<div class="feat"><h4>1. Fitment Check</h4><p>Send make, model, year, body type and drive side. We confirm existing tooling or quote a new mould.</p></div>
<div class="feat"><h4>2. Sample</h4><p>First-article sample in your colour and thickness so you can test the fit before committing.</p></div>
<div class="feat"><h4>3. Mould &amp; Mass Production</h4><p>Tooling, compound, brand marking and packaging set to your market requirements.</p></div>
<div class="feat"><h4>4. Packing &amp; Shipping</h4><p>Export cartons, container loading plan and full document set for your customs broker.</p></div>
</div>
<p style="color:var(--t2);margin-top:22px;font-size:.92rem">Send us your specification or a photo of the vehicle floor - our engineer replies with tooling status, FOB price and sample lead time. <a href="https://wa.me/{WA}" style="color:var(--accent)" target="_blank" rel="noopener">Start on WhatsApp</a>.</p>
</div></section>
{cert_sec}
<section id="contact" class="cta"><div class="wrap">
<h2>Sourcing TPE Car Mats?</h2>
<p>Factory-direct FOB pricing, low MOQ, samples before bulk. Send your vehicle list and target market.</p>
<a href="javascript:void(0)" onclick="openQuote('')" class="btn btn-p">Get Wholesale Quote</a>
<a href="https://wa.me/{WA}" class="btn btn-wa" target="_blank" rel="noopener">WhatsApp +{WA}</a>
</div></section>
<script>{finder_js()}</script>
{footer()}"""

    title = f"TPE Car Floor Liners Factory - 3D Custom Fit Liners, Mats & Cargo Liners | {BRAND}"
    desc = ("Factory-direct 3D TPE car floor liners, all-weather mats and cargo liners moulded for specific "
            "vehicles. Odourless TPE, OEM/ODM, low MOQ, worldwide shipping.")
    return shell(title, desc, URL, og_image("/images/og-default.jpg"), body, ld_script(ld_org()))


# ---------------------------------------------------------------------------
# category / product / vehicle / blog pages
# ---------------------------------------------------------------------------

def category_html(cid):
    c = next(x for x in CATEGORIES if x["id"] == cid)
    items = [p for p in PRODUCTS if p["cat"] == cid]
    canonical = f'{URL}{cid}/'
    title = f'{c["name"]} - TPE Car Mats, Factory Direct | {BRAND}'
    desc = (f'{c["blurb"]} FOB pricing, OEM/ODM welcome, low MOQ.')[:158]
    if items:
        cards = "".join(product_card(p) for p in items)
        head_html = f'<div class="sec-head"><div><span class="tag">{c["name"]}</span><h1>{c["name"]}</h1><p style="color:var(--t3);margin-top:8px">{len(items)} products in this category.</p></div></div>'
        grid = f'<div class="grid">{cards}</div>'
    else:
        head_html = f'<div class="sec-head"><div><span class="tag">{c["name"]}</span><h1>{c["name"]}</h1></div></div>'
        grid = ('<div class="empty"><b>Listings for this category are being finalised.</b> Each product page '
                'states the exact make, model, year range and drive side it fits. Ask us for the vehicle you '
                'need and we reply with tooling status and FOB price.</div>')
    ld = ld_script(ld_collection(c["name"], desc, canonical)) + \
         ld_script(ld_crumbs([("Home", "/"), (c["name"], f"/{cid}/")]))
    body = f"""<body>
{nav(cid)}
{breadcrumb([("Home", "/"), (c["name"], f"/{cid}/")])}
<section><div class="wrap">
{head_html}
{('<div class="guide">' + CATEGORY_COPY[cid] + '</div>') if CATEGORY_COPY.get(cid) else ''}
{grid}
</div></section>
<section id="contact" class="cta"><div class="wrap">
<h2>Need Bulk Pricing for {c["name"]}?</h2>
<p>Send your vehicle list and target market - we quote from existing tooling and suggest the SKUs that move in your country.</p>
<a href="javascript:void(0)" onclick="openQuote('{c["name"]}')" class="btn btn-p">Get Wholesale Quote</a>
<a href="https://wa.me/{WA}" class="btn btn-wa" target="_blank" rel="noopener">WhatsApp +{WA}</a>
</div></section>
{footer()}"""
    og = og_image(items[0]["img"]) if items else ""
    return shell(title, desc, canonical, og, body, ld)


def product_page(p):
    canonical = f'{URL}products/{p["slug"]}/'
    title = f'{p["name"]} | Factory Direct | {BRAND}'
    desc = p["desc"][:155]
    cat = category_name(p["cat"])
    f = p.get("fitment") or {}

    fit_rows = []
    if f:
        for label, key in (("Make", "make"), ("Model", "model"), ("Years", "years"),
                           ("Body", "body"), ("Drive side", "hand")):
            if f.get(key):
                fit_rows.append(f'<div><span>{label}</span><b>{f[key]}</b></div>')
        if f.get("positions"):
            fit_rows.append(f'<div><span>Positions</span><b>{", ".join(f["positions"])}</b></div>')
    fit_html = ""
    if fit_rows:
        vs = vehicles_for_product(p)
        more = ""
        if vs:
            more = f'<p style="font-size:.84rem;margin-top:10px"><a href="{vurl(vs[0])}" style="color:var(--accent)">See all mats for {vs[0]["make"]} {vs[0]["model"]} &rarr;</a></p>'
        fit_html = f'<div class="block"><h4>Vehicle Fitment</h4><div class="fit">{"".join(fit_rows)}</div>{more}</div>'

    specs = "".join(f"<tr><td>{k}</td><td>{v}</td></tr>" for k, v in p["specs"])
    pts = "".join(f"<li>{x}</li>" for x in p["points"])

    related = []
    for s in p.get("related") or []:
        if s in RELATED_INDEX:
            related.append(RELATED_INDEX[s])
    if not related:
        for other in PRODUCTS:
            if other["slug"] != p["slug"] and (other.get("fitment") or {}).get("model") == f.get("model"):
                related.append(other)
            if len(related) >= 3:
                break
    if len(related) < 3:
        for other in PRODUCTS:
            if other["slug"] != p["slug"] and other not in related:
                related.append(other)
            if len(related) >= 3:
                break
    rel_html = f'<section class="related"><div class="wrap"><div class="sec-head"><div><span class="tag">Related</span><h2>Fits the Same Vehicle</h2></div></div><div class="grid">{"".join(product_card(x) for x in related)}</div></div></section>' if related else ""

    trail = [("Home", "/"), (cat, f'/{p["cat"]}/')]
    if f.get("make") and f.get("model"):
        trail.append((f'{f["make"]} {f["model"]}', ""))
    trail.append((p["name"], ""))
    ld = ld_script(ld_product(p, canonical)) + ld_script(ld_crumbs(trail[:2] + [(p["name"], "")])) + \
         ld_script(ld_faq(product_faq(p)))
    body = f"""<body>
{nav(p["cat"])}
{breadcrumb(trail)}
<div class="wrap pd">
<div class="pd-img">{picture(p["img"], p["name"], 800, 600, card=False, loading="eager")}</div>
<div class="pd-info">
<h1>{p["name"]}</h1>
<div class="pd-price">{p["price"]}</div>
<div class="pd-moq">{p["moq"]} &middot; FOB China &middot; Worldwide shipping</div>
<p class="pd-desc">{p["desc"]}</p>
<div class="cta-row">
<a href="javascript:void(0)" onclick="openQuote('{p["name"]}')" class="btn btn-p">Get Wholesale Quote</a>
<a href="https://wa.me/{WA}?text={p["slug"].replace("-", "%20")}%20inquiry" class="btn btn-wa" target="_blank" rel="noopener">WhatsApp Inquiry</a>
</div>
{fit_html}
<div class="block"><h4>Material: TPE (Thermoplastic Elastomer)</h4>
<ul><li>Odourless - no plasticiser, no chemical smell in a hot cabin</li>
<li>Flexible in cold weather, does not go brittle</li>
<li>Halogen-free and 100 percent recyclable</li>
<li>Laser-measured 3D form with raised edges to hold water, mud and snow</li></ul></div>
<table class="specs">{specs}</table>
<div class="pts"><h4>Why Buyers Choose This Product</h4><ul>{pts}</ul></div>
</div>
</div>
{faq_block(product_faq(p))}
{rel_html}
{footer()}"""
    return shell(title, desc, canonical, og_image(p["img"]), body, ld)


def vehicle_page(v):
    canonical = URL.rstrip("/") + vurl(v)
    prods = products_for_vehicle(v)
    title = f'3D TPE Floor Liners for {vfull(v)} - Factory Direct | {BRAND}'
    desc = (f'Custom-fit 3D TPE floor liners, mats and cargo liners for {vfull(v)}. '
            f'Odourless TPE, OEM branding, FOB pricing, low MOQ.')[:158]
    trail = [("Home", "/"), ("Shop by Vehicle", "/shop-by-vehicle/"),
             (v["make"], "/shop-by-vehicle/"), (vname(v), vurl(v))]
    meta = [("Make", v["make"]), ("Model", v["model"]),
            ("Years", v["years"] or "tell us your year - we confirm the mould")]
    if v.get("body"):
        meta.append(("Body", v["body"]))
    if v.get("hand"):
        meta.append(("Drive side", v["hand"]))
    if v.get("positions"):
        meta.append(("Positions available", ", ".join(v["positions"])))
    meta_html = "".join(f'<div><span>{k}</span><b>{val}</b></div>' for k, val in meta)

    if prods:
        grid = f'<div class="grid">{"".join(product_card(p) for p in prods)}</div>'
    else:
        grid = ('<div class="empty"><b>Send us your model and year.</b> '
                'We confirm whether the tooling exists for that exact combination, then quote FOB price, '
                'MOQ and sample lead time directly.</div>')

    sibs = [x for x in VEHICLES if x["make"] == v["make"] and x["slug"] != v["slug"]]
    sib_html = ""
    if sibs:
        sib_html = (f'<section style="background:var(--bg2)"><div class="wrap">'
                    f'<div class="sec-head"><div><span class="tag">Same Brand</span><h2>Other {v["make"]} Models</h2></div>'
                    f'<a href="/shop-by-vehicle/">All vehicles &rarr;</a></div>'
                    f'<div class="vgrid">{"".join(vehicle_card(x) for x in sorted(sibs, key=lambda z: z["model"]))}</div>'
                    f'</div></section>')
    note = f'<p style="color:var(--t2);font-size:.9rem;margin-top:14px">{v["note"]}</p>' if v.get("note") else ""
    vimg = og_image(v.get("img") or "")
    hero = ""
    if vimg:
        hero = (f'<div class="vhero"><img src="{vimg}" alt="{vname(v)} TPE floor liners" '
                f'width="1200" height="600" loading="lazy" decoding="async"></div>')

    ld = ld_script(ld_collection(f'{v["make"]} {v["model"]} TPE floor liners', desc, canonical)) + \
         ld_script(ld_crumbs([("Home", "/"), ("Shop by Vehicle", "/shop-by-vehicle/"),
                              (v["make"], "/shop-by-vehicle/"), (vname(v), vurl(v))])) + \
         ld_script(ld_faq(vehicle_faq(v)))
    body = f"""<body>
{nav()}
{breadcrumb([("Home", "/"), ("Shop by Vehicle", "/shop-by-vehicle/"), (v["make"], "/shop-by-vehicle/"), (vname(v), "")])}
<section><div class="wrap">
<div class="sec-head"><div><span class="tag">Vehicle Fitment</span>
<h1>3D TPE Floor Liners for {vfull(v)}</h1>
<p style="color:var(--t3);margin-top:8px">Custom-moulded to the {vname(v)} floor pan - not a universal trim-to-fit mat.</p></div>
<a href="javascript:void(0)" onclick="openQuote('{vfull(v)}')">Get quote &rarr;</a></div>
{hero}
<div class="fit">{meta_html}</div>
{note}
</div></section>
<section><div class="wrap">
<div class="sec-head"><div><span class="tag">Available Products</span><h2>{vname(v)} Mats &amp; Liners</h2></div></div>
{grid}
<p style="color:var(--t2);font-size:.9rem;margin-top:20px">Not the right year? Fitment changes between generations - <a href="/shop-by-vehicle/" style="color:var(--accent)">pick another year</a> or <a href="javascript:void(0)" onclick="openQuote('{vname(v)} - other year')" style="color:var(--accent)">tell us your year</a>.</p>
</div></section>
{faq_block(vehicle_faq(v))}
{sib_html}
<section id="contact" class="cta"><div class="wrap">
<h2>{vname(v)} Floor Liners - Wholesale</h2>
<p>Samples before bulk, OEM branding, container consolidation. Send your quantity and market.</p>
<a href="javascript:void(0)" onclick="openQuote('{vname(v)}')" class="btn btn-p">Get Wholesale Quote</a>
<a href="https://wa.me/{WA}" class="btn btn-wa" target="_blank" rel="noopener">WhatsApp +{WA}</a>
</div></section>
{footer()}"""
    og = vimg or (og_image(prods[0]["img"]) if prods else "")
    return shell(title, desc, canonical, og, body, ld)


def vehicle_index():
    canonical = URL + "shop-by-vehicle/"
    title = f'Shop TPE Floor Liners by Vehicle - Full Fitment Index | {BRAND}'
    desc = "Browse custom-fit TPE floor liners by make and model. Every listing states the exact year range, body type and drive side it fits."
    makes = {}
    for v in VEHICLES:
        makes.setdefault(v["make"], []).append(v)
    if makes:
        blocks = ""
        for make in sorted(makes):
            items = sorted(makes[make], key=lambda x: x["model"])
            blocks += (f'<div style="margin-bottom:34px"><div class="sec-head" style="margin-bottom:14px">'
                       f'<div><span class="tag">{make}</span><h2>{make} TPE Floor Liners</h2></div>'
                       f'<span style="color:var(--t3);font-size:.85rem">{len(items)} models</span></div>'
                       f'<div class="vgrid">{"".join(vehicle_card(x) for x in items)}</div></div>')
    else:
        blocks = ('<div class="empty"><b>The fitment index is being compiled from our mould list.</b> '
                  'We mould for a defined list of vehicles and publish each one with its exact year range and '
                  'drive side. Send us the make, model and year you need - we check the tooling list the same day.</div>')
    ld = ld_script(ld_collection("Shop by Vehicle", desc, canonical)) + \
         ld_script(ld_crumbs([("Home", "/"), ("Shop by Vehicle", "/shop-by-vehicle/")]))
    body = f"""<body>
{nav()}
{breadcrumb([("Home", "/"), ("Shop by Vehicle", "")])}
<section><div class="wrap">
<div class="sec-head"><div><span class="tag">Fitment Index</span><h1>Shop by Vehicle</h1>
<p style="color:var(--t3);margin-top:8px">Every vehicle below has confirmed tooling. Pick your model to see the liners, mats and cargo liners available for it.</p></div></div>
{blocks}
</div></section>
<section id="contact" class="cta"><div class="wrap">
<h2>Don't See Your Car?</h2>
<p>Send the make, model and year. We check the tooling list and reply with FOB pricing, MOQ and sample lead time - or tell you straight away if it is not something we can make.</p>
<a href="javascript:void(0)" onclick="openQuote('New vehicle request')" class="btn btn-p">Request Your Vehicle</a>
<a href="https://wa.me/{WA}" class="btn btn-wa" target="_blank" rel="noopener">WhatsApp +{WA}</a>
</div></section>
{footer()}"""
    return shell(title, desc, canonical, "", body, ld)


def blog_index():
    canonical = URL + "blog/"
    title = f'TPE Car Mat Guides &amp; Buying Advice | {BRAND}'
    desc = "Guides for importers and distributors: TPE versus PVC and rubber, how to spec floor liners, and what to check in a custom mat OEM project."
    cards = "".join(
        f'<a href="/blog/{a["slug"]}/" class="feat"><h4>{a["title"]}</h4><p>{a["desc"]}</p>'
        f'<span style="color:var(--accent);font-size:.85rem;display:block;margin-top:10px">Read &rarr;</span></a>'
        for a in ARTICLES)
    ld = ld_script(ld_collection("Blog", desc, canonical))
    body = f"""<body>
{nav()}
{breadcrumb([("Home", "/"), ("Blog", "")])}
<section><div class="wrap">
<div class="sec-head"><div><span class="tag">Guides</span><h1>TPE Car Mat Guides</h1></div></div>
<div class="feats">{cards}</div>
</div></section>
{footer()}"""
    return shell(title, desc, canonical, "", body, ld)


def article_page(a):
    canonical = f'{URL}blog/{a["slug"]}/'
    title = f'{a["title"]} | {BRAND}'
    desc = a["desc"]
    ld = ld_script(json.dumps({
        "@context": "https://schema.org", "@type": "Article",
        "headline": a["title"], "description": a["desc"], "datePublished": a.get("date", ""),
        "author": {"@type": "Organization", "name": BRAND},
        "publisher": {"@type": "Organization", "name": BRAND}, "mainEntityOfPage": canonical
    }, ensure_ascii=False)) + ld_script(ld_crumbs([("Home", "/"), ("Blog", "/blog/"), (a["title"], canonical)]))
    body = f"""<body>
{nav()}
{breadcrumb([("Home", "/"), ("Blog", "/blog/"), (a["title"], "")])}
<article class="wrap post" style="padding-bottom:50px">
<span class="tag">{a.get("kind", "Guide")}</span>
<h1>{a["title"]}</h1>
<p style="color:var(--t3);font-size:.85rem;margin-bottom:22px">{a.get("date", "")}</p>
{a["body"]}
</article>
<section id="contact" class="cta"><div class="wrap">
<h2>Need a Quote for TPE Mats?</h2>
<p>Send your vehicle list, quantity and target market.</p>
<a href="javascript:void(0)" onclick="openQuote('')" class="btn btn-p">Get Wholesale Quote</a>
</div></section>
{footer()}"""
    return shell(title, desc, canonical, a.get("img", ""), body, ld)


def site_map():
    """Crawlable HTML index of everything - helps discovery and spreads
    internal link equity to the deep vehicle and product pages."""
    canonical = URL + "site-map/"
    title = f'Site Map - All TPE Floor Liners, Vehicle Pages and Guides | {BRAND}'
    desc = (f'Every page on {DOMAIN}: TPE floor liner categories, the full '
            f'vehicle fitment index and our importer guides.')[:158]
    cats = "".join(f'<a href="/{c["id"]}/">{c["name"]}</a>' for c in CATEGORIES)

    by_make = {}
    for v in VEHICLES:
        by_make.setdefault(v["make"], []).append(v)
    veh_html = "".join(
        f'<div class="sm-col"><h3>{make} ({len(vs)})</h3>' +
        "".join(f'<a href="{vurl(x)}">{vname(x)}</a>' for x in sorted(vs, key=lambda z: z["model"])) +
        "</div>" for make, vs in sorted(by_make.items()))

    by_cat = {}
    for p in PRODUCTS:
        by_cat.setdefault(p["cat"], []).append(p)
    prod_html = ""
    for c in CATEGORIES:
        items = by_cat.get(c["id"], [])
        if not items:
            continue
        prod_html += (f'<div class="sm-col"><h3>{c["name"]} ({len(items)})</h3>' +
                      "".join(f'<a href="/products/{p["slug"]}/">{p["name"]}</a>'
                              for p in sorted(items, key=lambda z: z["name"])) + "</div>")

    blog_html = ""
    if ARTICLES:
        blog_html = ('<div class="sm-col"><h3>Guides</h3>' +
                     "".join(f'<a href="/blog/{a["slug"]}/">{a["title"]}</a>' for a in ARTICLES) + "</div>")

    body = f"""<body>
{nav()}
{breadcrumb([("Home", "/"), ("Site Map", "")])}
<section><div class="wrap">
<div class="sec-head"><div><span class="tag">Index</span><h1>Site Map</h1>
<p style="color:var(--t3);margin-top:8px">{len(CATEGORIES)} categories &middot; {len(VEHICLES)} vehicle pages &middot; {len(PRODUCTS)} products{(' &middot; ' + str(len(ARTICLES)) + ' guides') if ARTICLES else ''}</p></div></div>
<div class="sm-col"><h3>Categories</h3>{cats}</div>
{veh_html}
{prod_html}
{blog_html}
<div class="sm-col"><h3>Site</h3><a href="/">Home</a><a href="/blog/">Blog</a><a href="/#finder">Fitment finder</a></div>
</div></section>
{footer()}"""
    ld = ld_script(ld_crumbs([("Home", "/"), ("Site Map", canonical)]))
    return shell(title, desc, canonical, "", body, ld)


def not_found():
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">
<title>404 - Page Not Found | {BRAND}</title>
<meta name="description" content="This page could not be found. Browse TPE floor liners by vehicle from the factory, or send us your make, model and year for a quotation.">
<meta name="robots" content="noindex"><link rel="canonical" href="{URL}404.html">
<style>body{{background:#0A0C10;color:#E9EEF4;font-family:Inter,system-ui,sans-serif;text-align:center;padding:80px 20px}}
a{{color:#FF6A1F}}h1{{font-family:Oswald;font-size:3rem;color:#FF6A1F}}</style></head><body>
<h1>404</h1><p>Page not found.</p>
<p><a href="/">Back to {BRAND}</a> &middot; <a href="/shop-by-vehicle/">Shop by vehicle</a></p></body></html>"""


# ---------------------------------------------------------------------------
# vehicles.json + build
# ---------------------------------------------------------------------------

def vehicles_payload():
    """Compact payload for the home-page finder (one request, no backend)."""
    out = []
    for v in VEHICLES:
        prods = []
        for p in products_for_vehicle(v):
            d = p["desc"][:100] + ("..." if len(p["desc"]) > 100 else "")
            base = p["img"][:-4] if p["img"].lower().endswith(".jpg") else p["img"]
            card_webp = base + "-card.webp"
            prods.append({
                "slug": p["slug"], "name": p["name"], "price": p["price"], "moq": p["moq"],
                "img": p["img"], "badge": p.get("badge", ""), "desc": d,
                "imgc": base + "-card.jpg" if base != p["img"] else p["img"],
                "imgw": card_webp if img_exists(card_webp) else "",
                "url": f'/products/{p["slug"]}/',
            })
        out.append({
            "slug": v["slug"], "make": v["make"], "model": v["model"], "years": v["years"],
            "body": v.get("body", ""), "hand": v.get("hand", ""),
            "url": vurl(v), "products": prods,
        })
    return out


def write_file(rel, text):
    path = os.path.join(BASE, rel.replace("/", os.sep))
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    return rel


def sitemap_xml():
    today = datetime.now().strftime("%Y-%m-%d")
    rows = [(URL, "1.0", "daily"), (URL + "shop-by-vehicle/", "0.9", "weekly"),
            (URL + "site-map/", "0.4", "monthly")]
    for c in CATEGORIES:
        rows.append((f'{URL}{c["id"]}/', "0.9", "daily"))
    for v in VEHICLES:                       # vehicle pages rank above product pages
        rows.append((URL.rstrip("/") + vurl(v), "0.9", "weekly"))
    for p in PRODUCTS:
        rows.append((f'{URL}products/{p["slug"]}/', "0.8", "weekly"))
    if ARTICLES:
        rows.append((URL + "blog/", "0.7", "weekly"))
    for a in ARTICLES:
        rows.append((f'{URL}blog/{a["slug"]}/', "0.7", "weekly"))
    body = "".join(
        f"<url><loc>{u}</loc><lastmod>{today}</lastmod><priority>{pr}</priority>"
        f"<changefreq>{cf}</changefreq></url>" for u, pr, cf in rows)
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + body + "\n</urlset>\n")


def images_note():
    return (
        f"Images for {DOMAIN}\n"
        "====================\n\n"
        "Required naming (referenced by products_data.py):\n"
        "  images/<product-slug>.jpg          product main image, 816x816 recommended\n"
        "  images/vehicles/<make>-<model>.jpg vehicle page image, 1200x800 recommended\n\n"
        "Rules for this site:\n"
        "  * factory-owned or own-product photos only - never competitor or branded images\n"
        "  * no third-party brand marks, no OEM logos, no model codes from other companies\n"
        "  * no watermarks, no supplier company names\n"
        "  * one product = one image, JPG, under 200 KB, square or 4:3\n"
    )


def main():
    made = []
    check_unique_vehicle_urls()
    # Always create the directories GitHub Pages serves from, even when the
    # catalogue is still empty, so the repo layout is complete from day one.
    for d in ("products", "images", "shop-by-vehicle", "blog"):
        os.makedirs(os.path.join(BASE, d), exist_ok=True)
    made.append(write_file("index.html", index_html()))
    for c in CATEGORIES:
        made.append(write_file(f'{c["id"]}/index.html', category_html(c["id"])))
    for p in PRODUCTS:
        made.append(write_file(f'products/{p["slug"]}/index.html', product_page(p)))
    for v in VEHICLES:
        made.append(write_file(vurl(v).strip("/") + "/index.html", vehicle_page(v)))
    made.append(write_file("shop-by-vehicle/index.html", vehicle_index()))
    made.append(write_file("site-map/index.html", site_map()))
    if ARTICLES:
        made.append(write_file("blog/index.html", blog_index()))
        for a in ARTICLES:
            made.append(write_file(f'blog/{a["slug"]}/index.html', article_page(a)))

    write_file("vehicles.json", json.dumps(vehicles_payload(), ensure_ascii=False, indent=1))
    write_file("CNAME", DOMAIN + "\n")
    write_file(".nojekyll", "")          # skip Jekyll processing on GitHub Pages
    # IndexNow ownership proof: Bing/Yandex fetch this file to verify we are
    # allowed to push URLs. tools/indexnow_push.py does the submitting.
    write_file(f"{INDEXNOW_KEY}.txt", INDEXNOW_KEY + "\n")
    write_file("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {URL}sitemap.xml\n")
    write_file("sitemap.xml", sitemap_xml())
    write_file("404.html", not_found())
    write_file("images/README.txt", images_note())

    print(f"HTML pages written : {len(made)}")
    print(f"  home             : 1")
    print(f"  category pages   : {len(CATEGORIES)}")
    print(f"  product pages    : {len(PRODUCTS)}")
    print(f"  vehicle pages    : {len(VEHICLES)}")
    print(f"  blog pages       : {len(ARTICLES) + (1 if ARTICLES else 0)}")
    print(f"vehicles.json      : {len(VEHICLES)} vehicles, "
          f"{sum(len(v['products']) for v in vehicles_payload())} linked product cards")
    sitemap_urls = sitemap_xml().count("<url>")
    print(f"sitemap.xml        : {sitemap_urls} URLs")
    missing = [k for k in ("email", "formspree", "ga4", "clarity") if not SITE.get(k)]
    if missing:
        print("PLACEHOLDER config still empty (generator skipped them): " + ", ".join(missing))
    if not PRODUCTS:
        print("NOTE: PRODUCTS is empty - listings await the real factory catalogue.")
    if not VEHICLES:
        print("NOTE: VEHICLES is empty - the fitment index awaits the real mould list.")


if __name__ == "__main__":
    main()
