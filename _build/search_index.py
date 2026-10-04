"""Build assets/search-index.json from the online chapters (run after render.py / overview.py)."""
import re, html, json, os
SITE=os.path.expanduser('~/Documents/FamilyPurity')
ORDER=['overview','from-the-rebbe','perfect-marriage','niddah','source-of-niddah','gynecological-considerations','stains',
       'making-sure-menstruation-has-finished','seven-white-days','times-chabad','times-major-customs']
clean=lambda s: re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>','',s))).strip()
out=[]
for slug in ORDER:
    h=open(f'{SITE}/read/{slug}.html').read()
    num=clean(re.search(r'<p class="num">(.*?)</p>',h,re.S).group(1))
    title=clean(re.search(r'<header class="opener">.*?<h1>(.*?)</h1>',h,re.S).group(1))
    sub=re.search(r'<p class="opener-sub">(.*?)</p>',h,re.S)
    if sub: title+=' · '+clean(sub.group(1))
    art=h[h.find('<article'):h.find('</article>')]
    art=re.sub(r'<figure class="cal".*?</figure>','',art,flags=re.S)
    notes=[clean(n) for n in re.findall(r'<small class="sn"><b>\d+</b>(.*?)</small>',art,re.S)]
    body=re.sub(r'<label class="fn"[^>]*>\d+</label><input[^>]*><small class="sn">.*?</small>','',art,flags=re.S)
    paras=[]
    for tag,txt in re.findall(r'<(h2|h3|p|li|blockquote)[^>]*>(.*?)</\1>',body,re.S):
        t=clean(txt)
        if t and not (tag=='p' and t in [p for _,p in paras]): paras.append(('h' if tag in('h2','h3') else 'p',t))
    out.append({'slug':slug,'num':num,'title':title,'paras':[p for k,p in paras if k=='p'],'heads':[p for k,p in paras if k=='h'],'notes':notes})
json.dump(out,open(f'{SITE}/assets/search-index.json','w'),ensure_ascii=False,separators=(',',':'))
print(len(out),'chapters,',sum(len(c['paras']) for c in out),'paragraphs,',sum(len(c['notes']) for c in out),'footnotes,',os.path.getsize(f'{SITE}/assets/search-index.json')//1024,'KB')
