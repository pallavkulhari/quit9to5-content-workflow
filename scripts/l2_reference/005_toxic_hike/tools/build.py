import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from art import (
    art_offer_scene,
    art_career_ladder,
    art_cracked_dimensions,
    art_seven_cards,
    art_squash_salary,
    art_wrong_metric,
    art_trade_bars,
    art_offer_resolved,
    art_cta_bg,
)

PROJ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DUR = 58.0

HEAD = '''<!doctype html>
<html data-resolution="portrait">
<head>
<meta charset="utf-8">
<style>
@font-face{font-family:'Inter Tight';src:url(assets/InterTight.ttf) format('truetype');font-weight:100 900;}
@font-face{font-family:'Inter';src:url(assets/Inter.ttf) format('truetype');font-weight:100 900;}
@font-face{font-family:'Caveat';src:url(assets/Caveat.ttf) format('truetype');font-weight:400 700;}
html,body{margin:0;padding:0;background:#F3EDE1;}
#root{position:relative;width:100%;height:100%;overflow:hidden;background:#F3EDE1;}
.scene{position:absolute;left:0;top:0;width:1080px;height:1920px;}
.title{position:absolute;left:90px;top:184px;width:870px;font-family:'Inter Tight',sans-serif;font-weight:800;
  line-height:1.02;letter-spacing:-0.045em;color:#141312;}
.ln{display:block;overflow:hidden;white-space:nowrap;padding:0.03em 0.08em 0.16em 0.08em;margin:-0.03em 0 -0.16em 0;}
.w{display:inline-block;position:relative;z-index:0;isolation:isolate;}
.red{color:#D54E4C;}
.hl{position:absolute;left:-0.07em;right:-0.05em;top:0.24em;bottom:0.02em;background:#F2D98B;z-index:-1;border-radius:0.07em;transform-origin:0% 50%;}
.obj{position:absolute;left:80px;top:460px;width:880px;height:700px;overflow:hidden;}
.obj.cta{top:338px;height:760px;overflow:visible;}
.cam{width:100%;height:100%;transform-origin:50% 50%;}
.art{display:block;}
.k{stroke:#141312;stroke-width:5;stroke-linejoin:round;stroke-linecap:round;}
svg text{stroke:none;}
.lbl{font-family:'Inter',sans-serif;font-weight:600;font-size:30px;letter-spacing:0.1em;fill:#141312;}
.lbl.cream{fill:#FFFBF3;}
.num{font-family:'Inter Tight',sans-serif;font-weight:800;letter-spacing:-0.02em;}
.hand{font-family:'Caveat',cursive;font-weight:700;letter-spacing:0.01em;}
.dr{stroke-dasharray:1 1;}
</style>
</head>
<body>
'''

JSHELP = '''
const tl=gsap.timeline({paused:true});
const Q=s=>document.querySelector(s), QA=s=>Array.from(document.querySelectorAll(s));
function wordsIn(sel,t,st,d){tl.fromTo(QA(sel+' .w'),{yPercent:125},{yPercent:0,duration:d||0.46,ease:'power4.out',stagger:st||0.08},t);}
function wordsOut(sel,t,d){tl.to(QA(sel+' .w'),{yPercent:-125,duration:d||0.20,ease:'power2.in',stagger:0.02},t);}
function swipe(sel,t,d){tl.fromTo(sel,{scaleX:0},{scaleX:1,duration:d||0.38,ease:'power2.inOut'},t);}
function draw(sel,t,d,ease,st){tl.fromTo(QA(sel),{strokeDashoffset:1},{strokeDashoffset:0,duration:d||0.38,ease:ease||'power2.inOut',stagger:st||0},t);}
function pop(sel,t,o,d,st,b){tl.fromTo(QA(sel),{scale:0,opacity:0,transformOrigin:o||'50% 100%'},{scale:1,opacity:1,duration:d||0.42,ease:'back.out('+(b||1.85)+')',stagger:st||0},t);}
'''


def title(id_, lines, size, extra_attr=''):
    out = f'<div class="title" id="{id_}" style="font-size:{size}px" {extra_attr}>'
    for ln in lines:
        out += '<span class="ln">'
        parts = []
        for w in ln:
            if isinstance(w, tuple):
                t, k = w
                if k == 'hl':
                    parts.append(f'<span class="w"><span class="hl"></span>{t}</span>')
                else:
                    parts.append(f'<span class="w red">{t}</span>')
            else:
                parts.append(f'<span class="w">{w}</span>')
        out += ' '.join(parts) + '</span>'
    return out + '</div>'


def build():
    sections = []
    js = []

    def add_scene(idx, start, dur, inner):
        sections.append(
            f'<section class="clip scene" id="s{idx}" data-start="{start:.2f}" '
            f'data-duration="{dur:.2f}" data-track-index="{idx+1}">{inner}</section>'
        )

    # ============================================================
    # BEAT 1: 0.00 - 3.02  "You get a job offer with a fifty percent hike."
    # FRAME 1 ALREADY VISIBLE: Cream offer letter, gentle push-in.
    # At 1.80 ("percent" / "fifty"): red "+50%" stamp slams onto letter with recoil!
    # ============================================================
    add_scene(
        0, 0.00, 3.02,
        title('t0', [['Job', 'offer:'], [('+50%.', 'red')]], 130)
        + f'<div class="obj" id="o0"><div class="cam" id="c0">{art_offer_scene("b1", mode="b1")}</div></div>'
    )
    js.append('''{
// Beat 1: 0.00 - 3.02 (FRAME 1 already shows offer letter & headline — NO blank frame!)
tl.fromTo('#c0', {scale: 1.0, transformOrigin: '50% 48%'}, {scale: 1.045, duration: 2.96, ease: 'sine.inOut'}, 0.0);
// Subtle lively sparkle twinkle from frame 0
tl.fromTo('#b1sp1,#b1sp2,#b1sp3', {scale: 0.85, transformOrigin: '50% 50%'},
          {scale: 1.12, duration: 0.48, yoyo: true, repeat: 1, stagger: 0.14, ease: 'sine.inOut'}, 0.36);

// 1.74 -> lands sharply at 1.80 ("fifty" 1.50 / "percent" 1.80): red "+50%" rubber stamp slams onto letter!
tl.fromTo('#b1stamp', {scale: 2.35, opacity: 0, rotation: -18, svgOrigin: '46 96'},
          {scale: 1, opacity: 1, rotation: 0, duration: 0.24, ease: 'power4.out'}, 1.74);
// Recoil squash on letter + impact burst lines + punch on red "+50%."
tl.fromTo('#b1letter', {scale: 1, svgOrigin: '456 292'},
          {scale: 0.965, duration: 0.07, yoyo: true, repeat: 1, ease: 'power2.out'}, 1.94);
tl.fromTo('#b1sburst', {scale: 0.65, opacity: 0, svgOrigin: '46 96'},
          {scale: 1.1, opacity: 1, duration: 0.14, ease: 'power2.out'}, 1.94);
tl.to('#b1sburst', {opacity: 0, duration: 0.30, ease: 'power2.in'}, 2.18);
tl.fromTo('#t0 .red', {scale: 1, transformOrigin: '15% 60%'},
          {scale: 1.08, duration: 0.15, yoyo: true, repeat: 1, ease: 'back.out(2.2)'}, 1.82);

// Exit ONLY the title at 2.80 -> 3.00 so the stamped offer letter stays rock-steady into Beat 2!
wordsOut('#t0', 2.80, 0.20);
}''')

    # ============================================================
    # BEAT 2: 3.02 - 8.02  "But former employees warn you the culture is toxic. Would you take it?"
    # Same stamped letter: 3.20 warning notes pin to margin; 5.98 red TOXIC CULTURE tag slaps on;
    # 7.00 handwritten "Would you take it?" + underline draws beneath letter. Hold.
    # ============================================================
    add_scene(
        1, 3.02, 5.00,
        title('t1', [['The', 'culture'], ['is', ('toxic.', 'red')]], 126)
        + f'<div class="obj" id="o1"><div class="cam" id="c1">{art_offer_scene("b2", mode="b2")}</div></div>'
    )
    js.append('''{
// Beat 2: 3.02 - 8.02 (seamless continuation of Beat 1's stamped offer letter!)
const T = 3.02;
// Match Beat 1 end camera scale (1.045) and gently settle back to 1.0 so question has full room
tl.fromTo('#c1', {scale: 1.045, transformOrigin: '50% 48%'}, {scale: 0.99, duration: 4.5, ease: 'sine.inOut'}, T);

// Title cadence: "The culture" enters early, "is toxic." punches on 5.54 / 5.98!
tl.fromTo(QA('#t1 .ln:first-child .w'), {yPercent: 125}, {yPercent: 0, duration: 0.42, ease: 'power4.out', stagger: 0.08}, T + 0.04);
tl.fromTo(QA('#t1 .ln:last-child .w'), {yPercent: 125}, {yPercent: 0, duration: 0.40, ease: 'power4.out', stagger: 0.09}, 5.52);

// 3.18 ("former employees"): stack of 3 warning notes pins onto the left margin!
tl.fromTo('#b2n3', {x: -110, y: -40, opacity: 0, rotation: -24, svgOrigin: '136 254'},
          {x: 0, y: 0, opacity: 1, rotation: 0, duration: 0.34, ease: 'back.out(1.6)'}, 3.18);
tl.fromTo('#b2n2', {x: -110, y: -40, opacity: 0, rotation: -18, svgOrigin: '148 232'},
          {x: 0, y: 0, opacity: 1, rotation: 0, duration: 0.34, ease: 'back.out(1.6)'}, 3.44);
tl.fromTo('#b2n1', {x: -120, y: -50, opacity: 0, scale: 1.15, svgOrigin: '160 212'},
          {x: 0, y: 0, opacity: 1, scale: 1, duration: 0.38, ease: 'back.out(1.8)'}, 3.70);
tl.fromTo('#b2letter', {x: 0}, {x: 6, duration: 0.06, yoyo: true, repeat: 2, ease: 'sine.inOut'}, 3.78);

// 5.92 (lands on 5.98 "toxic."): red "TOXIC CULTURE" tag slaps onto the letter!
tl.fromTo('#b2toxic', {scale: 2.15, opacity: 0, rotation: -12, svgOrigin: '478 232'},
          {scale: 1, opacity: 1, rotation: 0, duration: 0.24, ease: 'power4.out'}, 5.92);
tl.fromTo('#b2letter', {x: 0, y: 0}, {x: -7, y: 5, duration: 0.05, yoyo: true, repeat: 3, ease: 'sine.inOut', immediateRender: false}, 6.10);
tl.fromTo('#b2tburst', {scale: 0.65, opacity: 0, svgOrigin: '478 232'},
          {scale: 1.08, opacity: 1, duration: 0.14, ease: 'power2.out'}, 6.10);
tl.to('#b2tburst', {opacity: 0, duration: 0.28, ease: 'power2.in'}, 6.32);
tl.fromTo('#t1 .red', {scale: 1, transformOrigin: '25% 60%'},
          {scale: 1.08, duration: 0.15, yoyo: true, repeat: 1, ease: 'back.out(2.2)'}, 6.02);

// 6.96 (lands on 7.00 "Would you take it?"): handwritten question + drawn underline!
tl.set('#b2asku', {strokeDashoffset: 1}, T);
tl.fromTo('#b2askt', {y: 22, opacity: 0}, {y: 0, opacity: 1, duration: 0.34, ease: 'power3.out'}, 6.96);
draw('#b2asku', 7.06, 0.44, 'power2.out');

// Hold question clean to 7.80, then push title up & slide offer back left into Beat 3
wordsOut('#t1', 7.80, 0.20);
tl.to('#o1', {x: -80, scale: 0.92, opacity: 0, duration: 0.22, ease: 'power2.in'}, 7.80);
}''')

    # ============================================================
    # BEAT 3: 8.02 - 13.84  "Most people would, in a heartbeat. Because on the career ladder, that screams growth."
    # Offer shrinks/slides back as tall CAREER LADDER grows; heartbeat pulse at 9.38;
    # +50% HIKE climbs ladder; red GROWTH banner unfurls at 12.10 with shake.
    # ============================================================
    add_scene(
        2, 8.02, 5.82,
        title('t2', [['It', 'screams'], [('growth.', 'red')]], 130)
        + f'<div class="obj" id="o2"><div class="cam" id="c2">{art_career_ladder("b3")}</div></div>'
    )
    js.append('''{
// Beat 3: 8.02 - 13.84
const T = 8.02;
// Title enters: "It screams" right away / punches on 12.10, "growth." lands at 12.66 (or both visible smoothly)
tl.fromTo(QA('#t2 .ln:first-child .w'), {yPercent: 125}, {yPercent: 0, duration: 0.44, ease: 'power4.out', stagger: 0.08}, T + 0.06);
tl.fromTo(QA('#t2 .ln:last-child .w'), {yPercent: 125}, {yPercent: 0, duration: 0.46, ease: 'power4.out'}, T + 0.24);
tl.fromTo('#c2', {scale: 0.99, transformOrigin: '50% 55%'}, {scale: 1.03, duration: 5.4, ease: 'sine.inOut'}, T);

// Shrinking stamped offer slides back to the left edge (outer g has no transform -> scale 1.0 = 0.42!)
tl.fromTo('#b3oldoff', {x: 240, y: -80, scale: 1.5, opacity: 0, svgOrigin: '158 492'},
          {x: 0, y: 0, scale: 1.0, opacity: 0.92, duration: 0.56, ease: 'power3.out'}, T + 0.02);

// Tall CAREER LADDER grows up from floor!
tl.fromTo('#b3ladder', {scaleY: 0, opacity: 0, svgOrigin: '480 642'},
          {scaleY: 1, opacity: 1, duration: 0.68, ease: 'back.out(1.3)'}, T + 0.14);

// +50% HIKE climber badge hops cleanly onto center of bottom rung!
tl.fromTo('#b3climber', {x: -160, y: 40, scale: 0.5, opacity: 0, svgOrigin: '480 510'},
          {x: 0, y: 0, scale: 1, opacity: 1, duration: 0.46, ease: 'back.out(1.7)'}, T + 0.62);

// 9.34 (lands on 9.38 "heartbeat."): red ECG pulse draws + double heartbeat thump!
tl.set('#b3hbline', {strokeDashoffset: 1}, T);
draw('#b3hbline', 9.26, 0.34, 'power2.out');
tl.fromTo('#b3hbdot', {scale: 0, opacity: 0, svgOrigin: '244 236'},
          {scale: 1.35, opacity: 1, duration: 0.14, ease: 'back.out(2.2)'}, 9.38);
tl.to('#b3hbdot', {scale: 1.0, duration: 0.12}, 9.54);
tl.to('#b3climber', {scale: 1.10, duration: 0.11, yoyo: true, repeat: 3, ease: 'sine.inOut'}, 9.36);

// 10.60 - 11.90 ("Because on the career ladder"): +50% HIKE climbs rung by rung up the ladder!
tl.to('#b3hb', {opacity: 0.25, duration: 0.4}, 10.50);
tl.to('#b3climber', {y: -74, duration: 0.24, ease: 'back.out(1.6)'}, 10.56);
tl.to('#b3climber', {y: -148, duration: 0.24, ease: 'back.out(1.6)'}, 10.90);
tl.to('#b3climber', {y: -222, duration: 0.24, ease: 'back.out(1.6)'}, 11.24);
tl.to('#b3climber', {y: -296, duration: 0.26, ease: 'back.out(1.8)'}, 11.58);

// 12.08 ("screams") -> 12.78 ("growth."): red GROWTH banner unfurls at top with shake & shout rays!
tl.fromTo('#b3banner', {opacity: 0, scaleY: 0.4, svgOrigin: '480 156'},
          {opacity: 1, scaleY: 1, duration: 0.26, ease: 'back.out(1.9)'}, 12.08);
tl.fromTo('#b3bflag', {scaleX: 0.08, svgOrigin: '480 84'},
          {scaleX: 1, duration: 0.36, ease: 'back.out(1.7)'}, 12.12);
tl.fromTo('#b3sburst', {scale: 0.7, opacity: 0, svgOrigin: '486 84'},
          {scale: 1.08, opacity: 1, duration: 0.18, ease: 'power2.out'}, 12.24);
// Energetic scream shake + title red punch on "growth." (12.78)
tl.fromTo('#b3bflag', {rotation: 0, svgOrigin: '486 84'},
          {rotation: -3.5, duration: 0.07, yoyo: true, repeat: 5, ease: 'sine.inOut', immediateRender: false}, 12.34);
tl.fromTo('#t2 .red', {scale: 1, transformOrigin: '20% 60%'},
          {scale: 1.09, duration: 0.16, yoyo: true, repeat: 1, ease: 'back.out(2.2)'}, 12.74);
pop('#b3sp1,#b3sp2,#b3sp3', 12.30, '50% 50%', 0.34, 0.08, 2.1);

// Exit (13.62 -> 13.84)
wordsOut('#t2', 13.62, 0.20);
tl.to('#o2', {y: -50, opacity: 0, duration: 0.20, ease: 'power2.in'}, 13.64);
}''')

    # ============================================================
    # BEAT 4: 13.84 - 18.98  "But here's the problem. A career isn't one line. It has many dimensions."
    # 15.24-16.74: single ladder/line cracks and splits as too thin.
    # 17.16: 7 dimension cards fan out faintly; headline swaps cleanly to "Many dimensions." at 17.46!
    # ============================================================
    add_scene(
        3, 13.84, 5.14,
        title('t3a', [['A', 'career', "isn't"], [('one line.', 'hl')]], 114, extra_attr='data-layout-allow-overlap')
        + title('t3b', [['Many'], [('dimensions.', 'red')]], 124, extra_attr='data-layout-allow-overlap')
        + f'<div class="obj" id="o3"><div class="cam" id="c3">{art_cracked_dimensions("b4")}</div></div>'
    )
    js.append('''{
// Beat 4: 13.84 - 18.98
const T = 13.84;
// Wait: t3b had an inline style attribute override above, ensure t3b starts hidden via GSAP
tl.set('#t3b', {opacity: 0}, T);
tl.set('#t3a .hl', {scaleX: 0}, T);
tl.set('#b4crack', {strokeDashoffset: 1}, T);

wordsIn('#t3a', T + 0.04, 0.07, 0.42);
tl.fromTo('#c3', {scale: 0.98, transformOrigin: '50% 50%'}, {scale: 1.0, duration: 4.9, ease: 'sine.inOut'}, T);
tl.fromTo('#b4single', {scaleY: 0.6, opacity: 0, svgOrigin: '440 642'},
          {scaleY: 1, opacity: 1, duration: 0.44, ease: 'back.out(1.4)'}, T + 0.04);

// 14.44 ("problem."): single ladder gives an uneasy wobble
tl.fromTo('#b4single', {rotation: 0, svgOrigin: '440 600'},
          {rotation: -2.4, duration: 0.07, yoyo: true, repeat: 3, ease: 'sine.inOut'}, 14.42);

// 15.24 - 16.74 ("A career isn't one line."): rungs disappear -> revealed as one thin line -> CRACKS!
tl.to('#b4rungs', {scaleX: 0.1, opacity: 0, svgOrigin: '440 350', duration: 0.36, ease: 'power2.in'}, 15.26);
swipe('#t3a .hl', 16.16, 0.36);
// Crack jaggedly draws across the thin line at 16.20 -> splits top & bottom halves!
draw('#b4crack', 16.16, 0.34, 'power3.out');
tl.to('#b4ltop', {x: -14, y: -12, rotation: -8, svgOrigin: '440 344', duration: 0.36, ease: 'power3.out'}, 16.38);
tl.to('#b4lbot', {x: 12, y: 8, rotation: 6, svgOrigin: '440 344', duration: 0.36, ease: 'power3.out'}, 16.38);

// 17.16 ("It has many dimensions."): single cracked line dissolves back & 7 cards bloom/fan out!
tl.to('#b4single', {opacity: 0, scale: 0.85, svgOrigin: '440 350', duration: 0.36, ease: 'power2.in'}, 17.12);
tl.to('#b4arc', {opacity: 1, duration: 0.42, ease: 'power2.out'}, 17.28);
tl.set('#b4cards', {opacity: 1}, 17.18);
for (let i = 0; i < 7; i++) {
  tl.fromTo('#b4c' + i, {scale: 0.2, opacity: 0, svgOrigin: '440 340'},
            {scale: 1, opacity: 1, duration: 0.48, ease: 'back.out(1.4)'}, 17.20 + i * 0.06);
}
// Swap headline cleanly to "Many dimensions." right on "many dimensions." (17.46 / 17.84)!
wordsOut('#t3a', 17.34, 0.18);
tl.set('#t3b', {opacity: 1}, 17.46);
wordsIn('#t3b', 17.48, 0.12, 0.42);
tl.fromTo('#t3b .red', {scale: 1, transformOrigin: '20% 60%'},
          {scale: 1.06, duration: 0.16, yoyo: true, repeat: 1, ease: 'back.out(2)'}, 17.86);
pop('#b4sp1,#b4sp2', 17.90, '50% 50%', 0.32, 0.08, 2.0);
// DO NOT exit title or cards at 18.98 -> Beat 5 holds the EXACT same "Many dimensions." title & 7-card grid!
}''')

    # ============================================================
    # BEAT 5: 18.98 - 25.54  "Income, title, freedom, colleagues, location, work-life balance, toxicity."
    # Statement "Many dimensions." HELD seamlessly!
    # The SAME 7 cards snap bright & active one by one on their exact spoken words!
    # ============================================================
    add_scene(
        4, 18.98, 6.56,
        title('t4', [['Many'], [('dimensions.', 'red')]], 124)
        + f'<div class="obj" id="o4"><div class="cam" id="c4">{art_seven_cards("b5")}</div></div>'
    )
    js.append('''{
// Beat 5: 18.98 - 25.54 (seamless hold of "Many dimensions." and the exact 7-card arc!)
const T = 18.98;
tl.fromTo('#c4', {scale: 1.0, transformOrigin: '50% 50%'}, {scale: 0.99, duration: 6.2, ease: 'sine.inOut'}, T);

// Hide active overlays initially so ghost silhouettes match Beat 4's final frame seamlessly
const b5Centers = [
  [174, 224], [440, 206], [706, 224],
  [124, 486], [335, 472], [545, 472], [756, 486]
];
b5Centers.forEach(([cx, cy], i) => {
  tl.set('#b5c' + i, {scale: 0.72, opacity: 0, svgOrigin: cx + ' ' + cy}, T);
});

// Exact spoken word timestamps from captions.json (±0.06 s):
// INCOME 18.98, TITLE 19.72, FREEDOM 20.48, COLLEAGUES 21.32, LOCATION 22.14, WORK-LIFE 23.18, TOXICITY 24.54
const cardTimes = [18.98, 19.70, 20.46, 21.30, 22.12, 23.16, 24.52];
cardTimes.forEach((ct, i) => {
  const [cx, cy] = b5Centers[i];
  tl.to('#b5c' + i, {scale: 1, opacity: 1, duration: 0.34, ease: 'back.out(2.0)', svgOrigin: cx + ' ' + cy}, ct);
  // Subtle pop-lift settle on outer wrapper (y=0 keeps inner translate(cx cy) exact!)
  tl.fromTo('#b5c' + i, {y: -14}, {y: 0, duration: 0.28, ease: 'power2.out', immediateRender: false}, ct);
});
pop('#b5sp1,#b5sp2', 24.62, '50% 50%', 0.34, 0.08, 2.0);

// Exit ONLY the title at 25.32 -> 25.52 so all 7 bright cards stay rock-steady for Beat 6's jitter & squash!
wordsOut('#t4', 25.32, 0.20);
}''')

    # ============================================================
    # BEAT 6: 25.54 - 33.02  "Our brain can't handle that many, so it takes a shortcut.
    #                         It shrinks the whole career into one number. Salary."
    # HERO MOVE: 25.54 cards jitter; 27.80 red clamp appears; 28.64-31.90 squashes 7 cards into
    # ONE thick SALARY bar; 32.12 bold SALARY label slams on & "Salary." highlights!
    # ============================================================
    add_scene(
        5, 25.54, 7.48,
        title('t5', [['One', 'number:'], [('Salary.', 'hl')]], 126)
        + f'<div class="obj" id="o5"><div class="cam" id="c5">{art_squash_salary("b6")}</div></div>'
    )
    js.append('''{
// Beat 6: 25.54 - 33.02 (HERO MOVE — seamless start from Beat 5's 7 active cards!)
const T = 25.54;
tl.set('#t5 .hl', {scaleX: 0}, T);
// Title enters: "One number:" at 30.80 (matching "into one number" 31.04) or earlier? Let's show "One number:" at 25.60 so no empty title zone!
tl.fromTo(QA('#t5 .ln:first-child .w'), {yPercent: 125}, {yPercent: 0, duration: 0.44, ease: 'power4.out', stagger: 0.08}, T + 0.04);
tl.fromTo(QA('#t5 .ln:last-child .w'), {yPercent: 125}, {yPercent: 0, duration: 0.40, ease: 'power4.out'}, 32.04);

// 25.54 - 27.70 ("Our brain can't handle that many"): 7 cards jitter / overcrowd nervously!
tl.fromTo('#b6stress', {opacity: 0, y: 12}, {opacity: 1, y: 0, duration: 0.28, ease: 'power2.out'}, 25.68);
tl.to('#b6stress', {y: -6, duration: 0.16, yoyo: true, repeat: 9, ease: 'sine.inOut'}, 25.96);
const jitters = [
  [-8, 6, -4], [7, -7, 4], [-7, -5, 5],
  [8, -6, -5], [-6, 7, 4], [7, 6, -4], [-8, -6, 5]
];
jitters.forEach(([jx, jy, jr], i) => {
  tl.to('#b6c' + i, {
    x: jx, y: jy, rotation: '+=' + jr,
    duration: 0.11, yoyo: true, repeat: 15, ease: 'sine.inOut'
  }, 25.64 + (i % 3) * 0.04);
});

// 27.80 - 28.60 ("so it takes a shortcut."): red compressing clamps + SHORTCUT badge slam in!
tl.to('#b6stress', {opacity: 0, duration: 0.20}, 27.78);
tl.fromTo('#b6clampL', {x: -110, opacity: 0}, {x: 0, opacity: 1, duration: 0.34, ease: 'back.out(1.6)'}, 27.80);
tl.fromTo('#b6clampR', {x: 110, opacity: 0}, {x: 0, opacity: 1, duration: 0.34, ease: 'back.out(1.6)'}, 27.80);
tl.fromTo('#b6scbadge', {y: -48, scale: 0.7, opacity: 0, svgOrigin: '440 57'},
          {y: 0, scale: 1, opacity: 1, duration: 0.36, ease: 'back.out(1.8)'}, 28.22);

// 28.64 - 31.90 ("It shrinks the whole career into one number."):
// Clamps crush inward! All 7 cards compress into a flat base pancake while ONE thick SALARY bar extrudes up!
tl.to('#b6clampL', {x: 266, duration: 2.30, ease: 'power2.inOut'}, 28.72);
tl.to('#b6clampR', {x: -266, duration: 2.30, ease: 'power2.inOut'}, 28.72);
tl.to('#b6scbadge', {opacity: 0, y: -24, duration: 0.32, ease: 'power2.in'}, 30.80);

// Target displacements to squash each of the 7 cards into the center-bottom stack (cx=440, cy=602)
const cardCenters = [
  [174, 224], [440, 206], [706, 224],
  [124, 486], [335, 472], [545, 472], [756, 486]
];
cardCenters.forEach(([cx, cy], i) => {
  tl.to('#b6c' + i, {
    x: 440 - cx,
    y: 602 - cy,
    scaleX: 0.56,
    scaleY: 0.16,
    rotation: 0,
    opacity: 0.0,
    svgOrigin: cx + ' ' + cy,
    duration: 2.10,
    ease: 'power3.inOut'
  }, 28.80 + (i % 3) * 0.06);
});

// Crushed pancake base emerges & ONE thick SALARY column extrudes smoothly upward!
tl.fromTo('#b6crushed', {scaleY: 0.2, opacity: 0, svgOrigin: '440 642'},
          {scaleY: 1, opacity: 1, duration: 0.55, ease: 'power2.out'}, 30.40);
tl.fromTo('#b6sbar', {scaleY: 0.06, opacity: 0, svgOrigin: '440 580'},
          {scaleY: 1, opacity: 1, duration: 1.40, ease: 'power3.out'}, 30.20);
// Clamps retract cleanly once forging finishes
tl.to('#b6clampL', {x: -120, opacity: 0, duration: 0.36, ease: 'power2.in'}, 31.38);
tl.to('#b6clampR', {x: 120, opacity: 0, duration: 0.36, ease: 'power2.in'}, 31.38);

// 32.10 (lands sharply on 32.12 "Salary."): big SALARY plaque slams onto bar + highlighter swipes "Salary."!
tl.fromTo('#b6slabel', {scale: 2.2, opacity: 0, rotation: -8, svgOrigin: '440 364'},
          {scale: 1, opacity: 1, rotation: 0, duration: 0.26, ease: 'power4.out'}, 32.08);
tl.fromTo('#b6sbar', {scaleY: 1, scaleX: 1, svgOrigin: '440 580'},
          {scaleY: 0.96, scaleX: 1.04, duration: 0.08, yoyo: true, repeat: 1, ease: 'power2.out', immediateRender: false}, 32.28);
tl.fromTo('#b6sburst', {scale: 0.7, opacity: 0, svgOrigin: '440 364'},
          {scale: 1.1, opacity: 1, duration: 0.15, ease: 'power2.out'}, 32.26);
tl.to('#b6sburst', {opacity: 0, duration: 0.28, ease: 'power2.in'}, 32.50);
swipe('#t5 .hl', 32.12, 0.38);
pop('#b6sp1,#b6sp2', 32.26, '50% 50%', 0.32, 0.08, 2.0);

// Exit ONLY title at 32.82 -> 33.00 so the SALARY bar + crushed base continue seamlessly into Beat 7!
wordsOut('#t5', 32.82, 0.20);
}''')

    # ============================================================
    # BEAT 7: 33.02 - 38.06  "That's how people end up chasing the wrong metric,
    #                         and optimising for the wrong life."
    # SALARY bar shoots upward; crushed base stays flattened; FREEDOM & WORK-LIFE sag;
    # red TOXICITY wedge creeps in! Highlighter swipe on "wrong" at 34.64!
    # ============================================================
    add_scene(
        6, 33.02, 5.04,
        title('t6', [['The', ('wrong', 'hl')], ['metric.']], 130)
        + f'<div class="obj" id="o6"><div class="cam" id="c6">{art_wrong_metric("b7")}</div></div>'
    )
    js.append('''{
// Beat 7: 33.02 - 38.06
const T = 33.02;
tl.set('#t6 .hl', {scaleX: 0}, T);
wordsIn('#t6', T + 0.04, 0.09, 0.42);
tl.fromTo('#c6', {scale: 0.99, transformOrigin: '50% 55%'}, {scale: 1.03, duration: 4.7, ease: 'sine.inOut'}, T);

// Bar starts at Beat 6 height (scaleY 0.84) and shoots UPWARD on "chasing the wrong metric" (33.94-35.34)!
tl.set('#b7bar', {scaleY: 0.84, svgOrigin: '440 582'}, T);
tl.to('#b7bar', {scaleY: 1.04, duration: 1.15, ease: 'power3.out'}, 33.86);
tl.fromTo('#b7speed', {y: 50, opacity: 0}, {y: -24, opacity: 0.85, duration: 0.65, ease: 'power2.out'}, 33.92);
tl.to('#b7speed', {opacity: 0.25, duration: 0.6}, 34.80);

// Highlighter swipes on "wrong" right at 34.64 ("wrong" metric)
swipe('#t6 .hl', 34.60, 0.36);

// Left crushed FREEDOM & WORK-LIFE cards appear already flattened, then SAG/WILT at 35.86-37.30 ("optimising for the wrong life")!
tl.fromTo('#b7sagL', {x: 40, opacity: 0}, {x: 0, opacity: 1, duration: 0.42, ease: 'power2.out'}, T + 0.22);
tl.to('#b7sag1', {rotation: -11, y: 24, svgOrigin: '290 540', duration: 0.85, ease: 'power2.inOut'}, 35.88);
tl.to('#b7sag2', {scaleY: 0.82, y: 8, svgOrigin: '166 638', duration: 0.85, ease: 'power2.inOut'}, 35.98);
tl.fromTo('#b7droop', {y: -16, opacity: 0}, {y: 0, opacity: 0.85, duration: 0.42, ease: 'power2.out'}, 36.28);

// Right side: sharp RED TOXICITY WEDGE creeps upward out from beneath the crushed stack (36.20-37.45)!
tl.fromTo('#b7wedge', {x: 110, y: 90, opacity: 0},
          {x: 0, y: 0, opacity: 1, duration: 0.92, ease: 'power3.out'}, 36.24);
tl.fromTo('#b7wrip', {scale: 0.85, opacity: 0.4, svgOrigin: '780 390'},
          {scale: 1.08, opacity: 1, duration: 0.26, yoyo: true, repeat: 2, ease: 'sine.inOut'}, 36.92);
// Second subtle emphasis on "wrong" at 36.92 ("wrong life")
tl.fromTo('#t6 .ln:first-child .w:last-child', {scale: 1, transformOrigin: '50% 60%'},
          {scale: 1.06, duration: 0.16, yoyo: true, repeat: 1, ease: 'back.out(2)'}, 36.90);

// Exit (37.84 -> 38.06)
wordsOut('#t6', 37.84, 0.20);
tl.to('#o6', {x: -90, opacity: 0, duration: 0.20, ease: 'power2.in'}, 37.86);
}''')

    # ============================================================
    # BEAT 8: 38.06 - 46.36  "When I quit my 9to5, people said I was ruining my career.
    #                         I wasn't. I simply gave up some income to get more free time."
    # 40.48: "RUINING MY CAREER" tag slams on; 41.90: strike-through draws across;
    # 43.34-45.80: INCOME steps down modestly & FREE TIME grows tall & radiant!
    # ============================================================
    add_scene(
        7, 38.06, 8.30,
        title('t7', [['I', 'traded', 'income'], ['for', ('free time.', 'hl')]], 110)
        + f'<div class="obj" id="o7"><div class="cam" id="c7">{art_trade_bars("b8")}</div></div>'
    )
    js.append('''{
// Beat 8: 38.06 - 46.36
const T = 38.06;
tl.set('#t7 .hl', {scaleX: 0}, T);
tl.set('#b8strike', {strokeDashoffset: 1}, T);
wordsIn('#t7', T + 0.04, 0.07, 0.44);
tl.fromTo('#c7', {scale: 0.99, transformOrigin: '50% 55%'}, {scale: 1.025, duration: 7.9, ease: 'sine.inOut'}, T);

// Initial 9to5 state: INCOME bar starts tall (scaleY=1.0), FREE TIME bar starts cramped/low (scaleY=0.38)
tl.set('#b8ftBar', {scaleY: 0.38, svgOrigin: '632 580'}, T);
tl.set('#b8ftIcon', {y: 232}, T);

// Both columns rise cleanly onto the floor
tl.fromTo('#b8incG', {y: 90, opacity: 0}, {y: 0, opacity: 1, duration: 0.48, ease: 'back.out(1.4)'}, T + 0.04);
tl.fromTo('#b8ftG', {y: 90, opacity: 0}, {y: 0, opacity: 1, duration: 0.48, ease: 'back.out(1.4)'}, T + 0.14);

// 40.46 (lands on 40.48 "ruining"): "RUINING MY CAREER" red stamp tag slams on!
tl.fromTo('#b8ruin', {scale: 2.1, opacity: 0, rotation: -10, svgOrigin: '440 74'},
          {scale: 1, opacity: 1, rotation: 0, duration: 0.26, ease: 'power4.out'}, 40.44);
tl.fromTo('#o7', {y: 0}, {y: 6, duration: 0.06, yoyo: true, repeat: 1, ease: 'power2.out'}, 40.66);

// 41.88 (lands on 41.90 "I wasn't."): bold ink strike-through draws across "RUINING MY CAREER"!
draw('#b8strike', 41.88, 0.38, 'power2.inOut');
tl.to('#b8ruin', {opacity: 0.36, duration: 0.35, ease: 'power2.out'}, 42.22);
tl.to('#b8strike', {opacity: 0.42, duration: 0.35, ease: 'power2.out'}, 42.22);

// 43.34 - 45.80 ("gave up some income to get more free time."):
// INCOME steps down modestly (1.0 -> 0.64, showing dashed ghost outline); FREE TIME grows TALL & RADIANT (0.38 -> 1.0)!
tl.fromTo('#b8arrows', {opacity: 0, scale: 0.8, svgOrigin: '440 336'},
          {opacity: 1, scale: 1, duration: 0.32, ease: 'back.out(1.6)'}, 43.34);
tl.to('#b8incGhost', {opacity: 0.85, duration: 0.25}, 43.40);
tl.to('#b8incBar', {scaleY: 0.64, svgOrigin: '248 580', duration: 1.05, ease: 'power2.inOut'}, 43.42);
tl.to('#b8incIcon', {y: 138, duration: 1.05, ease: 'power2.inOut'}, 43.42);

// FREE TIME rises big & bright right on "to get more free time." (44.44 - 45.80)!
tl.to('#b8ftBar', {scaleY: 1.0, svgOrigin: '632 580', duration: 1.15, ease: 'back.out(1.35)'}, 44.36);
tl.to('#b8ftIcon', {y: 0, duration: 1.15, ease: 'back.out(1.35)'}, 44.36);
tl.fromTo('#b8halo', {scale: 0.4, opacity: 0, svgOrigin: '632 370'},
          {scale: 1, opacity: 0.32, duration: 0.72, ease: 'power2.out'}, 44.68);
pop('#b8ftrays', 45.14, '50% 100%', 0.36, 0, 1.8);
pop('#b8sp1,#b8sp2,#b8sp3', 45.18, '50% 50%', 0.34, 0.08, 2.1);

// Highlighter swipes across "free time." right at 45.12!
swipe('#t7 .hl', 45.12, 0.38);

// Exit (46.14 -> 46.36)
wordsOut('#t7', 46.14, 0.20);
tl.to('#o7', {y: -50, opacity: 0, duration: 0.20, ease: 'power2.in'}, 46.16);
}''')

    # ============================================================
    # BEAT 9: 46.36 - 51.32  "So next time an offer screams growth, ask: growth in which dimension?"
    # Return to SAME offer-letter composition as Frame 1 (+50% stamp).
    # 47.32: faint GROWTH echo; 48.82-50.88: cards spread out around offer; TOXICITY red & forward!
    # Hold resolved state so loop back to Frame 1 reads intentionally!
    # ============================================================
    add_scene(
        8, 46.36, 4.96,
        title('t8', [['Growth', 'in', 'which'], [('dimension?', 'red')]], 112)
        + f'<div class="obj" id="o8"><div class="cam" id="c8">{art_offer_resolved("b9")}</div></div>'
    )
    js.append('''{
// Beat 9: 46.36 - 51.32 (Return to SAME offer letter composition + spread dimensions + RED TOXICITY forward!)
const T = 46.36;
wordsIn('#t8', T + 0.04, 0.08, 0.44);
tl.fromTo('#c8', {scale: 0.97, transformOrigin: '50% 50%'}, {scale: 1.00, duration: 4.5, ease: 'sine.inOut'}, T);

// Stamped Offer Letter returns cleanly center-stage (outer g has NO transform -> scale 1.0 = exact 0.78!)
tl.fromTo('#b9letter', {scale: 0.84, opacity: 0, svgOrigin: '440 326'},
          {scale: 1.0, opacity: 1, duration: 0.46, ease: 'back.out(1.4)'}, T + 0.02);

// 47.32 ("screams" / "growth"): faint GROWTH echo pops briefly above the offer letter
tl.fromTo('#b9gecho', {scaleX: 0.4, opacity: 0, svgOrigin: '440 54'},
          {scaleX: 1, opacity: 0.45, duration: 0.34, ease: 'back.out(1.5)'}, 47.30);
tl.to('#b9gecho', {opacity: 0.16, duration: 0.60, ease: 'power2.out'}, 48.40);

// 48.80 ("ask:") -> 50.38 ("dimension?"): 6 dimension cards fan cleanly out around the offer letter!
tl.to('#b9spokes', {opacity: 0.9, duration: 0.40, ease: 'power2.out'}, 48.88);
const ringStarts = [
  [150, 110, 128, 178], [165, 0, 124, 330], [150, -110, 128, 482],
  [-150, 110, 752, 178], [-165, 0, 756, 330], [-150, -110, 752, 482]
];
ringStarts.forEach(([dx, dy, cx, cy], i) => {
  tl.fromTo('#b9c' + i, {x: dx, y: dy, scale: 0.35, opacity: 0, svgOrigin: cx + ' ' + cy},
            {x: 0, y: 0, scale: 1, opacity: 1, duration: 0.48, ease: 'back.out(1.55)'}, 48.82 + i * 0.09);
});

// 49.84 -> 50.38 ("growth in which dimension?"): RED TOXICITY comes boldly forward in front!
tl.fromTo('#b9toxwrap', {scale: 0.4, y: -90, opacity: 0, svgOrigin: '440 594'},
          {scale: 1.06, y: 0, opacity: 1, duration: 0.46, ease: 'back.out(1.9)'}, 49.86);
tl.fromTo('#b9toxrays', {scale: 0.7, opacity: 0, svgOrigin: '440 594'},
          {scale: 1.08, opacity: 1, duration: 0.22, ease: 'power2.out'}, 50.22);
tl.fromTo('#t8 .red', {scale: 1, transformOrigin: '25% 60%'},
          {scale: 1.08, duration: 0.16, yoyo: true, repeat: 1, ease: 'back.out(2.2)'}, 50.36);
pop('#b9sp1,#b9sp2', 50.24, '50% 50%', 0.32, 0.08, 2.0);

// Hold resolved state steady until 51.12, then clean exit into CTA end card
wordsOut('#t8', 51.10, 0.20);
tl.to('#o8', {opacity: 0, scale: 0.96, duration: 0.20, ease: 'power2.in'}, 51.12);
}''')

    # ============================================================
    # BEAT 10: 51.32 - 58.00  CTA End Card (approved Reel 003 treatment!)
    # Tilted book cover + warm halo, "Coming soon." (~52.78),
    # red pill "Join the waitlist -> link in bio" pops at 54.30 ("Join").
    # NO URL anywhere. Holds completely still 56.10 -> 58.00 (1.90 s >= 1.5 s still)!
    # ============================================================
    cta_inner = (
        title('t9', [['Coming', ('soon.', 'hl')]], 132)
        + f'<div class="obj cta" id="o9">{art_cta_bg("b10")}</div>'
        + '<div id="bookw" style="position:absolute;left:330px;top:368px;width:380px;height:537px;z-index:5;">'
          '<img id="book" src="assets/book_cover.jpeg" alt="Quit 9to5 book cover" '
          'style="display:block;width:380px;height:537px;border-radius:10px;'
          'box-shadow:18px 22px 0 #E4D9C4, 0 22px 46px rgba(20,19,18,0.22);border:4px solid #141312;box-sizing:border-box;">'
          '</div>'
        + '<div id="ctapill" style="position:absolute;left:90px;top:988px;width:860px;height:110px;'
          'border-radius:55px;background:#D54E4C;border:5px solid #141312;box-sizing:border-box;'
          'box-shadow:10px 12px 0 #D3C5AB;display:flex;align-items:center;justify-content:center;gap:14px;'
          'font-family:\'Inter Tight\',sans-serif;font-weight:800;font-size:46px;letter-spacing:-0.015em;color:#FFFBF3;z-index:6;">'
          '<span>Join the waitlist</span>'
          '<span id="ctaarr" style="display:inline-block;color:#F2D98B;">→</span>'
          '<span>link in bio</span>'
          '</div>'
    )
    add_scene(9, 51.32, 6.68, cta_inner)
    js.append('''{
// Beat 10: 51.32 - 58.00 (CTA End Card; holds completely still 56.10 -> 58.00 = 1.90 s!)
const T = 51.32;
// Book cover rises right on "My book Quit 9to5" (51.32)
tl.fromTo('#b10halo', {scale: 0.4, opacity: 0, transformOrigin: '50% 50%'},
          {scale: 1, opacity: 0.34, duration: 0.65, ease: 'power2.out'}, T + 0.06);
tl.fromTo('#bookw', {y: 120, opacity: 0, rotation: 5, scale: 0.90},
          {y: 0, opacity: 1, rotation: -3, scale: 1, duration: 0.66, ease: 'back.out(1.4)'}, T + 0.04);
pop('#b10rays', T + 0.56, '50% 50%', 0.44, 0, 1.8);
pop('#b10sp1,#b10sp2,#b10sp3,#b10sp4', T + 0.62, '50% 50%', 0.36, 0.07, 2.2);

// "Coming soon." lands cleanly on "is coming out soon." (52.78)
tl.set('#t9 .hl', {scaleX: 0}, T);
wordsIn('#t9', 52.72, 0.10, 0.44);
swipe('#t9 .hl', 53.12, 0.36);

// Red pill pops right on "Join the waitlist in bio." (54.30)
tl.fromTo('#ctapill', {scale: 0.72, y: 36, opacity: 0, transformOrigin: '50% 50%'},
          {scale: 1, y: 0, opacity: 1, duration: 0.48, ease: 'back.out(1.8)'}, 54.26);
// Crisp arrow nudge settles completely by 56.06 -> 1.94 s completely still hold to 58.00 for loop!
tl.fromTo('#ctaarr', {x: 0}, {x: 10, duration: 0.28, yoyo: true, repeat: 3, ease: 'sine.inOut'}, 54.86);
}''')

    chunks_json = open(os.path.join(PROJ, 'assets/captions.json'), 'r', encoding='utf-8').read().strip()

    html = (
        HEAD
        + f'<div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="1080" data-height="1920">\n'
        + '\n'.join(sections)
        + '\n</div>\n'
        + '<script src="assets/gsap.min.js"></script>\n'
        + '<script src="assets/captions4.js"></script>\n'
        + '<script>\n'
        + JSHELP
        + '\n'.join(js)
        + f'\nconst CHUNKS={chunks_json};\n'
        + f'window.addCaptions4(tl,CHUNKS,{{theme:"ink",lastEnd:58}});\n'
        + f'tl.to({{}},{{duration:0.01}},{DUR}-0.01);\n'
        + 'window.__timelines=window.__timelines||{};window.__timelines["main"]=tl;\n'
        + '</script>\n</body>\n</html>\n'
    )

    out_path = os.path.join(PROJ, 'index.html')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'Wrote {out_path} ({len(html)} bytes)')


if __name__ == '__main__':
    build()
