// Family Purity free tools. Everything is computed in the visitor's browser; nothing is sent anywhere.
// Rules follow Rabbi Jacobs's texts: Family Purity ch. 5-6 and the two Times web editions.
(function(){
  'use strict';
  document.querySelectorAll('[data-em]').forEach(el=>{const [u,d]=el.dataset.em.split('|'),a=u+'@'+d,s=el.dataset.subject;if(el.tagName==='A')el.href='mailto:'+a+(s?'?subject='+encodeURIComponent(s):'');});
  const $=(s,r=document)=>r.querySelector(s);
  const $$=(s,r=document)=>[...r.querySelectorAll(s)];
  const DAY=86400000;

  // ---------- dates (each Hebrew day is keyed by the civil date of its daytime, held at UTC noon) ----------
  const parse=s=>{const [y,m,d]=s.split('-').map(Number);return new Date(Date.UTC(y,m-1,d,12));};
  const add=(d,n)=>new Date(d.getTime()+n*DAY);
  const diff=(a,b)=>Math.round((a-b)/DAY);
  const iso=d=>d.toISOString().slice(0,10);
  const fmtLong=new Intl.DateTimeFormat('en-US',{weekday:'long',month:'long',day:'numeric',year:'numeric',timeZone:'UTC'});
  const fmtShort=new Intl.DateTimeFormat('en-US',{weekday:'short',month:'short',day:'numeric',timeZone:'UTC'});
  const fmtWd=new Intl.DateTimeFormat('en-US',{weekday:'long',timeZone:'UTC'});
  const hebEn=new Intl.DateTimeFormat('en-u-ca-hebrew',{day:'numeric',month:'long',year:'numeric',timeZone:'UTC'});
  const hebHe=new Intl.DateTimeFormat('he-u-ca-hebrew',{day:'numeric',month:'long',year:'numeric',timeZone:'UTC'});
  const hebParts=d=>{const o={};hebEn.formatToParts(d).forEach(p=>{if(p.type!=='literal')o[p.type]=p.value});return {day:+o.day,month:o.month,year:+o.year};};
  const long=d=>fmtLong.format(d), short=d=>fmtShort.format(d), wd=d=>fmtWd.format(d);
  const heb=d=>hebEn.format(d);
  // Hebrew-letter numerals (gematria), e.g. 23 -> כ״ג, 5787 -> תשפ״ז
  const gem=n=>{
    const H=[[400,'ת'],[300,'ש'],[200,'ר'],[100,'ק']],T=['','י','כ','ל','מ','נ','ס','ע','פ','צ'],U=['','א','ב','ג','ד','ה','ו','ז','ח','ט'];
    let s='';n=n%1000;
    for(const [v,c] of H){while(n>=v){s+=c;n-=v;}}
    if(n===15)s+='טו';else if(n===16)s+='טז';else s+=T[Math.floor(n/10)]+U[n%10];
    return s.length>1?s.slice(0,-1)+'״'+s.slice(-1):s+'׳';
  };
  const hebH=d=>{const o={};hebHe.formatToParts(d).forEach(p=>{if(p.type!=='literal')o[p.type]=p.value});return `${gem(+o.day)} ${o.month} ${gem(+o.year)}`;};
  const esc=s=>String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));

  // When did it begin? day = sunrise-sunset; evening = after sunset, before midnight; night = after midnight, before sunrise.
  const hebrewDay=(dateStr,when)=>{const d=parse(dateStr);return when==='evening'?add(d,1):d;};
  const onahOf=when=>when==='day'?'day':'night';

  const onahText=(h,onah)=>{
    if(onah==='day') return `${wd(h)} daytime, ${short(h)} &middot; sunrise to sunset`;
    if(onah==='night') return `${wd(add(h,-1))} night, ${short(add(h,-1))} &middot; sunset to sunrise`;
    return `From sunset ${short(add(h,-1))} until sunset ${short(h)} &middot; a full day`;
  };

  // Same Hebrew date in the next month (logic and tests live in fp-calc.js)
  const nextSameHebrewDate=h=>FPCalc.nextSameHebrewDate(h);

  // ---------- storage helpers (per-device only) ----------
  const store={get(k){try{return JSON.parse(localStorage.getItem(k))}catch(e){return null}},set(k,v){try{localStorage.setItem(k,JSON.stringify(v))}catch(e){}}};

  // ---------- calendar file (.ics) ----------
  const icsDate=d=>iso(d).replace(/-/g,'');
  function downloadIcs(name,events,detailed){
    const lines=['BEGIN:VCALENDAR','VERSION:2.0','PRODID:-//FamilyPurity.com//Tools//EN','CALSCALE:GREGORIAN'];
    const stamp=new Date().toISOString().replace(/[-:]/g,'').slice(0,15)+'Z';
    events.forEach((e,i)=>{
      lines.push('BEGIN:VEVENT',`UID:${stamp}-${i}@familypurity.com`,`DTSTAMP:${stamp}`,
        `DTSTART;VALUE=DATE:${icsDate(e.date)}`,`DTEND;VALUE=DATE:${icsDate(add(e.date,1))}`,
        `SUMMARY:${detailed?e.title:'◆ Reminder'}`,`DESCRIPTION:${(detailed?e.detail:'Family Purity calendar reminder').replace(/\n/g,'\\n')}`,'END:VEVENT');
    });
    lines.push('END:VCALENDAR');
    const blob=new Blob([lines.join('\r\n')],{type:'text/calendar'});
    const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download=name;document.body.append(a);a.click();
    setTimeout(()=>{URL.revokeObjectURL(a.href);a.remove();},500);
  }

  // ---------- 1. Mikveh night ----------
  const mk=$('#mikveh-form');
  if(mk){
    const out=$('#mikveh-out');
    let lastEvents=[];
    mk.addEventListener('submit',e=>{
      e.preventDefault();
      const start=mk.start.value; if(!start){out.innerHTML='<p class="warn">Please enter the date the niddah state began.</p>';return;}
      const h=hebrewDay(start,mk.when.value);
      const earliest=add(h,4);
      let hef=earliest, note='';
      if(mk.hefsek.value){
        hef=parse(mk.hefsek.value);
        if(diff(hef,earliest)<0){out.innerHTML=`<p class="warn">That is too early. The <em>hefsek tahara</em> can be done from the fifth day, counting the day the niddah state began as day one. The earliest date here is <b>${long(earliest)}</b>, before sunset.</p>`;return;}
      } else note='<p class="small">Showing the earliest possible dates. If the <em>hefsek tahara</em> is done later, enter its date above.</p>';
      const days=[...Array(7)].map((_,i)=>add(hef,i+1));
      const mikveh=days[6];
      out.innerHTML=`
        <div class="result-hero">
          <span class="eyebrow">Mikveh night</span>
          <strong>${wd(mikveh)} night</strong>
          <span>${long(mikveh)}, after nightfall</span>
          <span class="heb">${esc(heb(add(mikveh,1)))} &middot; <span lang="he">${esc(hebH(add(mikveh,1)))}</span></span>
        </div>
        <ol class="timeline-steps">
          <li><b>Day 1</b><span>Niddah state began &middot; ${short(h)}</span></li>
          <li><b>Day 5</b><span>${mk.hefsek.value?'Hefsek tahara':'Earliest hefsek tahara'}, before sunset &middot; ${short(hef)}</span></li>
          <li><b>7 days</b><span>Seven white days &middot; ${short(days[0])} to ${short(days[6])}</span></li>
          <li><b>Night</b><span>Immersion after nightfall &middot; ${wd(mikveh)} night</span></li>
        </ol>
        ${note}
        ${[5,6].includes(mikveh.getUTCDay())?'<p class="small">Mikveh night falls on Friday night or after Shabbos. Special preparation rules apply. See Chapter 7 or ask Rabbi Jacobs.</p>':''}
        ${FPCalc.holidayOf(add(mikveh,1))?`<p class="warn">Mikveh night falls on <b>${FPCalc.holidayOf(add(mikveh,1))}</b>. Special rules apply. Ask Rabbi Jacobs before going.</p>`:''}
        <div class="row-actions">
          <a class="btn btn-line" href="#checklist" data-fill="${iso(hef)}">Track the seven days</a>
          <button class="btn btn-line" type="button" id="mikveh-ics">Add to my calendar</button>
        </div>`;
      lastEvents=[...days.map((d,i)=>({date:d,title:`Day ${i+1} of 7`,detail:`Seven white days, day ${i+1} of 7. Examinations twice daily.`})),
        {date:mikveh,title:'Mikveh tonight',detail:'Immersion after nightfall.'}];
      $('#mikveh-ics').addEventListener('click',()=>downloadIcs('mikveh-dates.ics',lastEvents,mk.details.checked));
      $('[data-fill]',out).addEventListener('click',ev=>{const f=$('#check-form');if(f){ev.preventDefault();f.hefsek.value=ev.currentTarget.dataset.fill;f.dispatchEvent(new Event('submit'));f.scrollIntoView({behavior:'smooth'});}else{ev.currentTarget.href='seven-white-days-checklist.html?h='+ev.currentTarget.dataset.fill;}});
    });
  }

  // ---------- 2. Seven white days checklist ----------
  const ck=$('#check-form');
  if(ck){
    const out=$('#check-out');
    const saved=store.get('fp-checks')||{};
    const qh=new URLSearchParams(location.search).get('h');
    if(qh&&/^\d{4}-\d{2}-\d{2}$/.test(qh)){ck.hefsek.value=qh;if(!saved.hefsek||saved.hefsek!==qh)store.set('fp-checks',{hefsek:qh,marks:{}});}
    else if(saved.hefsek) ck.hefsek.value=saved.hefsek;
    const render=()=>{
      if(!ck.hefsek.value){out.innerHTML='';return;}
      const hef=parse(ck.hefsek.value);
      const state=store.get('fp-checks');
      const marks=(state&&state.hefsek===ck.hefsek.value)?state.marks:{};
      const today=iso(new Date(Date.now()-new Date().getTimezoneOffset()*60000));
      let done=0;
      const rows=[...Array(7)].map((_,i)=>{
        const d=add(hef,i+1), k=iso(d);
        const a=marks[k+'a'], b=marks[k+'b']; done+=(a?1:0)+(b?1:0);
        return `<div class="ck-day${k===today?' today':''}">
          <span class="ck-n">Day ${i+1}</span><span class="ck-d">${short(d)}</span>
          <label><input type="checkbox" data-k="${k}a" ${a?'checked':''}> 1st</label>
          <label><input type="checkbox" data-k="${k}b" ${b?'checked':''}> 2nd</label></div>`;
      }).join('');
      out.innerHTML=`<div class="ck-head"><b>${done} of 14</b> examinations marked<span class="bar"><i style="width:${done/14*100}%"></i></span></div>
        <div class="ck-grid">${rows}</div>
        <p class="small">Saved only on this device. Mikveh night: <b>${wd(add(hef,7))} night, ${short(add(hef,7))}</b>.</p>
        <button class="btn btn-line" type="button" id="ck-clear">Clear checklist</button>`;
      $$('input[data-k]',out).forEach(c=>c.addEventListener('change',()=>{
        const st=store.get('fp-checks'); const m=(st&&st.hefsek===ck.hefsek.value)?st.marks:{};
        m[c.dataset.k]=c.checked; store.set('fp-checks',{hefsek:ck.hefsek.value,marks:m}); render();
      }));
      $('#ck-clear').addEventListener('click',()=>{store.set('fp-checks',{hefsek:ck.hefsek.value,marks:{}});render();});
    };
    ck.addEventListener('submit',e=>{e.preventDefault();const st=store.get('fp-checks');if(!st||st.hefsek!==ck.hefsek.value)store.set('fp-checks',{hefsek:ck.hefsek.value,marks:{}});render();});
    render();
  }

  // ---------- 3. Separation dates (vestos) ----------
  const vs=$('#vestos-form');
  if(vs){
    const out=$('#vestos-out');
    const syncCustom=()=>{
      const chabad=vs.custom.value==='chabad';
      $$('.only-chabad',vs).forEach(el=>el.hidden=!chabad);
      $$('.only-other',vs).forEach(el=>el.hidden=chabad);
    };
    $$('input[name=custom]',vs).forEach(r=>r.addEventListener('change',syncCustom)); syncCustom();
    let lastEvents=[];
    vs.addEventListener('submit',e=>{
      e.preventDefault();
      if(!vs.start.value){out.innerHTML='<p class="warn">Please enter the date this period began.</p>';return;}
      const chabad=vs.custom.value==='chabad';
      const h=hebrewDay(vs.start.value,vs.when.value), onah=onahOf(vs.when.value);
      const items=[];
      // Monthly cycle
      const m=nextSameHebrewDate(h);
      if(m.date) items.push({key:'Monthly cycle',he:'Yom Hachodesh',date:m.date,onah,why:`Same Hebrew date next month (${esc(heb(m.date))}), same half of the day as when it began.`});
      else items.push({key:'Monthly cycle',he:'Yom Hachodesh',date:null,why:`It began on the 30th of the Hebrew month and next month has only 29 days. Please ask Rabbi Jacobs which day to observe.`});
      // Average cycle
      items.push({key:'Average cycle',he:'Onah Beinonis',date:add(h,29),onah:'full',why:'The 30th day, counting the day it began as day one. Separate for the full day.'});
      if(!chabad&&vs.d31.checked) items.push({key:'Average cycle, 31st day',he:'Onah Beinonis',date:add(h,30),onah:'full',why:'The custom in many communities is to separate on the entire 31st day as well.'});
      // Interval cycle
      if(chabad){
        if(vs.prevHefsek.value&&vs.curHefsek.value){
          const ph=parse(vs.prevHefsek.value), ch=parse(vs.curHefsek.value), gap=diff(h,ph);
          if(gap>0&&diff(ch,h)>=0) items.push({key:'Interval cycle',he:'Veses Haflagah',date:add(ch,gap),onah,why:`From the last hefsek tahara to this period was ${gap+1} days, counting both days. The same interval from this hefsek tahara.`});
          else items.push({key:'Interval cycle',he:'Veses Haflagah',date:null,why:'Please check the hefsek tahara dates. The previous one should be before this period began, and this one after.'});
        } else items.push({key:'Interval cycle',he:'Veses Haflagah',date:null,why:'Add the previous and the current hefsek tahara dates to calculate this.'});
      } else {
        if(vs.prevStart.value){
          const ph=hebrewDay(vs.prevStart.value,vs.prevWhen.value), gap=diff(h,ph);
          if(gap>0) items.push({key:'Interval cycle',he:'Veses Haflagah',date:add(h,gap),onah,why:`The last interval was ${gap+1} days, counting both days. The same interval from this period.`});
          else items.push({key:'Interval cycle',he:'Veses Haflagah',date:null,why:'The previous period should be before this one.'});
        } else items.push({key:'Interval cycle',he:'Veses Haflagah',date:null,why:'Add when the previous period began to calculate this. It needs one full cycle.'});
      }
      // Or Zarua: one extra half-day before each
      if(!chabad&&vs.oz.checked){
        items.filter(i=>i.date&&!i.key.includes('31st')).forEach(i=>{
          const prev=i.onah==='day'?{date:i.date,onah:'night'}:{date:add(i.date,-1),onah:'day'};
          items.push({key:'Or Zarua',he:'before the '+i.key.toLowerCase(),date:prev.date,onah:prev.onah,why:'The custom in many communities is to separate one extra half-day before.'});
        });
      }
      const sortKey=i=>i.date?(i.date.getTime()-(i.onah==='day'?0:DAY/2)):Infinity;
      items.sort((a,b)=>sortKey(a)-sortKey(b));
      out.innerHTML=`<div class="v-list">${items.map(i=>`
        <article class="v-item${i.date?'':' muted'}">
          <header><b>${esc(i.key)}</b><span>${esc(i.he)}</span></header>
          ${i.date?`<p class="v-when">${onahText(i.date,i.onah)}</p><p class="heb">${esc(heb(i.date))}</p>`:''}
          <p class="small">${i.why}</p>
        </article>`).join('')}</div>
        <p class="small">On each of these, an examination is made from the time of day the last period began. Only actual menstruation counts here, not stains. If your cycle follows a fixed pattern, ask Rabbi Jacobs.</p>
        <button class="btn btn-line" type="button" id="vestos-ics">Add to my calendar</button>`;
      lastEvents=items.filter(i=>i.date).map(i=>({date:i.onah==='day'?i.date:add(i.date,-1),title:`${i.key}${i.onah==='full'?' (full day from tonight)':i.onah==='night'?' (tonight)':' (today)'}`,detail:`${i.key} · ${i.he}. ${i.why.replace(/<[^>]+>/g,'')}`}));
      $('#vestos-ics').addEventListener('click',()=>downloadIcs('separation-dates.ics',lastEvents,vs.details.checked));
    });
  }

  // ---------- 4. Hebrew date converter ----------
  const hc=$('#heb-form');
  if(hc){
    const out=$('#heb-out');
    const conv=()=>{
      if(!hc.date.value){out.innerHTML='';return;}
      let d=parse(hc.date.value); if(hc.after.checked) d=add(d,1);
      out.innerHTML=`<div class="result-hero small-hero"><strong>${esc(heb(d))}</strong><span lang="he" class="heb-big">${esc(hebH(d))}</span>${hc.after.checked?'<span class="small">After sunset, the Hebrew date has already moved to the next day.</span>':''}</div>`;
    };
    hc.addEventListener('input',conv); hc.addEventListener('submit',e=>{e.preventDefault();conv();});
    if(!hc.date.value){hc.date.value=iso(new Date(Date.now()-new Date().getTimezoneOffset()*60000));} conv();

    const hr=$('#heb2-form'), out2=$('#heb2-out');
    if(hr){
      const y0=hebParts(new Date()).year;
      hr.year.value=y0;
      hr.addEventListener('submit',e=>{
        e.preventDefault();
        const day=+hr.day.value, month=hr.month.value, year=+hr.year.value;
        const start=new Date(Date.UTC(year-3761,6,1,12));
        let found=null;
        for(let i=0;i<460;i++){const c=add(start,i),p=hebParts(c);if(p.year===year&&p.month===month&&p.day===day){found=c;break;}}
        out2.innerHTML=found?`<div class="result-hero small-hero"><strong>${long(found)}</strong><span class="small">Begins the evening before, at sunset (${short(add(found,-1))}).</span></div>`
          :`<p class="warn">That date does not exist in ${year}. Check the month (in a leap year there are Adar I and Adar II) and the day.</p>`;
      });
    }
  }

  // ---------- 5. Sunrise and sunset ----------
  const sn=$('#sun-form');
  if(sn){
    const out=$('#sun-out');
    const rad=Math.PI/180;
    function sunUTC(y,m,d,lat,lng,rising){
      const N=Math.floor((Date.UTC(y,m-1,d)-Date.UTC(y,0,0))/DAY);
      const lh=lng/15, t=N+((rising?6:18)-lh)/24;
      const M=0.9856*t-3.289;
      let L=(M+1.916*Math.sin(M*rad)+0.020*Math.sin(2*M*rad)+282.634)%360; if(L<0)L+=360;
      let RA=Math.atan(0.91764*Math.tan(L*rad))/rad; RA=(RA+360)%360;
      RA=(RA+(Math.floor(L/90)*90-Math.floor(RA/90)*90))/15;
      const sinDec=0.39782*Math.sin(L*rad), cosDec=Math.cos(Math.asin(sinDec));
      const cosH=(Math.cos(90.833*rad)-sinDec*Math.sin(lat*rad))/(cosDec*Math.cos(lat*rad));
      if(cosH>1||cosH<-1) return null;
      let H=rising?360-Math.acos(cosH)/rad:Math.acos(cosH)/rad; H/=15;
      let UT=(H+RA-0.06571*t-6.622-lh)%24; if(UT<0)UT+=24;
      const base=Date.UTC(y,m-1,d)-lh*3600000;
      let ms=Date.UTC(y,m-1,d)+UT*3600000;
      while(ms<base)ms+=DAY; while(ms>=base+DAY)ms-=DAY;
      return new Date(ms);
    }
    let coords=null;
    const show=()=>{
      const opt=sn.city.selectedOptions[0];
      const lat=coords?coords.lat:+opt.dataset.lat, lng=coords?coords.lng:+opt.dataset.lng;
      const tz=coords?Intl.DateTimeFormat().resolvedOptions().timeZone:opt.dataset.tz;
      const tf=new Intl.DateTimeFormat('en-US',{hour:'numeric',minute:'2-digit',timeZone:tz});
      const first=parse(sn.date.value||iso(new Date()));
      const rows=[...Array(7)].map((_,i)=>{
        const d=add(first,i), y=d.getUTCFullYear(), m=d.getUTCMonth()+1, dd=d.getUTCDate();
        const r=sunUTC(y,m,dd,lat,lng,true), s=sunUTC(y,m,dd,lat,lng,false);
        return `<tr${i===0?' class="first"':''}><td>${short(d)}</td><td>${r?tf.format(r):'none'}</td><td>${s?tf.format(s):'none'}</td></tr>`;
      }).join('');
      out.innerHTML=`<p class="small">${coords?'Your location':esc(opt.textContent)} &middot; times in ${esc(tz.replace(/_/g,' '))}</p>
        <div class="table-wrap"><table class="sun"><thead><tr><th>Date</th><th>Sunrise</th><th>Sunset</th></tr></thead><tbody>${rows}</tbody></table></div>
        <p class="small">Approximate, within a minute or two. The <em>hefsek tahara</em> is done before sunset. Daytime is sunrise to sunset; nighttime is sunset to sunrise. For nightfall times, follow your community&rsquo;s calendar.</p>`;
    };
    if(!sn.date.value) sn.date.value=iso(new Date(Date.now()-new Date().getTimezoneOffset()*60000));
    sn.addEventListener('input',()=>{coords=null;show();});
    sn.addEventListener('submit',e=>{e.preventDefault();show();});
    const geo=$('#sun-geo');
    if(geo) geo.addEventListener('click',()=>{
      if(!navigator.geolocation){out.insertAdjacentHTML('afterbegin','<p class="warn">Location is not available in this browser. Choose a city instead.</p>');return;}
      geo.textContent='Finding you…';
      navigator.geolocation.getCurrentPosition(p=>{coords={lat:p.coords.latitude,lng:p.coords.longitude};geo.textContent='Use my location';show();},
        ()=>{geo.textContent='Use my location';out.insertAdjacentHTML('afterbegin','<p class="warn">We could not get your location. Choose the nearest city instead.</p>');},{timeout:10000});
    });
    show();
  }

  // ---------- 6. Glossary ----------
  const gq=$('#gloss-q');
  if(gq){
    const items=$$('#gloss-list > div');
    const empty=$('#gloss-empty');
    gq.addEventListener('input',()=>{
      const q=gq.value.trim().toLowerCase(); let n=0;
      items.forEach(it=>{const hit=!q||it.textContent.toLowerCase().includes(q);it.hidden=!hit;if(hit)n++;});
      empty.hidden=n>0;
    });
  }
})();
