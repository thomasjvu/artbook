/* Native integer lattice: pixels, animation cells and anchors share one origin. */
for(const figure of document.querySelectorAll('figure.pixel')){
 const img=figure.querySelector('img');if(!img)continue;
 const meta=JSON.parse(figure.dataset.grid||'{}');
 const panel=document.createElement('section');panel.className='pixel-inspector';
 const controls=document.createElement('div');const zoom=document.createElement('select');zoom.setAttribute('aria-label','Integer pixel zoom');
 for(const n of [1,2,4,8])zoom.add(new Option(n+'×',n,n===4,n===4));
 const label=document.createElement('label'),grid=document.createElement('input');grid.type='checkbox';grid.checked=true;label.append(grid,' Pixel grid');
 const cell=document.createElement('select');cell.setAttribute('aria-label','Animation cel');cell.add(new Option('Full sheet','-1'));
 if(meta.cell_size)for(let i=0;i<(meta.columns||4)*(meta.rows||2);i++)cell.add(new Option('Cel '+String(i+1).padStart(2,'0'),i));
 const guideLabel=document.createElement('label'),guides=document.createElement('input');guides.type='checkbox';guides.checked=true;guideLabel.append(guides,' Cells / anchors');
 const viewport=document.createElement('div');viewport.className='pixel-viewport';const canvas=document.createElement('canvas');viewport.append(canvas);
 const info=document.createElement('p'),readout=document.createElement('p');readout.textContent='Point at a pixel to inspect its coordinates and RGBA.';
 controls.append(zoom,cell,label,guideLabel);panel.append(controls,info,readout,viewport);img.after(panel);img.classList.add('pixel-fallback');
 const raw=document.createElement('canvas');let crop=[0,0,0,0];
 function draw(){if(!img.naturalWidth)return;const z=Number(zoom.value),cw=meta.cell_size?.[0]||img.naturalWidth,ch=meta.cell_size?.[1]||img.naturalHeight,i=Number(cell.value);crop=i<0?[0,0,img.naturalWidth,img.naturalHeight]:[i%(meta.columns||4)*cw,Math.floor(i/(meta.columns||4))*ch,cw,ch];const [sx,sy,w,h]=crop;
 canvas.width=w*z;canvas.height=h*z;const c=canvas.getContext('2d');c.imageSmoothingEnabled=false;c.clearRect(0,0,canvas.width,canvas.height);c.drawImage(img,sx,sy,w,h,0,0,w*z,h*z);
 if(grid.checked&&z>=2){c.strokeStyle='rgba(55,65,75,.25)';c.lineWidth=1;c.beginPath();for(let x=0;x<=w;x++){c.moveTo(x*z+.5,0);c.lineTo(x*z+.5,h*z)}for(let y=0;y<=h;y++){c.moveTo(0,y*z+.5);c.lineTo(w*z,y*z+.5)}c.stroke()}
 if(guides.checked&&meta.cell_size){c.strokeStyle='#ce4668';c.lineWidth=1;for(let y=0;y<h;y+=ch)for(let x=0;x<w;x+=cw){c.strokeRect(x*z+.5,y*z+.5,cw*z,ch*z);if(meta.anchor){const ax=(x+meta.anchor[0])*z,ay=(y+meta.anchor[1])*z;c.beginPath();c.moveTo(ax-6,ay);c.lineTo(ax+6,ay);c.moveTo(ax,ay-6);c.lineTo(ax,ay+6);c.stroke()}}}
 info.textContent=w+' × '+h+' native pixels · '+z+'× nearest · 1 grid square = 1 pixel'+(meta.cell_size?' · cells '+cw+' × '+ch:'');
 raw.width=img.naturalWidth;raw.height=img.naturalHeight;raw.getContext('2d').drawImage(img,0,0);figure.classList.add('grid-ready');}
 canvas.onpointermove=e=>{const r=canvas.getBoundingClientRect(),z=Number(zoom.value),x=Math.floor((e.clientX-r.left)/z),y=Math.floor((e.clientY-r.top)/z);if(x<0||y<0||x>=crop[2]||y>=crop[3])return;try{const rgba=raw.getContext('2d').getImageData(x+crop[0],y+crop[1],1,1).data;readout.textContent='Pixel ('+x+', '+y+') · sheet ('+(x+crop[0])+', '+(y+crop[1])+') · RGBA '+Array.from(rgba).join(', ')}catch{readout.textContent='Pixel ('+x+', '+y+') · browser restricts local-image color reads; use the linked original for editing.'}};
 zoom.onchange=cell.onchange=grid.onchange=guides.onchange=draw;img.addEventListener('load',draw);draw();
}
