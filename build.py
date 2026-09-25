"""Build a dependency-free, GitHub Pages-ready research website."""
import json
from pathlib import Path
from html import escape as e

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'dist'
D=json.loads((ROOT/'content.json').read_text())

def link(url,label,cls=''):
    return f'<a href="{e(url,quote=True)}"'+(f' class="{cls}"' if cls else '')+f'>{label}</a>'

def nav(active):
    entries=[('Home','index.html'),('Research','research.html'),('Publications','publications.html'),('About','about.html')]
    return '<header><div class="wrap header-inner"><a class="brand" href="index.html">Jinseok Lee</a><nav aria-label="Main navigation">'+''.join(f'<a href="{url}"'+(' aria-current="page"' if name==active else '')+f'>{name}</a>' for name,url in entries)+'</nav></div></header>'

def shell(title,content,active):
    desc='Jinseok Lee is a Ph.D. student at Yale University studying fluid mechanics, soft matter, and transport through experiments and simulations.'
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{e(title)} · Jinseok Lee</title><meta name="description" content="{desc}"><meta name="theme-color" content="#00356b"><link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='10' fill='%2300356b'/%3E%3Ctext x='32' y='44' text-anchor='middle' font-family='Georgia' font-size='36' fill='white'%3EJL%3C/text%3E%3C/svg%3E"><link rel="stylesheet" href="style.css"></head><body><a class="skip" href="#main">Skip to content</a>{nav(active)}<main id="main" class="wrap">{content}</main><footer><div class="wrap footer-inner"><div>Jinseok Lee · Yale University<br>Fluid mechanics, soft matter &amp; transport</div><div>{link('mailto:'+D['email'],e(D['email']))}<br>New Haven, Connecticut</div></div></footer></body></html>'''

def social():
    return '<div class="links">'+link(D['scholar'],'Google Scholar')+link('mailto:'+D['email'],'Email')+'</div>'

def pub(p):
    title=e(p['title']); title=link(p['url'],title) if p.get('url') else title
    authors=e(p['authors']).replace('Jinseok Lee','<strong>Jinseok Lee</strong>')
    if p['id']=='stability': authors=authors.replace('J. Lee*','<strong>J. Lee*</strong>',1)
    if p['id']=='cyanobacteria': authors=authors.replace('J. Lee*','<strong>J. Lee*</strong>',1)
    links=[]
    if p.get('url'): links.append(link(p['url'],'Preprint' if p['badge']=='Preprint' else 'Article'))
    if p.get('pdf'): links.append(link(p['pdf'],'PDF'))
    badge=f'<span class="badge">{e(p["badge"])}</span>' if p['badge'] else ''
    return f'<article class="pub" id="{p["id"]}"><div class="pub-year">{p["year"]}</div><div><h3>{title}</h3><p class="authors">{authors}</p><p class="venue"><em>{e(p["venue"])}</em> {badge}</p>'+('<div class="links">'+''.join(links)+'</div>' if links else '')+'</div></article>'

def current_cards():
    return '<div class="current-grid">'+''.join(f'<article class="current-card"><h3>{link("research.html#"+r["id"],e(r["title"]))}</h3><p>{e(r["question"])}</p></article>' for r in D['research'])+'</div>'

home=f'''<section class="hero" aria-labelledby="home-title"><figure class="profile-photo"><img src="assets/portrait.jpg" alt="Portrait of Jinseok Lee" width="361" height="421"></figure><div><h1 id="home-title">Jinseok Lee</h1><p class="affiliation">Ph.D. Student<br>Mechanical Engineering &amp; Materials Science<br><a href="https://www.yale.edu/">Yale University</a></p><p class="home-intro">I study fluid mechanics and soft matter, with a focus on transport in crowded and deformable environments working with Prof. <a href="https://luogroup.research.yale.edu/" target="_blank" rel="noopener">Yimin Luo</a>.</p>{social()}</div></section>
<section class="section"><div class="section-head"><h2>Current research</h2>{link('research.html','Research details')}</div>{current_cards()}</section>
<section class="section"><div class="section-head"><h2>Selected publications</h2>{link('publications.html','All publications')}</div>{''.join(pub(D['publications'][i]) for i in [0,2,5,6])}</section>
<section class="section"><div class="section-head"><h2>Recent updates</h2></div><div class="news-row"><time datetime="2026">Summer 2026</time><p>Presented research on confined diffusion at the 100th ACS Colloids symposium and iPoLS 2026.</p></div><div class="news-row"><time datetime="2026-05">May 2026</time><p>New preprint: {link('https://arxiv.org/abs/2605.29424','Model-free estimation in scattering analysis of microscopy')}.</p></div><div class="news-row"><time datetime="2026-05">May 2026</time><p>New preprint: {link('https://arxiv.org/abs/2605.04216','Accessible pore geometry governs tracer diffusion in crowded environments')}.</p></div></section>'''

r0,r1=D['research']
def tags(r):return '<div class="tags">'+''.join(f'<span class="tag">{e(t)}</span>' for t in r['tags'])+'</div>'
research=f'''<div class="page-title research-intro"><h1>Research</h1><p>I am a fluid mechanician by training. My research connects small-scale fluid mechanics with soft matter, asking how interfaces and particle-scale structure govern transport.</p></div>
<article class="research-feature" id="diffusion"><figure class="research-video"><video autoplay loop controls muted playsinline preload="metadata" poster="assets/diffusion-poster.jpg" width="512" height="512" aria-label="Confined diffusion microscopy video" aria-describedby="diffusion-caption"><source src="assets/confined-diffusion.mp4" type="video/mp4">Your browser does not support embedded video.</video><figcaption id="diffusion-caption">Fluorescent tracers (green) moving among densely packed soft particles. Bright-field and fluorescence overlay.</figcaption></figure><div><span class="eyebrow">Current research / Yale</span><h2>{r0['title']}</h2><p>{r0['text']}</p>{tags(r0)}<div class="links">{link('https://arxiv.org/abs/2605.04216','Read the preprint')}</div></div></article>
<article class="research-feature" id="deformation"><figure class="research-video"><video autoplay loop controls muted playsinline preload="metadata" poster="assets/deformation-poster.jpg" width="640" height="480" aria-label="Flow-induced deformation microscopy video" aria-describedby="deformation-caption"><source src="assets/flow-deformation.mp4" type="video/mp4">Your browser does not support embedded video.</video><figcaption id="deformation-caption">Flow through a mixed hydrogel particle packing.</figcaption></figure><div><span class="eyebrow">Current research / Yale</span><h2>{r1['title']}</h2><p>{r1['text']}</p>{tags(r1)}</div></article>
<section class="section" id="earlier"><div class="section-head"><div><span class="eyebrow">Earlier work / Sungkyunkwan University</span><h2>Previous research</h2></div></div><div class="past-grid">
<article class="past-card" id="nanobubbles"><img src="assets/nanobubbles.JPG" alt="Schematic of ions surrounding a nanobubble" loading="lazy"><h3>Nanobubbles &amp; colloidal stability</h3><p>I studied the generation and stability of bulk nanobubbles, connecting surfactant chemistry and solution conditions to size and surface charge. Related work explored interactions with cyanobacteria and environmental applications.</p><div class="links">{link('publications.html#stability','Related publications →')}</div></article>
<article class="past-card" id="surfaces"><img src="assets/surfaces.JPG" alt="Micropatterned surfaces made from different polymers" loading="lazy"><h3>Drag-reducing surfaces</h3><p>I investigated slip over patterned polymeric surfaces, combining surface fabrication, rheological measurements, and modeling to examine the role of wettability and surface structure.</p><div class="links">{link('publications.html#slip','Physics of Fluids · 2025 →')}</div></article>
<article class="past-card" id="droplets"><video src="assets/droplet-web.mp4" autoplay loop controls muted playsinline preload="metadata" poster="assets/droplet-poster.jpg" aria-label="Oil droplet impact on layered liquids" style="display:block;width:100%;max-width:100%;height:auto;object-fit:contain;margin-bottom:22px;"></video><h3>Droplet impact on layered liquids</h3><p>I contributed to experiments and modeling of oil droplets impacting an oil layer on water, investigating how two deforming interfaces influence crater formation and jet dynamics.</p><div class="links">{link('publications.html#droplet','Journal of Fluid Mechanics · 2021 →')}</div></article></div></section>'''

publications='<div class="page-title"><h1>Publications</h1><p></p><div class="links" style="margin-top:20px">'+link(D['scholar'],'Google Scholar →')+'</div></div><h2 class="subheading">Preprints</h2>'+''.join(pub(p) for p in D['publications'] if p['badge']=='Preprint')+'<h2 class="subheading">Journal articles</h2>'+''.join(pub(p) for p in D['publications'] if p['badge']!='Preprint')+'<p class="small-note" style="margin:24px 0">* Equal contribution.</p>'

about=f'''
<div class="page-title">
  <h1>About</h1>
</div>

<div class="about-grid">
  <aside>
    <img src="assets/portrait_about.jpg" alt="Jinseok Lee" width="361" height="421">

    <div class="links" style="margin-top:22px;gap:12px 16px;">
      {link(D['scholar'],'Google Scholar')}
      {link('mailto:'+D['email'],'Email')}
      <a href="assets/Jinseok_Lee_CV.pdf" target="_blank" rel="noopener">CV</a>
    </div>
  </aside>

  <div>
    <p>I am a Ph.D. student in the Department of Mechanical Engineering and Materials Science at Yale University, advised by Prof. <a href="https://luogroup.research.yale.edu/" target="_blank" rel="noopener">Yimin Luo</a>. I also participate in Integrated Graduate Program in Physical and Engineering Biology.</p>

    <p>My research focuses on transport in crowded and deformable environments. I combine experiments and simulations to understand how particle-scale geometry and mechanics influence diffusion and fluid flow.</p>

    <p>Before Yale, I earned my B.S. and M.S. in Mechanical Engineering at Sungkyunkwan University in South Korea. My earlier research spans nanobubbles, drag-reducing surfaces, and droplet impact.</p>

    <h2>Education</h2>

    <div class="education-item">
      <strong>Yale University</strong>
      <span>Ph.D. student · Mechanical Engineering &amp; Materials Science</span>
      <span>2024–present · Advisor: Prof. <a href="https://luogroup.research.yale.edu/" target="_blank" rel="noopener">Yimin Luo</a></span>
    </div>

    <div class="education-item">
      <strong>Sungkyunkwan University</strong>
      <span>M.S. · Mechanical Engineering</span>
      <span>2022–2024 · Advisor: Prof. <a href="https://micon.skku.edu/" target="_blank" rel="noopener">Jinkee Lee</a></span>
    </div>

    <div class="education-item">
      <strong>Sungkyunkwan University</strong>
      <span>B.S. · Mechanical Engineering</span>
      <span>2016–2022 · Military service: 2019–2021</span>
    </div>

    <h2>Teaching</h2>
    <p>Teaching Fellow, Mechanical Engineering I: Strength &amp; Deformation (MENG 2311), Yale University · Fall 2026.</p>
    <p>Teaching Fellow, Mechanical Engineering III: Dynamics (MENG 3323), Yale University · Spring 2026.</p>

    <h2>Experimental &amp; computational approaches</h2>
    <p>Particle tracking and microscopy; confined-flow experiments; rheological measurements; particle image velocimetry and Schlieren visualization; particle-based simulations and statistical modeling.</p>

    <h2>Contact</h2>
    <p>
      {link('mailto:'+D['email'],D['email'],'inline-link')}<br>
      Yale University · New Haven, Connecticut
    </p>
  </div>
</div>
'''
pages={'index.html':('Home',home),'research.html':('Research',research),'publications.html':('Publications',publications),'about.html':('About',about)}
for file,(name,body) in pages.items(): (OUT/file).write_text(shell(name,body,name))
(OUT/'.nojekyll').touch()
print('Built 4 pages in',OUT)
