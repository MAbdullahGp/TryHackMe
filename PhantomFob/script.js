<script>
document.querySelectorAll('.fob button').forEach(btn=>{
 btn.addEventListener('click',async()=>{
  const b=btn.getAttribute('data-b'),m=document.getElementById('fobmsg');
  m.textContent='sending '+b+' …';
  try{const r=await fetch('/press',{method:'POST',headers:{'Content-Type':'application/json'},
    body:JSON.stringify({button:b})});const j=await r.json();
   m.textContent=(j.ok?'✓ ':'✗ ')+b+'  →  '+j.msg;}
  catch(e){m.textContent='✗ '+b+'  →  '+e;}
 });
});
// ---- build the speedometer gauge ----
const G=document.getElementById('gauge'),NS='http://www.w3.org/2000/svg';
const cx=140,cy=150,R=120,A0=-210,A1=30;                 // sweep 240deg
function pol(a,r){const rad=a*Math.PI/180;return[cx+r*Math.cos(rad),cy+r*Math.sin(rad)];}
for(let i=0;i<=14;i++){const a=A0+(A1-A0)*i/14;const[o1,o2]=pol(a,R);const[i1,i2]=pol(a,i%2?R-8:R-16);
 const l=document.createElementNS(NS,'line');l.setAttribute('x1',i1);l.setAttribute('y1',i2);
 l.setAttribute('x2',o1);l.setAttribute('y2',o2);l.setAttribute('stroke',i>11?'#f85149':'#3a4b5c');
 l.setAttribute('stroke-width',i%2?1.5:3);G.appendChild(l);
 if(i%2===0){const[tx,ty]=pol(a,R-30);const t=document.createElementNS(NS,'text');
  t.setAttribute('x',tx);t.setAttribute('y',ty+4);t.setAttribute('fill','#6f8296');
  t.setAttribute('font-size','11');t.setAttribute('text-anchor','middle');t.textContent=i*10;G.appendChild(t);}}
const needle=document.createElementNS(NS,'line');
needle.setAttribute('x1',cx);needle.setAttribute('y1',cy);needle.setAttribute('stroke','#f0883e');
needle.setAttribute('stroke-width',3.5);needle.setAttribute('stroke-linecap','round');G.appendChild(needle);
const hub=document.createElementNS(NS,'circle');hub.setAttribute('cx',cx);hub.setAttribute('cy',cy);
hub.setAttribute('r',7);hub.setAttribute('fill','#f0883e');G.appendChild(hub);
function setNeedle(k){const a=A0+(A1-A0)*Math.min(k,140)/140;const[x,y]=pol(a,R-18);
 needle.setAttribute('x2',x);needle.setAttribute('y2',y);}
setNeedle(0);

// ---- build the top-down car with four door locks ----
const C=document.getElementById('car');
function mk(t,a){const e=document.createElementNS(NS,t);for(const k in a)e.setAttribute(k,a[k]);return e;}
C.appendChild(mk('rect',{x:118,y:18,width:124,height:224,rx:44,fill:'#26333f',stroke:'#4a627a','stroke-width':2}));
C.appendChild(mk('rect',{x:134,y:46,width:92,height:44,rx:16,fill:'#0f171f'}));    // windshield
C.appendChild(mk('rect',{x:134,y:150,width:92,height:50,rx:16,fill:'#0f171f'}));   // rear window
C.appendChild(mk('rect',{x:146,y:100,width:68,height:44,rx:8,fill:'#0b1219'}));    // roof
// four door lock pads straddling the body edges: FL, FR, RL, RR
const pads=[[118,104],[242,104],[118,168],[242,168]];
const padEls=[];
pads.forEach(([x,y])=>{
 const r=mk('rect',{x:x-17,y:y-14,width:34,height:28,rx:7,stroke:'#0a0d11','stroke-width':2});
 const t=mk('text',{x:x,y:y+6,'text-anchor':'middle','font-size':'15','font-weight':'700'});
 C.appendChild(r);C.appendChild(t);padEls.push([r,t]);
});
function setDoors(locked){
 padEls.forEach(([r,t])=>{
  if(locked===null){r.setAttribute('fill','#33475a');t.textContent='';}
  else if(locked){r.setAttribute('fill','#f85149');t.textContent='\u{1F512}';}
  else{r.setAttribute('fill','#3fb950');t.textContent='\u{1F513}';}
 });
}
setDoors(null);

// ---- turn-signal blink ----
let turn=0,blink=false;
setInterval(()=>{blink=!blink;
 document.getElementById('tl').classList.toggle('on',turn===1&&blink);
 document.getElementById('tr').classList.toggle('on',turn===2&&blink);
},380);

// ---- live updates ----
const es=new EventSource('/events');
es.onmessage=e=>{const s=JSON.parse(e.data);
 setNeedle(s.speed||0);document.getElementById('kph').textContent=Math.round(s.speed||0);
 turn=s.turn||0;setDoors(s.locked);
 const d=document.getElementById('doors');
 d.textContent=s.locked===null?'…':(s.locked?'LOCKED':'UNLOCKED');
 d.className='val '+(s.locked===null?'mut':(s.locked?'bad':'ok'));
 const im=document.getElementById('immob');
 im.textContent=s.immob===null?'…':(s.immob?'ARMED':'DISARMED');
 im.className='val '+(s.immob===null?'mut':(s.immob?'ok':'warn'));
 const h=document.getElementById('horn');h.textContent=s.horn?'📢':'—';
 h.className='val '+(s.horn?'warn pulse':'mut');
 document.getElementById('fps').innerHTML=s.fps+'<span class=mut style="font-size:12px"> fps</span>';
 document.getElementById('ids').textContent=s.seen_ids;
 if(s.flag){document.getElementById('flagcard').style.display='block';
  document.getElementById('flag').textContent=s.flag;}
};
</script>