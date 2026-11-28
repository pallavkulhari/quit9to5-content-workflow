# Ported from the box (blog/post13-work/build_html.py). Builds the paste-ready beehiiv HTML from postNN.md.
# Usage: python3 build_html.py postNN.md postNN_publish.html   (needs the 'markdown' package)
import re,markdown,html,sys
if len(sys.argv)<3: sys.exit('usage: build_html.py postNN.md postNN_publish.html')
src=open(sys.argv[1],encoding='utf-8').read()
fm,body=src.split('---\n',2)[1:]
meta=dict(re.findall(r'^(\w+): "?(.*?)"?$',fm,re.M))
body=re.sub(r'^—{5,}$','<hr>',body,flags=re.M)
h=markdown.markdown(body,output_format='html')
h=h.replace('<p><hr></p>','<hr>').replace('<hr />','<hr>')
h=h.replace('&amp;','&').replace('&','&amp;')  # normalise
h=re.sub(r'&amp;(#?\w+;)',r'&\1',h)
out=f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{meta['seo_title']}</title>
<meta name="description" content="{html.escape(meta['meta_description'])}">
<style>body{{max-width:720px;margin:2em auto;font-family:Georgia,serif;line-height:1.6;padding:0 1em}}blockquote{{border-left:4px solid #222;margin:1.2em 0;padding:0.2em 1em;font-style:italic}}</style>
</head>
<body>
<!-- Paste the body into beehiiv. Title, subtitle, slug, SEO title, meta description and thumbnail go in post settings. Quote blocks: left-bar style (same as "Why Do People Stay in Jobs They Hate?"). Dividers: beehiiv divider block. -->
{h}
</body>
</html>
'''
open(sys.argv[2],'w',encoding='utf-8').write(out)
