
## https://pillow.readthedocs.io/en/latest/reference/ImageFont.html
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

CHIPSIZE=70
text = "あいうえおかきくけおさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよわをん"
print(len(text))

img = Image.new("RGBA",(CHIPSIZE,CHIPSIZE*len(text)),(0,0,123,255))
draw = ImageDraw.Draw(img)
font = ImageFont.truetype("meiryo.ttc", 64)

def drawtext(char,y):
    chWidth, chHight = draw.textsize(char, font=font)
    color = (0, 255, 0, 255)
    draw.text((0,y*CHIPSIZE), char, color, font=font)

for i in range(len(text)):
    drawtext(text[i],i)

img.save("kana_font.png")
img.show()