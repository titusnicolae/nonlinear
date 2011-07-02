#!/usr/bin/python
from PIL import Image,ImageDraw
im=Image.new("L",(100,100))
draw=ImageDraw.Draw(im)
draw.line([(0,0),(99,99)],fill=(255,0,0))
im.save("file.bmp","BMP")
