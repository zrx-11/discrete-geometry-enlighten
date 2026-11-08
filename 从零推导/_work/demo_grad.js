(function(){
  function ready(fn){ if(document.readyState!=='loading'){ fn(); } else { document.addEventListener('DOMContentLoaded', fn); } }

  function drawChain(){
    var cv=document.getElementById('cv-chain'); if(!cv) return;
    var sl=document.getElementById('sl-chain'), out=document.getElementById('out-chain');
    var ctx=cv.getContext('2d');
    function draw(){
      var T=(+sl.value)/10;          // 末端位置，2.0 .. 6.0
      var L=220;                      // 画布上的像素长度
      var x0=60, y=150;
      var sc=L/T;
      var pts=[0, T/3, 2*T/3, T];
      ctx.clearRect(0,0,cv.width,cv.height);
      ctx.fillStyle='#f3f6fa'; ctx.fillRect(0,0,cv.width,cv.height);
      ctx.strokeStyle='#c9d6e6'; ctx.lineWidth=1;
      ctx.beginPath(); ctx.moveTo(40,y); ctx.lineTo(460,y); ctx.stroke();
      // 原位置（灰）
      ctx.fillStyle='#b9c6d6';
      for(var i=0;i<4;i++){
        var ox=x0+i*(140/3)*1.0;
        ctx.beginPath(); ctx.arc(ox,y-26,4,0,6.284); ctx.fill();
      }
      ctx.fillStyle='#8a97a6'; ctx.font='12px sans-serif';
      ctx.fillText('灰色：原来 0,1,2,3', 40, y-40);
      // 解
      ctx.strokeStyle='#2f6fb2'; ctx.lineWidth=2;
      ctx.beginPath();
      for(var i=0;i<4;i++){
        var px=x0+pts[i]*sc;
        if(i===0){ ctx.moveTo(px,y); } else { ctx.lineTo(px,y); }
      }
      ctx.stroke();
      for(var i=0;i<4;i++){
        var px=x0+pts[i]*sc;
        ctx.fillStyle= (i===0||i===3) ? '#c0392b' : '#2f6fb2';
        ctx.beginPath(); ctx.arc(px,y,6,0,6.284); ctx.fill();
        ctx.fillStyle='#333'; ctx.font='13px sans-serif';
        ctx.fillText(pts[i].toFixed(2), px-10, y+24);
      }
      var seg=T/3;
      out.textContent='末端 = '+T.toFixed(1)+'    三段长度 = '+seg.toFixed(2)+' / '+seg.toFixed(2)+' / '+seg.toFixed(2)+'    （首末固定，中间按“保差分”重新分布）';
    }
    sl.addEventListener('input', draw); draw();
  }

  ready(drawChain);
})();
