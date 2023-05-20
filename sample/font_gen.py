
## https://pillow.readthedocs.io/en/latest/reference/ImageFont.html
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

#text = "あ"
text = "あいうえお"

img = Image.new("RGBA",(70,350),(100,100,100,100))
draw = ImageDraw.Draw(img)
font = ImageFont.truetype("meiryo.ttc", 64)

chWidth, chHight = draw.textsize(text[0], font=font)
width, hight = img.size
textColor = (255, 0, 0, 255)
print(img.size)
print(text[0])
print(f"width={chWidth},hight={chHight}")
draw.text((0,0), text[0], textColor, font=font)

img.show()