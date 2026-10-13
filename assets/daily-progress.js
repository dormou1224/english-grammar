(function(){
const key='english-daily-scores-v1';
function read(){try{const value=JSON.parse(localStorage.getItem(key)||'{}');return value&&typeof value==='object'&&!Array.isArray(value)?value:{}}catch{return {}}}
window.saveDailyResult=function(result){const match=/^daily-(\d+)-quiz$/.exec(document.body.dataset.content||'');if(!match)return false;try{const data=read(),day=String(Number(match[1]));const attempts=Array.isArray(data[day])?data[day]:[];attempts.push({...result,date:new Date().toISOString()});data[day]=attempts.slice(-20);localStorage.setItem(key,JSON.stringify(data));return true}catch{return false}};
document.querySelectorAll('[data-day]').forEach(el=>{const attempts=read()[el.dataset.day];if(!Array.isArray(attempts)||!attempts.length)return;const last=attempts.at(-1);const best=attempts.reduce((a,b)=>a.score>b.score?a:b);el.textContent=`Τελευταία προσπάθεια: ${last.score}/${last.total} · Αναπάντητες: ${last.pending} · Καλύτερη: ${best.score}/${best.total} · Προσπάθειες: ${attempts.length}`});
})();
