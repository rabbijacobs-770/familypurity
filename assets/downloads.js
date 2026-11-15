// Counts PDF downloads with GoatCounter (familypurity.goatcounter.com).
// Only downloads are counted here; page visits stay in Cloudflare Web Analytics.
// No cookies, no personal data.
(function(){
  var CODE='familypurity';
  window.goatcounter={no_onload:true};
  var s=document.createElement('script');
  s.async=true;
  s.src='https://gc.zgo.at/count.js';
  s.setAttribute('data-goatcounter','https://'+CODE+'.goatcounter.com/count');
  document.head.appendChild(s);

  function hit(e){
    if(e.type==='auxclick'&&e.button!==1) return; // middle-click only
    var a=e.target.closest&&e.target.closest('a[href$=".pdf"]');
    if(!a||!window.goatcounter||!window.goatcounter.count) return;
    var file=a.getAttribute('href').split('/').pop();
    window.goatcounter.count({
      path:'download/'+file,
      title:'Download: '+file,
      referrer:location.href,
      event:true
    });
  }
  document.addEventListener('click',hit);
  document.addEventListener('auxclick',hit);
})();
