"""Search-friendly additions to the hand-built quiz pages (quiz-*.html): Open Graph tags, breadcrumbs
(visible and BreadcrumbList data), a sentence naming the sections the quiz covers (from the quiz's own
section names), and related reading. Safe to run again: pages already done are skipped.
   python3 _build/quiz_seo.py"""
import html, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render import BASE, LABEL
from finish_read import QUIZZES
from build import SITE

CHAPTER = {'quiz-niddah.html': ('niddah', 'Niddah'), 'quiz-stains.html': ('stains', 'Stains'),
           'quiz-making-sure.html': ('making-sure-menstruation-has-finished', 'Making Sure Menstruation Has Finished'),
           'quiz-seven-white-days.html': ('seven-white-days', 'The Seven White Days'),
           'quiz-preparing-for-immersion.html': ('preparing-for-immersion', 'Preparing for Immersion')}
READING = {'quiz-separation.html': ['overview', 'niddah'], 'quiz-intervening-substances.html': ['preparing-for-immersion', 'overview'],
           'quiz-what-is-a-mikveh.html': ['preparing-for-immersion', 'overview'], 'quiz-immersion.html': ['preparing-for-immersion', 'seven-white-days'],
           'quiz-intimate-relations.html': ['perfect-marriage', 'overview'], 'quiz-proper-times.html': ['perfect-marriage', 'overview'],
           'quiz-wedding-night.html': ['perfect-marriage', 'overview'], 'quiz-anticipated-menstruation.html': ['times-chabad', 'times-major-customs'],
           'quiz-birth.html': ['niddah', 'overview'], 'quiz-niddah.html': ['niddah', 'source-of-niddah'], 'quiz-stains.html': ['stains', 'niddah'],
           'quiz-making-sure.html': ['making-sure-menstruation-has-finished', 'seven-white-days'],
           'quiz-seven-white-days.html': ['seven-white-days', 'making-sure-menstruation-has-finished'],
           'quiz-preparing-for-immersion.html': ['preparing-for-immersion', 'seven-white-days']}
CSS = '''
.crumbs{display:flex;flex-wrap:wrap;gap:.1rem .4rem;margin:0 0 .6rem;font-size:.95rem;color:var(--muted)}
.crumbs a{color:var(--violet);text-decoration:none}
.crumbs a:hover{text-decoration:underline}
.intro p.covers{color:var(--fg)}
.reading{border-top:1px solid var(--line);padding-top:20px}
.reading h2{margin:0 0 .5rem;font-size:1.2rem;font-weight:600;color:var(--heading);font-variant:small-caps;letter-spacing:.06em}
.reading ul{margin:0;padding-left:1.2em}
.reading li{margin:.25em 0}
.reading li::marker{color:var(--gold)}
.reading a{color:var(--violet)}
'''

def sub1(s, old, new):
    assert s.count(old) == 1, old[:80]
    return s.replace(old, new)

def patch(page, n, name):
    p = os.path.join(SITE, page); s = open(p).read()
    if 'class="crumbs"' in s: return page + ': already done'
    url = f'{BASE}/{page}'
    h1 = re.sub(r'<[^>]+>', '', re.search(r'<h1>(.*?)</h1>', s, re.S).group(1)).strip()
    desc = re.search(r'<meta name="description" content="([^"]*)"', s).group(1)
    sections = []
    for sec in re.findall(r'\{s:\s*"([^"]+)"', s):
        if sec not in sections: sections.append(sec)
    ch = CHAPTER.get(page)
    # breadcrumbs
    items = [('Home', BASE + '/', 'index.html'), ('Read', BASE + '/read/', 'read/index.html')]
    if ch: items.append((ch[1], f'{BASE}/read/{ch[0]}.html', f'read/{ch[0]}.html'))
    items.append(('Review quiz' if ch else f'{name} review quiz', url, None))
    ld = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": t, "item": u} for i, (t, u, _) in enumerate(items)]}
    crumbs = '<nav class="crumbs" aria-label="Breadcrumb">' + '<span aria-hidden="true">&rsaquo;</span>'.join(
        f'<a href="{h}">{html.escape(t)}</a>' if h else f'<span aria-current="page">{html.escape(t)}</span>' for t, _, h in items) + '</nav>'
    head = (f'<meta property="og:site_name" content="Family Purity">\n<meta property="og:type" content="website">\n'
            f'<meta property="og:title" content="{html.escape(h1)} · Family Purity">\n<meta property="og:description" content="{desc}">\n'
            f'<meta property="og:url" content="{url}">\n<meta property="og:image" content="{BASE}/images/family-p-copy_orig.jpg">\n'
            f'<meta name="twitter:card" content="summary_large_image">\n'
            f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>\n')
    s = sub1(s, '<link rel="icon" href="favicon.svg" type="image/svg+xml">', head + '<link rel="icon" href="favicon.svg" type="image/svg+xml">')
    s = sub1(s, '.brand{font-weight:600;color:var(--heading)!important}', '.brand{font-weight:600;color:var(--heading)!important}' + CSS)
    s = sub1(s, '<a href="index.html#resources">All chapters &rarr;</a>', '<a href="read/index.html">All chapters &rarr;</a>')
    s = sub1(s, '<header class="intro">\n    <p class="eyebrow">', f'<header class="intro">\n    {crumbs}\n    <p class="eyebrow">')
    if len(sections) > 1:
        covers = ', '.join(sections[:-1]) + ' and ' + sections[-1]
        sent = f'<p class="covers">The questions follow Chapter {n} of the <em>Study Guide for Choson &amp; Kallah</em>, section by section: {html.escape(covers)}.</p>'
        s = re.sub(r'(<header class="intro">.*?</p>\n    <h1>.*?</h1>\n    <p>.*?</p>)', lambda m: m.group(1) + '\n    ' + sent, s, count=1, flags=re.S)
    else:
        sent = f'<p class="covers">The questions follow Chapter {n} of the <em>Study Guide for Choson &amp; Kallah</em>.</p>'
        s = re.sub(r'(<header class="intro">.*?</p>\n    <h1>.*?</h1>\n    <p>.*?</p>)', lambda m: m.group(1) + '\n    ' + sent, s, count=1, flags=re.S)
    assert 'class="covers"' in s, page
    links = [f'<li><a href="read/{r}.html">{html.escape(LABEL[r])}</a>{" (this chapter, free online)" if ch and r == ch[0] else ""}</li>' for r in READING[page]]
    if not ch: links.append(f'<li>Chapter {n} is in the book: <a href="index.html#books"><em>Family Purity: A Guide to Marital Fulfillment</em></a></li>')
    links.append('<li><a href="read/index.html#quizzes">All review quizzes</a></li>')
    reading = '<section class="reading" aria-label="Related reading">\n    <h2>Related reading</h2>\n    <ul>\n      ' + '\n      '.join(links) + '\n    </ul>\n  </section>\n'
    s = sub1(s, '</main>', '  ' + reading + '</main>')
    open(p, 'w').write(s)
    return f'{page}: {len(sections)} sections'

if __name__ == '__main__':
    for page, n, name in QUIZZES: print(patch(page, n, name))
