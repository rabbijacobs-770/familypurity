/* Family Purity calendar: the basic day block, drawn like the day boxes on Rabbi Jacobs's printed calendar sheets.
   One block is one Hebrew day, from sunset to sunset. Its grey top is the NIGHT (sunset to sunrise);
   its white bottom is the DAY (sunrise to sunset). The English (Gregorian) date runs from midnight to midnight,
   so it is INLAID in the blocks' sides: a channel is carved down the sides (its shaded wall shows the depth of the cut)
   and a strip is set into it. Each English date is one piece of the strip, from midnight (level with the middle of one
   night) to the next midnight, crossing the sunset where one block meets the next; a narrow gap marks each midnight.
   The pieces alternate two light shades; the number is cut into the middle of its piece.
   FPDay.svg(o) returns one block. Options:
     n          the Hebrew day of the month, in the white circle (the operative date): a number, or Hebrew letters (י״ד)
     dow        day of the week: Su Mo Tu We Th Fr Sh (Sh is set in italics), in the white half
     night      optional name of the night in the grey half, e.g. "Sunday night" (the calendar leaves it out: it is self-evident)
     nightNote  a bold note in the night half, e.g. "Mikveh"
     holiday    [name, detail] of a Yom Tov, Yom Kippur or Tisha B'Av: an italic tag on the line between night and day (sunrise)
     label      note in the white half, e.g. "White day 3"; a "\n" starts a second, smaller line; strong sets it in bold
     big        true sets the text larger, for the printed half-year sheet (where each block is about an inch wide)
     today      true outlines the block in the accent color and adds "Today" in the white half
     dot        'night' or 'day': marks when the niddah state began (as on the "Suggested Use" page in Times)
     line       'night' | 'day' | 'top': a line down the block starting there...
     lineEnd    'bottom' (continues into the next block) or 't' (ends with a bar: the hefsek tahara, before sunset)
     date       the English date of the daytime (a Date at UTC noon); FPDay.stack draws the ribbon from these
     theme      'book' (greys, as printed; the default) or 'site' (violets)
   FPDay.stack([...days], wrap, {extend}) returns a column of blocks with the English-date ribbon down their sides;
     extend: true lets the last Gregorian date run on below the column to its next midnight.
     wrap(svg, day, z) may return the markup around each block (e.g. with buttons); it must keep style="z-index:z".
   FPDay.HALVES gives the night and day halves as fractions of a block's height, for touch areas. */
(function (g) {
  const THEMES = {
    book: { line: '#1f1f1f', lid: '#c4c4c4', band: '#bdbdbd', body: '#ffffff', ink: '#111111', even: '#e3e3e3', odd: '#f6f6f6', face1: '#f4f4f4', face2: '#e7e7e7', floor: '#8f8f8f', wallDark: '#9b9b9b', wallLight: '#cbcbcb', wallLit: '#cfcfcf', shadow: 'rgba(0,0,0,.45)', lite: '#ffffff', soft: '#3f3f3f', tick: '#8c8c8c', accent: '#4b3a8c' },
    site: { line: '#2c2157', lid: '#c8bfe9', band: '#6f5dbb', body: '#ffffff', ink: '#2c2157', even: '#e4def5', odd: '#f6f4fc', face1: '#f5f3fc', face2: '#e8e3f6', floor: '#8b82b8', wallDark: '#978fc4', wallLight: '#cdc6e8', wallLit: '#d3cceb', shadow: 'rgba(44,33,87,.45)', lite: '#ffffff', soft: '#3f3766', tick: '#9b90c9', accent: '#94701f' }
  };
  const SANS = '"Helvetica Neue", Helvetica, Arial, sans-serif';
  const SERIF = '"Times New Roman", Times, serif';
  const HEB = '"Frank Ruhl Libre", "Times New Roman", serif';                       // for a Hebrew-letter date (י״ד)
  // Block geometry (viewBox 260 x 96), proportioned like the printed sheet: front face 8–206, side face 206–250.
  // The side is a slanted face: its top edge rises from (206,24) to (250,6), so a level line on it rises 18 units across.
  // The lid's left end recedes at the same angle and depth as the right side (44 across, 18 up), so both ends match.
  const OUTLINE = 'M8 24 52 6H250V74L206 92H8Z';
  const NIGHT_Y = 41, DAY_Y = 76, LINE_X = 84;             // middle of the night (about midnight), a spot in the day, the line's position
  const PITCH = 78;                                        // each block sits 78 units below the one above (96 tall, 18 overlapped)
  const HALVES = { night: [24 / 96, 58.5 / 96], day: [58.5 / 96, 92 / 96] };
  let uid = 0;
  const esc = s => String(s == null ? '' : s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const DOW_NAMES = { Su: 'Sunday', Mo: 'Monday', Tu: 'Tuesday', We: 'Wednesday', Th: 'Thursday', Fr: 'Friday', Sh: 'Shabbos' };
  const MON = new Intl.DateTimeFormat('en-US', { month: 'short', timeZone: 'UTC' });

  const shade = (t, d) => (Math.floor(d.getTime() / 864e5) % 2 ? t.odd : t.even);

  function svg(o) {
    const t = THEMES[o.theme || 'book'];
    const hebN = /[\u0590-\u05FF]/.test(String(o.n));                                   // the date written in Hebrew letters
    const name = [o.n, o.night, o.holiday && o.holiday.join(', '), o.nightNote, o.dow && DOW_NAMES[o.dow], o.date && 'English date ' + MON.format(o.date) + ' ' + o.date.getUTCDate(),
                  o.label && o.label.replace('\n', ', ')].filter(Boolean).join(', ');
    // The night band: an optional bold note (e.g. Mikveh).
    const band = [];
    if (o.night) band.push({ t: o.night, size: 12 });
    if (o.nightNote) band.push({ t: o.nightNote, size: 13, bold: true });
    const ys = band.length === 1 ? [46] : band.length === 2 ? [40, 53] : [35, 46, 56];
    // A Yom Tov sits on the line between night and day (sunrise), in a small white tag; any detail ("2nd day…") under it.
    let hol = '';
    if (o.holiday) {
      const size = o.big ? 14 : 12, w = Math.min(116, o.holiday[0].length * size * .56 + 13), top = 58.5 - size * .65;
      hol = `<rect x="90" y="${top}" width="${w}" height="${size * 1.3}" rx="${size * .65}" fill="${t.body}" stroke="${t.line}" stroke-width=".7"/>` +
            `<text x="96" y="${58.5 + size * .36}" font-family='${SANS}' font-size="${size}" font-style="italic" fill="${t.ink}">${esc(o.holiday[0])}</text>` +
            (o.holiday[1] ? `<text x="96" y="${58.5 + size * .65 + (o.big ? 11 : 10)}" font-family='${SANS}' font-size="${o.big ? 11 : 9.5}" font-style="italic" fill="${t.ink}">${esc(o.holiday[1])}</text>` : '');
    }
    const night = band.map((b, i) => `<text x="96" y="${ys[i]}" font-family='${SANS}' font-size="${b.size}"${b.it ? ' font-style="italic"' : ''}${b.bold ? ' font-weight="700"' : ''} fill="${t.ink}">${esc(b.t)}</text>`).join('');
    const dow = o.dow ? `<text x="${o.big ? 200 : 198}" y="${o.big ? 88 : 86}" text-anchor="end" font-family='${SERIF}' font-size="${o.big ? 27 : 20}" font-style="${o.dow === 'Sh' ? 'italic' : 'normal'}" fill="${t.ink}">${esc(o.dow)}</text>` : '';
    let lines = o.label ? String(o.label).split('\n') : [];
    if (o.today && lines.length < 2) lines = lines.length ? [lines[0], 'Today'] : ['Today'];
    const weight = o.strong || (o.today && lines.length === 1) ? 700 : 400;
    const label = lines.length === 1 ? `<text x="94" y="85" font-family='${SANS}' font-size="13" font-weight="${weight}" fill="${t.ink}">${esc(lines[0])}</text>`
      : lines.length > 1 ? `<text x="96" y="76" font-family='${SANS}' font-size="13.5" font-weight="${weight}" fill="${t.ink}">${esc(lines[0])}<tspan x="96" y="88" font-size="12">${esc(lines[1])}</tspan></text>` : '';
    let marks = '';
    if (o.line) {
      const y1 = o.line === 'night' ? NIGHT_Y : o.line === 'day' ? DAY_Y : 6, y2 = o.lineEnd === 't' ? 87 : 96;
      marks += `<path d="M${LINE_X} ${y1}V${y2}" stroke="${t.ink}" stroke-width="2"/>`;
      if (o.lineEnd === 't') marks += `<path d="M${LINE_X - 11} 87H${LINE_X + 11}" stroke="${t.ink}" stroke-width="2.6"/>`;
    }
    if (o.dot) marks += `<circle cx="${LINE_X}" cy="${o.dot === 'night' ? NIGHT_Y : DAY_Y}" r="5" fill="${t.ink}" stroke="${t.body}" stroke-width="1.5"/>`;
    const side = `<path d="M206 24 250 6V74L206 92Z" fill="${t.body}"/>` +
                 `<path d="M206 24 250 6V40.5L206 58.5Z" fill="${t.band}"/>`;                // the night band continues around the corner
    return `<svg class="fp-day" viewBox="0 0 260 96" role="img" aria-label="${esc(name)}" xmlns="http://www.w3.org/2000/svg">` +
      `<path d="${OUTLINE}" fill="${t.body}"/>` +
      `<path d="M8 24 52 6H250L206 24Z" fill="${t.lid}"/>` +                                      // lid
      `<path d="M8 24H206V58.5H8Z" fill="${t.band}"/>` +                                         // grey band: the night
      side +
      `<path d="M8 24H206L250 6M206 24V92" fill="none" stroke="${t.line}" stroke-width="1" stroke-linejoin="round"/>` +
      `<path d="${OUTLINE}" fill="none" stroke="${o.today ? t.accent : t.line}" stroke-width="${o.today ? 3 : 1.6}" stroke-linejoin="round"/>` +
      `<circle cx="50" cy="58.5" r="26" fill="${t.body}"/>` +                                     // arch rising into the band
      (hebN ? `<text x="50" y="${o.big ? 73 : 70}" text-anchor="middle" font-family='${HEB}' font-weight="500" font-size="${o.big ? 38 : 32}" fill="${t.ink}">${esc(o.n)}</text>`
            : `<text x="50" y="${o.big ? 74 : 71}" text-anchor="middle" font-family='${SANS}' font-size="${o.big ? 42 : 35}" fill="${t.ink}">${esc(o.n)}</text>`) +
      night + hol + dow + label + marks +
      `</svg>`;
  }

  // The English-date ribbon, drawn over the blocks' sides. Midnight on the side is a slanted line (the side face rises
  // 18 units over its 44-unit width), level with the middle of the night at the front edge.
  const midnight = (k, x) => k * PITCH + NIGHT_Y - (x - 206) * 18 / 44;
  // extend: let the last Gregorian date run on below the last block, to its next midnight (used for a single sample block).
  function ribbon(days, theme, extend) {
    const t = THEMES[theme || 'book'], n = days.length, H = extend ? n * PITCH + NIGHT_Y + 4 : (n - 1) * PITCH + 96;
    const flat = days[0] && days[0].big;   // the printed sheet: plain fills (gradients make PDFs about three times larger and print the same)
    // The groove cut into the side (c1–c2): a deep shaded left wall, a narrow lit right wall, and the strip set inside (x1–x2).
    // Light comes from the upper left, so inside a groove the left and top walls are in shadow and the right and bottom catch light.
    const c1 = 217, c2 = 251, x1 = c1 + 4.5, x2 = 249.6, xm = (x1 + x2) / 2;          // a thin left wall; the groove runs out to the side's back edge
    // The groove starts at the first midnight and ends at the last block's lower edge, both slanted like the side face.
    const startY = x => midnight(0, x), id = 'fpw' + (++uid);
    const boxEnd = x => (n - 1) * PITCH + 92 - (x - 206) * 18 / 44;                       // the last block's lower edge
    const endY = extend ? x => midnight(n, x) + 1.4 : boxEnd;                               // where the last date's strip stops
    const engrave = (x, y, size, font, text, extra = '') =>                              // cut-in lettering: a light edge under dark letters
      `<text x="${x + .6}" y="${y + .8}" text-anchor="middle" font-family='${font}' font-size="${size}" ${extra} fill="${t.lite}">${text}</text>` +
      `<text x="${x}" y="${y}" text-anchor="middle" font-family='${font}' font-size="${size}" ${extra} fill="${t.soft}">${text}</text>`;
    const quad = (xa, xb, ya, yb) => `M${xa} ${ya(xa)}L${xb} ${ya(xb)}V${yb(xb)}L${xa} ${yb(xa)}Z`;
    let out = `<defs><linearGradient id="${id}" x1="0" x2="1" y1="0" y2="0"><stop offset="0" stop-color="${t.wallDark}"/><stop offset="1" stop-color="${t.wallLight}"/></linearGradient>` +
      `<linearGradient id="${id}s" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#000" stop-opacity=".32"/><stop offset="1" stop-color="#000" stop-opacity="0"/></linearGradient>` +
      `<linearGradient id="${id}l" x1="0" x2="1" y1="0" y2="0"><stop offset="0" stop-color="#000" stop-opacity=".1"/><stop offset="1" stop-color="#000" stop-opacity="0"/></linearGradient></defs>` +
      `<path d="${quad(c1, c2, startY, boxEnd)}" fill="${t.floor}"/>` +                                   // the floor of the groove (seen in the gaps at midnight)
      `<path d="${quad(c1, x1, startY, boxEnd)}" fill="${flat ? t.wallLight : `url(#${id})`}"/>` +                                // its deep left wall, in shadow
      `<path d="M${c1} ${startY(c1)}V${boxEnd(c1)}" stroke="${t.tick}" stroke-width=".8"/>`;   // the cut edge, drawn light (the right side is the block's own edge)
    for (let k = 0; k < n; k++) {
      const d = days[k].date;
      // The Gregorian date: a strip set into the groove, from one midnight to the next; a narrow gap at each midnight.
      const a1 = midnight(k, x1) + 1.6, a2 = midnight(k, x2) + 1.6;
      const b1 = Math.min(midnight(k + 1, x1) - 1.6, endY(x1) - 1), b2 = Math.min(midnight(k + 1, x2) - 1.6, endY(x2) - 1);
      if (b1 - a1 < 4) continue;
      const odd = Math.floor(d.getTime() / 864e5) % 2;
      out += `<path d="M${x1} ${a1}L${x2} ${a2}V${b2}L${x1} ${b1}Z" fill="${odd ? t.face2 : t.face1}"/>` +
             (flat ? '' : `<path d="M${x1} ${a1}H${x1 + 5}V${b1}H${x1}Z" fill="url(#${id}l)"/>`) +                                         // shadow cast from the left wall
             `<path d="M${x1} ${b1}V${a1}L${x2} ${a2}" fill="none" stroke="${t.shadow}" stroke-width="1" stroke-linejoin="round"/>` +   // its shaded top and left edges
             `<path d="M${x2} ${b2}L${x1} ${b1}" fill="none" stroke="${t.lite}" stroke-width="1"/>`;      // its lit lower edge (no bright right edge: it was too loud)
      const ta = (a1 + a2) / 2, tb = (b1 + b2) / 2, mid = (ta + tb) / 2;
      if (tb - ta > 40) {
        const big = days[k].big;                                                           // larger on the printed sheet
        if (k === 0 || d.getUTCDate() === 1) out += engrave(xm, mid - (big ? 16 : 13), big ? 11 : 9, SERIF, MON.format(d), 'font-style="italic"');
        out += engrave(xm, mid + (big ? 8 : 6), big ? 23 : 18.5, SERIF, d.getUTCDate(), 'font-style="italic"');      // italic: shown for convenience only
      }
    }
    // One quiet grey line for the back edge, in place of the blocks' separate black corners there.
    out += `<path d="M250.4 ${startY(250.4)}V${endY(250.4) - (extend ? 1.6 : 0)}" stroke="${t.tick}" stroke-width=".8"/>`;
    return `<svg class="fp-ribbon" viewBox="0 0 260 ${H}" aria-hidden="true" style="z-index:${n + 1}" xmlns="http://www.w3.org/2000/svg">${out}</svg>`;
  }

  // A column of days, earlier days on top so each one's bottom covers part of the next one's lid; the ribbon over their sides.
  const cell = (s, d, z) => `<div class="fp-cell" style="z-index:${z}">${s}</div>`;
  const stack = (days, wrap = cell, opts = {}) => `<div class="fp-stack">${days.map((d, i) => wrap(svg(d), d, days.length - i)).join('')}` +
    (days[0] && days[0].date ? ribbon(days, days[0].theme, opts.extend) : '') + `</div>`;

  // Each block has 6 units of air above and 4 below: pulling the next one up 10/260 of the width makes them touch;
  // 18/260 (6.92%) slides each bottom 8 units over the lid below.
  const css = '.fp-stack{display:grid;position:relative;width:min(100%,260px)}.fp-stack>*{display:block;position:relative;width:100%}' +
    '.fp-stack .fp-day{display:block;width:100%;height:auto}.fp-stack>*+*{margin-top:-6.92%}' +
    '.fp-stack>.fp-ribbon{position:absolute;top:0;left:0;width:100%;height:auto;margin:0;pointer-events:none}';

  g.FPDay = { svg, stack, ribbon, css, THEMES, HALVES, PITCH };
})(window);
