// Family Purity date logic, kept free of page code so it can be tested on its own (_build/tests).
// Each Hebrew day is keyed by the civil date of its daytime, held at UTC noon.
(function(g){
  'use strict';
  const DAY=86400000;
  const parse=s=>{const [y,m,d]=s.split('-').map(Number);return new Date(Date.UTC(y,m-1,d,12));};
  const add=(d,n)=>new Date(d.getTime()+n*DAY);
  const iso=d=>d.toISOString().slice(0,10);
  const hebEn=new Intl.DateTimeFormat('en-u-ca-hebrew',{day:'numeric',month:'long',year:'numeric',timeZone:'UTC'});
  const hebParts=d=>{const o={};hebEn.formatToParts(d).forEach(p=>{if(p.type!=='literal')o[p.type]=p.value});return {day:+o.day,month:o.month,year:+o.year};};

  // Same Hebrew date in the very next Hebrew month. If that month is too short (e.g. 30 Kislev -> Tevet has 29 days), date is null.
  function nextSameHebrewDate(h){
    const p=hebParts(h); let i=1, q=hebParts(add(h,1));
    while(q.month===p.month && i<40){ i++; q=hebParts(add(h,i)); }
    const next=q.month;
    while(q.month===next && i<80){ if(q.day===p.day) return {date:add(h,i),month:next}; i++; q=hebParts(add(h,i)); }
    return {date:null,day:p.day,month:next};
  }

  // Yom Tov, Yom Kippur and Tisha B'Av, by Hebrew date (second days marked as outside Israel).
  const HOLIDAYS=[['Tishri',1,'Rosh Hashanah'],['Tishri',2,'Rosh Hashanah'],['Tishri',10,'Yom Kippur'],
    ['Tishri',15,'Sukkos'],['Tishri',16,'the second day of Sukkos (outside Israel)'],['Tishri',22,'Shemini Atzeres'],
    ['Tishri',23,'Simchas Torah (outside Israel)'],['Nisan',15,'Pesach'],['Nisan',16,'the second day of Pesach (outside Israel)'],
    ['Nisan',21,'the seventh day of Pesach'],['Nisan',22,'the last day of Pesach (outside Israel)'],
    ['Sivan',6,'Shavuos'],['Sivan',7,'the second day of Shavuos (outside Israel)'],['Av',9,'Tisha B’Av']];
  function holidayOf(d){
    const p=hebParts(d);
    if(p.month==='Av'&&p.day===9&&d.getUTCDay()===6) return null;                       // the fast moves to Sunday
    if(p.month==='Av'&&p.day===10&&add(d,-1).getUTCDay()===6) return 'Tisha B’Av (postponed from Shabbos)';
    const h=HOLIDAYS.find(x=>x[0]===p.month&&x[1]===p.day); return h?h[2]:null;
  }

  g.FPCalc={DAY,parse,add,iso,hebParts,nextSameHebrewDate,holidayOf};
})(typeof window!=='undefined'?window:this);
