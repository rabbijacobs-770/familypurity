"""Build an online chapter from the author's Nisus RTF (expanded-edition chapters).
The RTF stays in review/sources (not in the public repo): it carries tracked changes; only the final wording is used.
Usage: python3 _build/rtf_chapter.py   (writes read/preparing-for-immersion.html and images/ch7/*.png)"""
import html, re, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rtf_read import read
from render import page
import build
from build import SITE, glossify

build.GLOSS = dict(build.GLOSS,
    mikvah='A pool of natural water built according to Jewish law, used for immersion.',
    hafifah='The full preparation of the body and hair before immersion, so that nothing intervenes between her and the water.')

CHAPTERS = {
 'preparing-for-immersion': dict(
    src='review/sources/ch7-preparing-for-immersion.rtf', num='Chapter 7', title='Preparing for Immersion', img_dir='images/ch7',
    desc='Chapter 7 of Family Purity by Rabbi Fishel Jacobs, from the forthcoming expanded edition: how to prepare for immersion in the mikvah (hafifah), with every source.',
    seo='Preparing for Immersion in the Mikvah (Hafifah)',
    alts=['Diagram: the seventh of the seven white days. Ideally, preparations last from before sunset until after nightfall.',
          'Diagram of hafifah one day before immersion: the second night of a two-day Yom Tov; motzei Shabbos that is Yom Tov; Friday night when Friday is Yom Tov.',
          'Diagram of hafifah on Friday or a weekday, and again just before immersion on the night after Shabbos or Yom Tov.',
          'Diagram of hafifah three days before immersion, and again just before immersion: Wednesday before two days of Yom Tov and Shabbos; Friday before Shabbos and two days of Yom Tov.']),
}

def runs_html(runs, fnmap, italics=True):
    out = []
    for r in runs:
        if 'fn' in r: out.append('\x00FN%d\x00' % fnmap[r['fn']])
        elif 't' in r:
            t = html.escape(r['t'], quote=False)
            if italics and r['i'] and t.strip():
                m = re.match(r'^(\s*)(.*?)(\s*)$', t, re.S); out.append(f'{m[1]}<em>{m[2]}</em>{m[3]}')
            else: out.append(t)
    h = ''.join(out)
    h = re.sub(r'</em>(\s*)<em>', r'\1', h)
    h = re.sub(r'(?<![\w>;])(\w)<em>(?=\w)', r'<em>\1', h)   # "c<em>hatzitza</em>" -> one word
    h = re.sub(r'[ \t ]*\n[ \t ]*', '\n', h).replace('\t', ' ')
    h = re.sub(r' {2,}', ' ', h)
    return h.strip()

def split_runin(runs):
    """Leading bold words ending in a period ("Wording .") -> (head runs, rest runs)."""
    i = 0
    while i < len(runs) and 't' in runs[i] and not runs[i]['t'].strip(): i += 1
    if i >= len(runs) or 't' not in runs[i] or not runs[i]['b']: return None, runs
    head = []
    while i < len(runs):
        r = runs[i]
        if 'fn' in r: head.append(r); i += 1; continue
        if 't' in r and r['b']:
            head.append(r); i += 1
            if r['t'].rstrip().endswith('.'): break
            continue
        if 't' in r and r['t'].strip() in ('—', '–', '/') and i + 1 < len(runs) and runs[i+1].get('b'):
            head.append(r); i += 1; continue   # unbolded dash inside a heading
        break
    return head, runs[i:]

def plain(runs): return ''.join(r.get('t', '') for r in runs).strip()

def build_chapter(slug, cfg):
    paras, foot, images = read(os.path.join(SITE, cfg['src']))
    order = [r['fn'] for p in paras for r in p['runs'] if 'fn' in r]
    fnmap = {old: k + 1 for k, old in enumerate(order)}
    fnhtml = {fnmap[o]: runs_html(foot[o], fnmap).replace('\n', '<br>') for o in order}
    os.makedirs(os.path.join(SITE, cfg['img_dir']), exist_ok=True)
    for k, (_, kind, data) in enumerate(images, 1):
        open(os.path.join(SITE, cfg['img_dir'], f'diagram-{k}.png'), 'wb').write(data)

    out = []; epi = None; region = 'top'; pending_quote = None
    for k, p in enumerate(paras):
        st = p['style']; runs = p['runs']; text = plain(runs)
        imgs = [r['img'] for r in runs if 'img' in r]
        if imgs:
            for n in imgs:
                w, h = int.from_bytes(images[n-1][2][16:20], 'big'), int.from_bytes(images[n-1][2][20:24], 'big')
                out.append(f'<figure class="diagram"><img src="../{cfg["img_dir"]}/diagram-{n}.png" alt="{html.escape(cfg["alts"][n-1])}" width="{w}" height="{h}" loading="lazy"></figure>')
            continue
        if not text and not any('fn' in r for r in runs): continue
        if st in ('Chapter Names', '124') or (st == 'Normal' and len(text) <= 2): continue   # title, ornaments
        if st == 'Beginnings of Chapters':
            if text.startswith('—'): epi = (epi[0], runs_html(runs, fnmap).lstrip('—').replace('Likkutei Sichos', '<em>Likkutei Sichos</em>'))
            else: epi = (runs_html(runs, fnmap, italics=False), '')
            continue
        if st == 'Personal Perspective':
            region = 'persp'
            head, rest = split_runin(runs)
            if head and not plain(rest): out.append(f'<h3>{html.escape(text)}</h3>')
            else: out.append(f'<p><em>{runs_html(runs, fnmap, italics=False)}</em></p>')
            continue
        if st == 'Short Opening Quote': pending_quote = runs_html(runs, fnmap, italics=False); continue
        if st == 'Short Quote After Personal':
            out.append(f'<blockquote class="quote"><p>{pending_quote}</p><cite>{runs_html(runs, fnmap).lstrip("—")}</cite></blockquote>')
            pending_quote = None; region = 'body'; continue
        if st == 'Sections':
            t = text.strip()
            if t.islower(): t = t.capitalize()
            if t == 'Summary': region = 'summary'
            out.append(f'<h2>{html.escape(t)}</h2>'); continue
        if st == 'Lists':
            raw = ''.join(r.get('t', '') for r in runs)
            body = runs_html(runs, fnmap); body = re.sub(r'^(<em>)?•(</em>)?\s*', '', body)
            if region == 'persp': body = f'<em>{runs_html(runs, fnmap, italics=False).lstrip("•").strip()}</em>'
            if raw.lstrip(' ').startswith('\t') and not raw.strip().startswith('•') and out and out[-1].startswith('<ul>'):
                out[-1] = out[-1][:-10] + f'<span class="more">{body}</span></li></ul>'
            elif out and out[-1].startswith('<ul>'): out[-1] = out[-1][:-5] + f'<li>{body}</li></ul>'
            else: out.append(f'<ul><li>{body}</li></ul>')
            continue
        # main text
        head, rest = split_runin(runs)
        if head:
            hh = re.sub(r'\s*\.(\s*</em>)?\s*$', r'\1', runs_html(head, fnmap))
            hh = re.sub(r'\s*<em>\s*</em>', '', hh).strip()
            if not plain(rest) and not any('fn' in r for r in rest): out.append(f'<h3>{re.sub("</?em>", "", hh)}</h3>'); continue
            rest_h = re.sub(r'^(<em>)?\.(</em>)?\s*', '', runs_html(rest, fnmap))
            out.append(f'<p><strong class="runin">{hh}.</strong> {rest_h}</p>'); continue
        if region == 'summary' and len(text) < 40 and not re.search(r'[.:;,!?”]$', text):
            out.append(f'<h3>{html.escape(text)}</h3>'); continue
        out.append(f'<p>{runs_html(runs, fnmap)}</p>')

    # glossary taps (first use of each term, in paragraphs only), then footnotes
    used = set(); final = []
    for b in out:
        if b.startswith(('<p>', '<ul>')): b = glossify(b, used)
        def fnrep(m):
            n = int(m.group(1))
            return f'<label class="fn" for="n{n}">{n}</label><input class="fn-t" type="checkbox" id="n{n}"><small class="sn"><b>{n}</b>{fnhtml[n]}</small>'
        final.append(re.sub('\x00FN(\\d+)\x00', fnrep, b))
    body_html = '\n    '.join(final)
    h = page(slug, cfg['num'], cfg['title'], None, cfg['desc'], None, epi, body_html, seo=cfg['seo'], expanded=True)
    open(os.path.join(SITE, 'read', slug + '.html'), 'w').write(h)
    placed = body_html.count('class="fn"'); print(f'{slug}: {len(final)} blocks, {len(order)} footnotes, placed={placed}, {len(images)} diagrams')
    return paras, foot, body_html

if __name__ == '__main__':
    for slug, cfg in CHAPTERS.items(): build_chapter(slug, cfg)
