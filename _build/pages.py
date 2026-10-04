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
   'drop_lines':PRINT_LINES+['* This PDF']},
 'ch._2_-_gynecological_':{'slug':'gynecological-considerations','num':'Chapter 2','title':'Gynecological Considerations','pdf':'ch._2_-_gynecological_.pdf',
   'desc':'Family Purity on gynecological procedures: which procedures cause niddah, which do not, and when to consult a rabbi.',
   'drop_lines':PRINT_LINES,'body':10.6,'fnsize':10.6,'fn_any_size':True},
 'ch._3_-_stains':{'slug':'stains','num':'Chapter 3','title':'Stains','pdf':'ch._3_-_stains.pdf','add_italics':True,
   'desc':'Chapter 3 of Family Purity: the laws of stains (kesamim), the three conditions, minimum size, and how to approach a rabbi with a question.',
   'drop_lines':PRINT_LINES},
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
