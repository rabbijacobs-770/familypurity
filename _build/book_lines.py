"""Dump chapters of the current-edition book PDF (FP_Text, A4, Nisus 2010) into lines/<name>.json,
in the same format pdflines.swift writes, so build.py/render.py can turn them into reader pages.
usage: python3 book_lines.py /path/to/book.pdf
- Diagrams and the Hebrew prayers are cropped from the PDF into images/chapters/ and stand in the text
  as a one-line marker (font "FIGURE"); build.py turns that into a figure block.
- The book's Hebrew is in a legacy-encoded font (CorsivaHebrew), so short Hebrew words are given here
  in Unicode by position (read from the page images).
Not published (folder starts with "_"). The book PDF itself is not kept in the repo."""
import json, os, sys
import pymupdf

SP = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(SP)
# name: (first PDF page, last PDF page), 1-based, from FP_Text_copy.pdf (book page = PDF page - 22)
CHAPTERS = {
    'book_ch4_absence': (54, 72),
    'book_ch9_mikveh': (127, 133),
    'book_ch11_intimate': (151, 165),
    'book_ch12_times': (166, 169),
    'book_ch13_wedding': (170, 178),
    'book_ch14_anticipated': (179, 193),
    'book_ch15_birth': (194, 197),
}
FONT = {'AppleGaramondLight-Itali': 'AppleGaramondLight-Italic'}

# PDF page: [(x0, y0, x1, y1) in PDF points from the top-left, image file, alt text]
FIGS = {
    130: [((156, 282, 440, 450), 'mikveh-chabad-custom.png', 'Diagram of a mikveh built according to Chabad custom: (1) the immersion pool of tap water, (2) the otzar of rain water beneath it, (3) the two connecting apertures.')],
    132: [((143, 210, 454, 336), 'mikveh-other-poskim.png', 'Diagram of a mikveh built according to other poskim: (1) the immersion pool of tap water, (2) the otzar of rain water beside it, (3) the connecting aperture.')],
    157: [((112, 384, 482, 456), 'psalm-23-hebrew.png', 'Psalm 23 in Hebrew (Mizmor LeDovid).')],
    158: [((116, 231, 482, 286), 'atifah-bekitfah-hebrew.png', 'Atifah Bekitfah in Hebrew and Aramaic.')],
    181: [((135, 522, 447, 622), 'monthly-cycle.png', 'Diagram of the Monthly Cycle: menstruation began on the 9th of Kislev, so the couple separates on the corresponding night or day of the 9th of Tevas; in this example, during the daytime of the 9th of Tevas.')],
    183: [((125, 154, 483, 652), 'interval-cycle.png', 'Diagram of the Interval Cycle: count the number of half days (onahs) from last month’s hefsek tahara until the beginning of this month’s menstruation, then separate when the same number of half days passes from this month’s hefsek tahara. In this example, 46 half days.')],
    184: [((156, 231, 456, 411), 'average-cycle-29.png', 'Diagram of the Average (30 day) Cycle in a month of 29 days: there is no need to count; separation is observed on the corresponding Hebrew date on the following month, the complete day from sunset to sunset.'),
          ((156, 433, 453, 639), 'average-cycle-30.png', 'Diagram of the Average (30 day) Cycle in a month of 30 days: separation is observed on the previous date of the following month. The 30th day can also be found by counting four weeks and adding one weekday.')],
    188: [((171, 270, 426, 318), 'monthly-cycle-example-1.png', 'Diagram: menstruation began on the fifth in two consecutive months, then on the sixth in the third month.'),
          ((171, 461, 426, 509), 'monthly-cycle-example-2.png', 'Diagram: menstruation began twice on the sixth, then on the fifth in the third month.')],
    189: [((224, 280, 401, 552), 'monthly-cycle-recalculated.png', 'Diagram: menstruation began during the night of the second, and the next month during the day of the nineteenth, so both dates are observed as Monthly Cycle dates.')],
}
# Short Hebrew words: (PDF page, rounded x0 of the first span, rounded y0) -> Unicode text.
# Other Corsiva (Hebrew-font) spans on those lines are part of the same word and are dropped.
HEB = {
    (152, 315, 452): 'עונה',
    (154, 175, 258): 'יה', (154, 224, 258): 'י', (154, 321, 258): 'איש', (154, 408, 258): 'ה',
    (154, 116, 276): 'אשה', (154, 338, 276): 'יה',
    (181, 371, 437): 'יום החודש',
    (182, 363, 227): 'וסת הפלגה',
    (184, 361, 166): 'עונה בינונית',
}
HEB_LINES = {(p, y) for p, _, y in HEB}

def inside(b, r):
    cx, cy = (b[0] + b[2]) / 2, (b[1] + b[3]) / 2
    return r[0] <= cx <= r[2] and r[1] <= cy <= r[3]

def save_figs(doc):
    out = os.path.join(SITE, 'images', 'chapters'); os.makedirs(out, exist_ok=True)
    for p, figs in FIGS.items():
        for r, fn, alt in figs:
            pm = doc[p - 1].get_pixmap(dpi=200, clip=pymupdf.Rect(*r), colorspace=pymupdf.csGRAY)
            pm.save(os.path.join(out, fn))

def dump(doc, first, last):
    out = []
    for n, pno in enumerate(range(first - 1, last), start=1):
        page = doc[pno]; H = page.rect.height; P = pno + 1
        figs = FIGS.get(P, [])
        for r, fn, alt in figs:
            out.append({'p': n, 'x': r[0], 'y': H - r[1], 'w': r[2] - r[0], 'h': r[3] - r[1],
                        'runs': [{'f': 'FIGURE', 's': 11.0, 't': fn}]})
        for bl in page.get_text('dict')['blocks']:
            for ln in bl.get('lines', []):
                if any(inside(ln['bbox'], r) for r, _, _ in figs): continue
                spans = [s for s in ln['spans'] if s['text']]
                if not spans: continue
                text_spans = [s for s in spans if not s['font'].startswith('TypeEmbellishments')]
                runs = []
                if not text_spans:
                    # a standalone ornament: keep it as one large glyph (an ornament block)
                    runs = [{'f': 'Ornament', 's': 20.0, 't': '❦'}]
                else:
                    heb_done = set()
                    for s in text_spans:
                        f = FONT.get(s['font'], s['font'])
                        if 'Corsiva' in f and not s['text'].strip().isdigit():
                            x0, y0 = round(s['bbox'][0]), round(s['bbox'][1])
                            key = (P, x0, y0)
                            if key in HEB:
                                runs.append({'f': 'HEB', 's': 11.0, 't': HEB[key]}); continue
                            if any(k[0] == P and abs(k[2] - y0) <= 1 for k in HEB):
                                continue   # rest of a Hebrew word given above
                        runs.append({'f': f, 's': s['size'], 't': s['text'].replace('ﬁ', 'fi').replace('ﬂ', 'fl')})
                if not runs: continue
                x0, y0, x1, y1 = ln['bbox']
                main = max(spans, key=lambda s: (s['size'], len(s['text'])))
                out.append({'p': n, 'x': x0, 'y': H - main['origin'][1], 'w': x1 - x0, 'h': y1 - y0, 'runs': runs})
    return out

def fig_alts():
    return {fn: alt for figs in FIGS.values() for _, fn, alt in figs}

if __name__ == '__main__':
    doc = pymupdf.open(sys.argv[1])
    save_figs(doc)
    for name, (a, b) in CHAPTERS.items():
        data = dump(doc, a, b)
        json.dump(data, open(f'{SP}/lines/{name}.json', 'w'), ensure_ascii=False)
        print(name, a, b, len(data), 'lines')
