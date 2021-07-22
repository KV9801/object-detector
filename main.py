#!/usr/bin/env python3
import os
from time import time
from model import *
from werkzeug.exceptions import RequestEntityTooLarge
from flask import Flask, render_template, request, send_from_directory, flash, redirect


app = Flask(__name__)
app.config.from_object(Config)
model = Model()

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/static/photos/out/<path:path>')
def send_image(path):
    return send_from_directory('static/photos/out', path)

def clear(path) -> None:
    for item in os.listdir(path):
        p = f'{path}/{item}'
        now = time()
        created = os.path.getmtime(p)
        if round(now - created) > 150:
            os.remove(p)

@app.route('/', methods=['POST'])
def upload_file():
    try:
        f = request.files['file']
    except RequestEntityTooLarge:
        flash('File size too large. Max supported limit is 16 MB.')
        return redirect('/')

    if f.filename != '':
        # Check if uploaded image has correct format
        if f.content_type not in ('image/jpeg', 'image/jpg'):
            flash('Unsupported file type. Required format: JPG/JPEG')
            return redirect('/')

        _, ext = os.path.splitext(f.filename)
        name = f'{round(time()*1000)}{ext}'
        path = f'static/photos/in/{name}'
        f.save(path)
        photo = open(f'static/photos/in/{name}', 'rb')
        res = model.getphoto(path)
        res.save('static/photos/out')
        for p in ['static/photos/in','static/photos/out']: clear(p)
        return render_template('index.html', photo=name)

    return render_template('index.html')

if __name__ == '__main__':
    app.run()