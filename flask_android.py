#-*- coding:utf8 -*-
#encoding=utf-8
from flask import Flask,request,jsonify
import werkzeug
import datetime
import os



UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)),'affe_demos_uploads')

app = Flask(__name__,static_folder='static')
app.config['STATIC_FOLDER'] = UPLOAD_FOLDER
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
    for i in range(1,5):
        info=dict()
        info['id']=i
        info['label']='label:'+str(i)
        info['confidence']=float(i)
        array.append(info)
    jsonobject['arrayList']=array
    return jsonify(jsonobject)
@app.route('/query', methods=['GET'])
def query():
    ret = dict()
    ret['bValidate']= 0
    print str(ret)
    id_=request.args.get('id','0',type=str)
    if id_ is -1:
        print u'请求格式错误（如没有id）'
        return jsonify(ret)
    retsult='1'
    if retsult is None:
       print u'无数据'
       return jsonify(ret)
    ret['bValidate'] = 1
    ret['id']=retsult.id
    ret['name']=retsult.iedname
    ret['type']=retsult.iedtype
    ret['url']='static/img/test.jpg'
    ret['details']=u'手榴弹是一种能攻能防的小型手投弹药，也是使用较广、用量较大的弹药。它既能杀伤有生目标，又能破坏坦克和装甲车辆。手榴弹由于体积小、质量小，携带、使用方便，曾在历次战争中发挥过重要作用。'
    print '=============================================================='
    #print str(retsult.id), retsult.iedname, retsult.iedtype, retsult.ied_image_file, retsult.ied_video_file
    print ret
    return jsonify(ret)
if __name__ == '__main__':
    app.static_folder=UPLOAD_FOLDER
    app.run(debug=True,host='0.0.0.0')
