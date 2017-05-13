from app import db


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

class Consumer(db.Model):
    __tablename__ = 'Consumer'
    ConsumerID = db.Column(db.Integer, primary_key=True)
    ConsumerBirth = db.Column(db.Date)
    ConsumerTrueName = db.Column(db.String(45))
    ConsumerSex = db.Column(db.Enum('M', 'F'))
    ConsumerResident = db.Column(db.String(45))