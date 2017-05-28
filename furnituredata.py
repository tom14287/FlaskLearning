# -*- coding: utf-8 -*

from sqlalchemy import Column, String, create_engine, LargeBinary
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import base64

Base = declarative_base()


class User(Base):
    __tablename__='User'
    UserID=Column(String(20),primary_key=True)
    UserName=Column(String(20))
    UserEmail=Column(String(45))
    UserTel=Column(String(20))    
    UserPassword=Column(String(100))
    UserType=Column(String(20))
    UserImage=Column(LargeBinary)
    UserConfirm=Column(String(10))


class Company(Base):
    __tablename__ = 'Company'
    CompanyID = Column(String(20), primary_key=True)
    CompanyType = Column(String(20))
    CompanyAuth =Column(String(20))
    CompanyAddress= Column(String(45))
    CompanyIntro = Column(String(45))


class Furniture(Base):
    __tablename__ = 'Furniture'

    FurnitureID = Column(String(20), primary_key=True)
    CompanyId = Column(String(20))
    FurnitureName = Column(String(45))
    FurnitureNum =Column(String(20))
    FurniturePrice =Column(String(20))
    FurnitureDesc = Column(String(100))
    FurnitureImage = Column(LargeBinary)
    FurnitureStyle=Column(String(10))


img1 = open("E:/temp/1.jpg", "rb")
img1 = base64.b64encode(img1.read())


img2 = open("E:/temp/2.jpg", "rb")
img2 = base64.b64encode(img2.read())

img3 = open("E:/temp/3.jpg", "rb")
img3 = base64.b64encode(img3.read())

img4 = open("E:/temp/4.jpg", "rb")
img4 = base64.b64encode(img4.read())


print u'你好'

engine = create_engine('mysql://root:daijiarun553@localhost:3306/TYMT')
DBSession = sessionmaker(bind=engine)
session = DBSession()



new_user=User(UserID='1',UserName='ljh',UserEmail='ceshi@163.com',UserTel='12345',UserPassword='nonono',UserType='Company',UserConfirm='1')
session.add(new_user)
session.commit()

new_company=Company(CompanyID='1',CompanyType='Decoration',CompanyAuth='Y',CompanyAddress='linjinghuang',CompanyIntro='666')
session.add(new_company)
session.commit()
new_furniture1 = Furniture(FurnitureID='1',CompanyId='1',FurnitureName='daizong',FurnitureNum='3',FurniturePrice='1000',FurnitureDesc='66',FurnitureImage=img1,FurnitureStyle='C')
new_furniture2 = Furniture(FurnitureID='2',CompanyId='1',FurnitureName='daizong1',FurnitureNum='3',FurniturePrice='1500',FurnitureDesc='66',FurnitureImage=img2,FurnitureStyle='C')
new_furniture3 = Furniture(FurnitureID='3',CompanyId='1',FurnitureName='daizong2',FurnitureNum='3',FurniturePrice='1600',FurnitureDesc='66',FurnitureImage=img3,FurnitureStyle='C')
new_furniture4 = Furniture(FurnitureID='4',CompanyId='1',FurnitureName='linzong',FurnitureNum='3',FurniturePrice='1060',FurnitureDesc='66',FurnitureImage=img4,FurnitureStyle='C')
new_furniture5 = Furniture(FurnitureID='5',CompanyId='1',FurnitureName='linzong',FurnitureNum='3',FurniturePrice='1060',FurnitureDesc='66',FurnitureImage=img1,FurnitureStyle='C')
new_furniture6 = Furniture(FurnitureID='6',CompanyId='1',FurnitureName='daizong3',FurnitureNum='3',FurniturePrice='1300',FurnitureDesc='66',FurnitureImage=img2,FurnitureStyle='C')
new_furniture7 = Furniture(FurnitureID='7',CompanyId='1',FurnitureName='daizong4',FurnitureNum='3',FurniturePrice='1200',FurnitureDesc='66',FurnitureImage=img3,FurnitureStyle='C')
new_furniture8 = Furniture(FurnitureID='8',CompanyId='1',FurnitureName='daizong5',FurnitureNum='3',FurniturePrice='1300',FurnitureDesc='66',FurnitureImage=img4,FurnitureStyle='C')
new_furniture9 = Furniture(FurnitureID='9',CompanyId='1',FurnitureName='daizong6',FurnitureNum='3',FurniturePrice='1500',FurnitureDesc='66',FurnitureImage=img1,FurnitureStyle='C')
new_furniture10 = Furniture(FurnitureID='10',CompanyId='1',FurnitureName='daizong9',FurnitureNum='3',FurniturePrice='300',FurnitureDesc='66',FurnitureImage=img2,FurnitureStyle='C')
new_furniture11 = Furniture(FurnitureID='11',CompanyId='1',FurnitureName='daizong9',FurnitureNum='3',FurniturePrice='1500',FurnitureDesc='66',FurnitureImage=img3,FurnitureStyle='C')
new_furniture12 = Furniture(FurnitureID='12',CompanyId='1',FurnitureName='daizong99',FurnitureNum='3',FurniturePrice='1660',FurnitureDesc='66',FurnitureImage=img4,FurnitureStyle='C')
new_furniture13 = Furniture(FurnitureID='13',CompanyId='1',FurnitureName='daizong99',FurnitureNum='3',FurniturePrice='1060',FurnitureDesc='66',FurnitureImage=img1,FurnitureStyle='C')

session.add(new_furniture1)
session.commit()
session.add(new_furniture2)
session.commit()
session.add(new_furniture3)
session.commit()
session.add(new_furniture4)
session.commit()
session.add(new_furniture5)
session.commit()
session.add(new_furniture6)
session.commit()
session.add(new_furniture7)
session.commit()
session.add(new_furniture8)
session.commit()
session.add(new_furniture9)
session.commit()
session.add(new_furniture10)
session.commit()
session.add(new_furniture11)
session.commit()
session.add(new_furniture12)
session.commit()
session.add(new_furniture13)
session.commit()



system_path='app/static'

print system_path
def imgpath(testid):
	new_furniture = session.query(Furniture).filter(Furniture.FurnitureID == testid).one()
	print new_furniture.FurnitureDesc
	image = base64.b64decode(new_furniture.FurnitureImage)
	path=system_path+'/img/cache/'+str(new_furniture.FurnitureID)+'.jpg'
	with open(path, "wb") as f:
		f.write(image)
	session.close()
	relative_path='img/cache/'+str(new_furniture.FurnitureID)+'.jpg';
	print relative_path
	return relative_path,new_furniture

path1,furn=imgpath(3)
print furn.FurnitureStyle
