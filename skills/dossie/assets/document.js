// Resumo, transcrição e PDF original são fontes distintas. Nunca completar uma transcrição por inferência.
Object.assign(names,{texto_integral:'Transcrição do documento',texto_integral_status:'Completude da transcrição',texto_integral_origem:'Origem da transcrição'});
const openEntityBeforeFullDocument=openEntity;
openEntity=function(id){
 openEntityBeforeFullDocument(id);
 const doc=index.get(id);if(!doc||doc.kind!=='documentos')return;
 const body=$('dialog-body'),section=el('section','document-full');section.setAttribute('aria-label','Íntegra do documento '+id);
 section.append(el('h3','','Íntegra do documento'));
 const full=typeof doc.texto_integral==='string'?doc.texto_integral:'',hasText=full.trim().length>0;
 const complete=doc.texto_integral_status==='COMPLETO'&&typeof doc.texto_integral_origem==='string'&&doc.texto_integral_origem.trim().length>0;
 if(hasText){
  section.append(el('p','document-completeness',complete?'Transcrição integral registrada. Confira a fidelidade com o original.':doc.texto_integral_status==='PARCIAL'?'Transcrição parcial: o texto abaixo não representa a íntegra.':'Texto disponível, com completude não confirmada.'));
  const content=el('pre','document-transcript',full);content.tabIndex=0;content.setAttribute('aria-label','Texto do documento '+id);section.append(content);
  field(section,'Origem da transcrição',doc.texto_integral_origem||'Não informada');
 }else section.append(el('p','document-missing','A íntegra não está incorporada neste dossiê. O resumo e o conteúdo registrado não substituem o documento completo. Vincule o PDF original para consultá-lo nesta janela.'));
 const summary=Array.from(body.querySelectorAll(':scope > .field')).find(node=>node.querySelector('dt')?.textContent==='Resumo');
 if(summary){const firstField=body.querySelector(':scope > .field');if(firstField&&firstField!==summary)firstField.before(summary);summary.after(section)}else body.prepend(section);
};
