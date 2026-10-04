import json, html, re, os, sys, urllib.parse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build import blocks_for, render_body, join_lines, SITE
from pages import PAGES

# Reading order of everything available online (slug, label, title)
ORDER=[('overview','Introduction','Overview'),('from-the-rebbe','Introduction','From the Rebbe'),
 ('perfect-marriage','Chapter 1','Perfect Marriage'),('niddah','Chapter 2','Niddah'),('source-of-niddah','Chapter 2','Source of Niddah'),
 ('gynecological-considerations','Chapter 2','Gynecological Considerations'),('stains','Chapter 3','Stains'),
 ('making-sure-menstruation-has-finished','Chapter 5','Making Sure Menstruation Has Finished'),('seven-white-days','Chapter 6','The Seven White Days'),
 ('times-chabad','Times','Separation Dates · Chabad Custom'),('times-major-customs','Times','Separation Dates · Major Customs')]
BASE='https://www.familypurity.com'
AMAZON_FP='https://www.amazon.com/dp/B0DGGB859Z'; AMAZON_TIMES='https://www.amazon.com/dp/B0DC713M2P'

def nav(slug):
    i=[o[0] for o in ORDER].index(slug)
    prev=ORDER[i-1] if i>0 else None; nxt=ORDER[i+1] if i+1<len(ORDER) else None
    a=f'<a href="{prev[0]}.html">&larr; {prev[1]}<small>{prev[2]}</small></a>' if prev else '<a href="../index.html#resources">&larr; All chapters<small>Free resources</small></a>'
    b=f'<a href="{nxt[0]}.html" style="text-align:right">{nxt[1]} &rarr;<small>{nxt[2]}</small></a>' if nxt else '<a href="../index.html#resources" style="text-align:right">All chapters &rarr;<small>Free resources</small></a>'
    return a+'\n  '+b

def page(slug,num,title,sub,desc,pdf,epi,body_html,is_times=False,seo=None):
    full=f'{title} · {sub}' if sub else title
    head_title=(seo or full)+' | Family Purity'
    book='Times' if is_times else 'Family Purity: A Guide to Marital Fulfillment'
    amazon=AMAZON_TIMES if is_times else AMAZON_FP
    ld={"@context":"https://schema.org","@type":"Article","headline":full,"description":desc,
        "author":{"@type":"Person","name":"Rabbi Fishel Jacobs","url":BASE+"/#rabbi-jacobs"},
        "publisher":{"@type":"Organization","name":"Family Purity","url":BASE+"/"},
        "isPartOf":{"@type":"Book","name":book,"author":{"@type":"Person","name":"Rabbi Fishel Jacobs"}},
        "inLanguage":"en","mainEntityOfPage":f"{BASE}/read/{slug}.html","image":BASE+"/images/family-p-copy_orig.jpg"}
    crumbs={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"Family Purity","item":BASE+"/"},
        {"@type":"ListItem","position":2,"name":"Free resources","item":BASE+"/#resources"},
        {"@type":"ListItem","position":3,"name":full,"item":f"{BASE}/read/{slug}.html"}]}
    epi_html=''
    if epi:
        epi_html=f'''
  <blockquote class="epigraph" style="margin-inline:auto">
    {epi[0]}
    <cite>{epi[1]}</cite>
  </blockquote>'''
    ask_text=f'Shalom Rabbi Jacobs, I have a question about {full}: '
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{html.escape(head_title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{BASE}/read/{slug}.html">
<link rel="icon" href="../favicon.svg" type="image/svg+xml">
<meta property="og:site_name" content="Family Purity">
<meta property="og:type" content="article">
<meta property="og:title" content="{html.escape(full)} · Family Purity">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{BASE}/read/{slug}.html">
<meta property="og:image" content="{BASE}/images/family-p-copy_orig.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500&family=Frank+Ruhl+Libre:wght@500&display=swap">
<link rel="stylesheet" href="reader.css">
<script type="application/ld+json">{json.dumps(ld,ensure_ascii=False)}</script>
<script type="application/ld+json">{json.dumps(crumbs,ensure_ascii=False)}</script>
</head>
<body>
<div class="progress" aria-hidden="true"></div>

<header class="top">
  <div class="pill">
    <a class="brand" href="../index.html" aria-label="Family Purity, home"><img src="../images/brand/fp-wordmark.svg" alt="Family Purity" width="454" height="118"></a>
    <a class="ctl hide-sm" href="../index.html#resources">All chapters</a>
    <div class="size" role="group" aria-label="Text size">
      <button type="button" data-size="down" aria-label="Smaller text">A</button>
      <button type="button" data-size="up" aria-label="Larger text">A</button>
    </div>
    <a class="ctl pdf" href="../files/{pdf}" target="_blank" rel="noopener">PDF</a>
  </div>
</header>

<header class="opener">
  <p class="num">{html.escape(num)}</p>
  <span class="fleuron" aria-hidden="true">&#10087;</span>
  <h1>{html.escape(title)}</h1>{f'{chr(10)}  <p class="opener-sub">{html.escape(sub)}</p>' if sub else ''}{epi_html}
</header>

<main class="page">
  <article class="text">
    {body_html}
  </article>

  <aside class="end">
    <span class="fleuron" aria-hidden="true">&#10087;</span>
    <div class="end-card">
      <h2>{'The full guide, with calendars, is in the book' if is_times else 'The chapter continues in the book'}</h2>
      <p>{'From <em>Times</em> by Rabbi Fishel Jacobs.' if is_times else 'This is an excerpt from <em>Family Purity: A Guide to Marital Fulfillment</em>.'}</p>
      <div class="btn-row">
        <a class="btn btn-solid" href="{amazon}" target="_blank" rel="noopener">Get the book</a>
        <a class="btn btn-line" href="../files/{pdf}" target="_blank" rel="noopener">Download PDF</a>
      </div>
    </div>
    <a class="ask" href="https://wa.me/972587921788?text={re.sub(' ','%20',html.escape(ask_text))}" target="_blank" rel="noopener">
      <img src="../images/rabbi-portrait.jpg" alt="" width="726" height="800" loading="lazy">
      <span><b>A question about this?</b><small>Ask Rabbi Jacobs privately on WhatsApp.</small></span>
    </a>
    <p class="correction">Spotted a typo or something unclear? <a href="mailto:RabbiJacobs@FamilyPurity.com?subject={urllib.parse.quote('Correction: '+full)}">Send a correction</a></p>
  </aside>
</main>

<nav class="chapnav" aria-label="Chapters">
  {nav(slug)}
</nav>

<script src="reader.js"></script>
</body>
</html>
'''

if __name__=='__main__':
    out_dir=os.path.join(SITE,'read')
    for name,cfg in PAGES.items():
        blocks,fns,body,fnsize=blocks_for(name,cfg)
        epi=None
        if cfg.get('epigraph'): epi=(html.escape(cfg['epigraph'][0]),html.escape(cfg['epigraph'][1]))
        # leading quote(s) before any text become the epigraph
        lead=[]
        while blocks and blocks[0]['type'] in ('quote','orn'):
            b=blocks.pop(0)
            if b['type']=='quote': lead.append(b)
        if lead and not epi:
            q=lead[0]; epi=(join_lines(q['lines'],body,cfg.get('add_italics',False)),html.escape(q['cite']))
            for extra in lead[1:]: blocks.insert(0,extra)
        elif lead:
            for extra in reversed(lead): blocks.insert(0,extra)
        body_html=render_body(blocks,fns,body,cfg)
        for a,z in cfg.get('fix_html',{}).items(): body_html=re.sub(a,z,body_html,flags=re.S)
        h=page(cfg['slug'],cfg['num'],cfg['title'],cfg.get('sub'),cfg['desc'],cfg['pdf'],epi,body_html,is_times=name.startswith('times'),seo=cfg.get('seo'))
        open(os.path.join(out_dir,cfg['slug']+'.html'),'w').write(h)
        left=re.findall(r'\x00|\x01|\x02|\x03',body_html)
        placed=body_html.count('class="fn"')
        print(f"{cfg['slug']:34} {len(body_html):6} chars  footnotes={len(fns):3} placed={placed:3} stray={len(left)}")
