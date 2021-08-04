from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///cardata.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)

islogin=0

class Vehicles(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    longitude=db.Column(db.String(20),nullable=False)
    latitude = db.Column(db.String(20), nullable=False)
    speed = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Boolean, nullable=False)
    time= db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.id} - {self.time}"

@app.route("/",methods=['GET','POST'])
def login():
    global islogin
    if request.method=='POST':
        if request.form['username']=="deep@dnyindia.in" and request.form['password']=="testdemo":
            islogin=1
            return redirect("/dashboard")
        else:
            return render_template('login.html',message="Username / Password invalid! ")
    else:
        if islogin==1:
            return redirect("/dashboard")
        else:
            return render_template('login.html')

@app.route("/logout")
def logout():
    global islogin
    islogin=0
    return redirect('/')

@app.route("/dashboard")
def dashboard():
    all_data=Vehicles.query.all()
    enable=0
    for i in all_data:
        if i.status==True:
            enable+=1
    return render_template('dashboard.html',car_no=len(all_data),disable=len(all_data)-enable,enable=enable,car_data=all_data)

@app.route("/update_data",methods=['GET','POST'])
def update_data():
    if request.method == 'POST':
        id=request.args.get("id", "")
        #car_data=Vehicles(longitude="23.402040",latitude="87.547729",speed=10,status=1)
        #db.session.add(car_data)
        #db.session.commit()
        data = Vehicles.query.filter_by(id=id).first()
        data.longitude = request.args.get("longitude", "")
        data.latitude = request.args.get("latitude", "")
        data.speed = int(request.args.get("speed", ""))
        db.session.add(data)
        db.session.commit()
        return "Updated!"
    else:
        return "Failed"
@app.route("/enable/<int:id>")
def enable(id):
    data= Vehicles.query.filter_by(id=id).first()
    data.status=True
    db.session.add(data)
    db.session.commit()
    return redirect("/dashboard")
@app.route("/disable/<int:id>")
def desable(id):
    data = Vehicles.query.filter_by(id=id).first()
    data.status = False
    db.session.add(data)
    db.session.commit()
    return redirect("/dashboard")
@app.route("/locate/<int:id>")
def locate(id):
    data = Vehicles.query.filter_by(id=id).first()
    long=data.longitude
    lat=data.latitude
    url=f"https://www.google.com/maps/search/?api=1&query={long},{lat}"
    return redirect(url)
if __name__=="__main__":
    app.run(debug=True,host="0.0.0.0",port=6622)
