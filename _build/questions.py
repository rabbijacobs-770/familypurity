"""Questions and answers: one short page per real question, answered by Rabbi Jacobs.
   python3 _build/questions.py   (then python3 _build/sitemap.py)

To add one: copy the example entry in QUESTIONS, give it its own slug (the page address, e.g.
'can-i-use-a-shower-instead-of-a-bath'), write the question as people ask it, and put Rabbi
Jacobs's answer in 'answer' (paragraphs; a paragraph that is a list becomes a bulleted list).
Entries with answer=None are placeholders and are not published.

Until at least one answer is published, questions/index.html is marked noindex and is not in
the sitemap or menus. When the first answer goes up: add "Questions" to the site menus.
<!-- REVIEW: Rabbi Jacobs --> every answer is his to write; nothing here is drafted for him."""
import html, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render import BASE, LABEL
from build import SITE

QUESTIONS = [
    dict(slug='example-question',
         question='[The question, as people ask it]',
         answer=None,                      # [Rabbi Jacobs's answer: a list of paragraphs]
         chapter='overview',               # the chapter that explains this further (a slug from LABEL in render.py)
         date='2026-10-21'),               # date answered
]

OUT = os.path.join(SITE, 'questions')
BEACON = '''<!-- Cloudflare Web Analytics --><script type='module' src='https://static.cloudflareinsights.com/beacon.min.js' data-cf-beacon='{"token": "e8bc2fc425c042159999a4b01f919dea"}'></script><!-- End Cloudflare Web Analytics -->'''

def published(): return [q for q in QUESTIONS if q['answer']]

def long_date(d):
    y, m, dd = d.split('-')
    return f"{['January','February','March','April','May','June','July','August','September','October','November','December'][int(m)-1]} {int(dd)}, {y}"

def head(title, desc, url, ld, robots=''):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{html.escape(title)} | Family Purity</title>
<meta name="description" content="{html.escape(desc)}">
{robots}<link rel="canonical" href="{url}">
<link rel="icon" href="../favicon.svg" type="image/svg+xml">
<meta property="og:site_name" content="Family Purity">
<meta property="og:type" content="article">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}/images/family-p-copy_orig.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500&family=Frank+Ruhl+Libre:wght@500&display=swap">
<link rel="stylesheet" href="../read/reader.css">
{''.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>{chr(10)}' for x in ld)}</head>
<body>
<header class="top">
  <div class="pill">
    <a class="brand" href="../index.html" aria-label="Family Purity, home"><img src="../images/brand/fp-wordmark.svg" alt="Family Purity" width="454" height="118"></a>
    <a class="ctl hide-sm" href="../read/index.html">All chapters</a>
    <a class="ctl" href="../search.html" aria-label="Search the chapters"><svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="6.5"/><path d="M16 16l4.5 4.5"/></svg></a>
  </div>
</header>
'''

def crumbs(items):
    ld = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": t, "item": u} for i, (t, u, _) in enumerate(items)]}
    vis = '<nav class="crumbs" aria-label="Breadcrumb">' + '<span aria-hidden="true">&rsaquo;</span>'.join(
        f'<a href="{h}">{html.escape(t)}</a>' if h else f'<span aria-current="page">{html.escape(t)}</span>' for t, _, h in items) + '</nav>'
    return ld, vis

def answer_html(ans):
    return '\n    '.join('<ul>' + ''.join(f'<li>{html.escape(x)}</li>' for x in p) + '</ul>' if isinstance(p, list) else f'<p>{html.escape(p)}</p>' for p in ans)

def question_page(q):
    url = f"{BASE}/questions/{q['slug']}.html"
    first = q['answer'][0] if isinstance(q['answer'][0], str) else q['question']
    desc = (first[:150] + '…') if len(first) > 150 else first
    cl, cv = crumbs([('Home', BASE + '/', '../index.html'), ('Questions', BASE + '/questions/', 'index.html'), (q['question'], url, None)])
    art = {"@context": "https://schema.org", "@type": "Article", "headline": q['question'], "description": desc, "url": url, "mainEntityOfPage": url,
           "datePublished": q['date'], "dateModified": q['date'], "inLanguage": "en", "image": BASE + "/images/family-p-copy_orig.jpg",
           "author": {"@type": "Person", "name": "Rabbi Fishel Jacobs", "url": BASE + "/#rabbi-jacobs"},
           "publisher": {"@type": "Organization", "name": "Family Purity", "url": BASE + "/"}}
    ch = q.get('chapter')
    return head(q['question'], desc, url, [art, cl]) + f'''
<header class="opener">
  {cv}
  <p class="num">Question</p>
  <span class="fleuron" aria-hidden="true">&#10087;</span>
  <h1>{html.escape(q['question'])}</h1>
  <p class="byline">Answered by <a href="../index.html#about">Rabbi Fishel Jacobs</a> &middot; <time datetime="{q['date']}">{long_date(q['date'])}</time></p>
</header>

<main class="page">
  <article class="text">
    <!-- REVIEW: Rabbi Jacobs -->
    {answer_html(q['answer'])}
  </article>
  <aside class="end">
    <span class="fleuron" aria-hidden="true">&#10087;</span>
    <div class="end-card">
      <h2>Read more</h2>
      <p>{f'<a href="../read/{ch}.html">{html.escape(LABEL[ch])}</a>, free online.' if ch else ''} For a practical question, please ask an orthodox rabbi expert in these laws.</p>
      <div class="btn-row"><a class="btn btn-solid" href="../index.html#contact">Ask Rabbi Jacobs a question</a><a class="btn btn-line" href="index.html">More questions</a></div>
    </div>
  </aside>
</main>
{BEACON}
</body>
</html>
'''

def index_page():
    pub = published()
    url = BASE + '/questions/'
    desc = 'Short answers by Rabbi Fishel Jacobs to real questions about Jewish family purity: niddah, stains, the hefsek tahara, the seven white days and the mikveh.'
    cl, cv = crumbs([('Home', BASE + '/', '../index.html'), ('Questions', url, None)])
    robots = '' if pub else '<meta name="robots" content="noindex">\n'
    items = ('\n    '.join(f'<li><a href="{q["slug"]}.html">{html.escape(q["question"])}</a><small>{long_date(q["date"])}</small></li>' for q in sorted(pub, key=lambda q: q['date'], reverse=True))
             if pub else '<li>The first answers will appear here soon.</li>')
    return head('Questions and Answers on Family Purity', desc, url, [cl], robots) + f'''
<header class="opener">
  {cv}
  <p class="num">Questions</p>
  <span class="fleuron" aria-hidden="true">&#10087;</span>
  <h1>Questions and answers</h1>
  <p class="byline">Answered by <a href="../index.html#about">Rabbi Fishel Jacobs</a></p>
</header>

<main class="page">
  <div class="text toc-page">
    <p class="no-indent">Short answers to real questions about family purity. Each one links to the chapter that explains it more fully.</p>
    <ul class="toc">
    {items}
    </ul>
    <p class="no-indent">Have a question? <a href="../index.html#contact">Ask Rabbi Jacobs privately</a>.</p>
  </div>
</main>
{BEACON}
</body>
</html>
'''

if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for q in published():
        assert q['chapter'] is None or q['chapter'] in LABEL, q['slug']
        open(os.path.join(OUT, q['slug'] + '.html'), 'w').write(question_page(q))
    open(os.path.join(OUT, 'index.html'), 'w').write(index_page())
    print(f"{len(published())} answered question(s) published; {len(QUESTIONS) - len(published())} placeholder(s) waiting")
