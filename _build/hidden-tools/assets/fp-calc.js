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

  // Sunrise or sunset (UTC Date) for a civil date at a place; approximate, within a minute or two. Null in polar day/night.
  const rad=Math.PI/180;
  function sun(d,lat,lng,rising){
    const y=d.getUTCFullYear(), m=d.getUTCMonth()+1, dd=d.getUTCDate();
    const N=Math.floor((Date.UTC(y,m-1,dd)-Date.UTC(y,0,0))/DAY), lh=lng/15, t=N+((rising?6:18)-lh)/24;
    const M=0.9856*t-3.289;
    let L=(M+1.916*Math.sin(M*rad)+0.020*Math.sin(2*M*rad)+282.634)%360; if(L<0)L+=360;
    let RA=Math.atan(0.91764*Math.tan(L*rad))/rad; RA=(RA+360)%360;
    RA=(RA+(Math.floor(L/90)*90-Math.floor(RA/90)*90))/15;
    const sinDec=0.39782*Math.sin(L*rad), cosDec=Math.cos(Math.asin(sinDec));
    const cosH=(Math.cos(90.833*rad)-sinDec*Math.sin(lat*rad))/(cosDec*Math.cos(lat*rad));
    if(cosH>1||cosH<-1) return null;
    let H=rising?360-Math.acos(cosH)/rad:Math.acos(cosH)/rad; H/=15;
    let UT=(H+RA-0.06571*t-6.622-lh)%24; if(UT<0)UT+=24;
    const base=Date.UTC(y,m-1,dd)-lh*3600000;
    let ms=Date.UTC(y,m-1,dd)+UT*3600000;
    while(ms<base)ms+=DAY; while(ms>=base+DAY)ms-=DAY;
    return new Date(ms);
  }

  g.FPCalc={DAY,parse,add,iso,hebParts,nextSameHebrewDate,holidayOf,sun};
})(typeof window!=='undefined'?window:this);
