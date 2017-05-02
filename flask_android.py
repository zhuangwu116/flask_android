from flask import Flask,request,jsonify
import werkzeug
import datetime
import os

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)),'affe_demos_uploads')
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
if __name__ == '__main__':
    app.run(host='0.0.0.0')
