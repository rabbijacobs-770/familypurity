"""Write sitemap.xml: every page meant for search, with the date each was last changed (from git;
today for a page with changes not yet committed). Left out: search.html, the 404 page, and the
redirect pages for old addresses (home.html, blog/), and the Questions section until it has answers.   python3 _build/sitemap.py"""
import datetime, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render import ORDER, BASE
from finish_read import QUIZZES
from questions import published
from build import SITE

PAGES = ([('index.html', '', 'weekly', '1.0'), ('start-here.html', 'start-here.html', 'monthly', '0.9'), ('choson.html', 'choson.html', 'monthly', '0.9'), ('kallah.html', 'kallah.html', 'monthly', '0.9'), ('postpartum.html', 'postpartum.html', 'monthly', '0.8'), ('read/index.html', 'read/', 'monthly', '0.9')] +
         [(f'read/{o[0]}.html', f'read/{o[0]}.html', 'monthly', '0.8') for o in ORDER] +
         [('calendar.html', 'calendar.html', 'monthly', '0.8'), ('calendar-sheet.html', 'calendar-sheet.html', 'monthly', '0.7')] +
         [(q[0], q[0], 'monthly', '0.6') for q in sorted(QUIZZES, key=lambda q: q[1])] +
         [('recommended-sites.html', 'recommended-sites.html', 'monthly', '0.5')] +
         # Questions and answers, once the first answer is published (until then the section is hidden)
         ([('questions/index.html', 'questions/', 'weekly', '0.7')] + [(f"questions/{q['slug']}.html", f"questions/{q['slug']}.html", 'monthly', '0.6') for q in published()]
          if published() else []))

def lastmod(path):
    if subprocess.run(['git', 'status', '--porcelain', '--', path], cwd=SITE, capture_output=True, text=True).stdout.strip():
        return datetime.date.today().isoformat()
    return subprocess.run(['git', 'log', '-1', '--format=%cs', '--', path], cwd=SITE, capture_output=True, text=True).stdout.strip()

if __name__ == '__main__':
    rows = []
    for path, loc, freq, pri in PAGES:
        assert os.path.exists(os.path.join(SITE, path)), path
        rows.append(f'  <url><loc>{BASE}/{loc}</loc><lastmod>{lastmod(path)}</lastmod><changefreq>{freq}</changefreq><priority>{pri}</priority></url>')
    open(os.path.join(SITE, 'sitemap.xml'), 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + '\n'.join(rows) + '\n</urlset>\n')
    print(len(rows), 'pages in sitemap.xml')
