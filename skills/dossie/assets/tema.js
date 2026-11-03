/* Tema 1.8: marca selos e cartões com o tom da situação, sem alterar dados. */
(function(){
  function tone(t){
    t=(t||'').normalize('NFD').replace(/[̀-ͯ]/g,'').toUpperCase().trim();
    if(!t||t==='?')return 'neu';
    if(/^NAO |SEM FONTE|ILEGIVEL|CONFLIT|CONTROVERT|CONTRADI/.test(t))return 'bad';
    if(/PARCIAL|DUVIDOS|PENDENTE|CONFERIR|^BAIXA/.test(t))return 'warn';
    if(/^FATO COMPROVADO|^COMPROVADO|^ORIGINAL CONFERIDO|TEXTO NITIDO|^ALTA/.test(t))return 'ok';
    if(/ALEGACAO|INFERENCIA|CONCLUSAO|TESE|^MEDIA/.test(t))return 'info';
    return 'neu';
  }
  function paint(){
    document.querySelectorAll('.badge:not([data-tone])').forEach(function(b){b.dataset.tone=tone(b.textContent)});
    document.querySelectorAll('.req').forEach(function(r){var s=r.querySelector('.status');if(s&&!r.dataset.tone)r.dataset.tone=tone(s.textContent)});
  }
  function start(){
    paint();
    var pending=false;
    new MutationObserver(function(){if(pending)return;pending=true;requestAnimationFrame(function(){pending=false;paint()})}).observe(document.body,{childList:true,subtree:true});
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',start);else start();
})();
