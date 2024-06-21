import os
from flask import Flask, render_template, request, redirect, url_for, session
from sqlmodel import Field, SQLModel, create_engine, Session, select
from pydantic import BaseModel
from enc import Encryption
import ai_process


app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = './uploads'
app.config["ALLOWED_EXTENSION"] = {'png', 'jpg', 'jpeg'}


class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    city: str = Field()
    email: str = Field()
    username: str = Field()
    password: str = Field()
    
engine = create_engine('sqlite:///./database.db', echo=True)
SQLModel.metadata.create_all(engine)


class RegisterModel(BaseModel):
    city: str
    email: str
    username: str
    password: str
    
    
class LoginModel(BaseModel):
    username: str
    password: str


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
        try:
            login_model = LoginModel(
                username = request.form["username"],
                password = request.form["password"])
            
        except:
            print('Type Error')
            return redirect(url_for('login'))
        
        with Session(engine) as db_session:
            statement = select(User).where(User.username == login_model.username)
            result = db_session.exec(statement).first()
        
        if result:
            enc_obj = Encryption()
            if enc_obj.check(login_model.password, result.password):
                print('welcome, you are logged in')
                return redirect(url_for('upload'))
            else:
                print('Password is incorrect')
                return redirect(url_for('login'))
        else:
            print('Username is incorrect')
            return redirect(url_for('login'))


@app.route("/register", methods=['GET', "POST"])
def register():
    if request.method == "GET":
        return render_template('register.html')
    
    elif request.method == "POST":
        try:
            register_data = RegisterModel(
                city=request.form["city"], 
                email=request.form["email"], 
                username=request.form["username"], 
                password=request.form["password"])
        except:
            print('Type Error')
            return redirect(url_for('register'))
            
            
        with Session(engine) as db_session:
            statement = select(User).where(User.username == register_data.username)
            result = db_session.exec(statement).first()
            
        if not result:
            enc_obj = Encryption()
            hashed_password = enc_obj.hash_password(register_data.password)
            with Session(engine) as db_session:
                user = User(
                    city=register_data.city, 
                    username=register_data.username,
                    email=register_data.email,
                    password=hashed_password
                    )
                db_session.add(user)
                db_session.commit()
                print('Your register done succesfully.')
                return redirect(url_for('login'))
        else:
            print('username already exist, Try another username.')
            return redirect(url_for('register'))


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


@app.route("/BMR", methods=['GET', "POST"])
def BMR():
    if request.method == "GET":
        return render_template('BMR.html', result=None)
    
    elif request.method == "POST":
        height = request.form["height"]
        weight = request.form["weight"]
        age = request.form["age"]
        gender = request.form["gender"]
        result = ai_process.calculate_BMR(gender=gender, height=float(height), weight=float(weight), age=float(age))
        
        return render_template('BMR.html', result=result)


if __name__ == '__main__':
    app.run(debug=True)
