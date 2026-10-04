"""Build structured blocks from PDFKit run dumps, then render reader pages.
usage: python3 build.py outline <name> | python3 build.py render"""
import json, re, sys, collections, html, os

SP=os.path.dirname(os.path.abspath(__file__))
SITE=os.path.expanduser('~/Documents/FamilyPurity')

def italic(f): return any(k in f for k in ('Italic','Oblique','Inclined'))

def lines_of(runs):
    lines=[]; cur=[]; page=None
    for r in runs:
        if page is not None and r['p']!=page and cur: lines.append((page,cur)); cur=[]
        page=r['p']
        parts=r['t'].split('\n')
        for i,part in enumerate(parts):
            if part: cur.append({'t':part,'f':r['f'],'s':round(r['s'],1)})
            if i<len(parts)-1: lines.append((page,cur)); cur=[]
    if cur: lines.append((page,cur))
    return [(p,l) for p,l in lines if ''.join(s['t'] for s in l).strip()]


def lines_geo(name):
    """Visual lines in reading order (top to bottom, left to right), from the position dump."""
    sel=json.load(open(f'{SP}/lines/{name}.json'))
    out=[]
    for page in sorted({x['p'] for x in sel}):
        items=sorted([x for x in sel if x['p']==page],key=lambda x:(-x['y'],x['x']))
        groups=[]
        for it in items:
            if groups and abs(groups[-1][0]['y']-it['y'])<=2.5: groups[-1].append(it)
            else: groups.append([it])
        for g in groups:
            g.sort(key=lambda x:x['x']); segs=[]; prev_end=None
            for it in g:
                first=True
                for r in it['runs']:
                    t=r['t'].replace('\n',' ').replace('\r',' ')
                    if not t: continue
                    if first and segs and prev_end is not None and it['x']-prev_end>2 and not segs[-1]['t'].endswith(' ') and not re.match(r'^[\s\.,;:!?\)”’]',t):
                        t=' '+t
                    first=False
                    segs.append({'t':t,'f':r['f'],'s':round(r['s'],1)})
                prev_end=it['x']+it.get('w',0)
            if segs and segs[-1]['t'].endswith(' '): segs[-1]['t']=segs[-1]['t'].rstrip()
            if segs: segs[0]['x']=g[0]['x']
            if ''.join(x['t'] for x in segs).strip(): out.append((page,segs))
    return out

T=lambda l:''.join(s['t'] for s in l)
def dom(l):
    c=collections.Counter()
    for s in l: c[(s['f'],s['s'])]+=len(s['t'].strip()) or 0.1
    return c.most_common(1)[0][0]

FN_RE=re.compile(r'^(\d+)\.?\s+(\S.*)$')

def blocks_for(name, cfg):
    L=lines_geo(name) if os.path.exists(f'{SP}/lines/{name}.json') else lines_of(json.load(open(f'{SP}/runs/{name}.json')))
    pages_skip=set(cfg.get('skip_pages',[]))
    L=[(p,l) for p,l in L if p not in pages_skip]
    # footnote size: most common non-Palatino size among lines that look like "N text"
    fc=collections.Counter()
    for p,l in L:
        f,s=dom(l)
        if FN_RE.match(T(l).strip()) and 'Palatino' not in f and 'Corsiva' not in f: fc[s]+=1
    sizes=collections.Counter()
    for p,l in L:
        for sg in l:
            if 'Palatino' in sg['f'] or 'Corsiva' in sg['f']: continue
            sizes[sg['s']]+=len(sg['t'])
    fnsize=cfg.get('fnsize') or (fc.most_common(1)[0][0] if fc else None)
    body=cfg.get('body') or next(s for s,_ in sizes.most_common() if s!=fnsize)
    blens=sorted(len(T(l)) for p,l in L if dom(l)[1]==body)
    maxlen=blens[int(len(blens)*0.9)] if blens else 90
    diag_sizes=set(cfg.get('diagram_sizes',[]))
    marg={}
    for par in (0,1):
        xs=collections.Counter(round(l[0].get('x',-1)) for p,l in L if p%2==par and dom(l)[1]==body and 'x' in l[0])
        if xs: marg[par]=xs.most_common(1)[0][0]

    blocks=[]; para=[]; fns={}; cur_fn=None; last_fn=0; last_page=None; diag_on_page=set()
    def flush():
        nonlocal para
        if para: blocks.append({'type':'p','lines':para}); para=[]
    for idx,(p,l) in enumerate(L):
        t=T(l).strip(); f,s=dom(l)
        if p!=last_page: cur_fn=None; last_page=p
        nxt=L[idx+1][0] if idx+1<len(L) else None
        if re.fullmatch(r'\d{1,3}',t) and (s!=body or 'Corsiva' in f or nxt!=p): continue          # page numbers
        if 'Corsiva' in f: continue
        if t in ('k','n','!','l') and f.startswith('Helvetica'): continue
        if 'Dingbat' in f: continue
        if len(t)<=2 and s>12 and not t.isdigit(): flush(); blocks.append({'type':'orn'}); continue              # ornament glyphs
        if any(k in t for k in cfg.get('drop_lines',[])): continue
        if t in cfg.get('drop_exact',[]): continue
        if 'Palatino-Roman' in f and s<10 and p>1 and re.search(r'FAMILY PURITY|CHAPTER|RABBI|REBBE',t.upper()): continue
        if 'Palatino' in f and s>=15: flush(); blocks.append({'type':'orn'}); continue                             # chapter title (from config)
        if s in diag_sizes or f.startswith('HelveticaNeue') or (cfg.get('diagram_bold') and f=='Helvetica-Bold'):
            flush()
            if p not in diag_on_page: blocks.append({'type':'diagram','page':p}); diag_on_page.add(p)
            continue
        if 'Palatino-Bold' in f or ('Palatino' in f and cfg.get('palatino_headings')):
            # run-in heading if the line also carries body text
            lead=[]; rest=[]
            for sg in l:
                (lead if ('Palatino' in sg['f'] and not rest) else rest).append(sg)
            head=re.sub(r'\s+',' ',T(lead)).strip(' .')
            if rest and T(rest).strip():
                flush(); para=[[{'t':head,'f':'RUNIN','s':body}]+rest]; continue
            flush(); blocks.append({'type':'h2','text':head}); continue
        m=FN_RE.match(t)
        starts=bool(m) and last_fn<int(m.group(1))<=last_fn+3 and (s==fnsize or cfg.get('fn_any_size') or cur_fn)
        if starts:
            # keep the paragraph open: it may continue on the next page after these footnotes
            cur_fn=int(m.group(1)); last_fn=cur_fn
            lead_ws=len(T(l))-len(T(l).lstrip()); strip=lead_ws+len(t)-len(m.group(2)); acc=0; out=[]
            for sg in l:
                sg=dict(sg); n=len(sg['t'])
                if acc+n<=strip: acc+=n; continue
                if acc<strip: sg['t']=sg['t'][strip-acc:]
                acc+=n; out.append(sg)
            fns[cur_fn]=[out]; continue
        if cur_fn:
            fns[cur_fn].append(l); continue
        if t.startswith('—') or t.startswith('– '):
            # citation: the preceding run of same-style lines is a quote
            style=dom(para[-1]) if para else None
            q=[]
            while para and dom(para[-1])==style: q.insert(0,para.pop())
            if not q or True:
                while blocks and blocks[-1]['type']=='p' and len(blocks[-1]['lines'])<=2 and style and dom(blocks[-1]['lines'][-1])==style and len(blocks)>=2 and blocks[-2]['type'] in ('orn','quote'):
                    q=blocks.pop()['lines']+q
            flush()
            cite=re.sub(r'^[—–]\s*','',t); cite=re.sub(r'\bT (?=[a-z])','T',cite)
            if re.fullmatch(r'(\S ){3,}\S.*',cite): cite=re.sub(r'(?<=[A-Za-z]) ?(?=\d)',' ',cite.replace(' ',''))
            blocks.append({'type':'quote','lines':q,'cite':cite}); continue
        if ('BoldItalic' in f or 'Bold-Italic' in f) and len(t)<70 and s>=body*0.95 and not re.search(r'[\.,;]$',t):
            flush(); blocks.append({'type':'h3','text':t}); continue
        if t.startswith('•'): flush()
        if re.search(r'THE (MONTHLY|AVERAGE|INTERVAL) CYCLE',t) and re.search(r'[\u0590-\u05FF]',t): flush()
        # body line: paragraph break heuristics
        prevl = para[-1] if para else None
        dx = (l[0]['x']-prevl[0]['x']) if (prevl and 'x' in l[0] and 'x' in prevl[0]) else 0
        ind = (l[0]['x']-marg[p%2]) if ('x' in l[0] and (p%2) in marg) else 0
        pind = (prevl[0]['x']-marg[p%2]) if (prevl and 'x' in prevl[0] and (p%2) in marg) else 0
        notbullet = not (para and T(para[0]).lstrip().startswith('•'))
        indented = notbullet and (
            (6<dx<25 and len(T(prevl).rstrip())>=0.7*maxlen) or
            (abs(dx)<=2 and 6<ind<25 and 6<pind<25 and re.search(r'[\.!?”’]$',T(prevl).rstrip())))
        runin = re.match(r'^[A-Z][A-Z0-9&’\'/ -]{2,40}[A-Z] ?\. ',t)
        if para and (indented or runin) and not re.match(r'^[\.,;:!?\)”’]',t):
            flush()
        elif para:
            prev=T(para[-1]).rstrip()
            if not re.match(r'^[\.,;:!?\)”’]',t) and not (l[0]['s']<0.7*body and l[0]['t'].strip().isdigit()) and len(prev)<0.8*maxlen and re.search(r'[\.!?”’:\)]$',prev):
                flush()
        para.append(l)
    flush()
    return blocks,fns,body,fnsize

TERMS_IT=['hefsek tahara','moch dochuk','mikveh','niddah','kesomim','kesamim','bedikah','bedika','tahara','zavah','chupah','kesuva','halacha','halachic','poskim','vestos','veses','onah','Yom Hachodesh','Onah Beinonis','Veses Haflagah','Or Zaruah','seven white days']
SOURCES_IT=['Shulchan Aruch Admur Hazoken','Kitzur Shulchan Aruch','Bodei Hashulchan','Tzemach Tzedek','Tahara Kehalacha','Misgeres Hashulchan','Chavas Da’as','Igros Moshe','Gefen Poriah','Chochmat Hatahara','Kitzur Dinei Tahara','Shiurei Shevet Halevy','Pischei Teshuva','Sidrei Tahara','Mehaber','Ramo','Shach','Taz','Tanya','Likutei Sichos','Igros Kodesh']
GLOSS={'hefsek tahara':'An internal examination before sunset confirming that bleeding has stopped. It can be done from the fifth day.',
 'moch dochuk':'A soft white cloth inserted after the hefsek tahara and removed after nightfall.',
 'mikveh':'A pool of natural water built according to Jewish law, used for immersion.',
 'niddah':'The status of a woman from the start of menstruation until she immerses in a mikveh.',
 'kesomim':'Stains found on the body, clothing or sheets, rather than on an examination cloth.',
 'vestos':'The dates when the next period can be expected, on which a couple separates.',
 'onah':'A half-day: daytime (sunrise to sunset) or nighttime (sunset to sunrise).'}

def seg_html(segs, add_italics=False, sources=False):
    """segments -> html with <em>, run-in heads and footnote tokens kept as \x00FN n\x00"""
    out=[]
    for sg in segs:
        t=html.escape(sg['t'],quote=False)
        if sg['f']=='RUNIN': out.append(f'<strong class="runin">{t}.</strong> '); continue
        if italic(sg['f']) and t.strip(): out.append(f'<em>{t}</em>')
        else: out.append(t)
    h=''.join(out)
    if add_italics:
        words=SOURCES_IT if sources else TERMS_IT
        for w in sorted(words,key=len,reverse=True):
            h=re.sub(r'(?<![\w>/])('+re.escape(w)+r')(?![\w<])',r'<em>\1</em>',h)
        h=re.sub(r'<em>([^<]*)<em>([^<]*)</em>([^<]*)</em>',r'<em>\1\2\3</em>',h)
    return h

def join_lines(lines, body, add_italics, sources=False):
    parts=[]
    for l in lines:
        segs=[]
        for k,sg in enumerate(l):
            nb=(l[k+1]['t'] if k+1<len(l) else '')+(l[k-1]['t'][-1:] if k else '')
            if sg['f']!='RUNIN' and re.fullmatch(r'\s*\d{1,3}\s*',sg['t']) and sg['s']<0.7*body and '⁄' not in nb:
                segs.append({'t':f"\x00FN{sg['t'].strip()}\x00",'f':'','s':body})
            else: segs.append(sg)
        h=seg_html(segs,add_italics,sources).strip()
        if not parts: parts.append(h); continue
        prev=parts[-1]
        if re.search(r'[a-z]-$',prev) and re.match(r'^[a-z]',h): parts[-1]=prev[:-1]+h
        elif re.match(r'^(<em>)?[\.,;:!?\)”’]',h) or prev.endswith('\x00'): parts[-1]=prev+(' ' if prev.endswith('\x00') and not re.match(r'^(<em>)?[\.,;:!?\)”’]',h) else '')+h
        else: parts[-1]=prev+' '+h
    s=parts[0] if parts else ''
    s=re.sub(r'^(<strong class="runin">[^<]*</strong> )?([B-HJ-Z]) ([a-z])',r'\1\2\3',s)  # "T o make" -> "To make"
    s=re.sub(r'</em>(\s*)<em>',r'\1',s)
    s=re.sub(r'\bT (?=[a-z])','T',s)
    s=re.sub(r'^((?:<[^>]+>)*)([B-HJ-Z]) ([a-z])',r'\1\2\3',s)
    s=re.sub(r'(?<=[A-Za-z])- (?=[a-z])','-',s)
    s=re.sub(r'^((?:<[^>]+>)*)"\s*',r'\1',s)
    s=re.sub(r'^([A-Z][A-Z0-9&’\'/ -]{1,40}[A-Z]) \. ',lambda m:f'<strong class="runin">{title_case(m.group(1))}.</strong> ',s)
    return s

def assign_glued_markers(texts, nmax):
    """Find markers glued to words ("womb1") in reading order for numbers not already tokenised."""
    have=set()
    for t in texts: have|={int(x) for x in re.findall(r'\x00FN(\d+)\x00',t)}
    pos=(0,0)
    for n in range(1,nmax+1):
        if n in have:
            # advance position past existing token
            for i in range(pos[0],len(texts)):
                j=texts[i].find(f'\x00FN{n}\x00', pos[1] if i==pos[0] else 0)
                if j>=0: pos=(i,j+1); break
            continue
        pat=re.compile(r'(?<=[A-Za-z\.,”’\)\]:;’])'+str(n)+r'(?![\d:])')
        for i in range(pos[0],len(texts)):
            start=pos[1] if i==pos[0] else 0
            m=None
            for mm in pat.finditer(texts[i],start):
                # not inside a tag
                if texts[i].rfind('<',0,mm.start())>texts[i].rfind('>',0,mm.start()): continue
                m=mm; break
            if m:
                texts[i]=texts[i][:m.start()]+f'\x00FN{n}\x00'+texts[i][m.end():]
                pos=(i,m.start()+1); break
    return texts

def glossify(h, used):
    for term,defn in GLOSS.items():
        if term in used: continue
        pat=re.compile(r'(?:<em>)?(?<![\w>])('+re.escape(term)+r')(?![\w])(?:</em>)?')
        for m in pat.finditer(h):
            if h.rfind('<',0,m.start())>h.rfind('>',0,m.start()): continue
            if '<label' in h[max(0,m.start()-200):m.start()] and '</small>' not in h[max(0,m.start()-200):m.start()]: continue
            btn=f'<button class="term" type="button" data-word="{term}" data-def="{html.escape(defn)}">{m.group(1)}</button>'
            h=h[:m.start()]+btn+h[m.end():]; used.add(term); break
    return h

def render_body(blocks, fns, body, cfg):
    add_it=cfg.get('add_italics',False)
    texts=[]
    for b in blocks:
        if b['type']=='p': texts.append(join_lines(b['lines'],body,add_it))
        elif b['type']=='quote': texts.append(join_lines(b['lines'],body,add_it))
        else: texts.append('')
    texts=assign_glued_markers(texts, max(fns) if fns else 0)
    fnhtml={n:join_lines(v,body,add_it,sources=True) for n,v in fns.items()}
    for k,v in cfg.get('fix_fn',{}).items(): fnhtml[int(k)]=v
    TH={'MONTHLY':('The Monthly Cycle','Yom Hachodesh'),'AVERAGE':('The Average Cycle','Onah Beinonis'),'INTERVAL':('The Interval Cycle','Veses Haflagah')}
    for i,t in enumerate(texts):
        if 'CYCLE' in re.sub(r'<[^>]+>','',t[:240]): t=texts[i]=re.sub(r'<[^>]+>','',t[:240])+t[240:]
        m=re.match(r'^.{0,14}?THE (MONTHLY|AVERAGE|INTERVAL) CYCLE.*?(?=The lunar|Another factor|This third|$)',t)
        if m:
            a,b_=TH[m.group(1)]; texts[i]='\x01'+a+'\x02'+b_+'\x03'+t[m.end():]
    out=[]; used=set(); first_p=True
    for b,t in zip(blocks,texts):
        def fnrep(m):
            n=int(m.group(1)); body_=fnhtml.get(n,'').strip()
            if not body_: return ''
            return f'<label class="fn" for="n{n}">{n}</label><input class="fn-t" type="checkbox" id="n{n}"><small class="sn"><b>{n}</b>{body_}</small>'
        if b['type']=='h2': out.append(f'<h2>{html.escape(title_case(b["text"]))}</h2>')
        elif b['type']=='h3': out.append(f'<h3>{html.escape(b["text"])}</h3>')
        elif b['type']=='p':
            for a,z in cfg.get('fix_text',{}).items(): t=t.replace(a,z)
            mh=re.match('\x01(.*?)\x02(.*?)\x03',t)
            if mh: out.append(f'<h3>{mh.group(1)} <span class="he-term">{mh.group(2)}</span></h3>'); t=t[mh.end():]
            t=glossify(t,used) if cfg.get('gloss',True) else t
            t=re.sub('\x00FN(\\d+)\x00',fnrep,t)
            if t.startswith('• '):
                li=f'<li>{t[2:]}</li>'
                if out and out[-1].startswith('<ul>'): out[-1]=out[-1][:-5]+li+'</ul>'
                else: out.append(f'<ul>{li}</ul>')
            else: out.append(f'<p>{t}</p>')
        elif b['type']=='quote':
            t=re.sub('\x00FN(\\d+)\x00',fnrep,t)
            out.append(f'<blockquote class="quote"><p>{t}</p><cite>{html.escape(b["cite"])}</cite></blockquote>')
        elif b['type']=='diagram':
            out.append(cfg.get('diagram_html',''))
    return '\n    '.join(out)

SMALL={'a','an','and','as','at','but','by','for','in','of','on','or','the','to','with','from','which','do','not'}
def title_case(s):
    if not s.isupper() and not re.search(r'[A-Z]{3,}',s): return s
    w=s.lower().split(' ')
    return ' '.join(x if (i and x in SMALL) else (x[:1].upper()+x[1:]) for i,x in enumerate(w)).replace('Pms','PMS')

if __name__=='__main__':
    sys.path.insert(0,SP)
    from pages import PAGES
    if sys.argv[1]=='outline':
        name=sys.argv[2]; cfg=PAGES[name]
        blocks,fns,body,fnsize=blocks_for(name,cfg)
        print('body',body,'fn',fnsize,'footnotes',len(fns),sorted(fns)[:3],'...',sorted(fns)[-3:] if fns else '')
        for b in blocks:
            if b['type'] in('p','quote'): print(b['type'],repr(T(b['lines'][0])[:80]), ('— '+b.get('cite','')) if b['type']=='quote' else '', f"[{len(b['lines'])} lines]")
            else: print(b['type'],b.get('text',b.get('page','')))
