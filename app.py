from tabnanny import filename_only
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import pymysql
import os
conn = pymysql.connect(host='localhost', user="root", password="qsdrwe159", db='food_data', charset='utf8')


curs = conn.cursor()



app = Flask(__name__)


UPLOAD_FOLDER = './static/images'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/', methods=('GET', 'POST')) # 접속하는 url
def index():
    
    #sql="select * from food"
    #curs.execute(sql)
    #rows = curs.fetchall()
    #print(rows)
    #conn.close()
    
    if request.method == "POST":
        
        Img = request.files['file']
        Img.save(os.path.join(app.config['UPLOAD_FOLDER'], Img.filename))  # 이미지 서버에 저장
        
        
        
        
        return render_template('result.html', Img = 'images/'+Img.filename)
        ###
        
      
    return render_template('index.html')
  
  
  
  
@app.route('/result') # 접속하는 url
def result():
    return render_template('result.html')
if __name__ == '__main__':
    app.run()