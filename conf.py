#!/home/pi/.virtualenvs/fr/bin/python3
from flask import Flask, render_template, redirect, request, flash, jsonify, Response, url_for
import flask
import os
from werkzeug.utils import secure_filename
from FRs import VideoCamera
import cv2

#curl -X POST -F encode=@encodings.pickle 'http://192.168.100.64:5000/encode'

global email
global name

UPLOAD_FOLDER = 'encodings'

#UPLOAD_FOLDER = '/home/drexgen/Documentos/OPENCV/DESARROLLOS/PI-FACERECO/pi-face-recognition/enco'
ALLOWED_EXTENSIONS = {'pickle'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('form.html')


@app.route('/process', methods=['POST'])
def process():
    global email
    email = int(request.form['webcam'])
    print (email)

    name = request.form['resolucion']
    distanciamiento = request.form['distanciamiento']
    integracion = request.form['cliente']
    print (integracion)
 

    if name:
        newName = name[::-1]
        # Aca habria que definir algo para que haga una actualizacion de la camara si no es la misma
        return jsonify({'success': email})

    return jsonify({'error': 'Missing data!'})

def gen(camera):
    print (camera)

    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        key = 0xFF
        if key == ord("q"):
            break


@app.route('/video_feed')
def video_feed():

    global email
    return Response(gen(VideoCamera(email)),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

def loop(camera,band):
    while band:
        camera.get_frame()



@app.route("/encode", methods=["POST"])
def enco():
    #curl -X POST -F encode=@encodings.pickle 'http://192.168.100.64:5000/encode'
    if request.method == 'POST':
        file = request.files['encode']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            print ("OK LLEGO")
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
        d = {'success':True}
    return flask.jsonify(d)	

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)
