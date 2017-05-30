# from app import db, app
from werkzeug.security import check_password_hash, generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
app = Flask(__name__)
db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'User'
    UserID = db.Column(db.Integer, primary_key=True)
    UserName = db.Column(db.String(15))
    UserEmail = db.Column(db.String(45))
    UserTEL = db.Column(db.String(11))
    UserPassword = db.Column(db.String(200))
    UserType = db.Column(db.Enum("Consumer", "Designer", "Company"), default="Consumer")
    UserImage = db.Column(db.BLOB)
    UserConfirm = db.Column(db.Boolean, default=False)
    # Designer = db.relationship("Designer", uselist=False, back_populates="User")
    # UserAddresses = db.relationship("UserAddress", backref="User")


    def __init__(self, name, email, pwd, type_, confirm):
        self.UserEmail = email
        self.UserName = name
        self.UserPassword = generate_password_hash(pwd)
        self.UserType = type_
        self.UserConfirm = confirm

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.UserID)  # python 2
        except NameError:
            return str(self.UserID)  # python 3

    def __repr__(self):
        return '<User %r %d>' % (self.UserName, self.UserID)

class Consumer(db.Model):
    __tablename__ = 'Consumer'
    ConsumerID = db.Column(db.Integer, primary_key=True)
    ConsumerBirth = db.Column(db.Date)
    ConsumerTrueName = db.Column(db.String(45))
    ConsumerSex = db.Column(db.Enum('M', 'F'))
    ConsumerResident = db.Column(db.String(45))
    # UserID = db.Column(db.Integer, db.ForeignKey('User.UserID'))

    def __repr__(self):
        return '<Consumer %d>' % (self.ConsumerID)

class Advertisement(db.Model):
    __tablename__ = 'Advertisement'
    AdID = db.Column(db.Integer, primary_key=True)
    AdContent = db.Column(db.String(200))
    AdType = db.Column(db.Enum('Designer', 'Furniture', 'Company'))
    CompanyID = db.Column(db.Integer)
    FurnitureID = db.Column(db.Integer)
    AdImage = db.Column(db.BLOB)

    def __repr__(self):
        return '<Adver %d>' % (self.AdID)

class Designer(db.Model):
    __tablename__ = 'Designer'
    DesignerID = db.Column(db.Integer, primary_key = True)
    DesignerBirth = db.Column(db.Date)
    DesignerTrueName = db.Column(db.String(45))
    ConsumerID = db.Column(db.Integer)
    DesignerSex = db.Column(db.Enum('M', 'F'))
    DesignerIntro = db.Column(db.String(45))
    # UserID = db.Column(db.Integer, db.ForeignKey('User.UserID'))
    # User = db.relationship("User", back_populates="Designer")

    def __repr__(self):
        return '<Designer %d>' % (self.DesignerID)


class Company(db.Model):
    __tablename__ = 'Company'
    CompanyID = db.Column(db.Integer, primary_key = True)
    CompanyType = db.Column(db.Enum('Decoration', 'Furniture'))
    CompanyAuth  = db.Column(db.Enum('Y', 'N'))
    CompanyAddress  = db.Column(db.String(45))
    CompanyIntro  = db.Column(db.String(200))
    # UserID = db.Column(db.Integer, db.ForeignKey('User.UserID'))

    def __repr__(self):
        return  '<Company %d>' %(self.CompanyID)

class Comments(db.Model):
    __tablename__ = 'Comments'
    CommentsID = db.Column(db.Integer, primary_key = True)
    Content = db.Column(db.String(200))
    Rank = db.Column(db.Enum('1', '2', '3', '4', '5'))
    OrderFormID = db.Column(db.Integer)
    DcFormID = db.Column(db.Integer)

    def __repr__(self):
        return '<Comments %d>' % (self.CommentsID)

class CompetitiveBid(db.Model):
    __tablename__ = 'CompetitiveBid'
    DcFormID = db.Column(db.Integer, primary_key = True)
    SchemeID = db.Column(db.Integer)
    DSDESC = db.Column(db.String(200))
    SubmitTime = db.Column(db.DateTime)
    DSState = db.Column(db.Enum('Waiting', 'Reject', 'Accept'))

class UserAddress(db.Model):
    __tablename__ = 'UserAddress'
    UserID = db.Column(db.Integer, db.ForeignKey("User.UserID"))
    AddressID = db.Column(db.Integer, primary_key = True)
    DeliveryAddress = db.Column(db.String(200))

    def __repr__(self):
        return '<UAddress %d>' % (self.UserID)


class DecorationForm(db.Model):
    __tablename__ = 'DecorationForm'
    DcFormID = db.Column(db.Integer, primary_key = True)
    ConsumerID = db.Column(db.Integer)
    DcFormDESC = db.Column(db.String(200))
    DcFormState = db.Column(db.Enum('Waiting', 'Success', 'Overtime', 'Error', 'Compete', 'Cancel'))
    DcFormCreateTime = db.Column(db.DateTime)

class DesignerScheme(db.Model):
    __tablename__ = 'DesignerScheme'
    SchemeID = db.Column(db.Integer, primary_key = True)
    DesignerID = db.Column(db.Integer)
    CompanyID = db.Column(db.Integer)
    SchemeDESC = db.Column(db.String(200))
    SchemeImage = db.Column(db.BLOB)

class Furniture(db.Model):
    __tableanme__ = 'Furniture'
    FurnitureID = db.Column(db.Integer, primary_key = True)
    CompanyID = db.Column(db.Integer)
    FurnitureName = db.Column(db.String(45))
    FurnitureNum = db.Column(db.Integer)
    FurniturePrice = db.Column(db.Integer)
    FurnitureDESC = db.Column(db.String(200))
    FurnitureImage = db.Column(db.BLOB)


class OrderForm(db.Model):
    __tablename__ = 'OrderForm'
    OrderFormID = db.Column(db.Integer, primary_key = True)
    UserID = db.Column(db.Integer)
    OerderFormState = db.Column(db.Enum('Waiting', 'Success', 'Fail', 'Cancel'))
    CreateTime = db.Column(db.DateTime)

class OrderItem(db.Model):
    __tablename__ = 'OrderItem'
    OrderItemID = db.Column(db.Integer, primary_key = True)
    OrderFormID = db.Column(db.Integer)
    FurnitureID = db.Column(db.Integer)
    OrderItemNum = db.Column(db.Integer)


# from flask import render_template
#@app.route('/')
#def info():
 #  user = User.query.filter_by(UserID=3).first_or_404()
  # print user.UserType
   #return render_template('index.html')

if __name__ == '__main__':
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://kiinghom:atpatpatp@localhost:3306/TYMT?charset=utf8'
    db.init_app(app)
    app.run(debug=True)
