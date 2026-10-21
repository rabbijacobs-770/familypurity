"""Run after render.py, overview.py and rtf_chapter.py:
   1. gives the hand-built read/seven-white-days.html the same breadcrumbs, byline, quiz card and related chapters as the generated pages;
   2. writes read/index.html, the list of every chapter, review quiz and tool (the "Read" step in the breadcrumbs).
   python3 _build/finish_read.py"""
import html, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render import (ORDER, BASE, H1_TERM, H1_TITLE, crumbs_html, crumbs_ld, byline_html, quiz_html, related_html, h1_html, text_date, faq_html)
from build import SITE

READ = os.path.join(SITE, 'read')

def sub1(s, old, new):
    assert s.count(old) == 1, old[:80]
    return s.replace(old, new)

def seven_white_days():
    slug, title, full = 'seven-white-days', 'The Seven White Days', 'The Seven White Days'
    p = os.path.join(READ, slug + '.html'); s = open(p).read()
    if 'class="crumbs"' in s:
        if faq_html(slug) and 'class="faq"' not in s:          # common questions, once approved
            s = sub1(s, '  </article>\n', '  </article>' + faq_html(slug) + '\n'); open(p, 'w').write(s)
            return 'seven-white-days.html: common questions added'
        return 'seven-white-days.html already done'
    desc = re.search(r'<meta name="description" content="([^"]*)"', s).group(1)
    s = sub1(s, '<meta property="og:url"', f'<meta property="og:description" content="{desc}">\n<meta property="og:url"')
    s = sub1(s, '<link rel="preconnect" href="https://fonts.googleapis.com">', '<meta name="twitter:card" content="summary_large_image">\n<link rel="preconnect" href="https://fonts.googleapis.com">')
    s = sub1(s, '"image": "https://www.familypurity.com/images/family-p-copy_orig.jpg"}</script>',
             f'"image": "https://www.familypurity.com/images/family-p-copy_orig.jpg", "datePublished": "{text_date(slug)}", "dateModified": "{text_date(slug)}"}}</script>')
    s = re.sub(r'<script type="application/ld\+json">\{"@context": "https://schema.org", "@type": "BreadcrumbList".*?</script>',
               lambda m: '<script type="application/ld+json">' + json.dumps(crumbs_ld(slug, full), ensure_ascii=False) + '</script>', s, count=1, flags=re.S)
    s = sub1(s, '<a class="ctl hide-sm" href="../index.html#resources">All chapters</a>', '<a class="ctl hide-sm" href="index.html">All chapters</a>')
    s = sub1(s, '<header class="opener">\n  <p class="num">', f'<header class="opener">\n  {crumbs_html(full)}\n  <p class="num">')
    s = sub1(s, f'<h1>{title}</h1>', f'<h1>{h1_html(slug, title)}</h1>\n  {byline_html(slug)}')
    s = sub1(s, '''Share on WhatsApp</a>
      </div>
    </div>''', '''Share on WhatsApp</a>
      </div>
    </div>''' + quiz_html(slug))
    s = sub1(s, '</main>\n\n<nav class="chapnav"', '</main>\n\n' + related_html(slug) + '\n\n<nav class="chapnav"')
    open(p, 'w').write(s)
    return 'seven-white-days.html updated'

QUIZZES = [  # (page, chapter number, name) in the order of the Study Guide
    ('quiz-separation.html', 4, 'The laws of separation'), ('quiz-niddah.html', 2, 'Niddah'), ('quiz-stains.html', 3, 'Stains (kesamim)'),
    ('quiz-making-sure.html', 5, 'The hefsek tahara: making sure menstruation has finished'), ('quiz-seven-white-days.html', 6, 'The seven white days'),
    ('quiz-preparing-for-immersion.html', 7, 'Preparing for immersion'), ('quiz-intervening-substances.html', 8, 'Intervening substances (chatzitzah)'),
    ('quiz-what-is-a-mikveh.html', 9, 'What is a mikveh?'), ('quiz-immersion.html', 10, 'Immersion'), ('quiz-intimate-relations.html', 11, 'Intimate relations'),
    ('quiz-proper-times.html', 12, 'Proper times for marital relations'), ('quiz-wedding-night.html', 13, 'The wedding night'),
    ('quiz-anticipated-menstruation.html', 14, 'Time of the anticipated menstruation (separation dates)'), ('quiz-birth.html', 15, 'Birth')]

def meta(slug):
    s = open(os.path.join(READ, slug + '.html')).read()
    return html.unescape(re.search(r'<meta name="description" content="([^"]*)"', s).group(1))

def chapter_list():
    groups = [('Introduction', ['overview', 'from-the-rebbe']),
              ('Chapters from Family Purity: A Guide to Marital Fulfillment', [o[0] for o in ORDER if o[1].startswith('Chapter')]),
              ('Separation dates, from Times', ['times-chabad', 'times-major-customs'])]
    title = {o[0]: o[2] for o in ORDER}; num = {o[0]: o[1] for o in ORDER}
    out = []
    for head, slugs in groups:
        out.append(f'<h2>{html.escape(head)}</h2>\n    <ul class="toc">')
        for sl in slugs:
            t = H1_TITLE.get(sl, title[sl]) + (f' ({H1_TERM[sl]})' if H1_TERM.get(sl) else '')
            out.append(f'      <li><a href="{sl}.html">{html.escape(t)}</a><small>{html.escape(num[sl])}</small><p>{html.escape(meta(sl))}</p></li>')
        out.append('    </ul>')
    out.append('<h2 id="quizzes">Review quizzes</h2>\n    <p class="toc-note">From the <em>Study Guide for Choson &amp; Kallah</em>. Nothing you answer is saved.</p>\n    <ul class="toc">')
    for page, n, name in sorted(QUIZZES, key=lambda q: q[1]):
        out.append(f'      <li><a href="../{page}">{html.escape(name)} review quiz</a><small>Chapter {n}</small></li>')
    out.append('    </ul>')
    out.append('''<h2>Tools and guides</h2>
    <ul class="toc">
      <li><a href="../start-here.html">New to family purity? A simple beginner&rsquo;s guide</a></li>
      <li><a href="../calendar.html">The purity calendar: five days, hefsek tahara and seven white days</a></li>
      <li><a href="../calendar-sheet.html">Half-year Hebrew calendar sheet to print</a></li>
      <li><a href="../search.html">Search the chapters</a></li>
    </ul>''')
    return '\n    '.join(out)

def index_page():
    desc = ('Read chapters of Family Purity: A Guide to Marital Fulfillment and Times by Rabbi Fishel Jacobs free online: '
            'niddah, stains (kesamim), the hefsek tahara, the seven white days, preparing for the mikveh and separation dates, with review quizzes.')
    crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE + "/"},
        {"@type": "ListItem", "position": 2, "name": "Read", "item": BASE + "/read/"}]}
    coll = {"@context": "https://schema.org", "@type": "CollectionPage", "name": "Read Family Purity online", "description": desc, "url": BASE + "/read/",
            "inLanguage": "en", "author": {"@type": "Person", "name": "Rabbi Fishel Jacobs", "url": BASE + "/#rabbi-jacobs"},
            "hasPart": [{"@type": "Article", "name": o[2], "url": f"{BASE}/read/{o[0]}.html"} for o in ORDER]}
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Read Family Purity Chapters Free Online | Family Purity</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{BASE}/read/">
<link rel="icon" href="../favicon.svg" type="image/svg+xml">
<meta property="og:site_name" content="Family Purity">
<meta property="og:type" content="website">
<meta property="og:title" content="Read Family Purity chapters free online">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{BASE}/read/">
<meta property="og:image" content="{BASE}/images/family-p-copy_orig.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500&family=Frank+Ruhl+Libre:wght@500&display=swap">
<link rel="stylesheet" href="reader.css">
<script type="application/ld+json">{json.dumps(coll, ensure_ascii=False)}</script>
<script type="application/ld+json">{json.dumps(crumbs, ensure_ascii=False)}</script>
</head>
<body>
<header class="top">
  <div class="pill">
    <a class="brand" href="../index.html" aria-label="Family Purity, home"><img src="../images/brand/fp-wordmark.svg" alt="Family Purity" width="454" height="118"></a>
    <a class="ctl" href="../search.html" aria-label="Search the chapters"><svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="6.5"/><path d="M16 16l4.5 4.5"/></svg></a>
  </div>
</header>

<header class="opener">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="../index.html">Home</a><span aria-hidden="true">&rsaquo;</span><span aria-current="page">Read</span></nav>
  <p class="num">Free online</p>
  <span class="fleuron" aria-hidden="true">&#10087;</span>
  <h1>Read Family Purity <span class="h1-term">Chapters, review quizzes and tools</span></h1>
  <p class="byline">By <a href="../index.html#about">Rabbi Fishel Jacobs</a></p>
</header>

<main class="page">
  <div class="text toc-page">
    <p class="no-indent">Chapters from <em>Family Purity: A Guide to Marital Fulfillment</em> and from <em>Times</em> by Rabbi Fishel Jacobs, free to read online, with review quizzes from the <em>Study Guide for Choson &amp; Kallah</em>.</p>
    {chapter_list()}
  </div>
</main>

<nav class="chapnav" aria-label="More">
  <a href="../index.html">&larr; Home<small>Family Purity</small></a>
  <a href="../index.html#contact" style="text-align:right">Ask a question &rarr;<small>Rabbi Jacobs answers privately</small></a>
</nav>
<!-- Cloudflare Web Analytics --><script type='module' src='https://static.cloudflareinsights.com/beacon.min.js' data-cf-beacon='{{"token": "e8bc2fc425c042159999a4b01f919dea"}}'></script><!-- End Cloudflare Web Analytics -->
</body>
</html>
'''

if __name__ == '__main__':
    print(seven_white_days())
    open(os.path.join(READ, 'index.html'), 'w').write(index_page()); print('read/index.html written')
