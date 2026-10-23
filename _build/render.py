import json, html, re, os, sys, urllib.parse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build import blocks_for, render_body, join_lines, SITE
from pages import PAGES
from faq import FAQ

# Reading order of everything available online (slug, label, title)
ORDER=[('overview','Introduction','Overview'),('from-the-rebbe','Introduction','From the Rebbe'),
 ('perfect-marriage','Chapter 1','Perfect Marriage'),('niddah','Chapter 2','Niddah'),('source-of-niddah','Chapter 2','Source of Niddah'),
 ('gynecological-considerations','Chapter 2','Gynecological Considerations'),('stains','Chapter 3','Stains'),
 ('absence-makes-the-heart-grow-fonder','Chapter 4','Absence Makes the Heart Grow Fonder'),
 ('making-sure-menstruation-has-finished','Chapter 5','Making Sure Menstruation Has Finished'),('seven-white-days','Chapter 6','The Seven White Days'),
 ('preparing-for-immersion','Chapter 7','Preparing for Immersion'),
 ('intervening-substances','Chapter 8','Intervening Substances'),('what-is-a-mikveh','Chapter 9','What Is a Mikveh?'),('immersion','Chapter 10','Immersion'),('intimate-relations','Chapter 11','Intimate Relations'),
 ('proper-times-for-marital-relations','Chapter 12','Proper Times for Marital Relations'),('wedding-night','Chapter 13','The Wedding Night'),
 ('anticipated-menstruation','Chapter 14','Time of the Anticipated Menstruation'),('birth','Chapter 15','Birth'),
 ('times-chabad','Times','Separation Dates · Chabad Custom'),('times-major-customs','Times','Separation Dates · Major Customs')]
BASE='https://www.familypurity.com'
AMAZON_FP='https://www.amazon.com/dp/B0DGGB859Z'
NOTIFY='https://wa.me/972587921788?text=Shalom%20Rabbi%20Jacobs%2C%20please%20let%20me%20know%20when%20the%20expanded%20edition%20of%20Family%20Purity%20is%20published.'; AMAZON_TIMES='https://www.amazon.com/dp/B0DC713M2P'

# Search-friendly additions shared by every chapter page (also applied to the hand-built
# seven-white-days.html by finish_read.py).
# The book's own term after the chapter title in the H1, where the title alone lacks it.
H1_TERM={'overview':None,'stains':'Kesamim','making-sure-menstruation-has-finished':'Hefsek Tahara','seven-white-days':'Shiva Nekiim',
 'preparing-for-immersion':'Hafifah','absence-makes-the-heart-grow-fonder':'Harchakos','anticipated-menstruation':'Vestos','intervening-substances':'Chatzitzah','immersion':'Tevilah','times-chabad':'Vestos','times-major-customs':'Vestos'}
H1_TITLE={'overview':'Overview: The Purity Cycle'}
# Descriptive link text for each chapter (used for related-chapter links and the chapter list).
LABEL={'overview':'The family purity cycle, step by step','from-the-rebbe':'The Rebbe on family purity: letters and talks',
 'perfect-marriage':'Perfect marriage: a Torah view of marriage','niddah':'Niddah: the laws of menstruation',
 'source-of-niddah':'Source of niddah: uterine bleeding','gynecological-considerations':'Gynecological procedures and niddah',
 'stains':'The laws of stains (kesamim)','making-sure-menstruation-has-finished':'The hefsek tahara: making sure menstruation has finished',
 'seven-white-days':'The seven white days (shiva nekiim)','preparing-for-immersion':'Preparing for immersion in the mikveh (hafifah)',
 'absence-makes-the-heart-grow-fonder':'The laws of separation (harchakos)','intervening-substances':'Intervening substances (chatzitzah)','immersion':'Immersion in the mikveh (tevilah)','what-is-a-mikveh':'What is a mikveh?',
 'intimate-relations':'Intimate relations in holiness','proper-times-for-marital-relations':'Proper times for marital relations',
 'wedding-night':'The wedding night','anticipated-menstruation':'Time of the anticipated menstruation (vestos)','birth':'Birth and family purity',
 'times-chabad':'Separation dates (vestos): Chabad custom','times-major-customs':'Separation dates (vestos) for all communities'}
CALENDAR=('../calendar.html','The purity calendar: five days, hefsek tahara and seven white days')
RELATED={'overview':['niddah','making-sure-menstruation-has-finished','seven-white-days',CALENDAR],
 'from-the-rebbe':['perfect-marriage','overview','niddah'],
 'perfect-marriage':['from-the-rebbe','overview','niddah'],
 'niddah':['source-of-niddah','stains','making-sure-menstruation-has-finished'],
 'source-of-niddah':['niddah','gynecological-considerations','stains'],
 'gynecological-considerations':['source-of-niddah','niddah','stains'],
 'stains':['niddah','source-of-niddah','making-sure-menstruation-has-finished'],
 'making-sure-menstruation-has-finished':['seven-white-days','niddah','stains',CALENDAR],
 'seven-white-days':['making-sure-menstruation-has-finished','preparing-for-immersion','stains',CALENDAR],
 'preparing-for-immersion':['seven-white-days','making-sure-menstruation-has-finished','overview'],
 'absence-makes-the-heart-grow-fonder':['niddah','making-sure-menstruation-has-finished','overview'],
 'what-is-a-mikveh':['immersion','preparing-for-immersion','overview'],
 'intervening-substances':['preparing-for-immersion','immersion','what-is-a-mikveh'],
 'immersion':['preparing-for-immersion','intervening-substances','what-is-a-mikveh'],
 'intimate-relations':['proper-times-for-marital-relations','wedding-night','absence-makes-the-heart-grow-fonder'],
 'proper-times-for-marital-relations':['intimate-relations','wedding-night','overview'],
 'wedding-night':['intimate-relations','absence-makes-the-heart-grow-fonder','making-sure-menstruation-has-finished'],
 'anticipated-menstruation':['times-chabad','times-major-customs','niddah'],
 'birth':['niddah','absence-makes-the-heart-grow-fonder','seven-white-days'],
 'times-chabad':['times-major-customs','niddah','overview'],
 'times-major-customs':['times-chabad','niddah','overview']}
# Study Guide review quiz for each chapter: (page, questions, what it covers, button name)
QUIZ={'niddah':('quiz-niddah.html',21,'Chapter 2, Niddah','Niddah'),'source-of-niddah':('quiz-niddah.html',21,'Chapter 2, Niddah','Niddah'),
 'gynecological-considerations':('quiz-niddah.html',21,'Chapter 2, Niddah','Niddah'),'stains':('quiz-stains.html',10,'Chapter 3, Stains','Stains'),
 'making-sure-menstruation-has-finished':('quiz-making-sure.html',10,'Chapter 5, Making Sure Menstruation Has Finished','Hefsek Tahara'),
 'seven-white-days':('quiz-seven-white-days.html',10,'Chapter 6, Seven White Days','Seven White Days'),
 'preparing-for-immersion':('quiz-preparing-for-immersion.html',10,'Chapter 7, Preparing for Immersion','Preparing for Immersion'),
 'absence-makes-the-heart-grow-fonder':('quiz-separation.html',10,'Chapter 4, Absence Makes the Heart Grow Fonder','Separation'),
 'intervening-substances':('quiz-intervening-substances.html',10,'Chapter 8, Intervening Substances','Intervening Substances'),
 'immersion':('quiz-immersion.html',10,'Chapter 10, Immersion','Immersion'),
 'what-is-a-mikveh':('quiz-what-is-a-mikveh.html',10,'Chapter 9, What Is a Mikveh?','Mikveh'),
 'intimate-relations':('quiz-intimate-relations.html',10,'Chapter 11, Intimate Relations','Intimate Relations'),
 'proper-times-for-marital-relations':('quiz-proper-times.html',10,'Chapter 12, Proper Times for Marital Relations','Proper Times'),
 'wedding-night':('quiz-wedding-night.html',10,'Chapter 13, The Wedding Night','Wedding Night'),
 'anticipated-menstruation':('quiz-anticipated-menstruation.html',10,'Chapter 14, Time of the Anticipated Menstruation','Anticipated Menstruation'),
 'birth':('quiz-birth.html',10,'Chapter 15, Birth','Birth'),
 'times-chabad':('quiz-anticipated-menstruation.html',10,'separation dates (Chapter 14, Time of the Anticipated Menstruation)','Separation Dates'),
 'times-major-customs':('quiz-anticipated-menstruation.html',10,'separation dates (Chapter 14, Time of the Anticipated Menstruation)','Separation Dates')}
# When each chapter's text was last changed (shown as "Last updated").
TEXT_DATE={'preparing-for-immersion':'2026-10-05',**{s:'2026-10-23' for s in ('absence-makes-the-heart-grow-fonder','intervening-substances','immersion','what-is-a-mikveh','intimate-relations','proper-times-for-marital-relations','wedding-night','anticipated-menstruation','birth')}}
def text_date(slug): return TEXT_DATE.get(slug,'2026-10-04')
def long_date(d):
    y,m,dd=d.split('-'); return f"{['January','February','March','April','May','June','July','August','September','October','November','December'][int(m)-1]} {int(dd)}, {y}"

def h1_html(slug,title):
    t=html.escape(H1_TITLE.get(slug,title)); term=H1_TERM.get(slug)
    return t+(f' <span class="h1-term">({term})</span>' if term else '')
def crumbs_html(full):
    return (f'<nav class="crumbs" aria-label="Breadcrumb"><a href="../index.html">Home</a><span aria-hidden="true">&rsaquo;</span>'
            f'<a href="index.html">Read</a><span aria-hidden="true">&rsaquo;</span><span aria-current="page">{html.escape(full)}</span></nav>')
def crumbs_ld(slug,full):
    return {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"Home","item":BASE+"/"},
        {"@type":"ListItem","position":2,"name":"Read","item":BASE+"/read/"},
        {"@type":"ListItem","position":3,"name":full,"item":f"{BASE}/read/{slug}.html"}]}
def byline_html(slug):
    d=text_date(slug)
    return f'<p class="byline">By <a href="../index.html#about">Rabbi Fishel Jacobs</a> &middot; Last updated <time datetime="{d}">{long_date(d)}</time></p>'
def quiz_html(slug):
    q=QUIZ.get(slug)
    if not q: return ''
    return (f'\n    <div class="end-card quiz-card">\n      <h2>Test yourself</h2>\n      <p>{q[1]} review questions on {q[2]}, from the <em>Study Guide for Choson &amp; Kallah</em>. Nothing you answer is saved.</p>'
            f'\n      <div class="btn-row"><a class="btn btn-solid" href="../{q[0]}">Take the {q[3]} quiz</a></div>\n    </div>')
def related_html(slug):
    num={o[0]:o[1] for o in ORDER}; items=[]
    for r in RELATED.get(slug,[]):
        if isinstance(r,tuple): items.append(f'<li><a href="{r[0]}">{r[1]}</a><small>Interactive calendar</small></li>')
        else: items.append(f'<li><a href="{r}.html">{LABEL[r]}</a><small>{num[r]}</small></li>')
    return ('<nav class="related" aria-label="Related chapters">\n  <h2>Related chapters</h2>\n  <ul>\n    '+'\n    '.join(items)+
            '\n  </ul>\n  <p><a href="index.html">All chapters and review quizzes</a></p>\n</nav>') if items else ''

def faq_html(slug):
    """Common questions for a chapter, only once Rabbi Jacobs has approved them (faq.py); '' until then."""
    e=FAQ.get(slug)
    if not e or not e['approved']: return ''
    def ans(a): return ''.join('<ul>'+''.join(f'<li>{html.escape(x)}</li>' for x in p)+'</ul>' if isinstance(p,list) else f'<p>{html.escape(p)}</p>' for p in a)
    ld={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":ans(a)}} for q,a in e['items']]}
    qs=''.join(f'\n    <div class="qa"><h3>{html.escape(q)}</h3>{ans(a)}</div>' for q,a in e['items'])
    return (f'\n  <section class="faq" aria-labelledby="faq-h">\n    <h2 id="faq-h">Common questions</h2>{qs}\n  </section>'
            f'\n  <script type="application/ld+json">{json.dumps(ld,ensure_ascii=False)}</script>')

def nav(slug):
    i=[o[0] for o in ORDER].index(slug)
    prev=ORDER[i-1] if i>0 else None; nxt=ORDER[i+1] if i+1<len(ORDER) else None
    a=f'<a href="{prev[0]}.html">&larr; {prev[1]}<small>{prev[2]}</small></a>' if prev else '<a href="../index.html#resources">&larr; All chapters<small>Free resources</small></a>'
    b=f'<a href="{nxt[0]}.html" style="text-align:right">{nxt[1]} &rarr;<small>{nxt[2]}</small></a>' if nxt else '<a href="../index.html#resources" style="text-align:right">All chapters &rarr;<small>Free resources</small></a>'
    return a+'\n  '+b

def page(slug,num,title,sub,desc,pdf,epi,body_html,is_times=False,seo=None,expanded=False):
    full=f'{title} · {sub}' if sub else title
    head_title=(seo or full)+' | Family Purity'
    book='Times' if is_times else 'Family Purity: A Guide to Marital Fulfillment'
    amazon=AMAZON_TIMES if is_times else AMAZON_FP
    ld={"@context":"https://schema.org","@type":"Article","headline":full,"description":desc,
        "author":{"@type":"Person","name":"Rabbi Fishel Jacobs","url":BASE+"/#rabbi-jacobs"},
        "publisher":{"@type":"Organization","name":"Family Purity","url":BASE+"/"},
        "isPartOf":{"@type":"Book","name":book,"author":{"@type":"Person","name":"Rabbi Fishel Jacobs"},**({"bookEdition":"First expanded edition (forthcoming)"} if expanded else {})},
        "inLanguage":"en","mainEntityOfPage":f"{BASE}/read/{slug}.html","image":BASE+"/images/family-p-copy_orig.jpg",
        "datePublished":text_date(slug),"dateModified":text_date(slug)}
    crumbs=crumbs_ld(slug,full)
    epi_html=''
    if epi:
        epi_html=f'''
  <blockquote class="epigraph" style="margin-inline:auto">
    {epi[0]}
    <cite>{epi[1]}</cite>
  </blockquote>'''
    ask_text=f'Shalom Rabbi Jacobs, I have a question about {full}: '
    if expanded:
        end_h='A preview from the expanded edition'
        end_p='This chapter is from the forthcoming first expanded edition of <em>Family Purity: A Guide to Marital Fulfillment</em>. The current edition is available now.'
    else:
        end_h='The full guide, with calendars, is in the book' if is_times else 'The chapter continues in the book'
        end_p='From <em>Times</em> by Rabbi Fishel Jacobs.' if is_times else 'This is an excerpt from <em>Family Purity: A Guide to Marital Fulfillment</em>.'
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
<meta name="twitter:card" content="summary_large_image">
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
    <a class="ctl hide-sm" href="index.html">All chapters</a>
    <a class="ctl" href="../search.html" aria-label="Search the chapters"><svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="6.5"/><path d="M16 16l4.5 4.5"/></svg></a>
    <div class="size" role="group" aria-label="Text size">
      <button type="button" data-size="down" aria-label="Smaller text">A</button>
      <button type="button" data-size="up" aria-label="Larger text">A</button>
    </div>
    {f'<a class="ctl pdf" href="../files/{pdf}" target="_blank" rel="noopener">PDF</a>' if pdf else ''}
  </div>
</header>

<header class="opener">
  {crumbs_html(full)}
  <p class="num">{html.escape(num)}</p>
  <span class="fleuron" aria-hidden="true">&#10087;</span>
  <h1>{h1_html(slug,title)}</h1>{chr(10)+'  <p class="opener-sub">From the forthcoming expanded edition</p>' if expanded else ''}{f'{chr(10)}  <p class="opener-sub">{html.escape(sub)}</p>' if sub else ''}
  {byline_html(slug)}{epi_html}
</header>

<main class="page">
  <article class="text">
    {body_html}
  </article>{faq_html(slug)}

  <aside class="end">
    <span class="fleuron" aria-hidden="true">&#10087;</span>
    <div class="end-card">
      <h2>{end_h}</h2>
      <p>{end_p}</p>
      <div class="btn-row">
        <a class="btn btn-solid" href="{amazon}" target="_blank" rel="noopener">{'Get the current edition' if expanded else 'Get the book'}</a>
        {f'<a class="btn btn-line" href="../files/{pdf}" target="_blank" rel="noopener">Download PDF</a>' if pdf else (f'<a class="btn btn-line" href="{NOTIFY}" target="_blank" rel="noopener">Notify me when it&rsquo;s published</a>' if expanded else '')}
        <a class="btn btn-line" href="https://wa.me/?text={urllib.parse.quote(full+' · Family Purity by Rabbi Fishel Jacobs '+BASE+'/read/'+slug+'.html')}" target="_blank" rel="noopener">Share on WhatsApp</a>
      </div>
    </div>{quiz_html(slug)}
    <a class="ask" href="https://wa.me/972587921788?text={re.sub(' ','%20',html.escape(ask_text))}" target="_blank" rel="noopener">
      <img src="../images/rabbi-portrait.jpg" alt="" width="726" height="800" loading="lazy">
      <span><b>A question about this?</b><small>Ask Rabbi Jacobs privately on WhatsApp.</small></span>
    </a>
    <p class="correction">Spotted a typo or something unclear? <a href="#" data-em="RabbiJacobs|FamilyPurity.com" data-subject="Correction: {html.escape(full)}">Send a correction</a></p>
  </aside>
</main>

{related_html(slug)}

<nav class="chapnav" aria-label="Chapters">
  {nav(slug)}
</nav>

<script src="reader.js"></script>
<!-- Cloudflare Web Analytics --><script type='module' src='https://static.cloudflareinsights.com/beacon.min.js' data-cf-beacon='{{"token": "e8bc2fc425c042159999a4b01f919dea"}}'></script><!-- End Cloudflare Web Analytics -->
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
        h=page(cfg['slug'],cfg['num'],cfg['title'],cfg.get('sub'),cfg['desc'],cfg['pdf'],epi,body_html,is_times=name.startswith('times'),seo=cfg.get('seo'),expanded=cfg.get('expanded',False))
        open(os.path.join(out_dir,cfg['slug']+'.html'),'w').write(h)
        left=re.findall(r'\x00|\x01|\x02|\x03',body_html)
        placed=body_html.count('class="fn"')
        print(f"{cfg['slug']:34} {len(body_html):6} chars  footnotes={len(fns):3} placed={placed:3} stray={len(left)}")
