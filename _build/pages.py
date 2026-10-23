PRINT_LINES=['Permission granted to reprint','This PDF is formatted as US letter size','Permission is granted to','Questions or requests:','Excerpted from: Family Purity','Excerpted from:']
FIVE_DAYS='''<figure class="cal" aria-label="Example of the five minimum days">
      <figcaption>Minimum of five days, inclusive &middot; tap a day</figcaption>
      <div class="cal-grid five">
        <span class="dow">Su</span><span class="dow">Mo</span><span class="dow">Tu</span><span class="dow">We</span><span class="dow">Th</span>
        <button class="day niddah" type="button" aria-pressed="false" data-info="<b>Sunday the 6th &middot; Day 1.</b> In this example, the <em>niddah</em> state begins. This day counts as day one, whether it began in the daytime or the night before."><span class="d">6</span><span class="tag">Niddah began</span></button>
        <button class="day niddah" type="button" aria-pressed="false" data-info="<b>Monday the 7th &middot; Day 2.</b>"><span class="d">7</span><span class="tag">Day 2</span></button>
        <button class="day niddah" type="button" aria-pressed="false" data-info="<b>Tuesday the 8th &middot; Day 3.</b>"><span class="d">8</span><span class="tag">Day 3</span></button>
        <button class="day niddah" type="button" aria-pressed="false" data-info="<b>Wednesday the 9th &middot; Day 4.</b>"><span class="d">9</span><span class="tag">Day 4</span></button>
        <button class="day hefsek" type="button" aria-pressed="true" data-info="<b>Thursday the 10th &middot; Day 5.</b> The earliest day for the <em>hefsek tahara</em>, before sunset, confirming that bleeding has stopped."><span class="d">10</span><span class="tag">Hefsek tahara</span></button>
      </div>
      <p class="cal-info" role="status"><b>Thursday the 10th &middot; Day 5.</b> The earliest day for the <em>hefsek tahara</em>, before sunset, confirming that bleeding has stopped.</p>
    </figure>'''

PAGES={
 'ch._from_the_rebbe':{'slug':'from-the-rebbe','num':'Introduction','title':'From the Rebbe','pdf':'ch._from_the_rebbe.pdf',
   'desc':'Letters and talks of the Lubavitcher Rebbe on family purity, peace at home, fertility and the health of children.',
   'drop_lines':PRINT_LINES,'fix_text':{' (Note: it was on page 444, look up)':'','delayed WORD (mitakev) resulting':'delayed resulting'},'fix_fn':{'11':'<em>Igros Kodesh</em> Kislev 5713.'}},
 'ch._1_-_perfect_marriage':{'slug':'perfect-marriage','num':'Chapter 1','title':'Perfect Marriage','pdf':'ch._1_-_perfect_marriage.pdf',
   'desc':'Chapter 1 of Family Purity by Rabbi Fishel Jacobs: the body and soul of a Jewish marriage, mutual respect, and the words of the Rambam and the Rebbe.',
   'drop_lines':PRINT_LINES},
 'ch._2_-_niddah':{'slug':'niddah','num':'Chapter 2','title':'Niddah','pdf':'ch._2_-_niddah.pdf',
   'desc':'Chapter 2 of Family Purity: what niddah is, sensations of menstruation (hargasha), examinations, colors and their outcome, with sources.',
   'drop_lines':PRINT_LINES},
 'ch._2_-_source_of_niddah':{'slug':'source-of-niddah','num':'Chapter 2','title':'Source of Niddah','pdf':'ch._2_-_source_of_niddah.pdf',
   'desc':'Chapter 2 of Family Purity: uterine bleeding, niddah before marriage, examinations, discolored urine and additional purity, with sources.',
   'drop_lines':PRINT_LINES+['* This PDF'],'fix_html':{r'close proximity to friends\(\?\?\)\.':'close proximity to friends.',r'with her son or daughter \(\?\?\),':'with her son or daughter,'},
   'fix_fn':{'47':'<em>Shulchan Aruch Admur Hazoken</em> 88:2.'}},   # PDF had "Amur"; corrected at Rabbi Jacobs's request (2026-10-21)   # editor's note left in the PDF; removed at Rabbi Jacobs's request (2026-10-21)
 'ch._2_-_gynecological_':{'slug':'gynecological-considerations','num':'Chapter 2','title':'Gynecological Considerations','pdf':'ch._2_-_gynecological_.pdf',
   'desc':'Family Purity on gynecological procedures: which procedures cause niddah, which do not, and when to consult a rabbi.',
   'drop_lines':PRINT_LINES,'body':10.6,'fnsize':10.6,'fn_any_size':True},
 'ch._3_-_stains':{'slug':'stains','num':'Chapter 3','title':'Stains','pdf':'ch._3_-_stains.pdf','add_italics':True,
   'desc':'Chapter 3 of Family Purity: the laws of stains (kesamim), the three conditions, minimum size, and how to approach a rabbi with a question.',
   'drop_lines':PRINT_LINES,'fix_html':{r'usually one found on the , bed sheet':'usually one found on the underwear, bed sheet'}},   # word missing in the PDF; Rabbi Jacobs: "underwear" (2026-10-21)
 'ch._5_-_making_sure_menstruation':{'slug':'making-sure-menstruation-has-finished','num':'Chapter 5','title':'Making Sure Menstruation Has Finished','pdf':'ch._5_-_making_sure_menstruation.pdf','add_italics':True,
   'desc':'Chapter 5 of Family Purity: the hefsek tahara, the five minimum days, and why the timing matters, with an interactive example.',
   'diagram_sizes':[6.4,7.3],'diagram_bold':True,'diagram_html':FIVE_DAYS,'drop_lines':PRINT_LINES,'fix_html':{r'<p>(And this is the law when she ceases to notice blood, after seeing it for a few days\.)</p>\s*<blockquote class="quote"><p>':r'<blockquote class="quote"><p>\1 '}},
 'times_web_edition_chabad':{'slug':'times-chabad','num':'Times','title':'Separation Dates','sub':'Chabad custom','pdf':'times_web_edition_chabad.pdf','add_italics':True,'skip_pages':[1],
   'desc':'Times by Rabbi Fishel Jacobs, Chabad custom: the three separation dates (vestos), how long to separate, and the examination, with sources.',
   'epigraph':('Caution to separate on anticipated menstruation dates merits children fit to be prominent teachers of the Jewish people.','Rabbi Yehoshua ben Levy, Shavuos 18b'),
   'drop_lines':['On the following pages:','Illustrations, calendar','suggested use and sources'],'drop_exact':['Sources','❧','TIME OF THE ANTICIPATED MENSTRUATION','ESH','ONIS','GAH']},
 'times_web_edition_major_customs':{'slug':'times-major-customs','num':'Times','title':'Separation Dates','sub':'Major customs','pdf':'times_web_edition_major_customs.pdf','add_italics':True,'skip_pages':[1],
   'desc':'Times by Rabbi Fishel Jacobs, major customs: the monthly, average and interval separation dates, the 31st day and Or Zarua.',
   'epigraph':('Caution to separate on anticipated menstruation dates merits children fit to be prominent teachers of the Jewish people.','Rabbi Yehoshua ben Levy, Shavuos 18b'),
   'drop_lines':['On the following pages:','Illustrations, calendar','suggested use and sources'],'drop_exact':['Sources','❧','TIME OF THE ANTICIPATED MENSTRUATION','ESH','ONIS','GAH']},
}

SEO={'ch._from_the_rebbe': 'The Rebbe on Family Purity: Letters and Talks', 'ch._1_-_perfect_marriage': 'Perfect Marriage: A Torah View of Marriage', 'ch._2_-_niddah': 'Niddah: Laws of Menstruation in Jewish Law', 'ch._2_-_source_of_niddah': 'Source of Niddah: Uterine Bleeding', 'ch._2_-_gynecological_': 'Gynecological Procedures and Niddah', 'ch._3_-_stains': 'Stains (Kesamim): The Laws of Stains', 'ch._5_-_making_sure_menstruation': 'Hefsek Tahara and the Five Minimum Days', 'times_web_edition_chabad': 'Vestos: Separation Dates, Chabad Custom (Times)', 'times_web_edition_major_customs': 'Vestos: Separation Dates for All Communities (Times)'}
for k,v in SEO.items(): PAGES[k]["seo"]=v

# Chapters from the current edition's full text (FP_Text_copy.pdf, attached by Rabbi Jacobs 2026-10-23);
# lines/book_*.json are written by book_lines.py. No chapter PDF is offered for these.
from book_lines import fig_alts as _fa
_ALTS=_fa()

# Clean-ups for the chapters from the book's full text (applied to the rendered body with re.sub).
BOOK_FIX_ALL={
 r'<p>([A-Z])<em>([a-z’])': r'<p><em>\1\2',                      # drop cap set apart from the italic opening
 r'(<span class="he"[^>]*>[^<]*</span>) \.': r'\1.',
}
_RUNIN=lambda caps,title: {r'<p><em>'+caps+r' \.</em> ': '<p><strong class="runin">'+title+'.</strong> '}
BOOK_FIX={
 'book_ch11_intimate':{
   r'<p>Psalm 23(<label class="fn" for="n27">.*?</small>) Translation (.*?)</p>\s*(<figure class="book-fig"><img src="\.\./images/chapters/psalm-23-hebrew\.png".*?</figure>)':
     r'<h3 class="prayer">Psalm 23\1</h3>\n    \3\n    <p class="prayer-t">Translation</p>\n    <p>\2</p>',
   r'<p><em>Atifah Bekitfah</em> Translation (.*?)</p>\s*(<figure class="book-fig"><img src="\.\./images/chapters/atifah-bekitfah-hebrew\.png".*?</figure>)':
     r'<h3 class="prayer">Atifah Bekitfah</h3>\n    \2\n    <p class="prayer-t">Translation</p>\n    <p>\1</p>',
   '173⁄4':'17¾','581⁄2':'58½',
   **_RUNIN('MEZUZAH','Mezuzah'),**_RUNIN('SEFER TORAH','Sefer Torah')},
 'book_ch12_times':{**_RUNIN('YOM KIPPUR','Yom Kippur'),
   r'<p><em>TISHA BEAV</em>(<label class="fn" for="n16">16</label>.*?</small>)\. ': r'<p><strong class="runin">Tisha BeAv\1.</strong> '},
 'book_ch14_anticipated':{
   r'<p><strong class="runin">The (Monthly|Interval|Average) Cycle—([^<]*?)—\.</strong> (<span class="he"[^>]*>[^<]*</span>) ':
     r'<h3>The \1 Cycle—<em>\2</em> \3</h3>\n    <p>'},
 'book_ch4_absence':{r'\(one eating meat and the other milk\)</li></ul>\s*<p>can suffice with only (.*?)</p>': r'(one eating meat and the other milk) can suffice with only \1</li></ul>'},
 'book_ch13_wedding':{r'<blockquote class="quote"><p>(Most women have a certain number of days before which their menstruation does not appear)</p><cite>(for example, twenty days following the last hefsek tahara\. These examinations are to be)</cite></blockquote>\s*<p>performed ':
     r'<p>\1—\2 performed '},
 'book_ch15_birth':{r'^\s*<blockquote class="quote">.*?</blockquote>\s*<blockquote class="quote"><p></p>.*?</blockquote>\s*':''},
}
BOOK_HEAD=['FAMILY PURITY','CHAPTER 4','CHAPTER 9','CHAPTER 11','CHAPTER 12','CHAPTER 13','CHAPTER 14','CHAPTER 15']
for _name,_slug,_num,_title,_desc,_seo in [
 ('book_ch4_absence','absence-makes-the-heart-grow-fonder','Chapter 4','Absence Makes the Heart Grow Fonder',
  'Chapter 4 of Family Purity by Rabbi Fishel Jacobs: the laws of separation while the wife is niddah, and the reasons behind them, with sources.',
  'Harchakos: The Laws of Separation (Absence Makes the Heart Grow Fonder)'),
 ('book_ch9_mikveh','what-is-a-mikveh','Chapter 9','What Is a Mikveh?',
  'Chapter 9 of Family Purity by Rabbi Fishel Jacobs: what a mikveh is, how a kosher mikveh is built, and why its supervision matters, with sources.',
  'What Is a Mikveh? The Laws of a Kosher Mikveh'),
 ('book_ch11_intimate','intimate-relations','Chapter 11','Intimate Relations',
  'Chapter 11 of Family Purity by Rabbi Fishel Jacobs: marital relations in holiness, modesty, and holy books and a mezuzah in the room, with sources.',
  'Intimate Relations in Jewish Law'),
 ('book_ch12_times','proper-times-for-marital-relations','Chapter 12','Proper Times for Marital Relations',
  'Chapter 12 of Family Purity by Rabbi Fishel Jacobs: Shabbos, Yom Kippur, Tisha BeAv, the night of immersion and other times, with sources.',
  'Proper Times for Marital Relations in Jewish Law'),
 ('book_ch13_wedding','wedding-night','Chapter 13','The Wedding Night',
  'Chapter 13 of Family Purity by Rabbi Fishel Jacobs: preparing for the chupah, the wedding night, and the laws that follow, with sources.',
  'The Wedding Night in Jewish Law (Dam Besulim)'),
 ('book_ch14_anticipated','anticipated-menstruation','Chapter 14','Time of the Anticipated Menstruation',
  'Chapter 14 of Family Purity by Rabbi Fishel Jacobs: the separation dates (vestos), how they are recorded and calculated, and the examinations.',
  'Vestos: Time of the Anticipated Menstruation'),
 ('book_ch15_birth','birth','Chapter 15','Birth',
  'Chapter 15 of Family Purity by Rabbi Fishel Jacobs: the laws of family purity before and after childbirth, and after a miscarriage, with sources.',
  'Birth and Family Purity in Jewish Law'),
]:
    PAGES[_name]={'slug':_slug,'num':_num,'title':_title,'pdf':None,'desc':_desc,'seo':_seo,'book':True,'drop_lines':BOOK_HEAD,'fig_alts':_ALTS,
                  'fix_html':{**BOOK_FIX_ALL,**BOOK_FIX.get(_name,{})}}
PAGES['book_ch15_birth']['epigraph']=('The unborn child’s life is interwoven with its mother’s life. Hence the joy on the date of birth, for on this day the baby receives its own life-force—its soul.','Likutei Sichos vol. 24, p. 180')
