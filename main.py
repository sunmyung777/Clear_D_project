import os
from flask import Flask,render_template,request,url_for,send_file,make_response
from werkzeug.utils import secure_filename
import cv2
import numpy as np
from PIL import Image
import shutil
import zipfile

UPLOAD_FOLDER = 'C:/Users/user/Desktop/python/gong/images'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app=Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'helloworld'
app.config['SESSION_TYPE'] = 'filesystem'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/',methods=['GET','POST'])
def main():
    if(request.method=='GET'):
        return render_template('main.html')
    if(request.method=='POST'):
        if not os.path.exists('check'):
            os.makedirs('check')
        if not os.path.exists('images'):
            os.makedirs('images')
        files_list=request.files.getlist('file')
        for files in files_list:
            if files and allowed_file(files.filename):
                filename = secure_filename(files.filename)
                files.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        newfiles=[]
        for files in files_list:
            newfiles+=[files.filename.replace('/','_')]
        return check(newfiles)

@app.route('/check')
def check(files_list):
    
    lists=[]
    
    for i in range(0,len(files_list)):
        a=cv2.imread('C:/Users/user/Desktop/python/gong/images/'+files_list[i],cv2.IMREAD_GRAYSCALE)
        dst1 = cv2.resize(a, dsize=(300, 300), interpolation=cv2.INTER_AREA)
        lists.append(files_list[i])
        for j in range(0,i):
            b=cv2.imread('C:/Users/user/Desktop/python/gong/images/'+files_list[j],cv2.IMREAD_GRAYSCALE)
            dst2 = cv2.resize(b, dsize=(300, 300), interpolation=cv2.INTER_AREA)
            
            if(np.sum(dst1-dst2)==0):
                lists.remove(files_list[i])
                break

    for obj in lists:
        im = Image.open('C:/Users/user/Desktop/python/gong/images/'+obj)
        im.save('C:/Users/user/Desktop/python/gong/check/'+obj)

    zips = zipfile.ZipFile('C:/Users/user/Desktop/python/gong/sort.zip', 'w')

    for folder, subfolders, files in os.walk('C:/Users/user/Desktop/python/gong/check'):
        for file in files:
            zips.write(os.path.join(folder, file), os.path.relpath(os.path.join(folder,file), 'C:/Users/user/Desktop/python/gong/check'), compress_type = zipfile.ZIP_DEFLATED)
    
    zips.close()
    
    shutil.rmtree('images')
    shutil.rmtree('check')

    return render_template('check.html')

@app.route('/download')
def download():
    return send_file('C:/Users/user/Desktop/python/gong/sort.zip', as_attachment=True,attachment_filename='sort.zip')
if __name__ == "__main__":
    app.run(debug=True,port=5000)

