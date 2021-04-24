from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

#Init app
app = Flask(__name__)
basedir=os.path.abspath(os.path.dirname(__file__))

#database
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(basedir,'cryptDevs.sqlite')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False


#Initialize
db = SQLAlchemy(app)
#Initialize Marshmallow
ma = Marshmallow(app)

#Product Class/Model
class CryptDevs(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100))
    Platform = db.Column(db.String(100))
    testNetBal = db.Column(db.Float)

    def __init__(self,name,Platform,testNetBal):
        self.name = name
        self.Platform = Platform
        self.testNetBal = testNetBal

#Developers Schema
class DevSchema(ma.Schema):
    class Meta:
        fields =('id','name','Platform','testNetBal')


#initializing Schema 
dev_schema = DevSchema() 
devs_schema = DevSchema(many=True)



#Create User
@app.route('/create_user',methods=['POST'])
def create_User():
    name = request.json['name']
    Platform = request.json['Platform']
    testNetBal = request.json['testNetBal']

    new_user = CryptDevs(name,Platform,testNetBal)

    db.session.add(new_user)
    db.session.commit()

    return dev_schema.jsonify(new_user)

#getUsers
@app.route('/users',methods=['GET'])
def get_users():
    all_users=CryptDevs.query.all()
    result = devs_schema.dump(all_users)
    return jsonify(result)


#getUser
@app.route('/getUser/<id>',methods=['GET'])
def get_user(id):
    getuser = CryptDevs.query.get(id)
    result = dev_schema.dump(getuser)
    return jsonify(result)

#update user
@app.route('/updateuser/<id>',methods=['PUT'])
def update_user(id):
    user = CryptDevs.query.get(id)

    name = request.json['name']
    Platform = request.json['Platform']
    testNetBal=request.json['testNetBal']

    user.name = name
    user.Platform = Platform
    user.testNetBal = testNetBal

    db.session.commit()
    
    result = dev_schema.dump(user)
    return jsonify(result)

@app.route("/deleteuser/<id>",methods=["DELETE"])
def deleteUser(id):
    getuser = CryptDevs.query.get(id)
    db.session.delete(getuser)
    db.session.commit()

    return jsonify({"msg":" User Deleted Successfuly"})





#run server
if __name__=="__main__":
    app.run(debug=True)
