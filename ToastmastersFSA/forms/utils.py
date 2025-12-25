from PIL import Image, ImageDraw, ImageFont
import os
from datetime import datetime

def generate_certificat(titre, nom, date):
    
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    img_path = os.path.join(BASE_DIR, 'forms', 'static', 'forms', 'images', 'certificat_base.png')

    certificat = Image.open(img_path)
    draw = ImageDraw.Draw(certificat)

    font_path1 = os.path.join(BASE_DIR, 'forms', 'static', 'forms', 'fonts', 'alata-regular.ttf')
    font_path2 = os.path.join(BASE_DIR, 'forms', 'static', 'forms', 'fonts', 'bauer bodoni regular.otf')
    font_path3 = os.path.join(BASE_DIR, 'forms', 'static', 'forms', 'fonts', 'bauer bodoni condensed bold.otf')

    font_title = ImageFont.truetype(font_path3, 50)
    font_name = ImageFont.truetype(font_path2, 150) 
    font_date = ImageFont.truetype(font_path1, 30)  

    img_size, _ = certificat.size
    name_size = draw.textlength(nom, font=font_name)
    title_size = draw.textlength(titre, font=font_title) 

    x_name = (img_size - name_size) // 2
    x_title = (img_size - title_size) // 2

    draw.text((x_title, 720), titre, font=font_title, fill=(0, 0, 0))
    draw.text((x_name, 900), nom, font=font_name, fill=(0, 0, 0))
    draw.text((290, 1570), date, font=font_date, fill=(0, 0, 0))

    certificat.save("certificat_final.png")
