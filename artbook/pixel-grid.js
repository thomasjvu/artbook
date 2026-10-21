/* Integer-scale pixel inspection; grid is drawn at actual texel boundaries. */
for(const figure of document.querySelectorAll('figure.pixel')){
 const img=figure.querySelector('img');if(!img)continue;
 const panel=document.createElement('details');panel.className='pixel-inspector';
 const title=document.createElement('summary');title.textContent='Pixel grid / inspect native pixels';panel.append(title);
 const controls=document.createElement('div');const zoom=document.createElement('select');zoom.setAttribute('aria-label','Integer pixel zoom');
 for(const n of [1,2,4,8]){const o=new Option(n+'×',n,n===4,n===4);zoom.add(o)}
 const label=document.createElement('label'),grid=document.createElement('input');grid.type='checkbox';grid.checked=true;label.append(grid,' Pixel grid');
 const viewport=document.createElement('div');viewport.className='pixel-viewport';const canvas=document.createElement('canvas');viewport.append(canvas);
 const info=document.createElement('p');controls.append(zoom,label);panel.append(controls,info,viewport);figure.append(panel);
 function draw(){if(!img.naturalWidth)return;const z=Number(zoom.value),w=img.naturalWidth,h=img.naturalHeight;canvas.width=w*z;canvas.height=h*z;const c=canvas.getContext('2d');c.imageSmoothingEnabled=false;c.clearRect(0,0,canvas.width,canvas.height);c.drawImage(img,0,0,canvas.width,canvas.height);
 if(grid.checked&&z>=2){c.strokeStyle='rgba(55,65,75,.28)';c.lineWidth=1;c.beginPath();for(let x=0;x<=w;x++){c.moveTo(x*z+.5,0);c.lineTo(x*z+.5,h*z)}for(let y=0;y<=h;y++){c.moveTo(0,y*z+.5);c.lineTo(w*z,y*z+.5)}c.stroke()}
 info.textContent=w+' × '+h+' native pixels · '+z+'× nearest · grid = one source pixel';}
 zoom.onchange=grid.onchange=draw;img.addEventListener('load',draw);draw();
}
