from app import db, app
from werkzeug.security import check_password_hash, generate_password_hash
import base64
from datetime import datetime

class User(db.Model):
    __tablename__ = 'User'
    UserID = db.Column(db.Integer, primary_key=True)
    UserName = db.Column(db.String(15))
    UserEmail = db.Column(db.String(45))
    UserTEL = db.Column(db.String(11))
    UserPassword = db.Column(db.String(200))
    UserType = db.Column(db.Enum("Consumer", "Designer", "Company"), default="Consumer")
    UserImage = db.Column(db.LargeBinary())
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
    AdImage = db.Column(db.LargeBinary())

    def __repr__(self):
        return '<Adver %d>' % (self.AdID)

class Designer(db.Model):
    __tablename__ = 'Designer'
    DesignerID = db.Column(db.Integer, primary_key = True)
    DesignerBirth = db.Column(db.Date)
    DesignerTrueName = db.Column(db.String(45))
    CompanyID = db.Column(db.Integer)
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
    SubmitTime = db.Column(db.DateTime, default=datetime.now)
    DSState = db.Column(db.Enum('Waiting', 'Reject', 'Accept'))
    DSPrice = db.Column(db.Integer, default=100)

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
    DcFormCreateTime = db.Column(db.DateTime, default=datetime.now)

class DesignScheme(db.Model):
    __tablename__ = 'DesignScheme'
    SchemeID = db.Column(db.Integer, primary_key = True)
    DesignerID = db.Column(db.Integer)
    CompanyID = db.Column(db.Integer)
    SchemeDESC = db.Column(db.String(200))
    SchemeImage = db.Column(db.LargeBinary())
    SchemePrice = db.Column(db.Integer, default=1111)

class Furniture(db.Model):
    __tableanme__ = 'Furniture'
    FurnitureID = db.Column(db.Integer, primary_key = True)
    CompanyID = db.Column(db.Integer)
    FurnitureName = db.Column(db.String(45))
    FurnitureNum = db.Column(db.Integer)
    FurniturePrice = db.Column(db.Integer)
    FurnitureDESC = db.Column(db.String(200))
    FurnitureImage = db.Column(db.LargeBinary())
    FurnitureStyle = db.Column(db.Enum('C','J','E'), default='C')

    def insert(self, cid, name, num, price, desc, image):
        temp = Furniture(CompanyID=cid, FurnitureName=name, FurnitureNum=num, FurniturePrice=price, FurnitureDESC=desc, FurnitureImage=image)
        db.session.add(temp)
        db.session.commit()

class OrderForm(db.Model):
    __tablename__ = 'OrderForm'
    OrderFormID = db.Column(db.Integer, primary_key = True)
    UserID = db.Column(db.Integer)
    OrderFormState = db.Column(db.Enum('Waiting', 'Success', 'Fail', 'Cancel'))
    CreateTime = db.Column(db.DateTime, default=datetime.now)
    OrderFormcol = db.Column(db.String(45))

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

def init_mysql():
    user = User("LJH", "ljh@qq.com", "123456", "Consumer", True)
    path = "app/static/img/product/10.jpg"
    user.UserTEL = "12345678901"
    file = open(path, "rb")
    img1 = base64.b64encode(file.read())
    file.close()
    user.UserImage = img1

    db.session.add(user)
    db.session.commit()
    user1 = User("XZL", "xzl@qq.com", "1234", "Designer", True)
    user1.UserTEL = "23456789012"
    user1.UserImage = img1
    consumer = Consumer()
    consumer.ConsumerID = 1
    consumer.ConsumerTrueName = "LLjh"
    consumer.ConsumerSex = 'M'
    consumer.ConsumerResident = "resident1"
    des = Designer()
    des.DesignerID = 2
    des.DesignerIntro = "intro333"
    des.DesignerSex = 'M'
    des.DesignerTrueName = 'xzl'
    db.session.add(user1)
    db.session.commit()
    db.session.add(consumer)
    db.session.commit()
    db.session.add(des)
    db.session.commit()
    user2 = User("GJL", "gjl@qq.com", "123", "Company", True)
    user2.UserTEL = "34567890123"
    user2.UserImage = img1
    company = Company()
    company.CompanyID = 3
    company.CompanyIntro = "intro1"
    company.CompanyAddress = 'addr444'
    company.CompanyAuth = 'Y'
    company.CompanyType = 'Furniture'
    db.session.add(user2)
    db.session.commit()
    db.session.add(company)
    db.session.commit()
    ad = Advertisement()
    ad.CompanyID = 3
    ad.AdContent = "con123"
    ad.AdImage = img1
    ad.AdType = "Company"
    db.session.add(ad)
    db.session.commit()
    fr = Furniture()
    fr.CompanyID = 3
    fr.FurniturePrice = 103
    fr.FurnitureDESC = "desc123"
    fr.FurnitureName = "ShuiGuoMu"
    fr.FurnitureImage = img1
    fr.FurnitureNum = 111
    db.session.add(fr)
    db.session.commit()
    ds = DesignScheme()
    ds.CompanyID = 3
    ds.SchemeDESC = "desc234"
    ds.SchemeImage = img1
    ds.SchemePrice = 100
    db.session.add(ds)
    db.session.commit()
    df = DecorationForm()
    df.ConsumerID = 1
    df.DcFormDESC = "desc345"
    df.DcFormState = "Success"
    db.session.add(df)
    db.session.commit()
    cb = CompetitiveBid()
    cb.DcFormID = 1
    cb.SchemeID = 1
    cb.DSDESC = "desc456"
    cb.DSState = "Accept"
    db.session.add(cb)
    db.session.commit()
    ar = UserAddress()
    ar.UserID = 1
    ar.DeliveryAddress = "addre112"
    db.session.add(ar)
    db.session.commit()
    of = OrderForm()
    of.UserID = 1
    of.OrderFormState = "Success"
    of.OrderFormcol = "dontknow"
    db.session.add(of)
    db.session.commit()
    oitm = OrderItem()
    oitm.OrderFormID = 1
    oitm.FurnitureID = 1
    oitm.OrderItemNum = 2
    db.session.add(oitm)
    db.session.commit()
    of = OrderForm()
    of.UserID = 1
    of.OrderFormcol ='idontnow'
    of.OrderFormState = 'Waiting'
    db.session.add(of)
    db.session.commit()
    oitm = OrderItem()
    oitm.OrderFormID = 2
    oitm.FurnitureID = 1
    oitm.OrderItemNum = 3
    db.session.add(oitm)
    db.session.commit()
    cm = Comments()
    cm.Content = "con123"
    cm.Rank = '1'
    cm.OrderFormID = 1
    db.session.add(cm)
    db.session.commit()
    db.session.execute("insert into DesignScheme(DesignerID,SchemeDESC,SchemeImage,SchemePrice)value(2,'sdesc111','%s',111)" % img1)
    db.session.execute("insert into DesignScheme(CompanyID,SchemeDESC,SchemeImage,SchemePrice)value(3,'sdesc1121','%s',1121)" % img1)
    db.session.commit()

if __name__ == '__main__':
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://kiinghom:atpatpatp@localhost:3306/TYMT?charset=utf8'
    db.init_app(app)
    app.run(debug=True)
