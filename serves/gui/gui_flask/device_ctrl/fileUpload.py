#!/usr/bin/python3
from flask import Flask, render_template, request, send_from_directory
import os
from flask_cors import *
app = Flask(__name__)

# @app.route('/')
# def index():
#     entries = os.listdir('./upload')
#     return render_template('index.html', entries = entries)

@app.route('/upload', methods=['POST'])
@cross_origin(supports_credentials=True)
def upload():
    f = request.files['file']
    path = os.path.join('./upload', f.filename)
    f.save(path)
    # return render_template('upload.html')
    res = {}
    res['message'] = "success"
    return res

# @app.route('/files/<filename>')
# def files(filename):
#     return send_from_directory('./upload', filename, as_attachment=True)

app.run(debug = True,port = 5055)

