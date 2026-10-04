"""Split the tools into one SEO page each (tools/<slug>.html) and rebuild tools.html as a hub."""
import re, json, html, os, urllib.parse
SITE=os.path.expanduser('~/Documents/FamilyPurity')
B='https://www.familypurity.com'
HERE=os.path.dirname(os.path.abspath(__file__))
SRC=os.path.join(HERE,'tools-src.html')
if not os.path.exists(SRC): open(SRC,'w').write(open(f'{SITE}/tools.html').read())  # keep the original markup as the source
src=open(SRC).read()

def section(id_):
    m=re.search(rf'<section class="tool" id="{id_}">(.*?)\n    </section>',src,re.S)
    inner=m.group(1)
    # drop the small intro block: each page has its own hero
    inner=re.sub(r'<div class="intro">.*?</div>\s*','',inner,count=1,flags=re.S)
    return inner

ICON={ # same line icons as the homepage
 'mikveh-night-calculator':'<path d="M19.5 14.5A8 8 0 0 1 9.5 4.5a8 8 0 1 0 10 10z"/>',
 'seven-white-days-checklist':'<rect x="4" y="4" width="16" height="16" rx="3.5"/><path d="M8.5 12.5l2.5 2.5 4.5-5.5"/>',
 'vestos-calculator':'<rect x="3.5" y="5" width="17" height="15" rx="2.5"/><path d="M3.5 10h17M8 3v4M16 3v4"/>',
 'hebrew-date-converter':'<text x="12" y="17.5" text-anchor="middle" font-size="15" font-family="Frank Ruhl Libre, serif" fill="currentColor" stroke="none">א</text><rect x="3.5" y="3.5" width="17" height="17" rx="3.5"/>',
 'sunrise-sunset-times':'<path d="M3 18h18M7 18a5 5 0 0 1 10 0M12 6.5V10M5.8 10.3l1.9 1.9M18.2 10.3l-1.9 1.9"/>',
 'family-purity-glossary':'<path d="M5 4.5h10.5A3.5 3.5 0 0 1 19 8v12H8.5A3.5 3.5 0 0 1 5 16.5z"/><path d="M5 16.5A3.5 3.5 0 0 1 8.5 13H19"/>',
}
svg=lambda k:f'<svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICON[k]}</svg>'

TOOLS=[
 dict(slug='mikveh-night-calculator',sec='mikveh',short='Mikveh night',card='From the day it began to the night of immersion.',
  title='Mikveh Night Calculator: Hefsek & Seven Clean Days',h1='Mikveh night calculator',
  lede='Find the earliest hefsek tahara, the seven white days and the night of immersion, in English and Hebrew dates.',
  desc='Free mikveh night calculator. Enter the day the niddah state began to find the earliest hefsek tahara, the seven white days and mikveh night. Private, based on Rabbi Fishel Jacobs’s Family Purity.',
  how=['The day the niddah state began counts as day one, whether it began in the daytime or the night before.',
       'The <em>hefsek tahara</em> can be done from the fifth day, before sunset. <span class="src">Family Purity, <a href="../read/making-sure-menstruation-has-finished.html">Chapter 5</a>; Ramo 196:11</span>',
       'The seven white days begin the day after the <em>hefsek tahara</em>, with examinations twice daily. <span class="src"><a href="../read/seven-white-days.html">Chapter 6</a></span>',
       'Immersion in the <em>mikveh</em> is after nightfall at the end of the seventh day. <span class="src"><a href="../read/overview.html">Overview</a></span>'],
  example=('Example','Began Sunday &rarr; earliest hefsek tahara Thursday before sunset &rarr; seven white days Friday to the next Thursday &rarr; mikveh Thursday night.'),
  faq=[('What if the hefsek tahara was done later than the fifth day?','Enter its date in the optional field. The seven white days are counted from the day after it.'),
       ('What if mikveh night falls on Friday night or Yom Tov?','Special preparation rules apply. See Chapter 7 in Family Purity, or ask Rabbi Jacobs.'),
       ('Does this follow my community’s custom?','It follows the five-day minimum as brought in Family Purity (Ramo 196:11). If your community follows a different custom, ask your rabbi.'),
       ('Is anything I enter saved or sent?','No. The calculation happens on your own device. Nothing is sent to us or anyone else.')],
  related=['seven-white-days-checklist','vestos-calculator','sunrise-sunset-times'],chapters=[('making-sure-menstruation-has-finished','Chapter 5: Making Sure Menstruation Has Finished'),('seven-white-days','Chapter 6: The Seven White Days')]),
 dict(slug='seven-white-days-checklist',sec='checklist',short='Seven days checklist',card='Mark each examination as you go.',
  title='Seven White Days Checklist: Track Your Bedikos',h1='Seven white days checklist',
  lede='Mark each of the fourteen examinations, twice a day, as you go. It stays on your device only.',
  desc='Free seven white days (shiva nekiim) checklist. Track the twice-daily examinations privately on your phone, with mikveh night shown. Based on Family Purity by Rabbi Fishel Jacobs.',
  how=['During the seven white days, a woman checks herself twice daily. <span class="src">Tzemach Tzedek 196:5</span>',
       'She wears white underwear and sleeps on white sheets, checked for stains. <span class="src"><a href="../read/seven-white-days.html">Chapter 6</a></span>',
       'The first three days are stricter regarding stains. <span class="src">Ramo 196:10</span>',
       'Mikveh night is after nightfall at the end of the seventh day.'],
  example=('How to use it','Enter the hefsek tahara date, then tap each examination as you do it. Today is outlined in gold.'),
  faq=[('What if an examination was missed?','Ask Rabbi Jacobs or your rabbi. The answer depends on the details.'),
       ('Where is my checklist saved?','Only in this browser on this device. Clearing your browser data clears the checklist.'),
       ('Can I add the seven days to my calendar?','Yes. Use the mikveh night calculator and choose “Add to my calendar.” Entries are discreet unless you choose to show details.')],
  related=['mikveh-night-calculator','vestos-calculator','family-purity-glossary'],chapters=[('seven-white-days','Chapter 6: The Seven White Days')]),
 dict(slug='vestos-calculator',sec='vestos',short='Separation dates',card='Monthly, average and interval dates.',
  title='Vestos Calculator: Onah Beinonis & Haflagah',h1='Vestos calculator: separation dates',
  lede='Find the dates to separate in anticipation of the next period, for Chabad and other customs, from Times.',
  desc='Free vestos calculator for the onah beinonis (30th and 31st day), yom hachodesh and veses haflagah, with Chabad and other customs. Private, based on Times by Rabbi Fishel Jacobs.',
  how=['<b>Monthly cycle</b> (<em>yom hachodesh</em>): the same Hebrew date next month, in the same half of the day.',
       '<b>Average cycle</b> (<em>onah beinonis</em>): the 30th day, for a full day. Many communities also keep the 31st day.',
       '<b>Interval cycle</b> (<em>veses haflagah</em>): the same interval as last time. In the Chabad custom it is counted from the <em>hefsek tahara</em>; others count from one onset to the next.',
       'On each date an examination is made from the hour the last period began. Only actual menstruation counts, not stains. <span class="src"><a href="../read/times-chabad.html">Times, Chabad custom</a> &middot; <a href="../read/times-major-customs.html">Major customs</a></span>'],
  example=('Half a day or a full day?','The monthly and interval dates are a half day: sunset to sunrise, or sunrise to sunset. The average cycle is a full day, from one sunset to the next.'),
  faq=[('What is an onah?','A half day: daytime from sunrise to sunset, or nighttime from sunset to sunrise.'),
       ('Why does it ask what time the period began?','After sunset the Hebrew date has already moved to the next day, and the separation is kept in the same half of the day.'),
       ('Do stains count when calculating?','No. Only actual menstruation, or blood found through an examination, is recorded for these dates.'),
       ('What about a fixed cycle (veset kavua)?','This calculator covers the common case. If your cycle follows a fixed pattern, ask Rabbi Jacobs.')],
  related=['mikveh-night-calculator','hebrew-date-converter','sunrise-sunset-times'],chapters=[('times-chabad','Times: Separation Dates, Chabad Custom'),('times-major-customs','Times: Separation Dates, Major Customs')]),
 dict(slug='hebrew-date-converter',sec='hebrew',short='Hebrew dates',card='Convert between English and Hebrew dates.',
  title='Hebrew Date Converter: English to Hebrew and Back',h1='Hebrew date converter',
  lede='Find the Hebrew date for any day, or the English date for any Hebrew one, written in Hebrew letters too.',
  desc='Free Hebrew date converter. Convert English dates to Hebrew dates and Hebrew dates to English, with the after-sunset rule and leap years (Adar I and Adar II).',
  how=['The Hebrew day begins at sunset. After sunset, the Hebrew date has already moved to the next day.',
       'In a Jewish leap year there are two months of Adar: Adar I and Adar II.',
       'The monthly separation date (<em>yom hachodesh</em>) falls on the same Hebrew date as the last period began.'],
  example=('Example','10 Nisan 5787 is Saturday, April 17, 2027. It begins the evening before, at sunset.'),
  faq=[('Why does the date change at sunset?','In Jewish law the day begins at nightfall of the evening before, so the Hebrew date starts at sunset.'),
       ('Which Adar should I choose?','In a regular year choose Adar. In a leap year choose Adar I or Adar II.')],
  related=['vestos-calculator','sunrise-sunset-times','mikveh-night-calculator'],chapters=[('times-chabad','Times: Separation Dates')]),
 dict(slug='sunrise-sunset-times',sec='sun',short='Sunrise &amp; sunset',card='When daytime and nighttime begin where you live.',
  title='Sunrise and Sunset Times for Hefsek Tahara and Onah',h1='Sunrise and sunset times',
  lede='See when daytime and nighttime begin in your city this week. The hefsek tahara is done before sunset.',
  desc='Free sunrise and sunset times for Jerusalem, New York, London and more, or your own location. Know when the onah begins and the time for the hefsek tahara.',
  how=['Daytime is from sunrise to sunset; nighttime is from sunset to sunrise. <span class="src">Shulchan Aruch Admur Hazoken 184</span>',
       'The <em>hefsek tahara</em> is done before sunset.',
       'Separation dates are kept in the half of the day (<em>onah</em>) when the last period began.',
       'For nightfall times, such as for immersion, follow your community’s calendar.'],
  example=('Accuracy','Times are calculated on your device and are accurate to within a minute or two.'),
  faq=[('Why doesn’t it show nightfall?','Nightfall (tzeis) is calculated differently by different communities. Use your community’s calendar for it.'),
       ('Can it use my exact location?','Yes. Tap “Use my location.” Your location stays on your device.')],
  related=['vestos-calculator','mikveh-night-calculator','hebrew-date-converter'],chapters=[('making-sure-menstruation-has-finished','Chapter 5: Making Sure Menstruation Has Finished')]),
 dict(slug='family-purity-glossary',sec='glossary',short='Glossary',card='The Hebrew terms, in plain English.',
  title='Family Purity Glossary: Niddah, Mikveh & More',h1='Family purity glossary',
  lede='The Hebrew terms used in Rabbi Jacobs’s books, explained in plain English.',
  desc='A plain-English glossary of Jewish family purity terms: niddah, hefsek tahara, moch dochuk, seven white days, mikveh, kesamim, vestos, onah beinonis and more.',
  how=None,example=None,faq=None,
  related=['mikveh-night-calculator','vestos-calculator','seven-white-days-checklist'],chapters=[('overview','Overview: the purity cycle step by step')]),
]
BY={t['slug']:t for t in TOOLS}

NAV='''<header class="top">
  <div class="pill on-flowers">
    <a class="brand" href="{r}index.html" aria-label="Family Purity, home"><img src="{r}images/brand/fp-wordmark.svg" alt="Family Purity" width="454" height="118"></a>
    <nav class="links" id="links" aria-label="Main">
      <a href="{r}index.html#books">Books</a>
      <a href="{r}index.html#resources">Free resources</a>
      <a href="{r}search.html">Search</a>
      <a href="{r}tools.html">Tools</a>
      <a href="{r}index.html#about">About</a>
      <a href="{r}index.html#contact">Contact</a>
    </nav>
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="links">Menu</button>
    <a class="btn" href="https://wa.me/972587921788" target="_blank" rel="noopener">Ask a question</a>
  </div>
</header>'''
FOOT='''<footer class="panel on-flowers" style="margin-top:3rem">
  <div class="wrap">
    <div>
      <a class="brand" href="{r}index.html" aria-label="Family Purity, home"><img src="{r}images/brand/fp-wordmark.svg" alt="Family Purity" width="454" height="118"></a>
      <p>Rabbi Fishel Jacobs</p>
    </div>
    <ul>
      <li><a href="{r}index.html#books">Books</a></li>
      <li><a href="{r}index.html#resources">Free resources</a></li>
      <li><a href="{r}tools.html">Tools</a></li>
      <li><a href="{r}index.html#contact">Contact</a></li>
    </ul>
    <small>&copy; Family Purity <span class="credit">Photo: Hisu Lee / Unsplash</span></small>
  </div>
</footer>'''
MENU='''<script>
const menuBtn=document.querySelector('.menu-btn'), links=document.getElementById('links');
menuBtn.addEventListener('click',()=>{const open=links.classList.toggle('open');menuBtn.setAttribute('aria-expanded',open);menuBtn.textContent=open?'Close':'Menu'});
</script>'''
def head(title,desc,url,r,ld):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{url}">
<link rel="icon" href="{r}favicon.svg" type="image/svg+xml">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Family Purity">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{B}/images/family-p-copy_orig.jpg">
<meta name="twitter:card" content="summary">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500&family=Frank+Ruhl+Libre:wght@500&display=swap">
<link rel="stylesheet" href="{r}assets/site.css">
<link rel="stylesheet" href="{r}assets/tools.css">
{''.join(f'<script type="application/ld+json">{json.dumps(x,ensure_ascii=False)}</script>' for x in ld)}
</head>
<body>
'''
def cards(slugs,r):
    return '\n'.join(f'<a class="tool-card" href="{r}tools/{s}.html"><span class="ti">{svg(s)}</span><span><b>{BY[s]["short"]}</b><small>{BY[s]["card"]}</small></span></a>' for s in slugs)

OUT=f'{SITE}/_build/hidden-tools'  # hidden until Rabbi Jacobs signs off; move to the site root to publish
os.makedirs(f'{OUT}/tools',exist_ok=True)
for t in TOOLS:
    url=f'{B}/tools/{t["slug"]}.html'
    app={"@context":"https://schema.org","@type":"WebApplication","name":t['h1'][:1].upper()+t['h1'][1:],"url":url,"description":t['desc'],
         "applicationCategory":"LifestyleApplication","operatingSystem":"Any (web browser)","isAccessibleForFree":True,
         "offers":{"@type":"Offer","price":"0","priceCurrency":"USD"},
         "creator":{"@type":"Person","name":"Rabbi Fishel Jacobs","url":B+"/#rabbi-jacobs"},"publisher":{"@id":B+"/#organization"}}
    crumbs={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"Family Purity","item":B+"/"},
        {"@type":"ListItem","position":2,"name":"Free tools","item":B+"/tools.html"},
        {"@type":"ListItem","position":3,"name":t['short'].replace('&amp;','&'),"item":url}]}
    cur=' aria-current="page"'
    chips=''.join('<a href="'+s_+'.html"'+(cur if s_==t['slug'] else '')+'>'+BY[s_]['short']+'</a>' for s_ in BY)
    how=''
    if t['how']:
        how=f'''
    <section class="how">
      <div class="how-grid">
        <div>
          <h2>How it works</h2>
          <ol>{''.join(f'<li>{x}</li>' for x in t['how'])}</ol>
        </div>
        <div class="example"><b>{t['example'][0]}</b><p>{t['example'][1]}</p></div>
      </div>
    </section>'''
    faq=''
    if t['faq']:
        faq='\n    <section class="faq">\n      <h2>Common questions</h2>\n'+'\n'.join(f'      <details><summary>{q}</summary><p>{a}</p></details>' for q,a in t['faq'])+'\n    </section>'
    chaps=' &middot; '.join(f'<a href="../read/{s}.html">{l}</a>' for s,l in t['chapters'])
    body=f'''{NAV.format(r='../')}

<main>
  <section class="hero tools-hero panel on-flowers" style="padding-block:0">
    <div class="wrap">
      <p class="eyebrow">Free tool</p>
      <h1>{t['h1'][:1].upper()+t['h1'][1:]}</h1>
      <p class="lede">{t['lede']}</p>
      <span class="private">Private: nothing you enter leaves your device</span>
      <nav class="chips" aria-label="Other tools">{chips}</nav>
    </div>
  </section>

  <div class="wrap">
    <section class="tool" id="{t['sec']}">{section(t['sec'])}
    </section>{how}{faq}
    <section class="related">
      <h2>Related tools</h2>
      <div class="tool-cards">{cards(t['related'],'../')}</div>
      <p class="small" style="margin-top:1.2rem">Read more: {chaps}</p>
    </section>

    <div class="disclaimer">
      <p>These tools follow the common case as described in Rabbi Jacobs&rsquo;s books. Almost every detail can have exceptions. For your own situation, ask a rabbi.</p>
      <a class="btn btn-solid" href="https://wa.me/972587921788" target="_blank" rel="noopener">Ask Rabbi Jacobs, free</a>
    </div>
    <p class="correction-line">Spotted a typo or something unclear? <a href="#" data-em="RabbiJacobs|FamilyPurity.com" data-subject="Correction: {t['short']}">Send a correction</a></p>
  </div>
</main>

{FOOT.format(r='../')}

{MENU}
<script src="../assets/fp-calc.js"></script>
<script src="../assets/tools.js"></script>
</body>
</html>
'''
    page=head(t['title']+('' if 'Family Purity' in t['title'] else ' | Family Purity'),t['desc'],url,'../',[app,crumbs])+body
    page=page.replace('href="#checklist"','href="seven-white-days-checklist.html"')
    open(f'{OUT}/tools/{t["slug"]}.html','w').write(page)
    print('wrote tools/'+t['slug']+'.html')

# Hub
hub_ld={"@context":"https://schema.org","@type":"ItemList","name":"Free family purity tools","itemListElement":[
    {"@type":"ListItem","position":i+1,"url":f'{B}/tools/{t["slug"]}.html',"name":t['h1'][:1].upper()+t['h1'][1:]} for i,t in enumerate(TOOLS)]}
hub_crumbs={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Family Purity","item":B+"/"},{"@type":"ListItem","position":2,"name":"Free tools","item":B+"/tools.html"}]}
hub=head('Free Family Purity Calculators & Tools | Family Purity','Free, private family purity tools by Rabbi Fishel Jacobs: mikveh night calculator, seven white days checklist, vestos calculator, Hebrew date converter, sunrise and sunset times, and a glossary.',B+'/tools.html','',[hub_ld,hub_crumbs])+f'''{NAV.format(r='')}

<main>
  <section class="hero tools-hero panel on-flowers" style="padding-block:0">
    <div class="wrap">
      <p class="eyebrow">Free tools</p>
      <h1>Free family purity calculators</h1>
      <p class="lede">Plan dates, keep track and look things up, based on Rabbi Jacobs&rsquo;s books.</p>
      <span class="private">Private: nothing you enter leaves your device</span>
    </div>
  </section>
  <div class="wrap">
    <section class="related" style="border-top:0">
      <div class="tool-cards">{cards([t['slug'] for t in TOOLS],'')}</div>
    </section>
    <div class="disclaimer">
      <p>These tools follow the common case as described in Rabbi Jacobs&rsquo;s books. Almost every detail can have exceptions. For your own situation, ask a rabbi.</p>
      <a class="btn btn-solid" href="https://wa.me/972587921788" target="_blank" rel="noopener">Ask Rabbi Jacobs, free</a>
    </div>
  </div>
</main>

{FOOT.format(r='')}

{MENU}
</body>
</html>
'''
open(f'{OUT}/tools.html','w').write(hub); print('wrote tools.html hub')
