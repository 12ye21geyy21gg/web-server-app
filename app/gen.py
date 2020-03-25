import random
from PIL import Image,ImageDraw,ImageFont
class Gen():
    def __init__(self):
        self.r = random.Random()
    def gen_random_pixel_noise(self,size,num,inp):
        if not num:
            num = 5
        if not size:
            size = 200
        if inp:
            self.r.seed(inp)
        img = Image.new('RGB',(size,size),color='white')
        dr = ImageDraw.Draw(img)
        for h in range(num):
            for w in range(num):
                color = (self.r.randint(0,255),self.r.randint(0,255),self.r.randint(0,255))
                dr.rectangle([w*size//num,h*size//num,(w+1)*size//num,(h+1)*size//num],fill=color,width=0)
        del dr
        img.save('../data/src/temp.png')
    def gen_random_triangle_noise(self,size,num,inp):
        if not num:
            num = 5
        if not size:
            size = 200
        if inp:
            self.r.seed(inp)
        img = Image.new('RGB',(size,size),color='white')
        dr = ImageDraw.Draw(img)
        for i in range(num):
            color = (self.r.randint(0, 255), self.r.randint(0, 255), self.r.randint(0, 255))
            dr.polygon([self.r.randint(0,size),self.r.randint(0,size),self.r.randint(0,size),self.r.randint(0,size),self.r.randint(0,size),self.r.randint(0,size)],fill=color)
        del dr
        img.save('../data/src/temp.png')
    def gen_mirrored(self,size,num,inp,prim=None,othr=None):
        if not num:
            num = 5
        if not size:
            size = 200
        if inp:
            self.r.seed(inp)
        img = Image.new('RGB', (size, size), color='white')
        dr = ImageDraw.Draw(img)
        if prim is None:
            prim = (self.r.randint(0, 255), self.r.randint(0, 255), self.r.randint(0, 255))
        if othr is None:
            othr = (255-prim[0],255-prim[1],255-prim[2])
        if num % 2 == 0:
            for h in range(num):
                for w in range(num//2):
                    if self.r.random() > 0.5:
                        dr.rectangle([w*size//num,h*size//num,(w+1)*size//num,(h+1)*size//num],fill=prim,width=0)
                        dr.rectangle([(num-w)*size//num,h*size//num,(num-(w+1))*size//num,(h+1)*size//num],fill=prim,width=0)
                    else:
                        dr.rectangle([w * size // num, h * size // num, (w + 1) * size // num, (h + 1) * size // num],
                                     fill=othr, width=0)
                        dr.rectangle([(num - w) * size // num, h * size // num, (num - (w + 1)) * size // num,
                                      (h + 1) * size // num], fill=othr, width=0)
        else:
            for h in range(num):
                for w in range(num//2):
                    if self.r.random() > 0.5:
                        dr.rectangle([w*size//num,h*size//num,(w+1)*size//num,(h+1)*size//num],fill=prim,width=0)
                        dr.rectangle([(num-w)*size//num,h*size//num,(num-(w+1))*size//num,(h+1)*size//num],fill=prim,width=0)
                    else:
                        dr.rectangle([w * size // num, h * size // num, (w + 1) * size // num, (h + 1) * size // num],
                                     fill=othr, width=0)
                        dr.rectangle([(num - w) * size // num, h * size // num, (num - (w + 1)) * size // num,
                                      (h + 1) * size // num], fill=othr, width=0)
            for h in range(num):
                w = num//2
                if self.r.random() > 0.5:
                    dr.rectangle([w*size//num,h*size//num,(w+1)*size//num,(h+1)*size//num],fill=prim,width=0)
                else:
                    dr.rectangle([w * size // num, h * size // num, (w + 1) * size // num, (h + 1) * size // num],
                                 fill=othr, width=0)
        del dr
        img.save('../data/src/temp.png')
    def gen_mirrored_github(self,size,num,inp,prim=None):
        if not num:
            num = 5
        if not size:
            size = 200
        if inp:
            self.r.seed(inp)
        if prim is None:
            prim = (self.r.randint(0, 255), self.r.randint(0, 255), self.r.randint(0, 255))
        self.gen_mirrored(size,num,inp,prim,othr=(255,255,255))
    def gen_captcha(self,size,text):
        if not size:
            size = 200
        if not text:
            text = 'sample'
        prim = (self.r.randint(127,255),self.r.randint(127,255),self.r.randint(127,255))
        fnt = ImageFont.truetype(font='../templates/DejaVuSans.ttf', size=100)
        print(fnt.size)
        img = Image.new('RGB', (size, size), color='white')
        dr = ImageDraw.Draw(img)
        dr.text((0,size//2-size/len(text)),text,fnt=fnt,fill=prim)
        del dr
        img.save('../data/src/temp.png')


#a = gen()
#a.gen_captcha(400,'1212')