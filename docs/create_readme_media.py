"""Generate the Roomcast README illustrations and short animated demo with Pillow."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).parent / "images"
OUT.mkdir(parents=True, exist_ok=True)
W, H = 1280, 720
C = {"bg": "#101116", "panel": "#191a22", "line": "#30313b", "text": "#f3f2f8", "muted": "#9999a6", "purple": "#aa91ff", "mint": "#9de5c6"}
FONT_DIR = Path("C:/Windows/Fonts")
def f(size, bold=False): return ImageFont.truetype(str(FONT_DIR / ("segoeuib.ttf" if bold else "segoeui.ttf")), size)
F = {"tiny": f(11), "small": f(13), "body": f(16), "head": f(22, True), "title": f(32, True)}

def rr(d, box, rad=10, fill=None, outline=None, width=1):
    d.rounded_rectangle(box, rad, fill=fill, outline=outline, width=width)

def base():
    im = Image.new("RGB", (W, H), C["bg"])
    d = ImageDraw.Draw(im)
    d.ellipse((-240, 150, 460, 840), fill="#15131e")
    d.ellipse((800, 450, 1450, 1100), fill="#111a18")
    d.line((0, 72, W, 72), fill="#25262f", width=1)
    rr(d, (53, 19, 86, 52), 10, C["purple"])
    d.rectangle((61, 28, 75, 43), outline="#211936", width=2)
    d.polygon([(76, 32), (82, 29), (82, 42), (76, 39)], fill="#211936")
    d.text((98, 20), "roomcast", font=f(23, True), fill=C["text"])
    d.text((1008, 27), "●  Private rooms · No account needed", font=F["tiny"], fill=C["muted"])
    return im

def maximize_icon(d, x, y, size=28, active=False):
    rr(d, (x, y, x+size, y+size), 6, "#111219e8", "#ffffff60")
    col = "#ffffff" if active else "#ded7f3"
    # Four corner brackets, the familiar expand/fullscreen symbol.
    d.line((x+8,y+12,x+8,y+8,x+12,y+8), fill=col, width=2)
    d.line((x+16,y+8,x+20,y+8,x+20,y+12), fill=col, width=2)
    d.line((x+8,y+16,x+8,y+20,x+12,y+20), fill=col, width=2)
    d.line((x+16,y+20,x+20,y+20,x+20,y+16), fill=col, width=2)

def screen_content(d, box, kind, color):
    x,y,w,h = box
    rr(d, (x,y,x+w,y+h), 8, "#0d0e13", "#3b3b47")
    d.rectangle((x+1,y+1,x+w-1,y+21), fill="#20212a")
    for k,col in enumerate(("#ed7f83", "#e9c677", "#8cd6a9")):
        d.ellipse((x+9+k*13,y+8,x+15+k*13,y+14), fill=col)
    if kind == 0:
        for k in range(6):
            yy=y+39+k*25
            d.line((x+18,yy,x+w-20-(k%2)*47,yy), fill=color if k%3==0 else "#57536c", width=3)
        rr(d,(x+18,y+h-46,x+93,y+h-28),5,"#3b3153")
    elif kind == 1:
        rr(d,(x+22,y+38,x+w-22,y+h-28),7,"#202b2a")
        cx=x+w//2
        d.ellipse((cx-26,y+58,cx+26,y+110),fill=color)
        d.arc((cx-48,y+94,cx+48,y+155),180,360,fill=color,width=11)
        d.line((x+35,y+h-49,x+w-35,y+h-49),fill="#52665f",width=3)
    else:
        rr(d,(x+22,y+38,x+w-22,y+h-28),5,"#30344b")
        d.polygon([(x+23,y+h-29),(x+92,y+72),(x+145,y+111),(x+w-23,y+65),(x+w-23,y+h-29)],fill="#555276")
        d.ellipse((x+w-77,y+46,x+w-51,y+72),fill="#e3c98c")

def make_room(fullscreen=False, focus=0):
    im=base(); d=ImageDraw.Draw(im)
    rr(d,(45,92,83,130),10,"#1a1b22","#383943")
    d.text((57,96),"‹",font=F["head"],fill="#c2bfcc")
    d.text((99,94),"LIVE ROOM",font=F["tiny"],fill="#bcaaff")
    d.text((99,109),"Room with Alex",font=F["body"],fill=C["text"])
    d.text((790,102),"ROOM CODE",font=F["tiny"],fill=C["muted"])
    rr(d,(875,91,991,129),8,"#1c1c24","#403d49"); d.text((890,101),"MINT24  ▢",font=F["small"],fill="#d5caff")
    rr(d,(1010,91,1200,130),8,C["purple"]); d.text((1040,103),"▣  Share screen",font=F["small"],fill="#211936")
    sx,sy,sw,sh=45,150,858,510
    rr(d,(sx,sy,sx+sw,sy+sh),14,"#16171d","#30313b")
    if fullscreen:
        # One screen fills the stage; retain a small restore control and label.
        screen_content(d,(sx+20,sy+30,sw-40,sh-75),focus,"#aa91ff")
        maximize_icon(d,sx+sw-58,sy+46,34,True)
        rr(d,(sx+36,sy+sh-78,sx+177,sy+sh-48),7,"#111219e8")
        d.ellipse((sx+48,sy+sh-67,sx+56,sy+sh-59),fill=C["mint"])
        d.text((sx+66,sy+sh-73),["Alex’s screen","Jamie’s screen","Morgan’s screen"][focus],font=F["small"],fill=C["text"])
        d.text((sx+sw-225,sy+sh-26),"Fullscreen · press Esc to return",font=F["tiny"],fill=C["muted"])
    else:
        rr(d,(sx+sw-153,sy+12,sx+sw-12,sy+48),9,"#191a22","#393844")
        d.text((sx+sw-141,sy+22),"‹     1 / 2     ›",font=F["small"],fill="#d8d0f0")
        names=["Alex’s screen","Jamie’s screen","Morgan’s screen"]
        variants=[0,1,2]
        tw=264; gap=11; ty=sy+80
        for i,(name,kind) in enumerate(zip(names,variants)):
            tx=sx+15+i*(tw+gap)
            rr(d,(tx,ty,tx+tw,ty+333),10,"#0b0c10","#3b3b47")
            screen_content(d,(tx+8,ty+8,tw-16,299),kind,["#aa91ff","#9de5c6","#f0c291"][i])
            rr(d,(tx+14,ty+294,tx+149,ty+321),6,"#111219")
            d.ellipse((tx+23,ty+303,tx+30,ty+310),fill=C["mint"])
            d.text((tx+37,ty+300),name,font=F["tiny"],fill=C["text"])
            maximize_icon(d,tx+tw-45,ty+17,29,active=(i==focus))
        d.line((sx,sy+sh-43,sx+sw,sy+sh-43),fill="#292a34")
        d.ellipse((sx+16,sy+sh-26,sx+23,sy+sh-19),fill=C["mint"])
        d.text((sx+34,sy+sh-29),"3 SCREENS LIVE",font=F["tiny"],fill="#d7d3df")
        d.text((sx+sw-208,sy+sh-29),"Click a tile’s expand button",font=F["tiny"],fill=C["muted"])
    # People and room chat sidebar.
    px,py,pw=920,150,315; rr(d,(px,py,px+pw,py+sh),13,C["panel"],C["line"])
    d.text((px+17,py+17),"In this room",font=F["small"],fill=C["text"])
    d.text((px+17,py+39),"4 of 6 people",font=F["tiny"],fill=C["muted"])
    people=[("Alex","Room host"),("Jamie","Guest"),("Morgan","Guest"),("You","You")]
    for i,(name,role) in enumerate(people):
        yy=py+72+i*42; rr(d,(px+15,yy,px+44,yy+29),9,"#28263a" if i%2==0 else "#254039")
        d.text((px+25,yy+7),name[0],font=F["small"],fill=C["purple"] if i%2==0 else C["mint"])
        d.text((px+55,yy+2),name,font=F["tiny"],fill="#dedde5"); d.text((px+55,yy+16),role,font=F["tiny"],fill="#888894")
    cy=py+250; rr(d,(px+12,cy,px+pw-12,py+sh-13),9,"#15161c",C["line"])
    d.text((px+25,cy+12),"Room chat",font=F["small"],fill=C["text"])
    d.text((px+25,cy+32),"Messages are shared with everyone",font=F["tiny"],fill=C["muted"])
    d.line((px+13,cy+55,px+pw-13,cy+55),fill="#292a33")
    rr(d,(px+22,cy+67,px+194,cy+111),8,"#212129",C["line"])
    d.text((px+31,cy+74),"Jamie · 10:42",font=f(9),fill="#a8a6b2"); d.text((px+31,cy+91),"Can you see my screen?",font=f(10),fill="#e1dfe8")
    rr(d,(px+101,cy+120,px+280,cy+164),8,"#30283f","#4a3c68")
    d.text((px+110,cy+127),"You · 10:42",font=f(9),fill="#b8adc9"); d.text((px+110,cy+144),"Yep, looks great!",font=f(10),fill="#eeeaf5")
    return im

def make_home():
    im=base(); d=ImageDraw.Draw(im)
    d.text((74,151),"YOUR SPACE, YOUR SCREEN",font=F["small"],fill="#bcaaff")
    d.text((74,202),"Good things",font=f(58,True),fill=C["text"])
    d.text((74,270),"are better",font=f(58,True),fill=C["text"])
    d.text((74,338),"shared.",font=f(58,True),fill=C["purple"])
    d.multiline_text((78,428),"Start a room, invite your people with one simple\ncode, and put your screen in the middle of the\nconversation.",font=F["body"],fill="#aaaab5",spacing=8)
    x,y,w,h=720,115,474,545; rr(d,(x,y,x+w,y+h),18,"#1b1c24","#363641")
    d.line((x,y+62,x+w,y+62),fill=C["line"])
    d.text((x+76,y+21),"Create a room",font=F["small"],fill=C["text"]); d.text((x+304,y+21),"Join a room",font=F["small"],fill="#888894")
    d.line((x+35,y+61,x+218,y+61),fill=C["purple"],width=3)
    d.text((x+34,y+96),"Your room starts here",font=F["small"],fill=C["text"])
    d.text((x+34,y+132),"Your name",font=F["tiny"],fill="#d0cfda")
    rr(d,(x+32,y+153,x+w-32,y+198),8,"#15161c","#383943"); d.text((x+47,y+166),"Alex",font=F["tiny"],fill=C["text"])
    d.text((x+34,y+219),"How many people, including you?",font=F["tiny"],fill="#d0cfda")
    rr(d,(x+32,y+241,x+w-32,y+286),8,"#15161c","#383943"); d.text((x+47,y+255),"4 people",font=F["tiny"],fill=C["text"])
    rr(d,(x+32,y+315,x+w-32,y+364),8,C["purple"]); d.text((x+167,y+330),"Create your room  →",font=F["small"],fill="#211936")
    return im

def make_gif():
    shots=[make_home(),make_room(),make_room(True,0),make_room()]
    # The third panel demonstrates one shared screen maximized; final panel returns to tiles.
    frames=[]; durations=[]
    for i,shot in enumerate(shots):
        frames.extend([shot.copy()]*3); durations.extend([400,400,400])
        if i<len(shots)-1:
            for a in (.25,.5,.75):
                frames.append(Image.blend(shot,shots[i+1],a)); durations.append(90)
    frames=[im.resize((960,540),Image.Resampling.LANCZOS).convert("P",palette=Image.Palette.ADAPTIVE,colors=128) for im in frames]
    frames[0].save(OUT/"roomcast-walkthrough.gif",save_all=True,append_images=frames[1:],duration=durations,loop=0,optimize=True,disposal=2)

if __name__=="__main__":
    make_home().save(OUT/"create-room.png",optimize=True)
    make_room().save(OUT/"room-sharing-maximize.png",optimize=True)
    make_room(True,0).save(OUT/"maximized-screen.png",optimize=True)
    make_gif()
