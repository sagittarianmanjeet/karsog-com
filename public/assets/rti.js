/* karsog.com — RTI page: filter by type, search, copy an application template, copy a link to a document. */
(function(){
  var chips=[].slice.call(document.querySelectorAll('.rti .chip[data-cat]')),docs=[].slice.call(document.querySelectorAll('.rti .doc')),
      groups=[].slice.call(document.querySelectorAll('.rti .group')),q=document.getElementById('q'),none=document.getElementById('none'),cat='all';
  function apply(){
    var t=(q.value||'').toLowerCase().trim(),shown=0;
    docs.forEach(function(d){var ok=(cat==='all'||d.getAttribute('data-cat')===cat)&&(!t||d.textContent.toLowerCase().indexOf(t)>-1);d.hidden=!ok;if(ok)shown++;});
    groups.forEach(function(g){g.hidden=!g.querySelector('.doc:not([hidden])');});
    none.hidden=shown>0;
  }
  chips.forEach(function(c){c.addEventListener('click',function(){chips.forEach(function(x){x.setAttribute('aria-pressed','false');});c.setAttribute('aria-pressed','true');cat=c.getAttribute('data-cat');apply();});});
  q.addEventListener('input',apply);
  function copyText(txt,btn,done){
    function ok(){var o=btn.textContent;btn.textContent=done;setTimeout(function(){btn.textContent=o;},1800);}
    if(navigator.clipboard&&window.isSecureContext){navigator.clipboard.writeText(txt).then(ok,fallback);}else{fallback();}
    function fallback(){var ta=document.createElement('textarea');ta.value=txt;ta.setAttribute('readonly','');ta.style.position='fixed';ta.style.opacity='0';document.body.appendChild(ta);ta.select();try{document.execCommand('copy');ok();}catch(e){}document.body.removeChild(ta);}
  }
  [].slice.call(document.querySelectorAll('.copy')).forEach(function(b){b.addEventListener('click',function(){copyText(document.getElementById(b.getAttribute('data-target')).textContent,b,b.getAttribute('data-done'));});});
  [].slice.call(document.querySelectorAll('.copylink')).forEach(function(b){b.addEventListener('click',function(){copyText(location.origin+location.pathname+'#'+b.getAttribute('data-id'),b,b.getAttribute('data-done'));});});
  var y=document.getElementById('y');if(y)y.textContent=new Date().getFullYear();
})();
