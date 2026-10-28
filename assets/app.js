/* GeoCAD V2.2: keyboard-friendly search, result feedback, code copy and scroll control */
(()=>{'use strict';
const search=document.getElementById('search');
const filter=document.getElementById('filter');
const cards=Array.from(document.querySelectorAll('[data-category]'));
const empty=document.getElementById('empty');
const status=document.getElementById('results-status');
let counter=0;
function refresh(){const query=(search?.value||'').trim().toLocaleLowerCase();const category=filter?.value||'';let found=0;for(const card of cards){const show=(!query||card.textContent.toLocaleLowerCase().includes(query))&&(!category||card.dataset.category===category);card.hidden=!show;if(show)found++;}if(empty)empty.hidden=found!==0;if(status)status.textContent=String(found)+' / '+cards.length+(document.documentElement.lang==='ar'?' أداة':' tools');}
search?.addEventListener('input',refresh);
filter?.addEventListener('change',refresh);
search?.addEventListener('keydown',e=>{if(e.key==='Escape'){search.value='';refresh();search.blur();}});
if(cards.length)refresh();
const buttons=document.querySelectorAll('[data-copy]');
for(const button of buttons){const original=button.textContent;button.addEventListener('click',async()=>{const code=document.getElementById('code');if(!code)return;try{if(!navigator.clipboard?.writeText)throw new Error('Clipboard unsupported');await navigator.clipboard.writeText(code.textContent);button.textContent=button.dataset.done||'Copied';}catch{const selection=window.getSelection();const range=document.createRange();range.selectNodeContents(code);selection.removeAllRanges();selection.addRange(range);button.textContent=button.dataset.manual||'Selected';}window.setTimeout(()=>{button.textContent=original;},2200);});}
const back=document.getElementById('back-top');
if(back){const update=()=>{back.hidden=window.scrollY<350};window.addEventListener('scroll',update,{passive:true});update();back.addEventListener('click',()=>window.scrollTo({top:0,behavior:'smooth'}));}
})();
