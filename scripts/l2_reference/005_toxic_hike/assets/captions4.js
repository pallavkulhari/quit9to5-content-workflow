/* Quit 9to5 captions v4: a separate caption ZONE, lower than v3.
   A soft rounded band sits at y 1250-1390 (x 72-948, clear of the Reels right-side icons and the bottom 420 px UI).
   Usage: window.addCaptions4(tl, chunks, {theme:"ink"|"tape", lastEnd:N})
   ink  = near-black pill #1C1A18 (92%), cream text #F6F1E7, spoken word in soft coral #FF8A7A  (L1, L2)
   tape = torn masking-tape strip (#E9DFC6 with soft shadow), graphite text #2B2A28, spoken word red pencil #C8322F (P1)
   Text: Inter Tight 700, 50 px, sentence case (in-graphic labels must use other fonts/sizes). One chunk at a time, instant swap,
   upcoming words at 35%, spoken words 100%, current word in the accent colour. */
(function(){
  window.addCaptions4=function(tl,chunks,o){
    o=o||{}; var tape=o.theme==="tape";
    var root=document.getElementById("root");
    var band=document.createElement("div"); band.id="capband";
    band.style.cssText="position:absolute;left:72px;width:876px;top:1250px;height:140px;z-index:60;border-radius:"+(tape?"6px":"70px")+";"+
      (tape?"background:#E9DFC6;box-shadow:0 6px 14px rgba(60,45,20,0.18);transform-origin:50% 50%;":"background:rgba(28,26,24,0.92);box-shadow:0 10px 30px rgba(0,0,0,0.12);")+
      "opacity:0;";
    root.appendChild(band);
    var st=document.createElement("style");
    st.textContent="#capband .cw{opacity:.35}#capband .cw.on{opacity:1}#capband .cw.cur{color:"+(tape?"#C8322F":"#FF8A7A")+"}";
    document.head.appendChild(st);
    tl.fromTo(band,{opacity:0,y:20},{opacity:1,y:0,duration:0.4,ease:"power2.out"},Math.max(0,chunks[0].s-0.3));
    if(tape) tl.set(band,{rotation:-0.8},0);
    chunks.forEach(function(ch,i){
      var line=document.createElement("div");
      line.style.cssText="position:absolute;left:0;right:0;top:0;height:140px;line-height:140px;text-align:center;white-space:nowrap;opacity:0;"+
        "font-family:'Inter Tight',sans-serif;font-weight:700;font-size:50px;letter-spacing:-0.01em;color:"+(tape?"#2B2A28":"#F6F1E7")+";";
      var sp=ch.words.map(function(w,k){var s=document.createElement("span");s.className="cw";s.textContent=w.t+(k<ch.words.length-1?" ":"");line.appendChild(s);return s;});
      band.appendChild(line);
      var start=Math.max(0,ch.s-0.05), end=(i+1<chunks.length)?Math.max(0,chunks[i+1].s-0.05):(o.lastEnd||ch.e+0.8);
      tl.fromTo(line,{opacity:0},{opacity:1,duration:0.12,ease:"power1.out"},start+0.001);
      ch.words.forEach(function(w,k){
        var on=Math.max(start,w.s-0.02);
        tl.set(sp[k],{attr:{"class":"cw on cur"}},on);
        if(k+1<ch.words.length) tl.set(sp[k],{attr:{"class":"cw on"}},Math.max(on+0.05,ch.words[k+1].s-0.02));
      });
      tl.set(line,{opacity:0},end);
    });
  };
})();
