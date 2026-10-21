"""Check that every draft answer in faq.py is quoted word for word from its chapter's text on the site,
and write review/faq-drafts.html for Rabbi Jacobs to read (review/ is not published).
   python3 _build/faq_check.py"""
import html, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from faq import FAQ
from render import ORDER
from build import SITE

def plain(slug):
    s = open(os.path.join(SITE, 'read', slug + '.html')).read()
    a = re.search(r'<article class="text">(.*?)</article>', s, re.S).group(1)
    a = re.sub(r'<small class="sn">.*?</small>', '', a, flags=re.S)
    a = re.sub(r'<label class="fn".*?</label><input[^>]*>', '', a, flags=re.S)
    a = re.sub(r'</?(em|i|b|strong|span|a|button|sup|sub)\b[^>]*>', '', a)   # inline tags: no space
    a = re.sub(r'<li>', ' ', a); a = re.sub(r'<[^>]+>', ' ', a)
    return norm(html.unescape(a))

def norm(t): return re.sub(r'\s+', ' ', t.replace(' ', ' ')).strip()

def quotes(ans):
    for part in ans:
        yield from (part if isinstance(part, list) else [part])

def check():
    bad = 0
    for slug, entry in FAQ.items():
        text = re.sub(r'\s+([.,;:])', r'\1', plain(slug))
        for q, ans in entry['items']:
            for piece in quotes(ans):
                if norm(piece) not in text:
                    bad += 1; print(f'NOT FOUND in {slug}: {q}\n   {piece[:120]}')
    n = sum(len(e['items']) for e in FAQ.values())
    print(f'{n} questions on {len(FAQ)} pages; {bad} answer passages not found word for word')
    return bad

def answer_html(ans):
    out = []
    for part in ans:
        if isinstance(part, list): out.append('<ul>' + ''.join(f'<li>{html.escape(x)}</li>' for x in part) + '</ul>')
        else: out.append(f'<p>{html.escape(part)}</p>')
    return ''.join(out)

def review_page():
    title = {o[0]: f'{o[1]}: {o[2]}' for o in ORDER}
    secs = []
    for slug, entry in FAQ.items():
        qs = ''.join(f'<div class="qa"><h3>{i}. {html.escape(q)}</h3>{answer_html(a)}</div>' for i, (q, a) in enumerate(entry['items'], 1))
        secs.append(f'<section><h2>{html.escape(title[slug])}</h2><p class="src">Answers quoted from <a href="https://www.familypurity.com/read/{slug}.html">this chapter</a>. '
                    f'Status: {"approved" if entry["approved"] else "awaiting approval"}</p>{qs}</section>')
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Common questions: drafts for review</title>
<style>body{{margin:0;background:#fff;color:#221d33;font:18px/1.55 Georgia,serif}} main{{max-width:44rem;margin:0 auto;padding:24px 16px 60px}}
h1{{font-weight:500;color:#2c2157;margin:.2em 0}} .lead{{background:#f2effa;border-radius:14px;padding:14px 18px}} section{{border-top:1px solid #e0daee;margin-top:28px;padding-top:6px}}
h2{{color:#2c2157;font-weight:600}} .src{{color:#5f5976;font-size:.95rem}} .qa{{margin:16px 0 0;padding:12px 16px;border:1px solid #e0daee;border-radius:12px}}
h3{{margin:0 0 .3em;font-size:1.08rem;color:#4b3a8c}} .qa p{{margin:.35em 0}} a{{color:#4b3a8c}}</style></head><body><main>
<h1>Common questions: drafts for review</h1>
<p class="lead">These question-and-answer sections are proposed for the chapter pages, to help people who search with these questions find the chapters.
<b>Only the questions are new.</b> Every answer is copied word for word from the same chapter on the site. Nothing here is on the website yet; each page's questions go live only after you approve them.
For each page: approve, change a question, remove one, or suggest another passage.</p>
{''.join(secs)}
</main></body></html>'''

if __name__ == '__main__':
    bad = check()
    os.makedirs(os.path.join(SITE, 'review'), exist_ok=True)
    open(os.path.join(SITE, 'review', 'faq-drafts.html'), 'w').write(review_page()); print('review/faq-drafts.html written')
    sys.exit(1 if bad else 0)
