# Ported from the box (memes/batch3/make.py, helper part only; the batch's meme list is not included).
# meme(template, top=..., bottom=..., boxes=[((x0,y0,x1,y1 as 0-1 fractions of the template), text, max_size, 'w'|'b')])
# -> 1080x1350 PIL image with a small grey "quit9to5.in" corner mark.
# (The box file also starts a two-panel helper, two(), that was never finished; it is left out.)
# Env: MEME_TEMPLATES (folder of template images, default ./src/), Q9_FONT_INTER.
# Usage: from meme_lib import meme; meme('drake.jpg', boxes=[...]).save('meme01.png')
import os
from PIL import Image, ImageDraw, ImageFont
S=os.path.join(os.environ.get('MEME_TEMPLATES','src'),'');W,H=1080,1350
INTER=os.environ.get('Q9_FONT_INTER','/usr/share/fonts/truetype/sand-box/google/Inter/Inter-VariableFont_opsz,wght.ttf')
def F(sz,w='Black'):
    f=ImageFont.truetype(INTER,sz); f.set_variation_by_name(w); return f
def wrap(d,t,f,mw):
    out=[]
    for p in t.split('\n'):
        l=''
        for w in p.split(' '):   # split on plain spaces only, so \u00a0 keeps phrases together
            tt=(l+' '+w).strip()
            if d.textlength(tt,font=f)<=mw: l=tt
            else:
                if l: out.append(l)
                l=w
        out.append(l)
    return out
def text(d,t,box,mx,fill='black',stroke=0,mn=18):
    x0,y0,x1,y1=box
    for sz in range(mx,mn-1,-2):
        f=F(sz);ls=wrap(d,t,f,x1-x0-2*stroke);lh=int(sz*1.18)
        if lh*len(ls)<=y1-y0 and all(d.textlength(l,font=f)<=x1-x0-2*stroke for l in ls): break
    else: raise Exception('nofit '+t)
    y=y0+((y1-y0)-lh*len(ls))//2
    for l in ls:
        tw=d.textlength(l,font=f); d.text((x0+(x1-x0-tw)/2,y),l,font=f,fill=fill,stroke_width=stroke,stroke_fill='black'); y+=lh
def meme(tpl,top=None,bottom=None,boxes=(),topmx=64,crop=None,bg='white',th=None):
    im=Image.new('RGB',(W,H),bg);d=ImageDraw.Draw(im)
    t=Image.open(S+tpl).convert('RGB')
    if crop: t=t.crop(crop)
    th=th or (230 if top else 0); bh=200 if bottom else 0
    avail=H-th-bh-60
    sc=min(W/t.width,avail/t.height); t=t.resize((int(t.width*sc),int(t.height*sc)),Image.LANCZOS)
    ox=(W-t.width)//2; oy=th+(avail-t.height)//2+20
    im.paste(t,(ox,oy))
    if top: text(d,top,(40,20,W-40,th),topmx)
    if bottom: text(d,bottom,(40,oy+t.height+15,W-40,oy+t.height+15+bh-20),topmx)
    for (bx0,by0,bx1,by1),s,mx,kind in boxes:
        b=(ox+bx0*t.width,oy+by0*t.height,ox+bx1*t.width,oy+by1*t.height)
        if kind=='w': text(d,s,b,mx,fill='white',stroke=max(3,mx//12))
        else: text(d,s,b,mx)
    f=F(26,'Bold');m='quit9to5.in';tw=d.textlength(m,font=f)
    d.text((W-tw-24,H-44),m,font=f,fill=(140,140,140) if bg=='white' else (200,200,200))
    return im
