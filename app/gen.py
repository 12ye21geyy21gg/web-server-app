import random
from PIL import Image,ImageDraw,ImageFont
import numpy,time,hashlib,math
class Gen():
    def __init__(self):
        self.r = random.Random()
        self.names = list()

    def get_name(self):
        return '/static/' + hashlib.sha256(str(time.time()).encode('utf8')).hexdigest() + '.png'
    def get_fnames(self):
        return list(map(lambda x: x[8:],self.names))

    def gen_random_pixel_noise(self,size,num,inp):
        try:
            if not num or num == 0:
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
            name = self.get_name()
            img.save('..'+name)
            self.names.append(name)
        except Exception as e:
            return
    def gen_random_triangle_noise(self,size,num,inp):
        try:
            if not num or num == 0:
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
            name = self.get_name()
            img.save('..'+name)
            self.names.append(name)
        except Exception as e:
            return
    def gen_mirrored(self,size,num,inp,prim=None,othr=None):
        try:
            if not num or num == 0:
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
            name = self.get_name()
            img.save('..'+name)
            self.names.append(name)
        except Exception as e:
            return
    def gen_mirrored_github(self,size,num,inp,prim=None):
        try:
            if not num or num == 0:
                num = 5
            if not size:
                size = 200
            if inp:
                self.r.seed(inp)
            if prim is None:
                prim = (self.r.randint(0, 255), self.r.randint(0, 255), self.r.randint(0, 255))
            self.gen_mirrored(size,num,inp,prim,othr=(255,255,255))
        except Exception as e:
            return
    def gen_captcha(self,size,text):
        try:
            if not size:
                size = 200
            if not text:
                text = 'sample'
            prim = (self.r.randint(127,255),self.r.randint(127,255),self.r.randint(127,255))
            fs = 100
            fnt = ImageFont.truetype('../templates/DejaVuSerif.ttf', fs)
            while fnt.getsize(text)[0] > size-40:
                fs -= 1
                fnt = ImageFont.truetype('../templates/DejaVuSerif.ttf', fs)
            img1 = Image.new('RGB', (size, size), color='white')
            dr = ImageDraw.Draw(img1)
            for i in range(100):
                dr.ellipse([self.r.randint(0,size-1),self.r.randint(0,size-1),self.r.randint(0,size-1),self.r.randint(0,size-1)],fill=(self.r.randint(0, 255), self.r.randint(0, 255), self.r.randint(0, 255)))
            del dr
            img = Image.new('RGB', (size, size), color='white')
            dr = ImageDraw.Draw(img)
            dr.text((20,size//2-size/len(text)),text,font=fnt,fill=prim)
            del dr
            m = numpy.asarray(img)
            m2 = numpy.zeros((img.size[0], img.size[1], 3))

            A = m.shape[0] / 3.0
            w = 2.0 / m.shape[1]
            phase = self.r.randint(0,10)/10 * numpy.pi
            shift = lambda x: A * numpy.sin(2.0 * numpy.pi * x * w )
            for i in range(m.shape[0]):
                m2[:, i] = numpy.roll(m[:, i], int(shift(i)))
            #img = Image.fromarray(numpy.uint8(m2))
            pixs = img1.load()
            for i in range(img.size[0]):
                for j in range(img.size[1]):
                    pixs[i,j] = ((pixs[i,j][0] + int(m2[i][j][0]))%256,(pixs[i,j][1] + int(m2[i][j][1]))%256,(pixs[i,j][2] + int(m2[i][j][2]))%256,)
                    pass
            img1 =  img1.rotate(-90)
            img1 = img1.transpose(Image.FLIP_LEFT_RIGHT)
            name = self.get_name()
            img1.save('..'+name)
            self.names.append(name)
        except Exception:
            return
    def get_color(self,data):
        red = 0
        blue = 0
        green = 0
        for i in range(len(data)):
            for j in range(len(data[i])):
                red += data[i][j][0]
                blue += data[i][j][1]
                green += data[i][j][2]
        n = len(data) * len(data[0])
        return (red//n,blue//n,green//n)
    def get_color_mono(self,data,porog):
        red = 0
        blue = 0
        green = 0
        for i in range(len(data)):
            for j in range(len(data[i])):
                red += data[i][j][0]
                blue += data[i][j][1]
                green += data[i][j][2]
        n = len(data) * len(data[0])
        if (red + blue + green)/n > porog:
            return (255,255,255)
        else:
            return (0,0,0)
    def gen_pixilise(self,size,num,inp):
        try:
            if not num or num == 0:
                num = 5
            if 0>= num or num > size:
                num = size
            if not inp:
                return
            othr = Image.open(inp).resize((size,size))
            pixs = othr.load()
            img = Image.new('RGB', (size, size), color='white')
            dr = ImageDraw.Draw(img)
            for h in range(num):
                for w in range(num):
                    data = list()
                    k = size//num
                    if k == 0:
                        k = 1
                    for hh in range(h*k,(h+1)*k):
                        data.append(list())
                        for ww in range(w*k,(w+1)*k):
                            data[hh%(k)].append(pixs[hh,ww])
                    color = self.get_color(data)
                    dr.rectangle([w * k, h * k, (w + 1) * k, (h + 1) * k],fill=color, width=0)


            del dr
            img = img.rotate(-90)
            img = img.transpose(Image.FLIP_LEFT_RIGHT)
            name = self.get_name()
            img.save('..'+name)
            self.names.append(name)
        except Exception:
            return
    def gen_monopixilise(self,size,num,inp,porog=127):
        try:
            if not num or num == 0:
                num = 5
            if 0>= num or num > size:
                num = size
            if not(0 <= porog <= 255):
                porog = 255 * 3 / 2
            if not inp:
                return
            porog *= 3
            othr = Image.open(inp).resize((size,size))
            pixs = othr.load()
            img = Image.new('RGB', (size, size), color='white')
            dr = ImageDraw.Draw(img)
            for h in range(num):
                for w in range(num):
                    data = list()
                    k = size//num
                    if k == 0:
                        k = 1
                    for hh in range(h*k,(h+1)*k):
                        data.append(list())
                        for ww in range(w*k,(w+1)*k):
                            data[hh%(k)].append(pixs[hh,ww])
                    color = self.get_color_mono(data,porog)
                    dr.rectangle([w * k, h * k, (w + 1) * k, (h + 1) * k],fill=color, width=0)


            del dr
            img = img.rotate(-90)
            img = img.transpose(Image.FLIP_LEFT_RIGHT)
            name = self.get_name()
            img.save('..'+name)
            self.names.append(name)
        except Exception:
            return
    def get_length(self,h,w,h2,w2):
        return math.sqrt((h-h2)**2+(w-w2)**2)
    def get_nearest_color(self,h,w,pts):
        mind = 10e6
        col = (0,0,0)
        for i in pts:
            l =self.get_length(h,w,i[0],i[1])
            if l < mind:
                mind = l
                col = i[2]

        return col

    def gen_voronoise(self,size,num,inp):
        try:
            if not num or num == 0:
                num = 5
            if 0>= num or num > size:
                num = size
            self.r.seed(inp)
            img = Image.new('RGB', (size, size), color='white')
            pixs = img.load()
            pts = list()
            for i in range(num):
                pts.append([self.r.randint(0,size-1),self.r.randint(0,size-1),(self.r.randint(0,255),self.r.randint(0,255),self.r.randint(0,255))])
            for h in range(size):
                for w in range(size):
                    pixs[h,w] = self.get_nearest_color(h,w,pts)

            name = self.get_name()
            img.save('..'+name)
            self.names.append(name)
        except Exception:
            return
    def gen_photo_voronoise(self,size,num,inp):
        try:
            if not num or num == 0:
                num = 5
            if 0>= num or num > size:
                num = size
            if not inp:
                return
            othr = Image.open(inp).resize((size, size))
            pixs2 = othr.load()
            img = Image.new('RGB', (size, size), color='white')
            pixs = img.load()
            pts = list()
            cols = dict()
            for i in range(num):
                pts.append([self.r.randint(0,size-1),self.r.randint(0,size-1),(self.r.randint(0,255),self.r.randint(0,255),self.r.randint(0,255))])
            for h in range(size):
                for w in range(size):
                    col = self.get_nearest_color(h,w,pts)
                    pixs[h,w] = col
                    col2 = pixs2[h,w]
                    if col in cols.keys():
                        cols[col][0] += col2[0]
                        cols[col][1] += col2[1]
                        cols[col][2] += col2[2]
                        cols[col][3] += 1
                    else:
                        cols[col] = [col2[0],col2[1],col2[2],1]
            for i in cols.keys():
                cols[i] = (cols[i][0]//cols[i][3],cols[i][1]//cols[i][3],cols[i][2]//cols[i][3])
            for h in range(size):
                for w in range(size):
                    pixs[h,w] = cols[pixs[h,w]]

            name = self.get_name()
            img.save('..'+name)
            self.names.append(name)
        except Exception:
            return
    def gen_mono_voronoise(self,size,num,inp):
        try:
            if not num or num == 0:
                num = 5
            if 0>= num or num > size:
                num = size
            self.r.seed(inp)
            img = Image.new('RGB', (size, size), color='white')
            pixs = img.load()
            pts = list()
            for i in range(num):
                if random.randint(0,1) == 0:
                    pts.append([self.r.randint(0, size - 1), self.r.randint(0, size - 1),(0,0,0)])
                else:
                    pts.append([self.r.randint(0, size - 1), self.r.randint(0, size - 1),(255,255,255)])
            for h in range(size):
                for w in range(size):
                    pixs[h,w] = self.get_nearest_color(h,w,pts)

            name = self.get_name()
            img.save('..'+name)
            self.names.append(name)
        except Exception:
            return
