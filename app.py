from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'pin.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)


class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(80))
    address = db.Column(db.String(120))
    code = db.Column(db.String(12),unique=True)
    latitude = db.Column(db.String(25))
    longitude = db.Column(db.String(25))




    def __init__(self, Name, address,code,latitude,longitude):
        self.Name = Name
        self.address = address
        self.code = code
        self.latitude = latitude
        self.longitude = longitude


class UserSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('Name', 'address','code','latitude','longitude')


user_schema = UserSchema()
users_schema = UserSchema(many=True)

def Pin_exists(pin):
    if db.session.query(City).filter_by(code=pin).scalar() is not None:
        return True
    else: return False
    


# endpoint to create new CITY
@app.route("/post_location", methods=["POST"])
def post_location():
    if request.method  == 'POST':
        data = dict(request.args)

        Name = data['name'][0]
        address = data['address'][0]
        code = data['code'][0]
        latitude = data['lat'][0]
        longitude = data['lng'][0]
        print(type(Name))

        new_city = City(Name, address,code,latitude,longitude)
        
        
        if Pin_exists(code) == False:
            db.session.add(new_city)
            db.session.commit()

            return 'city added'
        else:return 'City Already exists' 
        
        
        
        
    else:
        print('not post')








if __name__ == '__main__':
    app.run(debug=True)
