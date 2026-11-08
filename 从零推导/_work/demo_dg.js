(function(){
  function ready(fn){ if(document.readyState!=='loading'){ fn(); } else { document.addEventListener('DOMContentLoaded', fn); } }

  function txt(el, s){ if(el){ el.textContent = s; } }

  function cotOf(ax,ay,bx,by,cx,cy){
    // 角在 (cx,cy)，两边指向 (ax,ay) 与 (bx,by)
    var ux=ax-cx, uy=ay-cy, vx=bx-cx, vy=by-cy;
    var dot=ux*vx+uy*vy, cr=ux*vy-uy*vx;
    if(Math.abs(cr)<1e-9){ return 0; }
    return dot/cr;
  }

  function drawCot(){
    var cv=document.getElementById('cv-cot'); if(!cv) return;
    var sl=document.getElementById('sl-cot'), out=document.getElementById('out-cot');
    var ctx=cv.getContext('2d');
    function draw(){
      var v=+sl.value, h=15+v*1.5, b=190;
      var A=[50,190], B=[430,190], C=[240,190-h];
      ctx.clearRect(0,0,cv.width,cv.height);
      ctx.fillStyle='#f3f6fa'; ctx.fillRect(0,0,cv.width,cv.height);
      ctx.strokeStyle='#c9d6e6'; ctx.lineWidth=1;
      ctx.beginPath(); ctx.moveTo(0,190); ctx.lineTo(cv.width,190); ctx.stroke();
      ctx.strokeStyle='#2f6fb2'; ctx.lineWidth=2;
      ctx.beginPath(); ctx.moveTo(A[0],A[1]); ctx.lineTo(B[0],B[1]); ctx.lineTo(C[0],C[1]); ctx.closePath(); ctx.stroke();
      var ang=2*Math.atan(b/h);
      var cot=Math.cos(ang)/Math.sin(ang);
      ctx.fillStyle='#333'; ctx.font='14px sans-serif';
      ctx.fillText('顶角 '+(ang*180/Math.PI).toFixed(1)+'°', C[0]+8, C[1]+34);
      txt(out, 'cot = '+cot.toFixed(3)+(cot<0?'（钝角 → 负权重）':'（锐角 → 正权重）')+'   高 '+h.toFixed(0));
    }
    sl.addEventListener('input', draw); draw();
  }

  function drawTri(){
    var cv=document.getElementById('cv-tri'); if(!cv) return;
    var sl=document.getElementById('sl-tri'), out=document.getElementById('out-tri');
    var ctx=cv.getContext('2d');
    function draw(){
      var v=+sl.value, cx=240+v*2.2;
      var A=[60,180], B=[420,180], C=[cx,70], D=[240,265];
      ctx.clearRect(0,0,cv.width,cv.height);
      ctx.fillStyle='#f3f6fa'; ctx.fillRect(0,0,cv.width,cv.height);
      ctx.strokeStyle='#c9d6e6'; ctx.beginPath(); ctx.moveTo(A[0],A[1]); ctx.lineTo(B[0],B[1]); ctx.stroke();
      ctx.strokeStyle='#2f6fb2'; ctx.lineWidth=2;
      ctx.beginPath(); ctx.moveTo(A[0],A[1]); ctx.lineTo(C[0],C[1]); ctx.lineTo(B[0],B[1]); ctx.stroke();
      ctx.strokeStyle='#c56a2c';
      ctx.beginPath(); ctx.moveTo(A[0],A[1]); ctx.lineTo(D[0],D[1]); ctx.lineTo(B[0],B[1]); ctx.stroke();
      var ca=cotOf(A[0],A[1],B[0],B[1],C[0],C[1]);
      var cb=cotOf(A[0],A[1],B[0],B[1],D[0],D[1]);
      var al=Math.atan2(Math.abs((B[0]-A[0])*(C[1]-A[1])-(B[1]-A[1])*(C[0]-A[0])), 1);
      ctx.fillStyle='#333'; ctx.font='14px sans-serif';
      ctx.fillText('cot α = '+ca.toFixed(3), 66, 210);
      ctx.fillText('cot β = '+cb.toFixed(3), 66, 232);
      txt(out, '边权重 = cot α + cot β = '+(ca+cb).toFixed(3));
    }
    sl.addEventListener('input', draw); draw();
  }

  function drawRing(){
    var cv=document.getElementById('cv-ring'); if(!cv) return;
    var sl=document.getElementById('sl-ring'), out=document.getElementById('out-ring');
    var ctx=cv.getContext('2d');
    function draw(){
      var n=+sl.value, cx=240, cy=125, R=82;
      ctx.clearRect(0,0,cv.width,cv.height);
      ctx.fillStyle='#f3f6fa'; ctx.fillRect(0,0,cv.width,cv.height);
      var per=60*Math.PI/180;
      var start=-Math.PI/2;
      for(var i=0;i<n;i++){
        var a0=start+i*per, a1=a0+per;
        ctx.beginPath(); ctx.moveTo(cx,cy);
        ctx.arc(cx,cy,R,a0,a1); ctx.closePath();
        ctx.fillStyle = i%2? '#9ec2e6':'#7fb0dc'; ctx.fill();
        ctx.strokeStyle='#2f6fb2'; ctx.lineWidth=1; ctx.stroke();
      }
      var used=n*60;
      if(used<360){
        var a0=start+n*per, a1=start+2*Math.PI;
        ctx.beginPath(); ctx.moveTo(cx,cy);
        ctx.arc(cx,cy,R,a0,a1); ctx.closePath();
        ctx.fillStyle='rgba(220,80,80,.18)'; ctx.fill();
        ctx.setLineDash([4,4]); ctx.strokeStyle='#c0392b'; ctx.stroke(); ctx.setLineDash([]);
      }
      var K=(360-used);
      ctx.fillStyle='#333'; ctx.font='14px sans-serif';
      ctx.fillText('绕一圈：'+n+' × 60° = '+used+'°', 12, 20);
      txt(out, '角度和 Σθ = '+used+'°   K = 360° − Σθ = '+K+'°   '+(K>0?'（球面型，正曲率）':(K===0?'（平面）':'（马鞍型，负曲率）')));
    }
    sl.addEventListener('input', draw); draw();
  }

  function drawK(){
    var cv=document.getElementById('cv-k'); if(!cv) return;
    var sl=document.getElementById('sl-k'), out=document.getElementById('out-k');
    var ctx=cv.getContext('2d');
    function draw(){
      var sel=+sl.value;
      ctx.clearRect(0,0,cv.width,cv.height);
      ctx.fillStyle='#f3f6fa'; ctx.fillRect(0,0,cv.width,cv.height);
      var x0=60, w=52, gap=14, base=190;
      ctx.strokeStyle='#999'; ctx.beginPath(); ctx.moveTo(40,base); ctx.lineTo(460,base); ctx.stroke();
      ctx.fillStyle='#333'; ctx.font='13px sans-serif';
      for(var n=3;n<=8;n++){
        var K=360-60*n;
        var hgt=Math.abs(K)*0.38;
        var x=x0+(n-3)*(w+gap);
        ctx.fillStyle = n===sel ? (K>0?'#2f6fb2':(K<0?'#c0392b':'#7a8a9a')) : '#c7d5e4';
        if(K>=0){ ctx.fillRect(x, base-hgt, w, hgt); } else { ctx.fillRect(x, base, w, hgt); }
        ctx.fillStyle='#333'; ctx.fillText('n='+n, x+8, base+16);
        ctx.fillText(K+'°', x+10, K>=0? base-hgt-6 : base+hgt+14);
      }
      txt(out, 'n = '+sel+'：K = 360° − '+(60*sel)+'° = '+(360-60*sel)+'°');
    }
    sl.addEventListener('input', draw); draw();
  }

  ready(function(){ drawCot(); drawTri(); drawRing(); drawK(); });
})();
