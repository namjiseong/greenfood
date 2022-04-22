from tabnanny import filename_only
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import pymysql
import os
import detect



conn = pymysql.connect(host='localhost', user="root", password="qsdrwe159", db='food_data', charset='utf8')




app = Flask(__name__)


UPLOAD_FOLDER = './static/images'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/', methods=('GET', 'POST')) # 접속하는 url
def index():
    
    
    
    if request.method == "POST":
        curs = conn.cursor()
        Img = request.files['file']
        Img.save(os.path.join(app.config['UPLOAD_FOLDER'], Img.filename))  # 이미지 서버에 저장
        
        f = open('./food_name.txt', 'w', encoding="UTF-8")
        f.close()
        
        detect.run(source='./static/images/' + Img.filename, weights="./best.pt", save_txt=True) # 음식 객체 인식
        
        f = open('./food_name.txt', 'r', encoding="UTF-8")
        lines = f.readlines()
        
        kal = []
        tan = []
        dan = []
        ji = []
        food_list = []
        for i in lines:
            i= i.strip()
            print('i='+i)
            sql="select * from food_data where 음식명=\'" + i + "\';"
            conn.ping()
            curs.execute(sql)
            
            rows = curs.fetchall()
            print(rows[0])
            kal.append(rows[0][5])
            tan.append(rows[0][6])
            dan.append(rows[0][7])
            ji.append(rows[0][8])
            food_list.append(rows[0][4])
        #conn.close()
            
        f.close()
        
        drt = os.listdir('./runs/detect')[-1] # 사진 출력하는 과정
        file_source = './runs/detect/' + drt +'/'+ Img.filename
        file_destination = './static/images/' 
        os.replace(file_source, file_destination + Img.filename)
        
        
        # 여기서 DB 정보 가공 후 넘기기
        # 총 칼로리 : 2300 탄수화물 : 324 단백질 : 55 지방 : 54  / 나트륨 2000 당류 : 100 
        kal_p = int(round(sum(kal)/2300, 2) * 100)
        print(kal_p)
        tan_p = int(round(sum(tan)/324, 2) * 100)
        print(tan_p)
        dan_p = int(round(sum(dan)/55, 2) * 100)
        print(dan_p)
        ji_p = int(round(sum(ji)/54, 2) * 100)
        print(ji_p)
        
        return render_template('result.html', Img = 'images/'+Img.filename, kal=kal_p, tan=tan_p, dan=dan_p, ji=ji_p, food_list = food_list, kal_list = kal, tan_list=tan, dan_list=dan, ji_list=ji)
        ###
    
        
      
    return render_template('index.html')
  
  
  
  
@app.route('/result') # 접속하는 url
def result():
    return render_template('result.html')
if __name__ == '__main__':
    

    
    app.run()
    
