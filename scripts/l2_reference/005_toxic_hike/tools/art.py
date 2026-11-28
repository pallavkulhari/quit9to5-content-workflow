# Flat-vector SVG illustrations for Reel 005 — "Growth in which dimension?" (L2 style)
# Strictly on-palette: cream #F3EDE1, ink #141312 (5px outlines), accent red #D54E4C, butter yellow #F2D98B.
# Every art function returns an <svg> whose content stays strictly inside its viewBox (880 x H),
# placed inside canvas x 80..960, y 460..1160 (or CTA y 338..1098) so y 1170..1250 stays clean.

import math

INK = '#141312'
R = '#D54E4C'
RS = '#B23F3D'
RL = '#E7716E'
Y = '#F2D98B'
YS = '#DDBF66'
W = '#FFFBF3'
CS = '#E4D9C4'
CSD = '#D3C5AB'
BG = '#F3EDE1'
PANTS = '#5B534C'
DARK = '#252321'
LEAF = '#2B2926'


def svg(body, w=880, h=700, extra=''):
    return (f'<svg class="art" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'xmlns="http://www.w3.org/2000/svg" {extra}>{body}</svg>')


def shadow(cx, cy, rx, ry=14, id_=''):
    i = f' id="{id_}"' if id_ else ''
    return f'<ellipse{i} cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{CS}" stroke="none"/>'


def sparkle(id_, x, y, s, fill=Y):
    d = f'M{x} {y-s} Q{x} {y} {x+s} {y} Q{x} {y} {x} {y+s} Q{x} {y} {x-s} {y} Q{x} {y} {x} {y-s} Z'
    return f'<path id="{id_}" class="spk" d="{d}" fill="{fill}" stroke="{INK}" stroke-width="4"/>'


def plant(id_, x, ybase, s=1.0, pot=R, potS=RS):
    """Clean L2 potted plant centred at x, bottom at ybase."""
    def X(px): return f'{x + px * s:.1f}'
    def Yy(py): return f'{ybase + py * s:.1f}'
    def P(px, py): return f'{x + px * s:.1f} {ybase + py * s:.1f}'
    leaves = [
        f'M{P(0,-66)} C{P(-42,-100)} {P(-54,-154)} {P(-26,-192)} C{P(-4,-156)} {P(-4,-110)} {P(0,-66)} Z',
        f'M{P(4,-66)} C{P(26,-118)} {P(54,-154)} {P(86,-158)} C{P(80,-116)} {P(44,-80)} {P(4,-66)} Z',
        f'M{P(-4,-68)} C{P(-36,-82)} {P(-72,-92)} {P(-88,-126)} C{P(-52,-134)} {P(-18,-108)} {P(-4,-68)} Z',
        f'M{P(2,-70)} C{P(8,-128)} {P(26,-178)} {P(18,-222)} C{P(44,-194)} {P(38,-126)} {P(2,-70)} Z',
    ]
    veins = [
        f'M{P(0,-70)} Q{P(-20,-128)} {P(-24,-180)}',
        f'M{P(6,-70)} Q{P(44,-110)} {P(78,-152)}',
        f'M{P(-4,-72)} Q{P(-46,-96)} {P(-80,-122)}',
        f'M{P(4,-74)} Q{P(22,-144)} {P(20,-208)}',
    ]
    out = f'<g id="{id_}">'
    for d in leaves:
        out += f'<path d="{d}" fill="{LEAF}" stroke-width="4"/>'
    for d in veins:
        out += f'<path d="{d}" fill="none" stroke="{CSD}" stroke-width="3"/>'
    out += (f'<polygon points="{X(-36)},{Yy(-68)} {X(36)},{Yy(-68)} {X(26)},{Yy(0)} {X(-26)},{Yy(0)}" fill="{pot}"/>'
            f'<polygon points="{X(8)},{Yy(-68)} {X(36)},{Yy(-68)} {X(26)},{Yy(0)} {X(4)},{Yy(0)}" fill="{potS}" stroke="none"/>'
            f'<polygon points="{X(-36)},{Yy(-68)} {X(36)},{Yy(-68)} {X(26)},{Yy(0)} {X(-26)},{Yy(0)}" fill="none"/>'
            f'<rect x="{X(-42)}" y="{Yy(-82)}" width="{84*s:.1f}" height="{18*s:.1f}" rx="{6*s:.1f}" fill="{pot}"/>'
            f'</g>')
    return out


# ============================================================
# RECURRING HERO OBJECT 1: THE CREAM JOB-OFFER LETTER (+50% STAMP)
# ============================================================

def offer_letter_core(p, stamped=False, mini=False):
    """Cream job-offer letter centered around (0, 0), body width=470, height=530 (-235..+235, -265..+265).
    Includes corporate logo block, 'JOB OFFER' header, salary line (no invented figures),
    body lines, signature squiggle, and the red '+50%' rubber stamp."""
    ig = ' data-layout-ignore' if mini else ''
    stamp_op = '1' if stamped else '0'
    return f'''
  <!-- Offset paper drop shadow -->
  <rect x="-218" y="-248" width="470" height="530" rx="22" fill="{CSD}" stroke="none"/>
  <!-- Main cream letter body -->
  <rect x="-235" y="-265" width="470" height="530" rx="22" fill="{W}"/>
  <!-- Butter-yellow top accent band -->
  <path d="M-213 -265 H213 Q235 -265 235 -243 V-168 H-235 V-243 Q-235 -265 -213 -265 Z" fill="{Y}" stroke="none"/>
  <path d="M-235 -168 H235" fill="none" stroke="{INK}" stroke-width="5"/>
  <!-- Crisp outer ink outline -->
  <rect x="-235" y="-265" width="470" height="530" rx="22" fill="none"/>

  <!-- Geometric company logo block (top-left of header) -->
  <g transform="translate(-186 -216)">
   <rect x="-22" y="-22" width="44" height="44" rx="10" fill="{W}" stroke="{INK}" stroke-width="4.5"/>
   <polygon points="-12,10 0,-12 12,10" fill="{R}" stroke="{INK}" stroke-width="3.5"/>
   <circle cx="0" cy="4" r="4" fill="{Y}" stroke="none"/>
  </g>
  <!-- Header Title -->
  <text x="-140" y="-202" class="lbl" style="font-size:36px;font-weight:700;letter-spacing:0.11em"{ig}>JOB OFFER</text>

  <!-- Document body: Greeting & Role lines -->
  <rect x="-195" y="-134" width="142" height="18" rx="9" fill="{CSD}" stroke="none"/>
  <rect x="-195" y="-102" width="386" height="14" rx="7" fill="{CS}" stroke="none"/>
  <rect x="-195" y="-76" width="320" height="14" rx="7" fill="{CS}" stroke="none"/>

  <!-- Highlighted SALARY line row (no currency figures!) -->
  <rect x="-198" y="-36" width="396" height="84" rx="16" fill="{BG}" stroke="{INK}" stroke-width="4.5"/>
  <path d="M-182 -36 H-166 V48 H-182 Q-198 48 -198 32 V-20 Q-198 -36 -182 -36 Z" fill="{Y}" stroke="none"/>
  <path d="M-166 -36 V48" fill="none" stroke="{INK}" stroke-width="4"/>
  <text x="-144" y="19" class="lbl" style="font-size:35px;font-weight:700;letter-spacing:0.08em"{ig}>SALARY</text>
  <rect x="44" y="-8" width="128" height="28" rx="14" fill="{Y}" stroke="{INK}" stroke-width="3.5"/>

  <!-- Terms lines below salary -->
  <rect x="-195" y="76" width="376" height="14" rx="7" fill="{CS}" stroke="none"/>
  <rect x="-195" y="102" width="340" height="14" rx="7" fill="{CS}" stroke="none"/>
  <rect x="-195" y="128" width="230" height="14" rx="7" fill="{CS}" stroke="none"/>

  <!-- Signature & red seal at bottom -->
  <path d="M-195 198 Q-170 166 -144 198 T-96 190 T-52 198" fill="none" stroke="{INK}" stroke-width="4.5"/>
  <path d="M-195 216 H-38" fill="none" stroke="{CSD}" stroke-width="4"/>
  <text x="-195" y="242" class="lbl" style="font-size:20px;fill:{PANTS};letter-spacing:0.12em" data-layout-ignore>SIGNED</text>
  <!-- Small ribbon seal bottom-right -->
  <g transform="translate(152 204)">
   <polygon points="-10,14 -18,46 0,36 18,46 10,14" fill="{RS}" stroke="{INK}" stroke-width="3.5"/>
   <circle cx="0" cy="0" r="24" fill="{Y}" stroke="{INK}" stroke-width="4.5"/>
   <circle cx="0" cy="0" r="14" fill="none" stroke="{YS}" stroke-width="3.5"/>
  </g>

  <!-- RED RUBBER "+50%" STAMP -->
  <g id="{p}stamp" opacity="{stamp_op}" data-layout-allow-overlap>
   <g transform="translate(46 96) rotate(-11)">
    <rect x="-144" y="-68" width="288" height="136" rx="20" fill="{W}" fill-opacity="0.96" stroke="{R}" stroke-width="11"/>
    <rect x="-128" y="-52" width="256" height="104" rx="12" fill="none" stroke="{R}" stroke-width="4" stroke-dasharray="10 6"/>
    <text x="0" y="26" text-anchor="middle" class="num" font-size="94" letter-spacing="-0.02em" fill="{R}" data-layout-allow-overlap{ig}>+50%</text>
   </g>
   <!-- Stamp impact burst lines -->
   <g id="{p}sburst" stroke="{R}" stroke-width="7" fill="none" opacity="0">
    <path d="M-104 40 L-134 24 M192 6 L224 -12 M-84 188 L-114 206 M198 158 L230 176"/>
   </g>
  </g>'''


# ============================================================
# BEAT 1 & BEAT 2: OFFER LETTER (+ WARNING NOTES, TOXIC TAG, QUESTION)
# ============================================================

def art_offer_scene(p, mode='b1'):
    """Shared Offer Letter composition for Beat 1 (Frame 1 already visible + +50% stamp)
    and Beat 2 (exact same stamped letter + warning notes + TOXIC CULTURE tag + handwritten question).
    ViewBox 880 x 700."""
    extras = ''
    if mode == 'b2':
        extras = f'''
 <!-- WARNING NOTES STACK pinned to left margin of letter (pins on at 3.20 "former employees") -->
 <g id="{p}notes" data-layout-allow-overlap>
  <!-- Back note 3 -->
  <g id="{p}n3" opacity="0">
   <g transform="translate(136 254) rotate(-13)">
    <rect x="-90" y="-68" width="180" height="136" rx="12" fill="{YS}" stroke="{INK}" stroke-width="4.5"/>
   </g>
  </g>
  <!-- Mid note 2 -->
  <g id="{p}n2" opacity="0">
   <g transform="translate(148 232) rotate(-6)">
    <rect x="-90" y="-68" width="180" height="136" rx="12" fill="{Y}" stroke="{INK}" stroke-width="4.5"/>
    <path d="M-60 -22 H52 M-60 4 H38" fill="none" stroke="{INK}" stroke-width="4.5" opacity="0.5"/>
   </g>
  </g>
  <!-- Front warning note 1 -->
  <g id="{p}n1" opacity="0">
   <g transform="translate(160 212) rotate(-3)">
    <rect x="-92" y="-66" width="194" height="146" rx="12" fill="{CSD}" stroke="none"/>
    <rect x="-100" y="-74" width="194" height="146" rx="12" fill="{Y}" stroke="{INK}" stroke-width="5"/>
    <!-- Warning triangle -->
    <polygon points="-60,-18 -38,-56 -16,-18" fill="{R}" stroke="{INK}" stroke-width="4"/>
    <text x="-38" y="-24" text-anchor="middle" class="num" font-size="24" fill="{W}" data-layout-ignore>!</text>
    <text x="24" y="-30" text-anchor="middle" class="lbl" style="font-size:21px;font-weight:700;letter-spacing:0.06em" data-layout-ignore>WARN</text>
    <path d="M-74 10 H66 M-74 34 H48 M-74 54 H22" fill="none" stroke="{INK}" stroke-width="5" opacity="0.72"/>
   </g>
   <!-- Red push-pin anchoring stack to letter left edge -->
   <circle cx="222" cy="156" r="14" fill="{R}" stroke="{INK}" stroke-width="4.5"/>
   <circle cx="218" cy="152" r="4" fill="{RL}" stroke="none"/>
  </g>
 </g>

 <!-- RED "TOXIC CULTURE" TAG (slaps on at 5.98 "toxic.") -->
 <g id="{p}toxic" opacity="0" data-layout-allow-overlap>
  <g transform="translate(478 232) rotate(3.8)">
   <rect x="-212" y="-44" width="440" height="96" rx="18" fill="{INK}" fill-opacity="0.22" stroke="none"/>
   <rect x="-220" y="-52" width="440" height="96" rx="18" fill="{R}" stroke="{INK}" stroke-width="5.5"/>
   <rect x="-206" y="-38" width="412" height="68" rx="11" fill="none" stroke="{W}" stroke-width="3" stroke-dasharray="9 6" opacity="0.65"/>
   <!-- Warning triangle inside tag -->
   <polygon points="-178,14 -158,-22 -138,14" fill="{Y}" stroke="{INK}" stroke-width="3.5"/>
   <text x="-158" y="9" text-anchor="middle" class="num" font-size="22" fill="{INK}" data-layout-ignore>!</text>
   <text x="26" y="11" text-anchor="middle" class="lbl cream" style="font-size:35px;font-weight:700;letter-spacing:0.09em" data-layout-allow-overlap>TOXIC CULTURE</text>
  </g>
  <g id="{p}tburst" stroke="{R}" stroke-width="7" fill="none" opacity="0">
   <path d="M232 184 L198 166 M712 204 L748 192 M242 286 L210 304 M704 312 L736 332"/>
  </g>
 </g>

 <!-- HANDWRITTEN-STYLE "Would you take it?" + DRAWN UNDERLINE (at 7.00) -->
 <g id="{p}ask" data-layout-allow-overlap>
  <text id="{p}askt" x="440" y="654" text-anchor="middle" class="hand" font-size="60" fill="{INK}" opacity="0" data-layout-allow-overlap>Would you take it?</text>
  <path id="{p}asku" class="dr" pathLength="1" d="M236 672 Q342 664 440 672 T644 668" fill="none" stroke="{R}" stroke-width="7" stroke-linecap="round"/>
 </g>'''

    b = f'''<g class="k">
 <!-- Subtle soft ground shadow -->
 {shadow(456, 586, 256, 16)}

 <!-- Supporting cozy L2 desk plant on far-right (keeps frame rich, uncluttered) -->
 {plant(p+'pl', 792, 578, 0.56)}

 <!-- THE CREAM JOB OFFER LETTER (outer wrapper has NO transform so GSAP x/y/scale never clobbers translate!) -->
 <g id="{p}letter">
  <g transform="translate(456 292) rotate(-1.5)">
   {offer_letter_core(p, stamped=(mode == 'b2'))}
  </g>
 </g>

 {extras}

 <!-- L2 Sparkles -->
 {sparkle(p+'sp1', 756, 108, 18, Y)}
 {sparkle(p+'sp2', 124, 480, 14, R)}
 {sparkle(p+'sp3', 132, 108, 15, Y)}
</g>'''
    return svg(b, 880, 700)


# ============================================================
# BEAT 3: CAREER LADDER + HEARTBEAT + GROWTH BANNER
# ============================================================

def art_career_ladder(p):
    """Beat 3: Offer shrinks/slides back as a tall one-rung career ladder grows.
    Heartbeat pulse at 9.38; +50% HIKE climber ascends; red GROWTH banner unfurls at 12.10."""
    F = 642
    # Ladder centred at x=480, width=172 (left rail x=394, right rail x=566), top y=154..610
    rungs = ''.join(
        f'<rect x="404" y="{ry}" width="152" height="18" rx="7" fill="{W}" stroke="{INK}" stroke-width="4.5"/>'
        for ry in [548, 474, 400, 326, 252, 178]
    )
    b = f'''<g class="k">
 <path id="{p}floor" d="M24 {F} H856" fill="none"/>
 {shadow(480, F+5, 210, 15)}
 {shadow(156, F+5, 108, 12)}

 <!-- Shrinking offer letter sliding back to left side (outer g has no transform!) -->
 <g id="{p}oldoff" data-layout-allow-overlap>
  <g transform="translate(158 492) scale(0.42) rotate(-5)">
   {offer_letter_core(p+'m', stamped=True, mini=True)}
  </g>
 </g>

 <!-- TALL ONE-RUNG CAREER LADDER -->
 <g id="{p}ladder">
  <!-- Offset shadow behind ladder rails -->
  <rect x="402" y="156" width="22" height="456" rx="10" fill="{CSD}" stroke="none"/>
  <rect x="558" y="156" width="22" height="456" rx="10" fill="{CSD}" stroke="none"/>
  <!-- Rungs -->
  {rungs}
  <!-- Left & right vertical rails -->
  <rect x="388" y="148" width="24" height="464" rx="11" fill="{Y}"/>
  <rect x="548" y="148" width="24" height="464" rx="11" fill="{Y}"/>
  <!-- Base plaque: CAREER LADDER -->
  <rect x="316" y="582" width="328" height="62" rx="16" fill="{W}"/>
  <rect x="316" y="582" width="24" height="62" rx="10" fill="{R}" stroke="none"/>
  <rect x="316" y="582" width="328" height="62" rx="16" fill="none"/>
  <text x="492" y="624" text-anchor="middle" class="lbl" style="font-size:28px;font-weight:700;letter-spacing:0.1em">CAREER LADDER</text>
 </g>

 <!-- HEARTBEAT ECG PULSE LINE (pulses at 9.38 "heartbeat.") -->
 <g id="{p}hb" data-layout-allow-overlap>
  <path id="{p}hbline" class="dr" pathLength="1"
        d="M64 316 H178 L198 280 L220 356 L244 236 L266 346 L284 316 H358"
        fill="none" stroke="{R}" stroke-width="7.5" stroke-linecap="round" stroke-linejoin="round"/>
  <circle id="{p}hbdot" cx="244" cy="236" r="11" fill="{R}" stroke="{INK}" stroke-width="4" opacity="0"/>
 </g>

 <!-- "+50% HIKE" CLIMBER BADGE ascending the ladder -->
 <g id="{p}climber" data-layout-allow-overlap>
  <!-- Friendly mini L2 climber holding +50% tag -->
  <g transform="translate(480 510)">
   <rect x="-104" y="-36" width="208" height="72" rx="16" fill="{W}" stroke="{INK}" stroke-width="5"/>
   <rect x="-104" y="-36" width="208" height="16" rx="8" fill="{Y}" stroke="none"/>
   <rect x="-104" y="-36" width="208" height="72" rx="16" fill="none" stroke="{INK}" stroke-width="5"/>
   <text x="0" y="16" text-anchor="middle" class="num" font-size="38" fill="{R}" data-layout-allow-overlap>+50% HIKE</text>
  </g>
 </g>

 <!-- RED "GROWTH" BANNER UNFURLING AT TOP (12.10 "screams" -> 12.78 "growth.") -->
 <g id="{p}banner" opacity="0" data-layout-allow-overlap>
  <!-- Banner pole -->
  <rect x="472" y="64" width="16" height="92" rx="7" fill="{INK}"/>
  <!-- Unfurling red pennant / ribbon banner -->
  <g id="{p}bflag">
   <path d="M276 34 H696 L668 84 L696 134 H276 L304 84 Z" fill="{RS}" stroke="none" transform="translate(8 8)"/>
   <path d="M276 34 H696 L668 84 L696 134 H276 L304 84 Z" fill="{R}" stroke="{INK}" stroke-width="5.5"/>
   <text x="486" y="102" text-anchor="middle" class="num" font-size="60" letter-spacing="0.08em" fill="{W}" data-layout-allow-overlap>GROWTH</text>
  </g>
  <!-- Scream / shout impact rays around banner -->
  <g id="{p}sburst" stroke="{R}" stroke-width="7.5" fill="none" opacity="0">
   <path d="M236 52 L196 34 M228 86 H184 M236 120 L196 138"/>
   <path d="M736 52 L776 34 M744 86 H788 M736 120 L776 138"/>
  </g>
 </g>

 {sparkle(p+'sp1', 720, 250, 18, Y)}
 {sparkle(p+'sp2', 756, 480, 15, R)}
 {sparkle(p+'sp3', 110, 198, 16, Y)}
</g>'''
    return svg(b, 880, 700)


# ============================================================
# RECURRING HERO OBJECT 2: THE 7 DIMENSION CARDS (Beats 4, 5, 6, 7, 9)
# ============================================================

def dim_icon(key, cx, cy, s=1.0, red_mode=False):
    """Crisp flat-vector L2 icon for each of the 7 career dimensions, centred at (cx, cy)."""
    ink = W if red_mode else INK
    acc = Y if red_mode else R
    fill2 = RS if red_mode else Y
    fillw = RL if red_mode else W

    if key == 'INCOME':
        # Clean upward money/wallet bars (NO invented numbers!)
        return (
            f'<g transform="translate({cx} {cy}) scale({s})">'
            f'<rect x="-32" y="2" width="16" height="24" rx="4" fill="{fillw}" stroke="{ink}" stroke-width="4"/>'
            f'<rect x="-8" y="-10" width="16" height="36" rx="4" fill="{fill2}" stroke="{ink}" stroke-width="4"/>'
            f'<rect x="16" y="-24" width="16" height="50" rx="4" fill="{acc}" stroke="{ink}" stroke-width="4"/>'
            f'</g>'
        )
    if key == 'TITLE':
        # Award ribbon / crown star badge
        return (
            f'<g transform="translate({cx} {cy}) scale({s})">'
            f'<polygon points="-14,10 -20,34 0,25 20,34 14,10" fill="{acc}" stroke="{ink}" stroke-width="3.8"/>'
            f'<circle cx="0" cy="-6" r="22" fill="{fill2}" stroke="{ink}" stroke-width="4.2"/>'
            f'<polygon points="0,-19 4,-8 15,-8 6,-1 9,10 0,3 -9,10 -6,-1 -15,-8 -4,-8" fill="{W}" stroke="{ink}" stroke-width="3"/>'
            f'</g>'
        )
    if key == 'FREEDOM':
        # Mini ajar red QUIT door with yellow glow (channel signature!)
        return (
            f'<g transform="translate({cx} {cy}) scale({s})">'
            f'<rect x="-24" y="-28" width="48" height="56" rx="5" fill="{CS}" stroke="{ink}" stroke-width="4"/>'
            f'<rect x="-18" y="-22" width="36" height="50" fill="{Y}" stroke="{ink}" stroke-width="3.5"/>'
            f'<polygon points="-18,-22 8,-16 8,28 -18,28" fill="{R}" stroke="{ink}" stroke-width="3.5"/>'
            f'<circle cx="2" cy="4" r="3.5" fill="{Y}" stroke="none"/>'
            f'</g>'
        )
    if key == 'COLLEAGUES':
        # Two friendly L2 silhouettes side by side
        return (
            f'<g transform="translate({cx} {cy}) scale({s})">'
            f'<circle cx="-15" cy="-12" r="12" fill="{fill2}" stroke="{ink}" stroke-width="4"/>'
            f'<path d="M-32 24 Q-32 4 -15 4 Q2 4 2 24 Z" fill="{fillw}" stroke="{ink}" stroke-width="4"/>'
            f'<circle cx="15" cy="-12" r="12" fill="{fillw}" stroke="{ink}" stroke-width="4"/>'
            f'<path d="M-2 24 Q-2 4 15 4 Q32 4 32 24 Z" fill="{acc}" stroke="{ink}" stroke-width="4"/>'
            f'</g>'
        )
    if key == 'LOCATION':
        # Clean map pin on soft base ring
        return (
            f'<g transform="translate({cx} {cy}) scale({s})">'
            f'<ellipse cx="0" cy="24" rx="22" ry="6" fill="{CS}" stroke="{ink}" stroke-width="3"/>'
            f'<path d="M0 22 C-20 4 -22 -18 0 -28 C22 -18 20 4 0 22 Z" fill="{acc}" stroke="{ink}" stroke-width="4.2"/>'
            f'<circle cx="0" cy="-8" r="8" fill="{W}" stroke="{ink}" stroke-width="3.8"/>'
            f'</g>'
        )
    if key == 'WORK-LIFE':
        # Balanced sun & calm crescent / seesaw balance
        return (
            f'<g transform="translate({cx} {cy}) scale({s})">'
            f'<path d="M-28 20 H28" fill="none" stroke="{ink}" stroke-width="4.5"/>'
            f'<polygon points="-8,20 0,6 8,20" fill="{ink}" stroke="none"/>'
            f'<path d="M-26 6 H26" fill="none" stroke="{ink}" stroke-width="4.5"/>'
            f'<circle cx="-16" cy="-10" r="12" fill="{Y}" stroke="{ink}" stroke-width="3.8"/>'
            f'<path d="M16 -22 A12 12 0 1 0 28 -8 A9 9 0 1 1 16 -22 Z" fill="{acc}" stroke="{ink}" stroke-width="3.5"/>'
            f'</g>'
        )
    # TOXICITY: sharp warning hazard triangle with '!'
    tri_fill = Y if red_mode else R
    exc_fill = INK if red_mode else W
    return (
        f'<g transform="translate({cx} {cy}) scale({s})">'
        f'<polygon points="0,-28 28,22 -28,22" fill="{tri_fill}" stroke="{ink}" stroke-width="4.5"/>'
        f'<text x="0" y="14" text-anchor="middle" class="num" font-size="30" fill="{exc_fill}" data-layout-ignore>!</text>'
        f'</g>'
    )


# Canonical 7-card layout coordinates for Beats 4, 5, 6 (inside 880x700, generous 22px outer safety margin!)
# Top row: 3 cards (w=236, h=220); Bottom row: 4 cards (w=198, h=214), all labels >= 28px!
DIM_CARDS_LAYOUT = [
    # (key, label, cx, cy, w, h, rot, font_size, tracking)
    ('INCOME',     'INCOME',     174, 224, 236, 220, -2.0, 30, '0.09em'),
    ('TITLE',      'TITLE',      440, 206, 236, 220,  0.0, 30, '0.09em'),
    ('FREEDOM',    'FREEDOM',    706, 224, 236, 220,  2.0, 30, '0.08em'),
    ('COLLEAGUES', 'COLLEAGUES', 124, 486, 198, 214, -2.0, 28, '-0.02em'),
    ('LOCATION',   'LOCATION',   335, 472, 198, 214, -0.7, 29, '0.04em'),
    ('WORK-LIFE',  'WORK-LIFE',  545, 472, 198, 214,  0.7, 29, '0.02em'),
    ('TOXICITY',   'TOXICITY',   756, 486, 198, 214,  2.0, 29, '0.04em'),
]


def dim_card(id_, key, label, cx, cy, w, h, rot=0.0, fs=28, tr='0.08em', ghost=False, red_mode=False):
    """One crisp L2 dimension card centred at (cx, cy). Outer <g> has NO transform so GSAP x/y/scale stay exact!"""
    hw, hh = w / 2, h / 2
    hdr_h = 34
    card_fill = BG if ghost else (R if red_mode else W)
    hdr_fill = CS if ghost else (RS if red_mode else Y)
    lbl_fill = CSD if ghost else (W if red_mode else INK)
    shd_fill = CS if ghost else CSD
    icon_op = '0.35' if ghost else '1'
    ig = ' data-layout-ignore' if ghost else ''
    return f'''<g id="{id_}" data-layout-allow-overlap>
  <g transform="translate({cx} {cy}) rotate({rot})">
   <rect x="{-hw+8:.1f}" y="{-hh+10:.1f}" width="{w}" height="{h}" rx="20" fill="{shd_fill}" stroke="none"/>
   <rect x="{-hw:.1f}" y="{-hh:.1f}" width="{w}" height="{h}" rx="20" fill="{card_fill}"/>
   <path d="M{-hw+20:.1f} {-hh:.1f} H{hw-20:.1f} Q{hw:.1f} {-hh:.1f} {hw:.1f} {-hh+20:.1f} V{-hh+hdr_h:.1f} H{-hw:.1f} V{-hh+20:.1f} Q{-hw:.1f} {-hh:.1f} {-hw+20:.1f} {-hh:.1f} Z" fill="{hdr_fill}" stroke="none"/>
   <path d="M{-hw:.1f} {-hh+hdr_h:.1f} H{hw:.1f}" fill="none" stroke="{INK}" stroke-width="4.5"/>
   <rect x="{-hw:.1f}" y="{-hh:.1f}" width="{w}" height="{h}" rx="20" fill="none"/>
   <g opacity="{icon_op}">{dim_icon(key, 0, -10, 1.05 if w > 210 else 0.96, red_mode=red_mode)}</g>
   <text x="0" y="{hh-30:.1f}" text-anchor="middle" class="lbl" style="font-size:{fs}px;font-weight:700;letter-spacing:{tr};fill:{lbl_fill}" data-layout-allow-overlap{ig}>{label}</text>
  </g>
 </g>'''


# ============================================================
# BEAT 4: CRACKED ONE-LINE -> 7 DIMENSION CARDS FAN OUT
# ============================================================

def art_cracked_dimensions(p):
    """Beat 4: Single career ladder strips down to one thin line that cracks,
    then 7 faintly labelled dimension cards fan out around the graphic zone."""
    F = 642
    cards = ''.join(
        dim_card(f'{p}c{i}', key, lbl, cx, cy, w, h, rot, fs, tr, ghost=True)
        for i, (key, lbl, cx, cy, w, h, rot, fs, tr) in enumerate(DIM_CARDS_LAYOUT)
    )
    b = f'''<g class="k">
 <path id="{p}floor" d="M24 {F} H856" fill="none"/>
 {shadow(440, F+5, 220, 15)}

 <!-- Subtle connecting arc behind cards (visible as cards fan out at 17.16) -->
 <path id="{p}arc" d="M120 476 Q140 206 440 188 Q740 206 760 476" fill="none" stroke="{CSD}" stroke-width="5" stroke-dasharray="10 12" opacity="0"/>

 <!-- 7 FAINT DIMENSION CARDS (bloom/fan out from center at 17.16) -->
 <g id="{p}cards" opacity="0">
  {cards}
 </g>

 <!-- SINGLE LADDER / THIN LINE IN CENTER (cracks at 15.24-16.74!) -->
 <g id="{p}single">
  <!-- Fading ladder rungs -->
  <g id="{p}rungs">
   <rect x="382" y="180" width="116" height="16" rx="6" fill="{W}" stroke-width="4"/>
   <rect x="382" y="264" width="116" height="16" rx="6" fill="{W}" stroke-width="4"/>
   <rect x="382" y="348" width="116" height="16" rx="6" fill="{W}" stroke-width="4"/>
   <rect x="382" y="432" width="116" height="16" rx="6" fill="{W}" stroke-width="4"/>
   <rect x="382" y="516" width="116" height="16" rx="6" fill="{W}" stroke-width="4"/>
  </g>
  <!-- Left & right halves of the thin single line (split apart on crack!) -->
  <g id="{p}ltop">
   <rect x="430" y="96" width="20" height="248" rx="8" fill="{Y}"/>
   <polygon points="440,54 414,104 466,104" fill="{R}"/>
  </g>
  <g id="{p}lbot">
   <rect x="430" y="344" width="20" height="252" rx="8" fill="{Y}"/>
  </g>
  <!-- Jagged crack fracture across middle -->
  <path id="{p}crack" class="dr" pathLength="1"
        d="M402 320 L432 340 L414 356 L464 374 L446 392 L478 408"
        fill="none" stroke="{R}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>
  <!-- "ONE LINE" base tag -->
  <g id="{p}tag">
   <rect x="330" y="578" width="220" height="58" rx="14" fill="{W}"/>
   <text x="440" y="617" text-anchor="middle" class="lbl" style="font-size:28px;font-weight:700;letter-spacing:0.12em">ONE LINE</text>
  </g>
 </g>

 {sparkle(p+'sp1', 836, 72, 16, Y)}
 {sparkle(p+'sp2', 44, 72, 15, R)}
</g>'''
    return svg(b, 880, 700)


# ============================================================
# BEAT 5: 7 DIMENSION CARDS SNAP INTO PLACE ONE BY ONE
# ============================================================

def art_seven_cards(p):
    """Beat 5: Exact same 7 cards as Beat 4 end, snapping bright & active one by one
    to each spoken dimension word (INCOME..TOXICITY)."""
    F = 642
    # Each card has a ghost under-slot + crisp illuminated card popping in on its exact word!
    ghosts = ''.join(
        dim_card(f'{p}g{i}', key, lbl, cx, cy, w, h, rot, fs, tr, ghost=True)
        for i, (key, lbl, cx, cy, w, h, rot, fs, tr) in enumerate(DIM_CARDS_LAYOUT)
    )
    actives = ''.join(
        dim_card(f'{p}c{i}', key, lbl, cx, cy, w, h, rot, fs, tr, ghost=False)
        for i, (key, lbl, cx, cy, w, h, rot, fs, tr) in enumerate(DIM_CARDS_LAYOUT)
    )
    b = f'''<g class="k">
 <path id="{p}floor" d="M24 {F} H856" fill="none"/>
 {shadow(440, F+5, 360, 15)}

 <!-- Subtle connecting architectural arc tying all 7 cards into ONE unified object -->
 <path d="M120 476 Q140 206 440 188 Q740 206 760 476" fill="none" stroke="{CSD}" stroke-width="5" stroke-dasharray="10 12"/>

 <!-- Subtle ghost silhouettes already present at Beat 5 start (seamless from Beat 4) -->
 <g id="{p}ghosts">{ghosts}</g>

 <!-- Illuminated crisp cards snapping in one by one on the spoken word -->
 <g id="{p}actives">{actives}</g>

 {sparkle(p+'sp1', 44, 72, 16, Y)}
 {sparkle(p+'sp2', 836, 72, 16, R)}
</g>'''
    return svg(b, 880, 700)


# ============================================================
# BEAT 6: HERO MOVE — SQUASH 7 CARDS INTO ONE SALARY BAR
# ============================================================

def art_squash_salary(p):
    """Beat 6: Starts on exact same 7 active cards.
    25.54: cards jitter/overcrowd (overload).
    27.80: red compressing clamp + SHORTCUT arrow appear.
    28.64-31.90: clamps & ladder squash cards into crushed base + extrude ONE thick SALARY bar.
    32.12: bold SALARY label slams onto bar!"""
    F = 642
    actives = ''.join(
        dim_card(f'{p}c{i}', key, lbl, cx, cy, w, h, rot, fs, tr, ghost=False)
        for i, (key, lbl, cx, cy, w, h, rot, fs, tr) in enumerate(DIM_CARDS_LAYOUT)
    )
    # Ladder notches inside the extruded thick SALARY bar
    notches = ''.join(
        f'<path d="M352 {ny} H528" fill="none" stroke="{YS}" stroke-width="6" opacity="0.65"/>'
        for ny in [492, 428, 364, 300, 236, 172]
    )
    b = f'''<g class="k">
 <path id="{p}floor" d="M24 {F} H856" fill="none"/>
 {shadow(440, F+5, 340, 16)}

 <!-- Brain overload stress squiggles above cards (25.54-27.70) -->
 <g id="{p}stress" stroke="{R}" stroke-width="6.5" fill="none" opacity="0">
  <path d="M168 62 Q180 42 194 62 T220 62"/>
  <path d="M406 42 Q420 22 434 42 T462 42"/>
  <path d="M662 62 Q676 42 690 62 T716 62"/>
 </g>

 <!-- CRUSHED DIMENSION CARDS STACK (sits flattened at bottom of SALARY bar after squash) -->
 <g id="{p}crushed" opacity="0" data-layout-allow-overlap>
  <rect x="196" y="610" width="488" height="28" rx="9" fill="{CS}"/>
  <rect x="218" y="588" width="444" height="26" rx="8" fill="{W}"/>
  <rect x="242" y="566" width="396" height="26" rx="8" fill="{CS}"/>
  <text x="440" y="608" text-anchor="middle" class="lbl" style="font-size:17px;fill:{PANTS};letter-spacing:0.12em" data-layout-ignore>FREEDOM · LIFE · CULTURE · REST</text>
 </g>

 <!-- ONE THICK VERTICAL SALARY BAR / LADDER (extrudes upward during squash!) -->
 <g id="{p}sbar" opacity="0" data-layout-allow-overlap>
  <!-- Offset shadow -->
  <rect x="336" y="136" width="234" height="444" rx="22" fill="{CSD}" stroke="none"/>
  <!-- Main butter-yellow SALARY column -->
  <rect x="322" y="122" width="236" height="446" rx="22" fill="{Y}"/>
  <!-- Right shade strip -->
  <path d="M518 122 H536 Q558 122 558 144 V546 Q558 568 536 568 H518 Z" fill="{YS}" stroke="none"/>
  {notches}
  <!-- Crisp outer border -->
  <rect x="322" y="122" width="236" height="446" rx="22" fill="none"/>
  <!-- Top red upward arrow cap -->
  <polygon points="440,52 384,122 496,122" fill="{R}"/>
 </g>

 <!-- THE 7 DIMENSION CARDS (identical start state to Beat 5 end!) -->
 <g id="{p}cards">{actives}</g>

 <!-- RED COMPRESSING CLAMP JAWS + SHORTCUT ARROWS (slam in at 27.80!) -->
 <g id="{p}clampL" opacity="0" data-layout-allow-overlap>
  <!-- Left piston arm + jaw (starts clean at left edge before crushing inward) -->
  <rect x="-24" y="328" width="52" height="58" rx="10" fill="{RS}"/>
  <rect x="14" y="164" width="34" height="388" rx="13" fill="{R}"/>
  <path d="M62 357 H116 M96 335 L120 357 L96 379" fill="none" stroke="{R}" stroke-width="8"/>
 </g>
 <g id="{p}clampR" opacity="0" data-layout-allow-overlap>
  <!-- Right piston arm + jaw -->
  <rect x="852" y="328" width="52" height="58" rx="10" fill="{RS}"/>
  <rect x="832" y="164" width="34" height="388" rx="13" fill="{R}"/>
  <path d="M818 357 H764 M784 335 L760 357 L784 379" fill="none" stroke="{R}" stroke-width="8"/>
 </g>
 <!-- "SHORTCUT" badge floating cleanly above TITLE card -->
 <g id="{p}scbadge" opacity="0" data-layout-allow-overlap>
  <rect x="314" y="14" width="252" height="56" rx="28" fill="{R}"/>
  <text x="440" y="52" text-anchor="middle" class="lbl cream" style="font-size:28px;font-weight:700;letter-spacing:0.12em">SHORTCUT</text>
 </g>

 <!-- BIG "SALARY" LABEL PLATE (slams on at 32.12 "Salary.") -->
 <g id="{p}slabel" opacity="0" data-layout-allow-overlap>
  <rect x="228" y="310" width="440" height="128" rx="22" fill="{INK}" fill-opacity="0.18" stroke="none"/>
  <rect x="220" y="300" width="440" height="128" rx="22" fill="{W}" stroke="{INK}" stroke-width="6"/>
  <rect x="236" y="316" width="408" height="96" rx="14" fill="none" stroke="{R}" stroke-width="4" stroke-dasharray="10 6"/>
  <text x="440" y="390" text-anchor="middle" class="num" font-size="82" letter-spacing="0.04em" fill="{R}" data-layout-allow-overlap>SALARY</text>
  <g id="{p}sburst" stroke="{R}" stroke-width="7.5" fill="none" opacity="0">
   <path d="M198 310 L164 290 M682 310 L716 290 M198 418 L164 438 M682 418 L716 438"/>
  </g>
 </g>

 {sparkle(p+'sp1', 152, 166, 17, Y)}
 {sparkle(p+'sp2', 728, 166, 17, R)}
</g>'''
    return svg(b, 880, 700)


# ============================================================
# BEAT 7: CHASING THE WRONG METRIC (SALARY SHOOTS UP, FREEDOM SAGS, TOXICITY CREEPS)
# ============================================================

def art_wrong_metric(p):
    """Beat 7: SALARY bar/ladder shoots upward while crushed base cards stay flattened;
    FREEDOM & life cue sag on left while a red TOXICITY wedge creeps in on right."""
    F = 642
    notches = ''.join(
        f'<path d="M370 {ny} H510" fill="none" stroke="{YS}" stroke-width="6" opacity="0.65"/>'
        for ny in [496, 434, 372, 310, 248, 186, 124]
    )
    b = f'''<g class="k">
 <path id="{p}floor" d="M24 {F} H856" fill="none"/>
 {shadow(440, F+5, 360, 15)}

 <!-- Upward chase speed lines behind rising SALARY bar -->
 <g id="{p}speed" stroke="{R}" stroke-width="6" fill="none" opacity="0">
  <path d="M294 260 V140 M318 340 V250 M586 260 V140 M562 340 V250"/>
 </g>

 <!-- LEFT SIDE: SAGGING FREEDOM & WORK-LIFE CARDS (outer g has NO transform!) -->
 <g id="{p}sagL" data-layout-allow-overlap>
  <!-- Tilted, sagging muted FREEDOM card -->
  <g id="{p}sag1">
   <g transform="translate(174 514)">
    <rect x="-130" y="-50" width="260" height="100" rx="16" fill="{CS}"/>
    <rect x="-130" y="-50" width="22" height="100" rx="8" fill="{CSD}" stroke="none"/>
    <rect x="-130" y="-50" width="260" height="100" rx="16" fill="none"/>
    <text x="10" y="10" text-anchor="middle" class="lbl" style="font-size:30px;font-weight:700;fill:{PANTS};letter-spacing:0.08em">FREEDOM</text>
   </g>
  </g>
  <!-- Crushed muted LIFE/PEACE card underneath -->
  <g id="{p}sag2">
   <g transform="translate(166 604)">
    <rect x="-138" y="-36" width="276" height="72" rx="14" fill="{BG}" stroke="{PANTS}" stroke-width="4.5"/>
    <!-- Muted sun/life icon -->
    <circle cx="-106" cy="0" r="13" fill="{CSD}" stroke="{PANTS}" stroke-width="3.5"/>
    <text x="16" y="10" text-anchor="middle" class="lbl" style="font-size:29px;font-weight:700;fill:{PANTS};letter-spacing:0.05em">WORK-LIFE</text>
   </g>
  </g>
  <!-- Downward droop arrow -->
  <path id="{p}droop" d="M74 374 V440 M58 424 L74 442 L90 424" fill="none" stroke="{PANTS}" stroke-width="6" opacity="0"/>
 </g>

 <!-- RIGHT SIDE: CREEPING RED TOXICITY WEDGE (creeps in at 36.36-37.54!) -->
 <g id="{p}wedge" opacity="0" data-layout-allow-overlap>
  <!-- Sharp triangular red toxicity wedge creeping up from crushed base -->
  <polygon points="560,640 842,640 842,410 560,556" fill="{RS}" stroke="none" transform="translate(6 4)"/>
  <polygon points="556,638 836,638 836,418 556,556" fill="{R}"/>
  <!-- Hazard triangle + TOXICITY label on wedge -->
  <polygon points="736,514 756,476 776,514" fill="{Y}" stroke="{INK}" stroke-width="3.8"/>
  <text x="756" y="509" text-anchor="middle" class="num" font-size="22" fill="{INK}" data-layout-ignore>!</text>
  <text x="714" y="600" text-anchor="middle" class="lbl cream" style="font-size:30px;font-weight:700;letter-spacing:0.09em">TOXICITY</text>
  <!-- Warning pulse ripples above wedge -->
  <g id="{p}wrip" stroke="{R}" stroke-width="6" fill="none">
   <path d="M792 384 L820 364 M748 398 L762 368 M834 402 L862 396"/>
  </g>
 </g>

 <!-- CRUSHED CARDS PANCAKE AT BASE OF SALARY BAR -->
 <g id="{p}base" data-layout-allow-overlap>
  <rect x="294" y="608" width="292" height="30" rx="9" fill="{CS}"/>
  <rect x="310" y="582" width="260" height="28" rx="8" fill="{W}"/>
 </g>

 <!-- SHOOTING-UP SALARY BAR / LADDER -->
 <g id="{p}bar" data-layout-allow-overlap>
  <rect x="356" y="106" width="194" height="476" rx="20" fill="{CSD}" stroke="none"/>
  <rect x="344" y="96" width="192" height="486" rx="20" fill="{Y}"/>
  <path d="M502 96 H516 Q536 96 536 116 V562 Q536 582 516 582 H502 Z" fill="{YS}" stroke="none"/>
  {notches}
  <rect x="344" y="96" width="192" height="486" rx="20" fill="none"/>
  <!-- Sharp red upward arrowhead at top -->
  <polygon points="440,22 374,98 506,98" fill="{R}"/>
  <!-- SALARY plaque -->
  <rect x="302" y="294" width="276" height="92" rx="18" fill="{W}" stroke="{INK}" stroke-width="5.5"/>
  <text x="440" y="357" text-anchor="middle" class="num" font-size="56" letter-spacing="0.04em" fill="{R}" data-layout-allow-overlap>SALARY</text>
 </g>

 {sparkle(p+'sp1', 214, 152, 16, Y)}
 {sparkle(p+'sp2', 666, 156, 15, R)}
</g>'''
    return svg(b, 880, 700)


# ============================================================
# BEAT 8: INCOME SHRINKS, FREE TIME GROWS + STRUCK "RUINING MY CAREER" TAG
# ============================================================

def art_trade_bars(p):
    """Beat 8: Two clean dimension bars: INCOME (left) and FREE TIME (right).
    40.48: 'RUINING MY CAREER' tag slams in.
    41.90: crisp strike-through draws across the tag.
    43.34-45.80: INCOME steps down modestly while FREE TIME grows tall & radiant!"""
    F = 636
    b = f'''<g class="k">
 <path id="{p}floor" d="M24 {F} H856" fill="none"/>
 {shadow(248, F+5, 160, 14)}
 {shadow(632, F+5, 160, 14)}

 <!-- Radiant warm halo behind growing FREE TIME bar -->
 <circle id="{p}halo" cx="632" cy="370" r="196" fill="{Y}" stroke="none" opacity="0"/>

 <!-- LEFT COLUMN: INCOME BAR (starts tall h=390 -> steps down to h=250) -->
 <g id="{p}incG">
  <!-- Dashed ghost outline showing original height when income steps down -->
  <rect id="{p}incGhost" x="128" y="190" width="240" height="390" rx="20" fill="none" stroke="{CSD}" stroke-width="5" stroke-dasharray="12 10" opacity="0"/>
  <!-- Animated bar body (grows/shrinks from bottom y=580!) -->
  <g id="{p}incBar">
   <rect x="138" y="198" width="240" height="386" rx="20" fill="{CSD}" stroke="none"/>
   <rect x="128" y="190" width="240" height="390" rx="20" fill="{W}"/>
   <path d="M336 190 H348 Q368 190 368 210 V560 Q368 580 348 580 H336 Z" fill="{CS}" stroke="none"/>
   <rect x="128" y="190" width="240" height="390" rx="20" fill="none"/>
  </g>
  <!-- Icon riding inside top of INCOME bar (outer g has NO transform!) -->
  <g id="{p}incIcon">
   <g transform="translate(248 258)">
    {dim_icon('INCOME', 0, 0, 1.15)}
   </g>
  </g>
  <!-- Base label plaque: INCOME -->
  <rect x="116" y="572" width="264" height="64" rx="16" fill="{W}"/>
  <rect x="116" y="572" width="22" height="64" rx="9" fill="{CS}" stroke="none"/>
  <rect x="116" y="572" width="264" height="64" rx="16" fill="none"/>
  <text x="256" y="616" text-anchor="middle" class="lbl" style="font-size:30px;font-weight:700;letter-spacing:0.1em">INCOME</text>
 </g>

 <!-- RIGHT COLUMN: FREE TIME BAR (starts low h=156 -> grows tall & yellow h=394!) -->
 <g id="{p}ftG">
  <!-- Animated bar body (origin at bottom y=580!) -->
  <g id="{p}ftBar">
   <rect x="522" y="194" width="240" height="390" rx="20" fill="{CSD}" stroke="none"/>
   <rect x="512" y="186" width="240" height="394" rx="20" fill="{Y}"/>
   <path d="M720 186 H732 Q752 186 752 206 V560 Q752 580 732 580 H720 Z" fill="{YS}" stroke="none"/>
   <rect x="512" y="186" width="240" height="394" rx="20" fill="none"/>
  </g>
  <!-- Radiant open-door / freedom icon riding inside top of FREE TIME bar (outer g has NO transform!) -->
  <g id="{p}ftIcon">
   <g transform="translate(632 262)">
    {dim_icon('FREEDOM', 0, 0, 1.25)}
   </g>
  </g>
  <!-- Upward freedom rays around top of FREE TIME bar -->
  <g id="{p}ftrays" stroke="{R}" stroke-width="6.5" fill="none" opacity="0">
   <path d="M632 152 V124 M560 172 L536 148 M704 172 L728 148"/>
  </g>
  <!-- Base label plaque: FREE TIME -->
  <rect x="500" y="572" width="264" height="64" rx="16" fill="{W}"/>
  <rect x="500" y="572" width="22" height="64" rx="9" fill="{R}" stroke="none"/>
  <rect x="500" y="572" width="264" height="64" rx="16" fill="none"/>
  <text x="640" y="616" text-anchor="middle" class="lbl" style="font-size:30px;font-weight:700;letter-spacing:0.1em">FREE TIME</text>
 </g>

 <!-- Center trade arrows (appear during trade 43.34-45.80) -->
 <g id="{p}arrows" opacity="0">
  <!-- Down arrow beside INCOME -->
  <path d="M412 296 V374 M394 354 L412 376 L430 354" fill="none" stroke="{PANTS}" stroke-width="7"/>
  <!-- Up arrow beside FREE TIME -->
  <path d="M468 376 V298 M450 318 L468 296 L486 318" fill="none" stroke="{R}" stroke-width="7.5"/>
 </g>

 <!-- "RUINING MY CAREER" STAMP TAG (slams in at 40.48, struck through at 41.90!) -->
 <g id="{p}ruin" opacity="0" data-layout-allow-overlap>
  <g transform="translate(440 74) rotate(-2.5)">
   <rect x="-272" y="-42" width="560" height="90" rx="18" fill="{INK}" fill-opacity="0.18" stroke="none"/>
   <rect x="-280" y="-50" width="560" height="90" rx="18" fill="{W}" stroke="{R}" stroke-width="8"/>
   <text x="0" y="9" text-anchor="middle" class="lbl" style="font-size:36px;font-weight:700;fill:{R};letter-spacing:0.09em" data-layout-allow-overlap>RUINING MY CAREER</text>
  </g>
 </g>
 <!-- Heavy strike-through drawing across RUINING MY CAREER at 41.90 ("I wasn't.") -->
 <path id="{p}strike" class="dr" pathLength="1" d="M138 82 L742 62"
       fill="none" stroke="{INK}" stroke-width="12" stroke-linecap="round"/>

 {sparkle(p+'sp1', 796, 178, 19, Y)}
 {sparkle(p+'sp2', 78, 224, 15, R)}
 {sparkle(p+'sp3', 488, 198, 15, Y)}
</g>'''
    return svg(b, 880, 700)


# ============================================================
# BEAT 9: RETURN TO OFFER LETTER + CARDS SPREAD AROUND + TOXICITY RED FORWARD
# ============================================================

def compact_card(id_, key, label, cx, cy, rot=0.0, red_hero=False):
    """Compact pill/card for Beat 9's spread around the returning offer letter (outer g has NO transform!)."""
    if red_hero:
        w, h = 286, 114
        hw, hh = w / 2, h / 2
        return f'''<g id="{id_}" data-layout-allow-overlap>
  <g transform="translate({cx} {cy}) rotate({rot})">
   <rect x="{-hw+7:.1f}" y="{-hh+8:.1f}" width="{w}" height="{h}" rx="18" fill="{RS}" stroke="none"/>
   <rect x="{-hw:.1f}" y="{-hh:.1f}" width="{w}" height="{h}" rx="18" fill="{R}" stroke="{INK}" stroke-width="6"/>
   <rect x="{-hw+10:.1f}" y="{-hh+10:.1f}" width="{w-20}" height="{h-20}" rx="12" fill="none" stroke="{W}" stroke-width="3" stroke-dasharray="8 6" opacity="0.6"/>
   {dim_icon(key, -hw + 52, 0, 0.86, red_mode=True)}
   <text x="24" y="12" text-anchor="middle" class="lbl" style="font-size:35px;font-weight:700;fill:{W};letter-spacing:0.1em" data-layout-allow-overlap>{label}</text>
  </g>
 </g>'''

    w, h = 202, 112
    hw, hh = w / 2, h / 2
    fs = 28 if len(label) > 8 else 29
    tr = '-0.02em' if len(label) > 8 else '0.04em'
    return f'''<g id="{id_}" data-layout-allow-overlap>
  <g transform="translate({cx} {cy}) rotate({rot})">
   <rect x="{-hw+7:.1f}" y="{-hh+8:.1f}" width="{w}" height="{h}" rx="18" fill="{CSD}" stroke="none"/>
   <rect x="{-hw:.1f}" y="{-hh:.1f}" width="{w}" height="{h}" rx="18" fill="{W}" stroke="{INK}" stroke-width="4.5"/>
   {dim_icon(key, 0, -20, 0.62, red_mode=False)}
   <text x="0" y="38" text-anchor="middle" class="lbl" style="font-size:{fs}px;font-weight:700;fill:{INK};letter-spacing:{tr}" data-layout-allow-overlap>{label}</text>
  </g>
 </g>'''


def art_offer_resolved(p):
    """Beat 9: Returns to the SAME cream offer letter (+50% stamp) as Frame 1,
    with faint GROWTH echo at 47.32, all 7 dimension cards fanning out around it,
    and TOXICITY bold red coming clearly forward at 48.82-50.88!"""
    # Left 3 cards (cx=128, w=202 -> x=27..229), Right 3 cards (cx=752, w=202 -> x=651..853) -> 27px outer margin!
    # Center Offer Letter scaled 0.78 -> width=367 (x=256..624) => clean 27px channel on both sides!
    left_cards = [
        compact_card(f'{p}c0', 'INCOME',     'INCOME',     128, 178, -2.5),
        compact_card(f'{p}c1', 'TITLE',      'TITLE',      124, 330, -1.2),
        compact_card(f'{p}c2', 'FREEDOM',    'FREEDOM',    128, 482,  2.2),
    ]
    right_cards = [
        compact_card(f'{p}c3', 'COLLEAGUES', 'COLLEAGUES', 752, 178,  2.5),
        compact_card(f'{p}c4', 'LOCATION',   'LOCATION',   756, 330,  1.2),
        compact_card(f'{p}c5', 'WORK-LIFE',  'WORK-LIFE',  752, 482, -2.2),
    ]
    # Subtle dashed connector rays from offer letter to surrounding cards
    spokes = (
        f'<g id="{p}spokes" stroke="{CSD}" stroke-width="4" stroke-dasharray="7 8" opacity="0">'
        f'<path d="M266 216 L228 186 M258 330 H224 M266 444 L228 474"/>'
        f'<path d="M614 216 L652 186 M622 330 H656 M614 444 L652 474"/>'
        f'</g>'
    )
    b = f'''<g class="k">
 {shadow(440, 628, 290, 16)}

 <!-- Faint "GROWTH" echo banner above offer letter (47.32 "screams") -->
 <g id="{p}gecho" opacity="0" data-layout-allow-overlap>
  <path d="M294 16 H586 L568 54 L586 92 H294 L312 54 Z" fill="{R}" stroke="{INK}" stroke-width="4.5"/>
  <text x="440" y="68" text-anchor="middle" class="num" font-size="40" letter-spacing="0.08em" fill="{W}" data-layout-ignore>GROWTH</text>
 </g>

 {spokes}

 <!-- SAME CREAM OFFER LETTER AS FRAME 1 (outer g has NO transform!) -->
 <g id="{p}letter">
  <g transform="translate(440 326) rotate(-1.5) scale(0.78)">
   {offer_letter_core(p, stamped=True)}
  </g>
 </g>

 <!-- 6 SURROUNDING DIMENSION CARDS -->
 <g id="{p}ring">
  {''.join(left_cards)}
  {''.join(right_cards)}
 </g>

 <!-- RED WARNING HALO + FORWARD HERO "TOXICITY" CARD (turns clearly RED & comes forward!) -->
 <g id="{p}toxwrap" opacity="0" data-layout-allow-overlap>
  <!-- Subtle red emphasis glow behind TOXICITY -->
  <ellipse cx="440" cy="594" rx="196" ry="74" fill="{R}" opacity="0.16" stroke="none"/>
  <!-- Red warning burst rays flanking TOXICITY -->
  <g id="{p}toxrays" stroke="{R}" stroke-width="7" fill="none">
   <path d="M278 564 L244 548 M274 624 L240 640"/>
   <path d="M602 564 L636 548 M606 624 L640 640"/>
  </g>
  {compact_card(f'{p}c6', 'TOXICITY', 'TOXICITY', 440, 594, -1.5, red_hero=True)}
 </g>

 {sparkle(p+'sp1', 246, 84, 16, Y)}
 {sparkle(p+'sp2', 636, 84, 16, R)}
</g>'''
    return svg(b, 880, 700)


# ============================================================
# BEAT 10: CTA END CARD DECORATION (exact approved Reel 003 treatment, 880 x 760)
# ============================================================

def art_cta_bg(p):
    """Warm L2 halo rays, ground shadow, and sparkles behind the tilted book cover."""
    b = f'''<g class="k">
 <circle id="{p}halo" cx="440" cy="300" r="248" fill="{Y}" stroke="none" opacity="0.34"/>
 <g id="{p}rays" stroke="{R}" stroke-width="7" fill="none">
  <path d="M174 170 L132 140 M140 304 H92 M186 440 L146 468"/>
  <path d="M706 170 L748 140 M740 304 H788 M694 440 L734 468"/>
 </g>
 {shadow(440, 566, 210, 16)}
 {sparkle(p+'sp1', 164, 92, 20, Y)}
 {sparkle(p+'sp2', 730, 106, 16, R)}
 {sparkle(p+'sp3', 746, 514, 18, Y)}
 {sparkle(p+'sp4', 142, 508, 13, R)}
</g>'''
    return svg(b, 880, 760)
