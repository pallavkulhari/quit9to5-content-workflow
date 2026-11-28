# Ported from the box (cards/make_insta.py). 9:16 story version of the v1a card: make_insta(text, out).
# Env: Q9_FONT_INTER, Q9_CARD_ASSETS (same as var.py). CLI: python3 make_insta.py "card text" out.png
import os,math
from PIL import Image,ImageDraw,ImageFont,ImageFilter
H=os.environ.get("Q9_CARD_ASSETS",os.path.dirname(os.path.abspath(__file__)))  # needs pallav_photo.jpg + book_cover.jpeg (not in repo)
FONT=os.environ.get("Q9_FONT_INTER","/usr/share/fonts/truetype/sand-box/google/Inter/Inter-VariableFont_opsz,wght.ttf")
S=3;W=1080;RED=(213,78,76);INK=(45,45,44);GR=(113,125,139)
def font(sz,w):
    f=ImageFont.truetype(FONT,sz*S)
    try:f.set_variation_by_axes([min(32,max(14,sz)),w])
    except:pass
    return f
def avatar(d):
    im=Image.open(os.path.join(H,"pallav_photo.jpg")).convert("RGB");w,h=im.size
    cx,cy,r=int(w*.49),int(h*.52),int(w*.47)
    im=im.crop((cx-r,cy-r,cx+r,cy+r)).resize((d,d),Image.LANCZOS)
    m=Image.new("L",(d,d),0);ImageDraw.Draw(m).ellipse((0,0,d-1,d-1),fill=255);return im,m
def badge(d,x,y,s):
    pts=[(x+s/2+s/2*(1 if i%4<2 else .86)*math.cos(2*math.pi*i/48),y+s/2+s/2*(1 if i%4<2 else .86)*math.sin(2*math.pi*i/48)) for i in range(48)]
    d.polygon(pts,fill=(29,155,240));d.line([(x+s*.3,y+s*.52),(x+s*.45,y+s*.66),(x+s*.71,y+s*.36)],fill="white",width=int(s*.11),joint="curve")
def wrap(d,t,f,mw):
    out=[];cur=""
    for wd in t.split():
        x=(cur+" "+wd).strip()
        if d.textlength(x,font=f)<=mw:cur=x
        else:out.append(cur);cur=wd
    return out+[cur]
def cover(h):
    cv=Image.open(os.path.join(H,"book_cover.jpeg")).convert("RGB");return cv.resize((int(h*cv.size[0]/cv.size[1]),h),Image.LANCZOS)
def shadow(img,box,blur=14,a=90,off=(8,12)):
    sh=Image.new("L",img.size,0);x0,y0,x1,y1=box
    ImageDraw.Draw(sh).rectangle((x0+off[0]*S,y0+off[1]*S,x1+off[0]*S,y1+off[1]*S),fill=a)
    img.paste((40,40,40),(0,0),sh.filter(ImageFilter.GaussianBlur(blur*S)))
import sys
from var import parse,rlines,rheight,rdraw
HH=1920
def make_insta(text,out,fs=68,lh=96):
    img=Image.new("RGB",(W*S,HH*S),"white");d=ImageDraw.Draw(img);L=88*S
    d.rectangle((0,0,W*S,18*S),fill=RED)
    AV=180*S;gap=80*S;mw=(W-176)*S
    cv=cover(330*S);cw,ch=cv.size;fy=HH*S-ch-300*S  # clear of IG bottom UI
    while True:   # shrink until the block leaves breathing room above the cover
        fb=font(fs,400);pg=int(lh*0.6)*S
        block=AV+gap+rheight(d,text,fb,mw,lh*S,pg)
        if block<=fy-18*S-260*S or fs<=50:break
        fs-=2;lh=int(fs*1.41)
    top=int(18*S+(fy-18*S-block)*0.5)
    y0=top
    d.ellipse((L-4*S,y0-4*S,L+AV+4*S,y0+AV+4*S),fill=RED);a,m=avatar(AV);img.paste(a,(L,y0),m)
    fn=font(44,700);tx=L+AV+36*S;nm="Pallav Kulhari"
    d.text((tx,y0+AV*.42),nm,font=fn,fill=INK,anchor="ls");badge(d,tx+d.textlength(nm,font=fn)+12*S,y0+AV*.42-43*S,46*S)
    d.text((tx,y0+AV*.8),"@Quit9to5Book",font=font(40,400),fill=GR,anchor="ls")
    y=y0+AV+gap
    rdraw(d,text,fb,mw,L,y,lh*S,pg,int(fs*1.05)*S,fs*S)
    x=L;shadow(img,(x,fy,x+cw,fy+ch),blur=18);d=ImageDraw.Draw(img);img.paste(cv,(x,fy))
    d.rectangle((x,fy,x+cw-1,fy+ch-1),outline=(225,225,225),width=S)
    tx=x+cw+44*S;mid=fy+ch//2
    # 19 Oct 2026 rule (Pallav): no bold "Quit 9to5" beside the cover
    d.line((tx,mid-30*S,tx+80*S,mid-30*S),fill=RED,width=5*S)
    d.text((tx,mid+34*S),"Coming January 2027",font=font(44,600),fill=RED,anchor="ls")
    img.resize((W,HH),Image.LANCZOS).save(out,optimize=True)
if __name__=="__main__":
    make_insta(sys.argv[1],sys.argv[2])
