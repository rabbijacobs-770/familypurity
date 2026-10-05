"""Read a Nisus/Word RTF chapter into paragraphs + footnotes, accepting tracked changes.
paragraphs: [{'style': name, 'runs': [{'t','i','b'} | {'fn': n}]}], footnotes: {n: runs}, images: [(position, kind, bytes)]"""
import re, sys, binascii

SKIP_DEST={'fonttbl','colortbl','stylesheet','info','listtable','listoverridetable','header','footer','headerl','headerr','headerf',
           'footerl','footerr','footerf','revtbl','rsidtbl','generator','xmlnstbl','themedata','colorschememapping','latentstyles',
           'datastore','pgdsctbl','filetbl','objdata','objclass','objname','nonshppict','fldinst','xe','txe','tc','tcn','sp','sn','sv','picprop','bkmkstart','bkmkend','listtext','pntext','pntxtb','pntxta'}
SYMBOLS={'ldblquote':'“','rdblquote':'”','lquote':'‘','rquote':'’','emdash':'—','endash':'–','bullet':'•','tab':'\t','line':'\n',
         'emspace':' ','enspace':' ','qmspace':' ','~':'\u00a0','-':'\u00ad','_':'\u2011'}

def styles_of(src):
    names={}
    i=src.find('{\\stylesheet')
    if i<0: return names
    d=0
    for j in range(i,len(src)):
        if src[j]=='{': d+=1
        elif src[j]=='}':
            d-=1
            if d==0: break
    for m in re.finditer(r'\{(?:\\\*)?\\(s|cs)(\d+)[^;{}]*?\s([A-Za-z][^;\\{}]*);',src[i:j]):
        names[(m.group(1),int(m.group(2)))]=m.group(3).strip()
    return names

def read(path):
    src=open(path,'rb').read().decode('latin-1')
    names=styles_of(src)
    tok=re.compile(r"\\([a-zA-Z]+)(-?\d+)? ?|\\'([0-9a-fA-F]{2})|\\(.)|([{}])|([^\\{}\r\n]+)|[\r\n]+",re.S)
    stack=[]
    st={'i':False,'b':False,'skip':False,'del':False,'hid':False,'fn':None,'pstyle':112,'uc':1,'pict':None,'super':False}
    paras=[]; foot={}; cur=[]; fncur=None; fnum=0; skipn=0; images=[]; pict_hex=None
    def emit(t):
        nonlocal skipn
        if skipn:  # unicode fallback characters
            n=min(skipn,len(t)); t=t[n:]; skipn-=n
            if not t: return
        if st['skip'] or st['del'] or st['hid']: return
        if st['pict'] is not None: st['pict'].append(t); return
        target=foot[st['fn']] if st['fn'] is not None else cur
        if target and 't' in target[-1] and target[-1]['i']==st['i'] and target[-1]['b']==st['b']:
            target[-1]['t']+=t
        else: target.append({'t':t,'i':st['i'],'b':st['b']})
    def end_para():
        nonlocal cur
        if st['fn'] is not None:
            foot[st['fn']].append({'t':'\n','i':False,'b':False}); return
        paras.append({'style':names.get(('s',st['pstyle']),str(st['pstyle'])),'runs':cur}); cur=[]
    pos=0; dest_next=False
    for m in tok.finditer(src):
        word,arg,hexc,sym,brace,text=m.groups()
        if brace=='{':
            stack.append(dict(st)); dest_next=False; continue
        if brace=='}':
            if st['pict'] is not None and (not stack or stack[-1]['pict'] is None):
                hx=re.sub(r'[^0-9a-fA-F]','',''.join(st['pict']))
                if not (st['skip'] or st['del'] or st['hid']):
                    images.append((len(paras),st.get('pictkind','?'),binascii.unhexlify(hx[:len(hx)//2*2])))
                    (foot[st['fn']] if st['fn'] is not None else cur).append({'img':len(images)})
            closing_fn = st['fn'] is not None and (not stack or stack[-1]['fn']!=st['fn'])
            if stack: st=stack.pop()
            if closing_fn:  # strip trailing paragraph mark inside the footnote
                r=foot[fnum]
                while r and 't' in r[-1] and r[-1]['t'].strip()=='' : r.pop()
            continue
        if hexc:
            emit(bytes([int(hexc,16)]).decode('mac_roman')); continue
        if sym:
            if sym=='*': st['skip_star']=True; dest_next=True; continue
            if sym in SYMBOLS: emit(SYMBOLS[sym]); continue
            if sym in '\\{}': emit(sym); continue
            continue
        if text is not None:
            if text: emit(text)
            continue
        if word is None: continue
        w=word; a=int(arg) if arg is not None else None
        if w in SKIP_DEST or (st.get('skip_star') and dest_next and w not in ('footnote','shppict')):
            st['skip']=True; dest_next=False; continue
        dest_next=False
        if w=='footnote':
            fnum+=1; foot[fnum]=[]
            if not st['del']:
                cur.append({'fn':fnum})
            st['fn']=fnum; st['i']=False; st['b']=False; continue
        if w=='chftn': continue
        if w=='deleted': st['del']=True; continue
        if w=='pict': st['pict']=[]; continue
        if w in('pngblip','jpegblip','macpict','emfblip','wmetafile','pmmetafile','dibitmap','wbitmap'): st['pictkind']=w; continue
        if w=='v': st['hid']=(a!=0); continue
        if w=='i': st['i']=(a!=0); continue
        if w=='b': st['b']=(a!=0); continue
        if w=='plain': st['i']=False; st['b']=False; continue
        if w=='pard': st['pstyle']=112; continue
        if w=='s' and a is not None: st['pstyle']=a; continue
        if w=='uc': st['uc']=a or 0; continue
        if w=='u':
            emit(chr(a if a>=0 else a+65536)); skipn=st['uc']; continue
        if w=='par': end_para(); continue
        if w in SYMBOLS: emit(SYMBOLS[w]); continue
    if cur: paras.append({'style':names.get(('s',st['pstyle']),str(st['pstyle'])),'runs':cur})
    # normalise footnotes: join, drop leading auto-number dot/space
    for n,r in foot.items():
        while r and 't' in r[0] and r[0]['t'].strip(' .\u00a0\t?')=='' : r.pop(0)
        if r and 't' in r[0]: r[0]['t']=re.sub(r'^[\s.\u00a0?]+','',r[0]['t'])
    return paras,foot,images

if __name__=='__main__':
    paras,foot,images=read(sys.argv[1])
    print(len(paras),'paragraphs',len(foot),'footnotes',len(images),'images')
    for p in paras[:int(sys.argv[2]) if len(sys.argv)>2 else 60]:
        t=''.join(r.get('t','') if 't' in r else f"[{r['fn']}]" for r in p['runs']).strip()
        if t: print(f"{p['style'][:22]:22} | {t[:110]}")
