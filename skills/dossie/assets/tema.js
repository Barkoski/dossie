/* Tema 2.0: tom por situação nos selos/cartões e ícones no menu. Não altera dados nem comportamento. */
(function(){
  var NS='http://www.w3.org/2000/svg';
  var ICONS={
    'visao geral':[['rect',{x:3,y:3,width:7,height:7,rx:2}],['rect',{x:14,y:3,width:7,height:7,rx:2}],['rect',{x:3,y:14,width:7,height:7,rx:2}],['rect',{x:14,y:14,width:7,height:7,rx:2}]],
    'documentos':[['path',{d:'M7 3h7l5 5v13H7z'}],['path',{d:'M14 3v5h5'}]],
    'provas':[['circle',{cx:11,cy:11,r:7}],['path',{d:'M20 20l-4-4'}]],
    'cronologia':[['circle',{cx:12,cy:12,r:9}],['path',{d:'M12 7v5l3 2'}]],
    'requisitos':[['path',{d:'M9 6h11M9 12h11M9 18h11'}],['path',{d:'M3.5 6l1.5 1.5L7 5M3.5 12l1.5 1.5L7 11M3.5 18l1.5 1.5L7 17'}]],
    'teses':[['path',{d:'M12 3v18M6 21h12'}],['path',{d:'M5 7h14'}],['path',{d:'M5 7l-3 7a3 3 0 006 0zM19 7l-3 7a3 3 0 006 0z'}]],
    'pendencias':[['circle',{cx:12,cy:12,r:9}],['path',{d:'M12 7v6M12 16.5v.5'}]]
  };
  function norm(t){return (t||'').normalize('NFD').replace(/[̀-ͯ]/g,'').toLowerCase().trim()}
  function tone(t){
    t=(t||'').normalize('NFD').replace(/[̀-ͯ]/g,'').toUpperCase().trim();
    if(!t||t==='?')return 'neu';
    if(/^NAO |SEM FONTE|ILEGIVEL|CONFLIT|CONTROVERT|CONTRADI/.test(t))return 'bad';
    if(/PARCIAL|DUVIDOS|PENDENTE|CONFERIR|^BAIXA/.test(t))return 'warn';
    if(/^FATO COMPROVADO|^COMPROVADO|^ORIGINAL CONFERIDO|TEXTO NITIDO|^ALTA/.test(t))return 'ok';
    if(/ALEGACAO|INFERENCIA|CONCLUSAO|TESE|^MEDIA/.test(t))return 'info';
    return 'neu';
  }
  function icon(shapes){
    var s=document.createElementNS(NS,'svg');
    var a={'class':'ico',viewBox:'0 0 24 24',fill:'none',stroke:'currentColor','stroke-width':'1.8','stroke-linecap':'round','stroke-linejoin':'round','aria-hidden':'true'};
    Object.keys(a).forEach(function(k){s.setAttribute(k,a[k])});
    shapes.forEach(function(sh){var e=document.createElementNS(NS,sh[0]);Object.keys(sh[1]).forEach(function(k){e.setAttribute(k,sh[1][k])});s.appendChild(e)});
    return s;
  }
  function paint(){
    document.querySelectorAll('.badge:not([data-tone])').forEach(function(b){b.dataset.tone=tone(b.textContent)});
    document.querySelectorAll('.req').forEach(function(r){var s=r.querySelector('.status');if(s&&!r.dataset.tone)r.dataset.tone=tone(s.textContent)});
    document.querySelectorAll('.nav button').forEach(function(b){
      if(b.querySelector('.ico'))return;
      var shapes=ICONS[norm(b.textContent)];if(!shapes)return;
      b.insertBefore(icon(shapes),b.firstChild);
    });
  }
  function start(){
    paint();
    var pending=false;
    new MutationObserver(function(){if(pending)return;pending=true;requestAnimationFrame(function(){pending=false;paint()})}).observe(document.body,{childList:true,subtree:true});
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',start);else start();
})();
