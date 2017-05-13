#-*- coding:utf8 -*-
#encoding=utf-8
from flask import Flask,request,jsonify
import werkzeug
import datetime
import os
from flask_sqlalchemy import SQLAlchemy


UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)),'affe_demos_uploads')

app = Flask(__name__,static_folder='static')
app.config['STATIC_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI']='mysql://zhuangwu:zhuangwu@localhost/flask_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db=SQLAlchemy(app)
class Edtz(db.Model):
    __tablename__ = 'ed_t_edtz'
    edbh=db.Column(db.String(40),primary_key=True)
    tzmc=db.Column(db.String(200),nullable=True)
    tznr=db.Column(db.String(2000),nullable=True)
    edlx=db.Column(db.String(20),nullable=False)
    ms=db.Column(db.String(2000),nullable=True)
    zdr=db.Column(db.String(200),nullable=True)
    zdsj=db.Column(db.Date,nullable=True)
    tzbh=db.Column(db.String(40),nullable=False)
    @staticmethod
    def add(edtz):
        db.session.add(edtz)
        db.session.commit()
class Ied(db.Model):
    __tablename__='ed_t_ied'
    bh=db.Column(db.String(20),primary_key=True)
    lx=db.Column(db.String(2),primary_key=True)
    mc=db.Column(db.String(20),nullable=True)
    tx=db.Column(db.String(200),nullable=True)
    zylx=db.Column(db.String(200),nullable=True)
    qbfs=db.Column(db.String(200),nullable=True)
    hgp=db.Column(db.String(200),nullable=True)
    fhjl=db.Column(db.String(200),nullable=True)
    wlpg=db.Column(db.String(200),nullable=True)
    bz=db.Column(db.String(200),nullable=True)
    ms=db.Column(db.String(200),nullable=True)
    tp1=db.Column(db.String(200),nullable=True)
    tp2=db.Column(db.String(200),nullable=True)
    tp3=db.Column(db.String(200),nullable=True)
    sp1=db.Column(db.String(200),nullable=True)
    sp2=db.Column(db.String(200),nullable=True)
    sp3=db.Column(db.String(200),nullable=True)
    czcl=db.Column(db.String(200),nullable=True)
    pbqc=db.Column(db.String(200),nullable=True)
    @staticmethod
    def add(ied):
        db.session.add(ied)
        db.session.commit()
@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/classify_upload_new',methods=['POST'])
def classify_upload_new():
    try:
        imagefile=request.files['imagefile']
        filename_=str(datetime.datetime.now()).replace(' ','_').replace(':','_').replace('.','_')+"_"+werkzeug.secure_filename(imagefile.filename)
        print('========>filename'+filename_)
        filename=os.path.join(UPLOAD_FOLDER,filename_)
        print ('===>filename'+str(filename))
        imagefile.save(filename)
    except Exception as err:
        print err
    array=[]
    jsonobject=dict()
    jsonobject['time']='0.3'
    jsonobject['errorMsg']='success'
    ieds=Ied.query.all()[:5]
    i=0;
    for ied in ieds:
        info=dict()
        info['id']=ied.bh
        info['label']='label:'+ied.mc
        info['confidence']=float(i)
        array.append(info)
        i+=1
    jsonobject['arrayList']=array
    return jsonify(jsonobject)
@app.route('/query', methods=['GET'])
def query():
    ret = dict()
    ret['bValidate']= 0
    print str(ret)
    id_=request.args.get('id','0',type=str)
    ied=Ied.query.filter_by(bh=id_).first()
    if ied is None:
       print u'无数据'
       return jsonify(ret)
    ret['bValidate'] = 1
    ret['bh']=ied.bh
    ret['mc']=ied.mc
    ret['url']=ied.tp1
    ret['ms']=ied.ms
    ret['czcl']=ied.czcl
    print '=============================================================='
    #print str(retsult.id), retsult.iedname, retsult.iedtype, retsult.ied_image_file, retsult.ied_video_file
    print ret
    return jsonify(ret)
if __name__ == '__main__':
    app.static_folder=UPLOAD_FOLDER
    app.run(debug=True,host='0.0.0.0')
