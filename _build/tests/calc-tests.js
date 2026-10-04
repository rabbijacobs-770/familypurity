// Run: jsc _build/hidden-tools/assets/fp-calc.js _build/tests/calc-tests.js   (macOS JavaScriptCore)
const C=FPCalc; let fail=0, pass=0;
const eq=(name,got,want)=>{ if(String(got)===String(want)) pass++; else { fail++; print('FAIL '+name+': got '+got+', want '+want); } };
const next=s=>{const r=C.nextSameHebrewDate(C.parse(s));return r.date?C.iso(r.date):'none ('+r.month+')';};
// Monthly cycle (yom hachodesh)
eq('23 Tishri -> 23 Heshvan', next('2026-10-04'), '2026-11-03');
eq('30 Tishri -> 30 Heshvan 5787', next('2026-10-11'), '2026-11-10');
eq('30 Kislev 5787 -> Tevet has no 30th', next('2026-12-10'), 'none (Tevet)');
eq('15 Adar I -> 15 Adar II', next('2027-02-22'), '2027-03-24');
// Holidays on mikveh night (Hebrew day of the night)
eq('10 Tishri 5787', C.holidayOf(C.parse('2026-09-21')), 'Yom Kippur');
eq('ordinary day', C.holidayOf(C.parse('2026-10-16')), 'null');
print(pass+' passed, '+fail+' failed');
