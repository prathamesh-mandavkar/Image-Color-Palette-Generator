from flask import Flask, render_template, flash, request, redirect, url_for
from flask_login import current_user
from werkzeug.utils import secure_filename
from flask_bootstrap import Bootstrap
import numpy as np
from PIL import Image
import os

UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png','gif'}
app = Flask(__name__)
Bootstrap(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'anfo[ihqwr02891hrd0wniefp[nq30[p98h4f0q32hr['


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def rgb2hex(r, g, b):
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)


def get_palette(filename):
    img = Image.open(filename)
    img_array = np.array(img)
    hex_pixels = []
    colors = {}
    for row in img_array:
        for pixel in row:
            hex_pixels.append(rgb2hex(pixel[0], pixel[1], pixel[2]))
    for pixel in hex_pixels:
        if pixel in colors:
            colors[pixel] += 1
        else:
            colors[pixel] = 1
    palette_list = list(colors.items())
    palette_list.sort(reverse=True, key=lambda x: x[1])
    top_10_palette_list = palette_list[:10]
    top_50_palette_list = palette_list[:50]
    return palette_list,top_10_palette_list,top_50_palette_list


# routes
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # check if post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(url_for('home'))
        file = request.files['file']
        # If the user does not select a file, the browser submits an empty file w/o filename
        if file.filename == '':
            flash('No file selected')
            return redirect(url_for('home'))
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            colors,top10_colors,top50_colors = get_palette(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return render_template('index.html', colors=colors,top10_colors=top10_colors,top50_colors=top50_colors,filename=filename)
        else:
            flash('Allowed image types are - png, jpg, jpeg, gif')
            return redirect(url_for('home'))    
    return render_template('index.html')

@app.route("/about")
def about():
    return render_template("about.html")

@app.route('/display/<filename>')
def display_image(filename):
    #print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)

if __name__ == '__main__':
    app.run(debug=True)