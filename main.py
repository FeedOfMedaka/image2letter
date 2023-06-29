import os
import glob
import shutil
import numpy as np
from PIL import Image, ImageFont, ImageDraw

class image2letter:
    
    def main(self):
        print('ファイル確認中...')
        jpg, jpeg, png = self.check_dir_file()
        
        print('画像読込中...')
        self.read_image(jpg, jpeg, png)
        
    def user_setting(self):
        colorset = "MWN$@%#&B89EGA6mK5HRkbYT43V0JL7gpaseyxznocv?jIftr1li*=-~^`':;,. "
        font = ImageFont.truetype('./font/Saitamaar.ttf', 15)
        compress = 1

        x, y = 0, 0
        for c in colorset:
            _, _, x_, y_ = font.getbbox(c)
            if x < x_:
                x = x_ 
            if y < y_:
                y = y_ 
        
        return colorset, font, compress, x, y

    
    def check_dir_file(self):
        jpg, jpeg, png = "", "", ""
        
        if os.path.isdir('./input') == True:
            if os.path.isdir('./output') == True:
                shutil.rmtree('./output')
            
            os.mkdir('./output')
            jpg = glob.glob(r'./input/*.jpg',recursive=True)
            jpeg = glob.glob(r'./input/*.jpeg',recursive=True)
            png = glob.glob(r'./input/*.png',recursive=True)
            
        else:
            print("./input is not found")
            print("make ./input")
            os.mkdir('./input')
            exit()
            
        return (jpg, jpeg, png)


    def read_image(self, jpg, jpeg, png):
        if len(jpg)==0 and len(jpeg)==0 and len(png)==0:
            print("image is not found")
            exit()
        
        print("画像変換中...")
        colorset, font, compress, x, y = self.user_setting()
        
        if not len(jpg)==0:
            for i in range(len(jpg)):
                self.image2letter(jpg[i], colorset, font, compress, x, y)
                
        if not len(jpeg)==0:
            for i in range(len(jpeg)):
                self.image2letter(jpeg[i], colorset, font, compress, x, y)
        
        if not len(png)==0:
            for i in range(len(png)):
                self.image2letter(png[i], colorset, font, compress, x, y)
                
    
    def image2letter(self, path, colorset, font, compress, x, y):
        img = Image.open(path)
        gray_img = np.asarray(img.convert("L"))
        #w, h = img.size
        
        # Generating AA
        txt = ""
        a, b = 0, 0
        for i in gray_img:
            a = a + 1
            if a % compress == 0:
                txt += "\n"
            else:
                continue
            for j in i:
                b = b + 1
                txt += colorset[j // 4] * 2 if b % compress == 0 else ""
        txt = txt[1:]

        output_txt_path = './output/' + os.path.basename(path) + '.txt'
        with open(output_txt_path, mode="w") as f:
            f.write(txt)

        # AA to image
        lines = txt.split("\n")
        nimg = Image.new("RGB", (len(lines[0])*x, len(lines)*y), "#ffffff")
        draw = ImageDraw.Draw(nimg)
        
        for i,line in enumerate(lines):
            for j, c in enumerate(line):
                draw.text((j*x, i*y), c, font=font, fill="#000000")
               
        #nimg = nimg.resize ((w*7, h*7)) 
        output_image_path = './output/' + os.path.basename(path)
        nimg.save(output_image_path)


if __name__ == "__main__":
    image2letter().main()