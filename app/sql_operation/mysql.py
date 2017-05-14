from app import db
from werkzeug.security import check_password_hash, generate_password_hash


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
        return '<User %r>' % (self.UserName)

class Consumer(db.Model):
    __tablename__ = 'Consumer'
    ConsumerID = db.Column(db.Integer, primary_key=True)
    ConsumerBirth = db.Column(db.Date)
    ConsumerTrueName = db.Column(db.String(45))
    ConsumerSex = db.Column(db.Enum('M', 'F'))
    ConsumerResident = db.Column(db.String(45))

class Advertisement(db.Model):
    __tablename__ = 'Advertisement'
    AdID = db.Column(db.Integer, primary_key=True)
    AdContent = db.Column(db.String(200))
    AdType = db.Column(db.Enum('Designer', 'Furniture', 'Company'))
    CompanyID = db.Column(db.Integer)
    FurnitureID = db.Column(db.Integer)
    AdImage = db.Column(db.BLOB)

class Designer(db.Model):
    __tablename__ = 'Designer'
    DesignerID = db.Column(db.Integer, primary_key = True)
    DesignerBirth = db.Column(db.Date)
    DesignerTrueName = db.Column(db.String(45))
    ConsumerID = db.Column(db.Integer)
    DesignerSex = db.Column(db.Enum('M', 'F'))
    DesignerIntro = db.Column(db.String(45))

class Company(db.Model):
    __tablename__ = 'Company'
    CompanyID = db.Column(db.Integer, primary_key = True)
    CompanyType = db.Column(db.Enum('Decoration', 'Furniture'))
    CompanyAuth  = db.Column(db.Enum('Y', 'N'))
    CompanyAddress  = db.Column(db.String(45))
    CompanyIntro  = db.Column(db.String(200))

class Comments(db.Model):
    __tablename__ = 'Comments'
    CommentsID = db.Column(db.Integer, primary_key = True)
    Content = db.Column(db.String(200))
    Rank = db.Column(db.Enum('1', '2', '3', '4', '5'))
    OrderFormID = db.Column(db.Integer)
    DcFormID = db.Column(db.Integer)

class CompetitiveBid(db.Model):
    __tablename__ = 'CompetitiveBid'
    DcFormID = db.Column(db.Integer, primary_key = True)
    SchemeID = db.Column(db.Integer)
    DSDESC = db.Column(db.String(200))
    SubmitTime = db.Column(db.DateTime)
    DSState = db.Column(db.Enum('Waiting', 'Reject', 'Accept'))
