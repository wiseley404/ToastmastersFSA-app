from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import os
from datetime import datetime

def generate_certificat(title, name, date):
    
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    img_path = os.path.join(BASE_DIR, 'forms', 'static', 'forms', 'images', 'certificat_base.png')

    certificat = Image.open(img_path)
    draw = ImageDraw.Draw(certificat)

    font_path1 = os.path.join(BASE_DIR, 'forms', 'static', 'forms', 'fonts', 'alata-regular.ttf')
    font_path2 = os.path.join(BASE_DIR, 'forms', 'static', 'forms', 'fonts', 'bauer bodoni regular.otf')
    font_path3 = os.path.join(BASE_DIR, 'forms', 'static', 'forms', 'fonts', 'bauer bodoni condensed bold.otf')

    font_title = ImageFont.truetype(font_path3, 50)
    font_name = ImageFont.truetype(font_path2, 120) 
    font_date = ImageFont.truetype(font_path1, 30)  

    display_name = name
    if len(name) > 15:
        parts = name.split()
        if len(parts) == 2:
            display_name = parts[0][0].upper() + '. ' + parts[1].upper()
        elif len(parts) == 3:
            if len(parts[-2] + parts[-1]) <= 17:
                display_name = parts[0][0].upper() + '. ' + parts[1].title() + ' ' + parts[2].upper()
            else:
                display_name = ' '.join([p[0].upper() + '.' for p in parts[:-1]]) + ' ' + parts[-1].upper()
        elif len(parts) > 3:
            if len(parts[-2] + parts[-1]) <= 17:
                display_name = ' '.join([p[0].upper() + '.' for p in parts[:-2]]) + ' ' + parts[-2].title() + ' ' + parts[-1].upper()
            else:
                display_name = ' '.join([p[0].upper() + '.' for p in parts[:-1]]) + ' ' + parts[-1].upper()
    else:
        parts = name.split()
        display_name = ' '.join([p.title() for p in parts[:-1]]) + ' ' + parts[-1].upper()

    img_size, _ = certificat.size
    name_size = draw.textlength(display_name, font=font_name)
    title_size = draw.textlength(title, font=font_title) 

    x_name = (img_size - name_size) // 2
    x_title = (img_size - title_size) // 2

    draw.text((x_title, 720), title.title(), font=font_title, fill=(0, 0, 0))
    draw.text((x_name, 900), display_name, font=font_name, fill=(0, 0, 0))
    draw.text((290, 1570), date, font=font_date, fill=(0, 0, 0))

    img_io = BytesIO()
    certificat.save(img_io, format='PNG')
    img_io.seek(0)
    return img_io.getvalue()



