// Family Purity online reader: progress bar, text size, footnote keyboard access, glossary pop-ups, calendar.
(function(){
  const root=document.documentElement;

  // Reading progress
  const bar=document.querySelector('.progress');
  const onScroll=()=>{
    const max=document.documentElement.scrollHeight-innerHeight;
    if(bar) bar.style.width=(max>0?Math.min(100,scrollY/max*100):0)+'%';
  };
  addEventListener('scroll',onScroll,{passive:true}); onScroll();

  // Text size, remembered per reader
  const sizes=[1.1,1.2,1.3,1.42,1.56];
  let idx=2;
  try{const saved=parseInt(localStorage.getItem('fp-size'),10); if(sizes[saved]) idx=saved;}catch(e){}
  const apply=()=>{root.style.setProperty('--reader-size',sizes[idx]+'rem');try{localStorage.setItem('fp-size',idx)}catch(e){}};
  apply();
  document.querySelectorAll('[data-size]').forEach(b=>b.addEventListener('click',()=>{
    idx=Math.max(0,Math.min(sizes.length-1,idx+(b.dataset.size==='up'?1:-1)));apply();
  }));

  // Footnote labels are reachable by keyboard
  document.querySelectorAll('label.fn').forEach(l=>{
    l.tabIndex=0; l.setAttribute('role','button');
    l.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();l.click();}});
  });

  // Glossary pop-ups
  let pop=null;
  const close=()=>{if(pop){pop.remove();pop=null;}};
  document.querySelectorAll('.term').forEach(t=>t.addEventListener('click',e=>{
    e.stopPropagation();
    const wasThis=pop&&pop.dataset.for===t.textContent; close(); if(wasThis) return;
    pop=document.createElement('div'); pop.className='pop'; pop.dataset.for=t.textContent; pop.setAttribute('role','dialog');
    const h=document.createElement('b'); h.textContent=t.dataset.word||t.textContent;
    pop.append(h,document.createTextNode(t.dataset.def)); document.body.append(pop);
    const r=t.getBoundingClientRect(), w=pop.offsetWidth;
    pop.style.left=Math.max(12,Math.min(scrollX+r.left,scrollX+innerWidth-w-12))+'px';
    pop.style.top=(scrollY+r.bottom+8)+'px';
  }));
  document.addEventListener('click',close);
  document.addEventListener('keydown',e=>{if(e.key==='Escape')close();});

  // Calendar diagram
  const info=document.querySelector('.cal-info');
  const days=document.querySelectorAll('.day');
  days.forEach(d=>d.addEventListener('click',()=>{
    days.forEach(x=>x.setAttribute('aria-pressed','false'));
    d.setAttribute('aria-pressed','true');
    if(info) info.innerHTML=d.dataset.info;
  }));
})();
