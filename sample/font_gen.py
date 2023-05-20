
## https://pillow.readthedocs.io/en/latest/reference/ImageFont.html
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

text = "あ"
img = Image.new("RGBA",(200,200),(100,100,100,100))
draw = ImageDraw.Draw(img)                 # 描画オブジェクトを生成

font = ImageFont.truetype("meiryo.ttc", 64)

textWidth, textHight = draw.textsize(text, font=font)
whidth, hight = img.size
textColor = (255, 0, 0, 255)
t_X = (whidth - textWidth) // 2
t_Y = (hight - textHight) // 2
draw.text((t_X, t_Y), text, textColor, font=font)

img.show()