// Family Purity online reader: progress bar, text size, footnote keyboard access, glossary pop-ups, calendar.
(function(){
  const root=document.documentElement;
  document.querySelectorAll('[data-em]').forEach(el=>{const [u,d]=el.dataset.em.split('|'),a=u+'@'+d,s=el.dataset.subject;if(el.tagName==='A')el.href='mailto:'+a+(s?'?subject='+encodeURIComponent(s):'');if(el.hasAttribute('data-em-text'))el.textContent=a;});

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

  // Highlight search words when arriving from the search page (?q=...)
  const q=new URLSearchParams(location.search).get('q');
  const article=document.querySelector('.text');
  if(q&&article){
    const fold=x=>x.normalize('NFD').replace(/[̀-ͯ]/g,'').replace(/[’‘]/g,"'").toLowerCase();
    const terms=fold(q).split(/\s+/).filter(t=>t.length>1);
    const walker=document.createTreeWalker(article,NodeFilter.SHOW_TEXT,{acceptNode:n=>n.parentNode.closest('label,button,script,style,mark')?NodeFilter.FILTER_REJECT:NodeFilter.FILTER_ACCEPT});
    const nodes=[]; while(walker.nextNode()) nodes.push(walker.currentNode);
    const hits=[];
    nodes.forEach(n=>{
      const f=fold(n.nodeValue); if(f.length!==n.nodeValue.length) return;
      const ranges=[]; terms.forEach(t=>{let i=f.indexOf(t);while(i>=0){ranges.push([i,i+t.length]);i=f.indexOf(t,i+t.length);}});
      if(!ranges.length) return;
      ranges.sort((a,b)=>a[0]-b[0]);
      const frag=document.createDocumentFragment(); let pos=0;
      ranges.forEach(([a,b])=>{ if(a<pos) return; frag.append(n.nodeValue.slice(pos,a)); const m=document.createElement('mark'); m.className='hit'; m.textContent=n.nodeValue.slice(a,b); frag.append(m); hits.push(m); pos=b; });
      frag.append(n.nodeValue.slice(pos)); n.parentNode.replaceChild(frag,n);
    });
    if(hits.length){
      hits.forEach(m=>{const sn=m.closest('.sn'); if(sn&&sn.previousElementSibling&&sn.previousElementSibling.matches('.fn-t')) sn.previousElementSibling.checked=true;});
      const bar=document.createElement('div'); bar.className='hitbar'; let k=0;
      bar.innerHTML=`<span>${hits.length} ${hits.length===1?'match':'matches'} for “<b></b>”</span><button type="button" data-a="next">Next</button><a href="../search.html?q=${encodeURIComponent(q)}">Back to results</a>`;
      bar.querySelector('b').textContent=q; document.body.append(bar);
      const go=()=>{hits.forEach(h=>h.classList.remove('cur')); hits[k].classList.add('cur'); hits[k].scrollIntoView({block:'center'});};
      bar.querySelector('[data-a=next]').addEventListener('click',()=>{k=(k+1)%hits.length;go();});
      setTimeout(go,300);
    }
  }
})();

// Study Guide quiz: a "Test yourself" card at the end of chapters that have a quiz
(function(){
  const quizzes={'niddah':'../quiz-niddah.html','source-of-niddah':'../quiz-niddah.html','gynecological-considerations':'../quiz-niddah.html'};
  const slug=location.pathname.split('/').pop().replace(/\.html$/,'');
  const href=quizzes[slug]; if(!href) return;
  const end=document.querySelector('aside.end .end-card'); if(!end) return;
  const card=document.createElement('div');
  card.className='end-card'; card.style.marginTop='1.25rem';
  card.innerHTML='<h2>Test yourself</h2><p>21 review questions on Chapter 2, Niddah, from the <em>Study Guide for Choson &amp; Kallah</em>. Nothing you answer is saved.</p><div class="btn-row"><a class="btn btn-solid" href="'+href+'">Take the Niddah quiz</a></div>';
  end.after(card);
})();
