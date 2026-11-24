# L2 reference build (reel 005, "Growth in which dimension?")

Code from the approved reel 005 build by agy (Gemini 4 Neon), 21–22 Nov 2026. New builds copy these into `project/tools_ref/` so the channel keeps one look (typography, end card, motion habits).

- `tools/art.py`: SVG drawing helpers in the L2 style (cream `#F3EDE1`, ink `#141312` 5 px outlines, red `#D54E4C`, butter `#F2D98B`): the offer letter, career ladder, dimension cards, salary squash, trade bars, CTA background and so on.
- `tools/build.py`: assembles `index.html`: the `@font-face` block, one `<section class="clip scene">` per beat, the paused GSAP timeline with word-timed motions, the inlined `captions.json`, `addCaptions4(tl, CHUNKS, {theme:"ink", lastEnd:58})`, and the `window.__timelines["main"]` registration. Run `python3 tools/build.py` from inside a project folder; it reads `assets/captions.json` and writes `index.html` next to `tools/`.
- `assets/captions4.js`: the caption component (dark pill at y 1250–1390, x 72–948; Inter Tight 700 50 px; upcoming words at 35%, the current word in coral). Do not edit it inside a reel build.
- `hyperframes.json`: the project config used by the build.

Not included: `gsap.min.js` (install the `gsap` npm package and copy `dist/gsap.min.js`), fonts, `book_cover.jpeg`, `vo.wav`, `captions.json`, the rendered `index.html` and all media. The beat timings in `build.py` are specific to reel 005's voiceover; a new reel needs its own timings from its `captions.json`.
