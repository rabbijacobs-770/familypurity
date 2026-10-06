"""Build the private calendar previews (not part of the website).
   python3 _build/hidden-tools/build_calendar.py [out_dir] [--site]   (--site also writes the live /calendar.html)
   Inlines assets/fp-calc.js and assets/day-block.js into calendar-tools-src.html and day-block-src.html.
   Writes review/calendar/*-preview.html (full pages) and, if out_dir is given, the bare pages for publishing."""
import base64, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.abspath(os.path.join(HERE, '..', '..'))
REVIEW = os.path.join(SITE, 'review', 'calendar')

def read(p): return open(os.path.join(HERE, p)).read()

calc = read('assets/fp-calc.js')
day = read('assets/day-block.js')
css = ''.join(re.findall(r"'([^']*)'", re.search(r"const css = (.*?);\n", day, re.S).group(1)))

def full(page):
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
            + page.replace('<main>', '</head><body><main>', 1) + '</body></html>')

pages = {
    'calendar-tools': read('calendar-tools-src.html').replace('/*FPCALC_JS*/', calc).replace('/*FPDAY_JS*/', day).replace('/*FPDAY_CSS*/', css),
    'calendar-half-year': read('half-year-src.html').replace('/*FPCALC_JS*/', calc).replace('/*FPDAY_JS*/', day).replace('/*FPDAY_CSS*/', css),
}
sheet = os.path.join(REVIEW, 'sheet-nissan.png')
if os.path.exists(sheet):
    img = 'data:image/png;base64,' + base64.b64encode(open(sheet, 'rb').read()).decode()
    pages['calendar-day-block'] = read('day-block-src.html').replace('/*FPDAY_JS*/', day).replace('/*FPDAY_CSS*/', css).replace('/*SHEET*/', img)

# The website version of the calendar: the same calendar inside the site's header, banner and footer.
def site_calendar(root):
    tools = pages['calendar-tools']
    style = tools[tools.index('<style>') + 7:tools.index('</style>')]
    cal_css = style[style.index('.key{'):]                                   # the calendar's own rules (the site supplies the rest)
    body = tools[tools.index('  <div class="key">'):tools.index('</main>')]
    bar = tools[tools.index('<div class="bar"'):tools.index('<script>')]
    js = tools[tools.index('<script>') + 8:tools.rindex('</script>')]
    return (read('calendar-site-src.html').replace('{ROOT}', root).replace('/*CAL_CSS*/', cal_css)
            .replace('<!--CAL_BODY-->', body).replace('<!--CAL_BAR-->', bar).replace('/*CAL_JS*/', js))

# The website version of the half-year sheet: the same sheet inside the site's header, banner and footer.
def site_sheet(root):
    sheet = pages['calendar-half-year']
    style = sheet[sheet.index('<style>') + 7:sheet.index('</style>')]
    css = style[style.index('.controls{'):]
    body = sheet[sheet.index('  <div class="controls no-print">'):sheet.index('</main>')]
    js = sheet[sheet.index('<script>') + 8:sheet.rindex('</script>')]
    return (read('half-year-site-src.html').replace('{ROOT}', root).replace('/*SHEET_CSS*/', css)
            .replace('<!--SHEET_BODY-->', body).replace('/*SHEET_JS*/', js))

os.makedirs(REVIEW, exist_ok=True)
open(os.path.join(SITE, 'review', 'calendar-sheet-preview.html'), 'w').write(site_sheet('../'))
open(os.path.join(SITE, 'review', 'calendar-site-preview.html'), 'w').write(site_calendar('../'))   # review/ sits one level below the site
print('calendar-site-preview written')
if '--site' in sys.argv:                                                     # publish: the live page at the site root
    open(os.path.join(SITE, 'calendar.html'), 'w').write(site_calendar(''))
    print('calendar.html written (live page)')
    open(os.path.join(SITE, 'calendar-sheet.html'), 'w').write(site_sheet(''))
    print('calendar-sheet.html written (live page)')
for name, page in pages.items():
    open(os.path.join(REVIEW, name + '-preview.html'), 'w').write(full(page))
    out_dir = next((a for a in sys.argv[1:] if not a.startswith('--')), None)
    if out_dir: open(os.path.join(out_dir, name + '.html'), 'w').write(page)
    print(name, len(page) // 1024, 'KB')
