from tabnanny import filename_only
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import pymysql
import os
import detect
import detect2

#DB선언
conn = pymysql.connect(host='localhost', user="root", password="qsdrwe159", db='food_data', charset='utf8')


app = Flask(__name__)
UPLOAD_FOLDER = './static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 홈페이지
@app.route('/', methods=('GET', 'POST')) # 접속하는 url
def index():
    
    # 사진 파일 업로드 시 실행
    if request.method == "POST":
        
        Img = request.files['file']
        Img.save(os.path.join(app.config['UPLOAD_FOLDER'], Img.filename))  # 이미지 서버에 저장
        file_name = 'images/'+Img.filename
        # 음식 리스트 저장 파일 초기화
        f = open('./food_name.txt', 'w', encoding="UTF-8")
        f.close()
        
        # 모델 실행
        detect.run(source='./static/images/' + Img.filename, weights="./best.pt", save_txt=True) # 음식 객체 인식
        # 인식된 음식 리스트 저장
        f = open('./food_name.txt', 'r', encoding="UTF-8")
        lines2 = f.readlines()
        f.close()
        # 검색된 이미지 경로 이동
        drt = os.listdir('./runs/detect')[-1] # 사진 출력하는 과정
        file_source = './runs/detect/' + drt +'/'+ Img.filename
        file_destination = './static/images/' 
        os.replace(file_source, file_destination + Img.filename)
        # 2번째 모델 - 밥, 김치, 국 위주 실행
        detect2.run(source='./static/images/' + Img.filename, weights="./v2_pt.pt", save_txt=True) # 음식 객체 인식
        # 검색된 이미지 경로 이동
        drt = os.listdir('./runs/detect')[-1] # 사진 출력하는 과정
        file_source = './runs/detect/' + drt +'/'+ Img.filename
        file_destination = './static/images/' 
        os.replace(file_source, file_destination + Img.filename)
        # 인식된 음식 리스트 저장
        f = open('./food_name.txt', 'r', encoding="UTF-8")
        lines = f.readlines()
        f.close()
        # 2 모델 리스트 합
        lines = lines + lines2
        
        kal = []
        tan = []
        dan = []
        ji = []
        food_list = []
        
        temp = set()
        # 중복 제거
        for i in lines:
            i = i.strip()
            if i not in temp:
                temp.add(i)
        curs = conn.cursor()
        # DB 검색
        for i in temp:
            i= i.strip()
            
            sql="select * from food_data where 음식명=\'" + i + "\';"
            conn.ping()
            curs.execute(sql)
            
            rows = curs.fetchall()
            if len(rows) > 0:
                print(rows[0])
                kal.append(rows[0][5])
                tan.append(rows[0][6])
                dan.append(rows[0][7])
                ji.append(rows[0][8])
                food_list.append(rows[0][4])
                
        #conn.close()
            
        
        return render_template('result.html', Img = 'images/'+Img.filename, food_list = food_list, kal_list = kal, tan_list=tan, dan_list=dan, ji_list=ji)
        ###
    
        
      
    return render_template('index.html')
  
  
  
  
@app.route('/result') # 접속하는 url
def result():
    return render_template('result.html')

@app.route('/add', methods=['POST']) # 접속하는 url
def add():
    
    if request.method == "POST":
        food_name = request.form['food_name']
        food_list = request.form['food_list']
        Img = request.form['image']
        print(Img)
        lines = food_list.split()
        lines.append(food_name)
        print(lines)
        kal = []
        tan = []
        dan = []
        ji = []
        food_list = []
        
        temp = set()
        # 중복 제거
        for i in lines:
            i = i.strip()
            if i not in temp:
                
                temp.add(i)
        # DB 검색
        curs = conn.cursor()
        for i in temp:
            i= i.strip()
            
            sql="select * from food_data where 음식명=\'" + i + "\';"
            conn.ping()
            curs.execute(sql)
            
            rows = curs.fetchall()
            if len(rows) > 0:
                print(rows[0])
                kal.append(rows[0][5])
                tan.append(rows[0][6])
                dan.append(rows[0][7])
                ji.append(rows[0][8])
                food_list.append(rows[0][4])
        
        
        return render_template('result.html', Img =Img, food_list = food_list, kal_list = kal, tan_list=tan, dan_list=dan, ji_list=ji)



if __name__ == '__main__':
    

    app.run(host='0.0.0.0',port=5000)
    #app.run()
    
    #set FLASK_APP=app
    #set FLASK_ENV=development
    # ngrok.exe http 5000

