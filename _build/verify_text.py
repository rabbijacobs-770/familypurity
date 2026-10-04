"""Compare every word of each online chapter with its PDF (order-independent word counts)."""
import re,html,collections,json,os,sys
SITE=os.path.expanduser('~/Documents/FamilyPurity')
TXT=sys.argv[1]  # folder of PDF text dumps (one .txt per PDF)
PAGES=[('overview','overview_us_letter'),('from-the-rebbe','ch._from_the_rebbe'),('perfect-marriage','ch._1_-_perfect_marriage'),
 ('niddah','ch._2_-_niddah'),('source-of-niddah','ch._2_-_source_of_niddah'),('gynecological-considerations','ch._2_-_gynecological_'),
 ('stains','ch._3_-_stains'),('making-sure-menstruation-has-finished','ch._5_-_making_sure_menstruation'),('seven-white-days','ch._6_-_seven_white_days'),
 ('times-chabad','times_web_edition_chabad'),('times-major-customs','times_web_edition_major_customs')]
def norm(t):
    t=t.replace('’',"'").replace('‘',"'").replace('“','"').replace('”','"').replace('—',' ').replace('–',' ').replace('­','')
    t=re.sub(r'(\w)-\n(\w)',r'\1\2',t)            # line-break hyphens in the PDF text
    t=re.sub(r'\b(?:[A-Za-z0-9:] ){3,}[A-Za-z0-9]\b',lambda m:m.group(0).replace(' ',''),t)   # spaced-out letters
    t=re.sub(r'\b([B-HJ-Z]) ([a-z]{2,})',r'\1\2',t)  # split capitals from drop caps and kerning
    t=re.sub(r'(?<=[a-z\.,;:"\)])\d{1,3}(?=[\s\.,;:"\)]|$)','',t)   # footnote numbers glued to words
    t=re.sub(r'\bT o\b','To',t); t=re.sub(r'\bW hen\b','When',t); t=re.sub(r'\bT ahara\b','Tahara',t); t=re.sub(r'\bT anhuma\b','Tanhuma',t); t=re.sub(r'\bT eshuva\b','Teshuva',t)
    return re.findall(r"[a-z0-9]+(?:'[a-z]+)?",t.lower())
def online_text(slug):
    h=open(f'{SITE}/read/{slug}.html').read()
    op=h[h.find('<header class="opener">'):h.find('</header>',h.find('<header class="opener">'))]
    art=h[h.find('<article'):h.find('</article>')]
    art=re.sub(r'<figure class="cal".*?</figure>','',art,flags=re.S)
    art=re.sub(r'<label class="fn"[^>]*>\d+</label>','',art)
    art=re.sub(r'<small class="sn"><b>\d+</b>',' ',art)
    t=html.unescape(re.sub(r'<[^>]+>',' ',op+' '+art))
    return t
NOISE=set('family purity rabbi fishel jacobs chapter n k excerpted from a guide to marital fulfillment permission granted reprint and distribute unaltered with credit this pdf is formatted as us letter size for ease of printing questions or requests rabbijacobs familypurity com'.split())
report=[]
for slug,pdf in PAGES:
    raw=open(f'{TXT}/{pdf}.txt').read()
    raw=re.sub(r'=== PAGE \d+ ===','\n',raw)
    A=collections.Counter(norm(raw)); B=collections.Counter(norm(online_text(slug)))
    missing=A-B; extra=B-A
    # running headers, page numbers and print notices are expected to be gone online
    missing={w:c for w,c in missing.items() if not (w in NOISE or w.isdigit())}
    extra={w:c for w,c in extra.items() if not w.isdigit()}
    total=sum(A.values()); same=sum((A&B).values())
    report.append({'slug':slug,'pdf':pdf,'pdf_words':total,'matched':same,'missing':missing,'extra':extra})
    print(f"{slug:32} PDF words {total:5}  matched {same/total:6.1%}  missing {sum(missing.values()):3} {dict(sorted(missing.items(),key=lambda x:-x[1])[:12])}")
    print(f"{'':32} extra online {sum(extra.values()):3} {dict(sorted(extra.items(),key=lambda x:-x[1])[:12])}")
json.dump(report,open(f'{SITE}/review/text-check.json','w'),ensure_ascii=False,indent=1)
