"""Common questions for the chapter pages. All approved by Rabbi Jacobs on 2026-10-21.

Every answer is quoted word for word from the same chapter's text on the site (faq_check.py verifies this);
only the questions are new. A page shows its Common questions section, with matching FAQPage data, only
once its entry is marked approved=True. New questions start as approved=False until he approves them.

Answer format: a list of paragraphs; a paragraph that is a list of strings becomes a bulleted list."""

FAQ = {
'overview': dict(approved=True, items=[
  ('When does a woman become niddah?', [
    'The wife enters a niddah state (impurity) when menstruation begins.',
    'Until she immerses, all physical contact with her husband ceases.']),
  ('What are the steps of the family purity cycle?', [
    'The following purity cycle, as it most commonly occurs, is presented as a succinct reference.',
    ['Niddah state. The wife enters a niddah state (impurity) when menstruation begins.',
     'Separation. Until she immerses, all physical contact with her husband ceases.',
     'Ascertaining bleeding ceased. When at least five days have passed, prior to sunset the wife washes her entire body, particularly the private area, with warm water. Then, with a soft white cloth wrapped around the fingers, she internally examines herself. If this is clean from discoloration, again before sunset, she inserts a soft white cloth into her private area. This is removed after nightfall.',
     'Seven White Days. If that is clean from discoloration, she begins the Seven White Days. During these days she wears white underpants, and sleeps on white bed sheets. Every day, she examines herself twice daily with a soft white cloth.',
     'Preparation. On the last of the Seven White Days she scrupulously washes her entire body, including shampooing and combing the hair, brushing her teeth and making sure the body is free from intervening substances.',
     'Immersion. After nightfall she immerses in the mikveh.'],
    'Note that almost every detail, however, can have deviations with potential repercussion, many of which are covered in this book.']),
  ('What are separation dates?', [
    'On an ongoing basis, throughout married life, the dates when menstruation begins and finishes are recorded. From these are projected separation dates in anticipation of the upcoming menstruation.']),
]),
'niddah': dict(approved=True, items=[
  ('What makes a woman niddah?', [
    'A woman becomes a “menstruant,” niddah in Hebrew, when blood leaves the womb.',
    'A woman becomes a niddah whenever blood leaves the womb regardless of the cause; i.e., whether related to the monthly menstruation, an internal gynecological examination which involved penetration of the uterus, giving birth or spotting.']),
  ('Does even a tiny amount of blood make a woman niddah?', [
    'Even a minuscule amount of blood coming from the uterus causes the niddah state, regardless of whether it is moist or dry—even if there was no sensation of menstrual bleeding or opening of the uterus accompanying the appearance of blood.']),
  ('What is a hargasha?', [
    'Feeling the womb open to expel blood or feeling blood flow from the womb into the vagina are considered hargasha. On the other hand, it is halachically questionable if feeling blood flow in the vaginal corridor qualifies as a hargasha.',
    'Note that many poskim hold it is doubtful if women, nowadays, can accurately discern a hargasha as halachically defined.']),
  ('Which colors on an examination cloth are pure, and which are impure?', [
    'Pure colors include:', ['White', 'Yellow', 'Blue', 'Green'],
    'Impure colors include:', ['Red, as well as any shade of red whether light, dark or deep', 'Pink',
     'Any shade of black, which is assumed to have been red which oxidized and therefore changed color',
     'Any shade of brown must be shown to an orthodox Rabbi expert in these laws']]),
  ('May a woman attend synagogue during menstruation?', [
    'During menstruation, it is customary for women to refrain from attending synagogue, looking at a sefer Torah or praying while standing in close proximity to friends. This custom is in the category of additional purity, not based on prohibition.',
    'At home, however, even during menstruation, women may pray, make kiddush and say all the blessings.']),
]),
'source-of-niddah': dict(approved=True, items=[
  ('Does the niddah state apply before marriage?', [
    'The other prohibitions associated with niddah, including kissing, hugging, and affectionate contact, also apply to an unmarried woman, since an unmarried woman has never left her niddah state by immersing in a mikveh.',
    'There is no minimum age for a woman to become niddah. Even a girl who has begun menstruating is in a constant niddah state until she immerses herself in a mikveh for the first time before her wedding.']),
  ('Does blood found on an examination cloth make a woman niddah?', [
    'If the wife performs an internal examination using a cloth which was previously checked to be clean and discovers a stain of any size, she enters the niddah state, even if she felt no menstrual sensation.']),
  ('What if blood is noticed after urinating?', [
    'If she notices blood after urinating, an orthodox Rabbi who is knowledgable in these matters should be consulted.',
    'Facts which might influence his decision include: whether the blood was found in the water or on the seat, if she sat over the middle of the toilet seat or on its edge, if this is a one time experience or it repeats itself, if she felt pain or burning during urination, and if she ate some red food, such as beets, prior to this.']),
]),
'gynecological-considerations': dict(approved=True, items=[
  ('Does a gynecological examination make a woman niddah?', [
    'An examination using the fingers only does not render the niddah state and she is not required to examine herself following such an examination.',
    'Examining the vagina, even using an instrument, does not render the niddah state. A standard gynecological examination does not penetrate the womb or cervix.',
    'If blood is found following these, an orthodox Rabbi knowledgable in these matters must be consulted.']),
  ('Does a transvaginal ultrasound cause niddah?', [
    'A transvaginal ultrasound does not penetrate the cervix and therefore does not cause niddah.']),
  ('Does inserting or removing an IUD make a woman niddah?', [
    'Insertion or removal of an intrauterine contraceptive device, IUD, renders the niddah state. An orthodox Rabbi who is knowledgable in these matters should be consulted regarding spotting.']),
  ('Which gynecological procedures cause niddah?', [
    'Bleeding caused by scraping the inside of the cervix; an endometrial biopsy; a hysterogram or hysterosalpingogram (HSG); a hysteroscopy; a foley bulb (induction for birth) cause niddah.',
    'In light of the above, it is advisable to arrange such procedures at a time when the woman is already a niddah. If this is not possible, an orthodox Rabbi should be consulted.']),
]),
'stains': dict(approved=True, items=[
  ('Does a stain (kesem) make a woman niddah?', [
    'The impurity brought about by finding stains is rabbinic in origin. The Rabbis limited their ruling, however, by stipulating that the following three conditions must be met in order for such a stain to render a woman niddah:',
    ['Its surface area must be at least a circle 11⁄16 of an inch in diameter (17 mm.), the size of a U.S. dime.',
     'It must be found on a white surface.',
     'The object on which it is found can “receive spiritual impurity” (mekabel tumah).'],
    'Even if all three conditions exist, a stain may still be dismissed due to other extraneous reasons, for example, a cut or the wife’s handling of dyes. In all these cases, an orthodox Rabbi expert in these laws should be consulted.']),
  ('Should a woman examine herself internally after finding a stain?', [
    'A stain can sometimes be dismissed as coming from some external source, e.g., a cut on the husband’s body, child’s crayon, etc. This is not the case with blood discovered through an internal examination. Therefore, a woman who found a stain on her body, undergarments, sheets, etc. should not perform an internal examination so as not to exclude the possibility of a favorable halachic ruling.',
    'A clean internal examination performed following the discovery of a stain does not nullify the stain.']),
  ('Who should show a stain to the rabbi?', [
    'If a stain is found, the couple should not be embarrassed.',
    'There is no preference in halacha as to who should approach the Rabbi. Each couple decides for itself. Many couples find it easier for the husband to do this.',
    'If, in spite of the above, neither of the couple feels up to approaching the Rabbi, or if they live far away and cannot, there is an alternative method. An envelope marked with an identifying symbol or sign containing the examination cloth or garment in question can be sent to the Rabbi, followed by a discreet telephone call.']),
  ('Do the laws of stains apply during pregnancy, nursing or after menopause?', [
    'The laws of staining apply to post-menopausal, pregnant, and nursing women as well.']),
]),
'making-sure-menstruation-has-finished': dict(approved=True, items=[
  ('What is a hefsek tahara?', [
    'To ascertain the complete cessation of any bleeding, the wife who is a niddah performs an internal examination called a hefsek tahara. This is an indispensable prerequisite to counting the seven white days (as explained in Chapter Six).']),
  ('When is the earliest day for the hefsek tahara?', [
    'The hefsek tahara can only be performed from at least the fifth day after she enters the niddah state.',
    'The sages therefore required this five day time barrier to ensure that any vestige of semen from the husband has had time to “spoil,” thereby losing its capability of invalidating the seven white day period. This requirement holds even if there was no possibility of marital relations, for example, the husband was elsewhere.']),
  ('What if the hefsek tahara was not done?', [
    'Even more than that—missing the hefsek tahara invalidates her immersion. Even if she was sure that there remained no signs of her impurity, the seven white day period passed, she washed as required and immersed in the mikveh, nonetheless if she hasn’t performed the hefsek tahara, her immersion is invalid and it is as if she didn’t immerse.']),
  ('Should the hefsek tahara be delayed for convenience?', [
    'The time she performs the hefsek tahara should not be played with. She should not make calculations which day is most convenient or inconvenient for her to go to the mikveh and adjust her performing the hefsek tahara accordingly.',
    'Halachic exceptions to this should be according to the directions of an orthodox Rabbi expert in these laws.']),
]),
'seven-white-days': dict(approved=True, items=[
  ('What are the seven white days (shiva nekiim)?', [
    'After the hefsek tahara, a woman waits seven days before going to the mikveh. During this time, she checks herself and her underwear twice daily.',
    'To make sure these days are completely void of any uterine bleeding, the Talmudic Rabbis required a woman during these days to perform internal examinations twice daily, wear white underwear and sleep on white sheets. Hence the name seven white days.']),
  ('When do the seven white days begin?', [
    'The seven white day period normally begins the day following the hefsek tahara. If the hefsek tahara was on Thursday afternoon then Friday is the first day of the seven white days. The following Thursday is the seventh day and Thursday night is the immersion in the mikveh.']),
  ('Must the bed sheets be white during the seven white days?', [
    'During the seven white day period, she must wear white underwear pre-checked for stains (kesomim).',
    'Commencing from the night of the hefsek tahara and until the end of the seven days, the wife’s bed sheets must be white and checked for any stains. The blankets and pillow covers need not be white. It is sufficient for them to be clean and checked for stains.']),
  ('Why are the first three days stricter?', [
    'Finding a stain on one of the first three days is stricter than the other days and cannot be readily dismissed as originating from an external source. However a stain smaller than the minimum size is pure even during the first three days.']),
]),
'preparing-for-immersion': dict(approved=True, items=[
  ('What is hafifah?', [
    'Before immersing in the mikvah, a wife prepares her entire body and hair through a process called hafifah — ensuring that nothing intervenes between her and the mikvah water.',
    'Hafifah encompasses the entire preparation: bathing, shampooing and combing the hair, trimming and cleaning the nails, brushing and flossing the teeth, removing all jewelry and makeup, and carefully checking the body for any intervening substance.']),
  ('What counts as an intervening substance (chatzitzah)?', [
    'Furthermore, there must not be any intervening issues, such as dirt, dry dough, knotted hair, lice, tangled hair, jewelry, or bandages during immersion.',
    'Skin: Bandages and adhesives removed; medicinal creams washed off. Dry scabs softened and removed unless painful. Calluses, warts, pacemakers, and subcutaneous bruises do not intervene.']),
  ('Must nail polish be removed before the mikvah?', [
    'Nails: Trimmed and cleaned. Nail polish should preferably be removed; if they can not be removed and are fully intact and irremovable, immersion is not postponed. Chipped polish must be removed.']),
  ('When should hafifah be done?', [
    'Ideally, hafifah begins before sunset and continues until just before immersion — approximately half an hour. When necessary, it may be performed entirely during the day or entirely at night, allowing at least an hour in the latter case.']),
  ('What should be avoided on the day of immersion?', [
    'From the morning preceding immersion, foods that lodge between the teeth — meat, corn, oranges — should be avoided. Contact with sticky substances such as dough or wax should also be avoided throughout the day. Nothing should be eaten between hafifah and immersion.']),
]),
'times-chabad': dict(approved=True, items=[
  ('What are separation dates (vestos)?', [
    'Based on the above verse, the Talmudic sages, of blessed memory, established a requirement that the husband and wife separate on the date(s) when the next menstrual period can be expected to appear.']),
  ('What are the three separation dates?', [
    'These must be recorded and all three observed: the Monthly Cycle, the Average Cycle (30 days) and the Interval Cycle.',
    ['The lunar cycle affects menstruation by influencing it to begin each time on the same date of the Hebrew (lunar) month. This is called the Monthly Cycle.',
     'Another factor is that on the average for most women, the menstrual period commences on a regular thirty day cycle. This is called the Average Cycle.',
     'This third possibility is the time interval from the end of one sighting of menstruation (hefsek tahara) until the beginning of the next.']]),
  ('How long is the separation on a separation date?', [
    'In both the Monthly and Interval Cycles separation is observed for a half day period. A half day is considered to be from either sunset to sunrise or sunrise to sunset of the projected date.',
    'In the Average Cycle separation is required to last a full day. (The Hebrew day begins at one sunset and ends at the next).']),
  ('What is not permitted on a separation date?', [
    'This includes marital relations, kissing, hugging, affectionate touching and sleeping in the same bed. The other restrictions observed during actual menstruation do not apply.']),
]),
'times-major-customs': dict(approved=True, items=[
  ('What are separation dates (vestos)?', [
    'Based on this verse, the Talmudic sages established a requirement that the husband and wife separate on the date(s) when the next menstrual period can be expected to appear.']),
  ('What are the three separation dates?', [
    'These must be recorded and all three observed: the Monthly Cycle, the Average Cycle (30 /31 days) and the Interval Cycle.',
    ['The lunar cycle affects menstruation by influencing it to begin each time on the same date of the Hebrew (lunar) month. This is called the Monthly Cycle.',
     'Another factor is that on the average for most women, the menstrual period commences on a regular thirty day cycle. This is called the Average Cycle.',
     'This third possibility is the time interval from one sighting of menstruation until the beginning of the next.']]),
  ('How long is the separation on a separation date?', [
    'In both the Monthly and Interval Cycles separation is observed for a half day period. A half day is considered to be from either sunset to sunrise or sunrise to sunset of the projected date.',
    'In the Average Cycle separation is required to last a full day. (The Hebrew day begins at one sunset and ends at the next).',
    'The custom in many communities is to separate on the entire thirty first day, as well.']),
  ('What is not permitted on a separation date?', [
    'This includes marital relations, kissing, hugging, affectionate touching and sleeping in the same bed. The other restrictions observed during actual menstruation do not apply.']),
]),
'perfect-marriage': dict(approved=True, items=[
  ('What is the Torah view of marriage?', [
    'Like all things so too is marriage comprised of two parts—body and soul.',
    'The body requires a vitalizing force, a spirit to enliven it. This cannot be legislated. It develops along with and to a degree due to the body of marriage. This is the emotional bond created between husband and wife.']),
  ('How should husband and wife treat each other, according to the Rambam?', [
    '“The Talmudic sages commanded: The husband is to honor and love his wife more than himself.',
    'Similarly, they commanded: The wife should honor her husband, even to the point of feeling awe towards him.',
    'It is important to emphasize that respect is a two-way street.']),
  ('Is there such a thing as a perfect marriage?', [
    'By definition, there is no perfect marriage. Perfection is without flaw. It even suggests effortlessness. Marriage is not this.',
    'The key to a harmonious and wholesome marriage lies in the couple’s realization that they must satisfy one another’s spiritual, emotional, and personal needs.']),
]),
'from-the-rebbe': dict(approved=True, items=[
  ('What did the Rebbe write about family purity and fertility?', [
    'It is known that the blessing for fertility lies in keeping the laws of family purity. Therefore, it is fitting for you to be exacting in your observance of these laws.']),
  ('What did the Rebbe write about family purity and the health of children?', [
    'Living in accordance with the laws of family purity a husband and wife merit happy, healthy children—healthy in body and soul, following the Torah’s ways, bringing true joy and pride to their parents.']),
  ('Which three mitzvos were given especially to Jewish women?', [
    'These three main commandments were given specifically to Jewish women—Shabbos and Yom Tov candle lighting, challah (kosher food), and family purity.']),
]),
}
