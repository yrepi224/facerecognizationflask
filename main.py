import os
import webbrowser
from app import app
import urllib.request
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import tensorflow as tf
from fer import FER
import cv2
import matplotlib.pyplot as plt

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	
@app.route('/')
def upload_form():
    return render_template('upload.html')

@app.route('/close')
def upload_redirect():
    return redirect(url_for('upload_form'))



@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('noselect')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
	#print('upload_image filename: ' + filename)
        img = cv2.imread(f'/home/rasa/test/static/uploads/{filename}')
        detector = FER()
        try:
            emotion, score = detector.top_emotion(img)
        except IndexError:
            flash('can not detect emotion')
            return render_template('upload.html', filename=filename)
        if emotion=='happy':
            return render_template('upload.html', filename=filename, vary=True)
        else:
            return render_template('upload.html', filename=filename)
    else:
        flash('Allowed image types are -> png, jpg, jpeg, gif')
        return redirect(request.url)

@app.route('/display/<filename>')
def display_image(filename):
    #print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port='5000')
    
