# -*- coding: utf-8 -*-
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1] / "public"
css_path = root / "css" / "site.css"
text = css_path.read_text(encoding="utf-8")
pgrid = """
/* Photo gallery grid */
#photos{padding:3rem 0 4rem}
.pgrid{display:grid;gap:.6rem;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));margin-top:2rem}
.pc{position:relative;display:block;overflow:hidden;background:#1a1a18}
.pc img{width:100%;height:auto;aspect-ratio:4/3;object-fit:cover;display:block;transition:transform .5s}
.pc:hover img{transform:scale(1.05)}
.pc-t{position:absolute;left:0;right:0;bottom:0;padding:1rem .9rem .8rem;background:linear-gradient(transparent,#000c);color:#fff;display:flex;flex-direction:column}
.pc-t b{font-family:'Playfair Display',serif;font-size:1.15rem}
.pc-t i{font-style:normal;font-size:.72rem;opacity:.85;margin-top:.15rem}
@media(min-width:900px) and (max-width:1280px){
  .nav-links{gap:.55rem}
  .nav-links a{font-size:.68rem;letter-spacing:.06em}
}
"""
if ".pgrid{" not in text:
    css_path.write_text(text + pgrid, encoding="utf-8")
    print("css updated")
else:
    print("pgrid already in css")

SECTION_HEAD = re.compile(r'<div class="section-head">.*?</div>\s*', re.S)
INLINE_STYLE = re.compile(r"<style>#photos\{.*?</style>", re.S)

for name in ["gallery", "places", "videos", "faq", "getting-here", "plan", "contact", "about"]:
    p = root / name / "index.html"
    t = p.read_text(encoding="utf-8")
    t2 = INLINE_STYLE.sub("", t, count=1)
    if name in ("gallery", "places", "videos", "faq"):
        # Remove only the first section-head after </header>
        parts = t2.split("</header>", 1)
        if len(parts) == 2:
            parts[1] = SECTION_HEAD.sub("", parts[1], count=1)
            t2 = "</header>".join(parts)
    if t2 != t:
        p.write_text(t2, encoding="utf-8")
        print("cleaned", name)
    else:
        print("no change", name)

# Also strip inline style from home if present
home = root / "index.html"
ht = home.read_text(encoding="utf-8")
ht2 = INLINE_STYLE.sub("", ht, count=1)
if ht2 != ht:
    home.write_text(ht2, encoding="utf-8")
    print("cleaned home")

js_path = root / "js" / "site.js"
jt = js_path.read_text(encoding="utf-8")
jt = jt.replace("navigator.serviceWorker.register('sw.js')", "navigator.serviceWorker.register('/sw.js')")
jt = jt.replace("fab.addEventListener", "if (fab) fab.addEventListener")
jt = jt.replace("closeMdl.addEventListener", "if (closeMdl) closeMdl.addEventListener")
jt = jt.replace("modal.addEventListener", "if (modal) modal.addEventListener")
jt = jt.replace("sendBtn.addEventListener", "if (sendBtn) sendBtn.addEventListener")
js_path.write_text(jt, encoding="utf-8")
print("js patched")
