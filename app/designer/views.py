# encoding=utf-8
from flask import Blueprint
from flask import render_template, request, redirect, url_for, g
from flask_login import login_required
from app.sql_operation.mysql import *
from app import db

designer_ = Blueprint('designer', __name__)


@designer_.route("")
@designer_.route("/index")
# @login_required
def designer_index():
    return render_template("designer.html", user_name='dyftug')


@designer_.route("/change_info", methods=['GET', 'POST'])
@login_required
def designer_change_info():
    return


def update_designer(id, cid, birth, truename, sex, intro):
    sql = ""
    if cid != None:
        sql += ",CompanyID=%d" % cid
    if birth != None:
        sql += ",DesignerBirth=str_to_date('%s', '%%Y-%%m-%%d')" % birth
    if truename != None:
        sql += ",DesignerTrueName='%s'" % truename
    if sex != None:
        sql += ",DesignerSex='%s'" % sex
    if intro != None:
        sql += ",DesignerIntro='%s'" % intro
    sql = sql[1:]
    db.session.execute("update Designer set %s where DesignerID=%d" % (sql, id))
    db.session.commit()

# Test ed
@designer_.route("/design_scheme", methods=['GET', 'POST'])
# @login_required
def designer_design_scheme():
	g.user = User.query.filter_by(UserID=2).first()
	design = []

	designer, schemes = get_allscheme_byid(g.user.UserID)
	for item in schemes:
		temp = {}
		# 链接到设计方案展示界面
		temp['url'] = 'http://127.0.0.1:5000/designer/scheme/' + str(item.SchemeID)
		temp['name'] = str(item.SchemeID)
		temp['price'] = '$' + str(item.SchemePrice)
		design.append(temp)

	return render_template("designer_scheme.html", design=design)


def get_allscheme_byid(id):
    designer = Designer.query.filter_by(DesignerID=id).first()
    if designer:
        schemes = DesignScheme.query.filter_by(DesignerID=id).all()
        return designer, schemes
    return None, None


@designer_.route("/orders", methods=['GET', 'POST'])
# @login_required
def designer_orders():
    g.user = User.query.filter_by(UserID=2).first()
    design = []
    schemes = get_all_success_scheme_byid(g.user.UserID)
    print schemes
    for item in schemes:
        print item
        temp = {}
        # 链接到设计方案展示界面
        temp['url'] = 'http://127.0.0.1:5000/designer/scheme/' + str(item[1])
        temp['name'] = str(item[1])
        temp['date'] = str(item[0])
        temp['user'] = str(item[4])
        temp['price'] = '$' + str(item[2])
        design.append(temp)
    print design
    return render_template("designer_order.html", design=design)


def get_all_success_scheme_byid(id):
    designer = Designer.query.filter_by(DesignerID=id).first()
    schemes = None
    if designer:
        schemes = db.session.execute(
            "select SubmitTime,DesignScheme.SchemeID,SchemePrice,SchemeDESC,UserName from DesignScheme, CompetitiveBid, DecorationForm, User where "
            "DesignScheme.SchemeID=CompetitiveBid.SchemeID and CompetitiveBid.DcFormID=DecorationForm.DcFormID "
            " and DecorationForm.ConsumerID = User.UserID and DesignScheme.DesignerID=%d" % id)
        for item in schemes:
            print item
        print schemes
        return schemes
    return None


def get_all_succeed_order(id):
    user = User.query.filter_by(UserID=id).first()
    if user and user.UserType:
        order_forms = OrderForm.query.filter_by(UserID=user.UserID, OrderFormState="Success").all()
        return user, order_forms
    return None, None


@designer_.route("/add_scheme", methods=['GET', 'POST'])
@login_required
def designer_add_scheme():
    return


def insert_design_scheme(did, desc, img):
    # have encode
    scheme = DesignScheme(DesignerID=did, SchemeDESC=desc, SchemeImage=img)
    db.session.add(scheme)
    db.session.commit()


# Test ed
@designer_.route("/scheme/<id>", methods=['GET', 'POST'])
def designer_scheme(id):
    g.user = User.query.filter_by(UserID=2).first()
    class Scheme():
        def __init__(self):
            self.id = "id_test"
            self.description = "des_test"
            self.designer_id = "43248329"

    class Commen():
        def __init__(self):
            self.name = "name_test"
            self.time = "2013._date"
            self.content = "is wrong"
            self.img = "/static/img/client/1.jpg"

    class De():
        def __init__(self):
            self.name = "jj"
            self.img = "/static/img/client/1.jpg"

    designer = De()
    scheme_imgs = []
    scheme = Scheme()
    comment = Commen()
    comments = [comment]
    designscheme = DesignScheme.query.filter_by(SchemeID=int(id)).first()
    scheme.id = id
    scheme.description = designscheme.SchemeDESC
    cpath = 'app/static/img/scheme/' + id + '.jpg'
    cpath_img = '/static/img/scheme/' + id + '.jpg'
    with open(cpath, "wb") as f:
        f.write(base64.b64decode(designscheme.SchemeImage))
        f.close()
    scheme_imgs.append(cpath_img)
    if designscheme.DesignerID != None:
        user = User.query.filter_by(UserID=designscheme.DesignerID).first()
        scheme.designer_id = designscheme.DesignerID
    else:
        user = User.query.filter_by(UserID=designscheme.CompanyID).first()
        scheme.designer_id = designscheme.CompanyID
    cpath = 'app/static/img/client/' + str(user.UserID) + '.jpg'
    cpath_img = '/static/img/client/' + str(user.UserID) + '.jpg'
    with open(cpath, "wb") as f:
        f.write(base64.b64decode(user.UserImage))
        f.close()
    designer.name = user.UserName
    designer.img = cpath_img
    return render_template('scheme.html', scheme=scheme, comments=comments, scheme_imgs=scheme_imgs, designer=designer)

