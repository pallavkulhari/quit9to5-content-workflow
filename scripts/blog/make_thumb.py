# Ported from the box (blog/thumbs/make.py, the post 1 thumbnail). Approved blog thumbnail series: 1200x630 JPG,
# notebook-grid background (from t4_seven.jpg, not in repo), flat charcoal icon with one red accent on the left,
# two-line Josefin Sans title on the right (line 1 ink, line 2 red, grey stroke).
# Copy this per post: change the icon block and the two title lines.
# Env: BLOG_THUMB_BG (path to t4_seven.jpg), Q9_FONT_JOSEFIN, Q9_FONT_DEJAVU_BOLD. Usage: python3 make_thumb.py OUT.jpg
import os,sys
from PIL import Image,ImageDraw,ImageFont
import numpy as np
a=np.array(Image.open(os.environ.get('BLOG_THUMB_BG','t4_seven.jpg')).convert('RGB'))
for x in range(1024,-1,-1): a[:,x]=a[:,x+155]
img=Image.fromarray(a).resize((2400,1260),Image.LANCZOS)
S=2;d=ImageDraw.Draw(img)
DG=(64,64,64);RED=(204,68,60);GR=(188,188,188)
# coin stack, centre x=310
cx=330*S;w=220*S;h=60*S;th=34*S;base=480*S
for i in range(6):
    y=base-i*th; col=DG
    d.rectangle([cx-w//2,y-h//2,cx+w//2,y],fill=col)
    d.ellipse([cx-w//2,y-h//2-h//2+h//2,cx+w//2,y+h//2],fill=col)
    d.ellipse([cx-w//2,y-h,cx+w//2,y],fill=(90,90,90),outline=(250,250,250),width=3*S)
# red top coin
y=base-6*th
d.ellipse([cx-w//2,y-h//2,cx+w//2,y+h//2+th//2],fill=(160,50,45))
d.ellipse([cx-w//2,y-h,cx+w//2,y],fill=RED,outline=(250,250,250),width=3*S)
f=ImageFont.truetype(os.environ.get('Q9_FONT_DEJAVU_BOLD','/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'),40*S)
d.text((cx,y-h//2),'₹',font=f,fill=(255,255,255),anchor='mm')
fp=os.environ.get('Q9_FONT_JOSEFIN','/usr/share/fonts/truetype/sand-box/google/Josefin Sans/JosefinSans-VariableFont_wght.ttf')
F=ImageFont.truetype(fp,104*S)
try: F.set_variation_by_name('Regular')
except Exception as e: print(e)
for txt,col,yy in [('How Much',(10,10,10),200),('Is Enough?',RED,310)]:
    d.text((560*S,yy*S),txt,font=F,fill=col,stroke_width=4*S,stroke_fill=GR)
img.resize((1200,630),Image.LANCZOS).save(sys.argv[1] if len(sys.argv)>1 else 'post01_thumb.jpg',quality=92)
