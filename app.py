import os
from flask import Flask, render_template, request, redirect, url_for, session
import ai_process


app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = './uploads'
app.config["ALLOWED_EXTENSION"] = {'png', 'jpg', 'jpeg'}


def auth(email, password):
    if email=="beni@beni.com" and password=='123':
        return True
    else:
        return False


def allowed_file(filename):
    return True


@app.route("/")
@app.route("/index")
def index():
    return render_template('index.html')


@app.route("/login", methods=['GET', "POST"])
def login():
    if request.method == "GET":
        return render_template('login.html')
    
    elif request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        result = auth(email=email, password=password)
        if result:
            return redirect(url_for('upload'))
        else:
            return redirect(url_for('login'))


@app.route("/upload", methods=['GET', "POST"])
def upload():
    if request.method == "GET":
        return render_template('upload.html')
    
    elif request.method == "POST":
        image = request.files['image']
        if image.filename == '':
            return redirect(url_for('upload'))
        else:
            if image and allowed_file(image.filename):
                save_path = os.path.join(app.config["UPLOAD_FOLDER"], image.filename)
                image.save(save_path)
                process = ai_process.Ai_analyze()
                result = process.analyze(save_path)
                
            return render_template('result.html', result=result)
            


@app.route("/result")
def result():
    return render_template('result.html')




if __name__ == '__main__':
    app.run(debug=True)
