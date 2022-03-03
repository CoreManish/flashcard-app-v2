from flask import Flask, jsonify, redirect, render_template, request, url_for
from models import *




#------User Authentication-------

@app.route('/login',methods=['POST'])
def login():
    data=request.get_json()
    check_record=User.query.filter_by(username=data['username'],password=data['password']).first()
    
    if check_record is not None:
        return jsonify({'message':'Logged in successfully'}),200
    else:
        return  jsonify({'message':'Not Registered'}),202


#------User Registration------

@app.route('/register',methods=['POST'])
def register():
    data=request.get_json()
    check_record_by_email = User.query.filter_by(email=data['email']).first()
    check_record_by_username=User.query.filter_by(username=data['username']).first()

    if check_record_by_email is None and check_record_by_username is None:
        new_user=User(username=data['username'],password=data['password'],name=data['name'],email=data['email'])
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message':'Registered successfully, now login'})
    else:
        return jsonify({"message":"Either email or username exists"})





@app.route("/")
def index():
    return render_template("index.html")




if __name__=='__main__':
    app.run(debug=True)