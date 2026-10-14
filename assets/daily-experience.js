(function(root){
class PracticeClock{
 constructor(now=()=>performance.now()){this.now=now;this.accumulated=0;this.running=false;this.active=false}
 start(){this.accumulated=0;this.started=this.now();this.running=true;this.active=true}
 pause(){if(this.active){this.accumulated+=this.now()-this.started;this.active=false}}
 resume(){if(this.running&&!this.active){this.started=this.now();this.active=true}}
 seconds(){return Math.floor((this.accumulated+(this.active?this.now()-this.started:0))/1000)}
 stop(){this.pause();this.running=false;return this.seconds()}
}
root.PracticeClock=PracticeClock;if(typeof module!=='undefined')module.exports={PracticeClock};if(typeof document==='undefined')return;
const match=/^daily-(\d+)-quiz$/.exec(document.body.dataset.content||'');if(!match)return;
const day=String(Number(match[1])),clock=new PracticeClock(),played=new Set();let ticker=null,dialog=null,rewardTick=null,rewardTimeout=null,returnFocus=null,rewardButton=null;
function node(tag,text,cls){const el=document.createElement(tag);if(text)el.textContent=text;if(cls)el.className=cls;return el}
function updateClock(){const el=document.getElementById('practice-time');if(el){const n=clock.seconds();el.textContent=`${String(Math.floor(n/60)).padStart(2,'0')}:${String(n%60).padStart(2,'0')}`}}
function start(){clock.start();if(document.hidden)clock.pause();clearInterval(ticker);ticker=setInterval(updateClock,1000);updateClock()}
function stop(){const seconds=clock.stop();clearInterval(ticker);ticker=null;updateClock();return seconds}
function closeReward(){clearInterval(rewardTick);clearTimeout(rewardTimeout);rewardTick=null;rewardTimeout=null;if(!dialog)return;const current=dialog;dialog=null;current.remove();if(rewardButton){rewardButton.disabled=true;rewardButton.textContent='🏅 Το μικρό διάλειμμα ολοκληρώθηκε';rewardButton=null}if(!document.hidden)clock.resume();if(returnFocus&&returnFocus.isConnected&&!returnFocus.disabled)returnFocus.focus();else{const heading=document.getElementById('app')?.querySelector('h2');if(heading){heading.tabIndex=-1;heading.focus()}}}
function play(button){if(played.has(day)||!root.DailyScores||root.DailyScores.perfectCount(day)<3)return;played.add(day);clock.pause();rewardButton=button;returnFocus=document.activeElement;dialog=document.createElement('dialog');dialog.className='goalkeeper-dialog';dialog.setAttribute('aria-labelledby','reward-title');
const top=node('div',undefined,'reward-heading'),title=node('h2','Ο Ροκ Τερματοφύλακας!');title.id='reward-title';const close=node('button','Κλείσιμο ×','secondary');close.onclick=closeReward;top.append(title,close);dialog.append(top,node('p','Τρία 10/10! Χατ τρικ γνώσεων!','reward-intro'));
const scene=node('div',undefined,'reward-scene playing');scene.setAttribute('aria-hidden','true');const goal=node('div',undefined,'goal-net'),lion=node('div',undefined,'lion-goalie');lion.append(node('span','🦁','lion-head'),node('span','1','lion-shirt'),node('span','🧤','glove glove-left'),node('span','🧤','glove glove-right'),node('span','🎸','tiny-guitar'));scene.append(goal,lion);for(let i=1;i<=3;i++)scene.append(node('span','⚽','reward-ball ball-'+i));scene.append(node('span','🎩','funny-hat'));dialog.append(scene);
const line=node('p','Τρεις μπάλες, τρεις αποκρούσεις!','reward-line'),learning=node('p','go → went → gone','reward-learning'),remaining=node('small','Το διάλειμμα κλείνει σε 20 δευτερόλεπτα.');dialog.append(line,learning,remaining,node('p','Μια μικρή κινούμενη επιβράβευση, χωρίς ήχο.','reward-note'));document.body.append(dialog);dialog.addEventListener('cancel',e=>{e.preventDefault();closeReward()});
if(typeof dialog.showModal==='function')dialog.showModal();else{dialog.setAttribute('open','');dialog.setAttribute('role','dialog');dialog.setAttribute('aria-modal','true')}close.focus();const started=performance.now();
function tick(){const sec=Math.floor((performance.now()-started)/1000);if(sec>=20){closeReward();return}remaining.textContent=`Το διάλειμμα κλείνει σε ${20-sec} δευτερόλεπτα.`;line.textContent=sec<5?'Τρεις μπάλες, τρεις αποκρούσεις!':sec<10?'Go, went, gone — keep learning on!':sec<15?'Δυνατή απόκρουση, δυνατή προσπάθεια!':sec<19?'Το καπέλο; Αυτή δεν ήταν στην ύλη!':'🏅 Το κατέκτησες!';learning.textContent=sec<10?'go → went → gone':'see → saw → seen'}
rewardTick=setInterval(tick,250);rewardTimeout=setTimeout(closeReward,20000)}
function addReward(container){if(!container)return;if(!root.DailyScores||root.DailyScores.perfectCount(day)<3)return;const box=node('section',undefined,'mastery-panel');box.append(node('h3','🏅 Το κατέκτησα!'),node('p','Πέτυχες τουλάχιστον τρία 10/10 σε αυτή την ημέρα.'));const button=node('button',played.has(day)?'Το διάλειμμα προβλήθηκε σε αυτή την επίσκεψη':'⚽ Άνοιξε το μικρό σου διάλειμμα (20″)','primary');button.disabled=played.has(day);button.onclick=()=>play(button);box.append(button);container.append(box)}
document.addEventListener('visibilitychange',()=>{if(document.hidden){clock.pause();closeReward()}else clock.resume();updateClock()});window.addEventListener('pagehide',()=>{clearInterval(ticker);closeReward()});root.DailyExperience={start,stop,addReward};addReward(document.getElementById('daily-history'));
})(globalThis);
