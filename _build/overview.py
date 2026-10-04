import os,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from render import page
from build import SITE
def fn(n,t): return f'<label class="fn" for="n{n}">{n}</label><input class="fn-t" type="checkbox" id="n{n}"><small class="sn"><b>{n}</b>{t}</small>'
def term(w,d): return f'<button class="term" type="button" data-word="{w}" data-def="{d}">{w}</button>'
step=lambda h,n,ft,body: f'<p class="no-indent"><strong class="runin">{h}</strong>{fn(n,ft)}. {body}</p>'
body='\n    '.join([
 '<p class="no-indent"><strong class="runin">About this overview.</strong> The following purity cycle, as it most commonly occurs, is presented as a succinct reference.</p>',
 '<p>Note that almost every detail, however, can have deviations with potential repercussion, many of which are covered in this book.</p>',
 '<h2>The Purity Cycle</h2>',
 step('Niddah state',1,'<a href="niddah.html">Chapter 2 - Niddah</a>; <a href="stains.html">Chapter 3 - Stains</a>.',
      f'The wife enters a {term("niddah","The status of a woman from the start of menstruation until she immerses in a mikveh.")} state (impurity) when menstruation{fn(2,"Other common causes include: premenstrual staining; childbirth; gynecological procedures penetration into the uterus.")} begins.'),
 step('Separation',3,'Chapter 4 - Absence Makes the Heart Grow Fonder.','Until she immerses, all physical contact with her husband ceases.'),
 step('Ascertaining bleeding ceased',4,'<a href="making-sure-menstruation-has-finished.html">Chapter 5 - Making Sure Menstruation Has Finished</a>.',
      f'When at least five days have passed{fn(5,"The day she became <em>niddah</em> (whether during the daytime or the preceding nighttime) is counted as day one.")}, prior to sunset the wife washes her entire body, particularly the private area, with warm water. Then, with a soft white cloth wrapped around the fingers, she internally examines herself. If this is clean from discoloration, again before sunset, she inserts a soft white cloth into her private area. This is removed after nightfall.'),
 step('Seven White Days',6,'<a href="seven-white-days.html">Chapter 6 - Seven White Days</a>.','If that is clean from discoloration, she begins the Seven White Days. During these days she wears white underpants, and sleeps on white bed sheets. Every day, she examines herself twice daily with a soft white cloth.'),
 step('Preparation',7,'Chapter 7 - Preparing For Immersion.','On the last of the Seven White Days she scrupulously washes her entire body, including shampooing and combing the hair, brushing her teeth and making sure the body is free from intervening substances.'),
 step('Immersion',8,'Chapter 10 - Immersion.',f'After nightfall she immerses in the {term("mikveh","A pool of natural water built according to Jewish law, used for immersion.")}{fn(9,"Chapter 9 - What is A Mikveh?")}.'),
 step('Permissible times',10,'Chapter 11 - Intimate Relations; Chapter 12 - Proper Times for Marital Relations.','The times when marital relations are permissible.'),
 step('Separation dates',11,'Chapter 14 - Separation Dates (Times of Anticipated Menstruation).',
      f'On an ongoing basis, throughout married life, the dates when menstruation begins and finishes{fn(12,"Chabad custom. Others project from the beginning of menstruation to the beginning of the following one, Dates—Other Methods of Calculation.")} are recorded. From these are projected separation dates in anticipation of the upcoming menstruation.'),
])
h=page('overview','Introduction','Overview',None,
 'A one-page overview of the Jewish family purity cycle: niddah, the hefsek tahara, the seven white days, immersion in the mikveh and separation dates.',
 'overview_us_letter.pdf',None,body,seo='The Jewish Purity Cycle, Step by Step')
h=h.replace('The chapter continues in the book','Every step is explained in the book').replace('This is an excerpt from','Based on')
open(os.path.join(SITE,'read','overview.html'),'w').write(h); print('overview written')
