from flask import Flask, render_template, request, url_for, redirect
from PIL import Image, ImageDraw, ImageFont
import os


def add_padding_wide(pil_img, background_color, padding_top_sides, padding_bottom):
    width, height = pil_img.size
    new_width = width + 2 * padding_top_sides
    new_height = height + padding_top_sides + padding_bottom
    result = Image.new(pil_img.mode, (new_width, new_height), background_color)
    result.paste(pil_img, (padding_top_sides, padding_top_sides))
    return result

def add_padding_tall(pil_img, background_color, padding_top_sides, padding_bottom):
    width, height = pil_img.size
    padding_top_sides_tall = padding_top_sides // 2
    padding_bottom_tall = padding_bottom // 2
    new_width = width + 2 * padding_top_sides_tall
    new_height = height + padding_top_sides_tall + padding_bottom_tall
    result = Image.new(pil_img.mode, (new_width, new_height), background_color)
    result.paste(pil_img, (padding_top_sides_tall, padding_top_sides_tall))
    return result

def draw_text(image, text, position, font_path='Moon2.0-Regular.otf', font_size=100):
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(font_path, font_size)
    text_width, text_height = draw.textsize(text, font=font)
    position = (image.width // 2, position[1])
    draw.text(position, text, font=font, fill='black', anchor='mm')




app = Flask(__name__)

@app.route('/')
def home ():
    return render_template('upload.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'GET':
        return render_template('upload.html')
    elif request.method == 'POST':
        file = request.files['example']
        text1 = request.form.get('text1')  #使用機材
        text2 = request.form.get('text2')  #使用フィルム


        img = Image.open(file)

        if img.width > img.height:
            
            img = add_padding_wide(img, (255, 255, 255), 150, 600)
            
            draw_text(img, text1, (0, img.height - 400)) 
            draw_text(img, text2, (0, img.height - 260))

        elif img.width == img.height:
            img = add_padding_tall(img, (255, 255, 255), 100, 500)
            draw_text(img, text1, (0, img.height - 160), font_size=70)  
            draw_text(img, text2, (0, img.height - 80), font_size=70)

        
        else:
            img = add_padding_tall(img, (255, 255, 255), 100, 500)
            draw_text(img, text1, (0, img.height - 160), font_size=50)  
            draw_text(img, text2, (0, img.height - 80), font_size=50)
            
        
        
        filepath = os.path.join('./static/image', file.filename)
        img.save(filepath)

        return redirect(url_for('result', filename=file.filename))




@app.route('/result.html/<string:filename>')
def result(filename):
    return render_template('result.html', filename=filename)

if __name__ == '__main__':
    app.run(debug=True)
