from msilib.schema import Environment
from tabnanny import filename_only
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import pymysql
import os
import detect
import detect2
import random
import food_detect
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
        
        answer = food_detect.boxbox(Img)
        
        return render_template('result.html', Img = 'images/'+Img.filename, food_list = answer[0], kal_list = answer[1], tan_list=answer[2], dan_list=answer[3], ji_list=answer[4])
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

@app.route('/recommend', methods=['POST']) # 접속하는 url
def recommend():
    if request.method == "POST":
        p_list = request.form['p_list']
        p_list = list(map(int, p_list.split()))
        for i in range(len(p_list)):
            p_list[i] = 33 - p_list[i]
            # 33기준으로 퍼센트 변환
        # 칼로리 1% = 23 탄수화물 1% =3.24 단백질 1% = 0.55 지방 1% = 0.54
        p_list[0] = p_list[0] * 23
        p_list[1] = p_list[1] * 3.24
        p_list[2] = p_list[2] * 0.55
        p_list[3] = p_list[3] * 0.54
        # 실제 값으로 변경 완료
        print(p_list)
        for i in range(len(p_list)):
            p_list[i] = str(p_list[i])
        # DB 검색
        curs = conn.cursor()

        sql="select * from food_data where 칼로리<=\'"+p_list[0]+"\' and 탄수화물<=\'"+p_list[1]+"\' and 단백질<=\'"+p_list[2]+"\' and 지방<=\'"+p_list[3]+"\';"
        conn.ping()
        curs.execute(sql)
            
        rows = curs.fetchall()
        
        reco = list(rows)
        if len(reco) > 0:
            
            random.shuffle(reco)
            print(reco[0][4])
            return render_template('comfirm.html', food_name = reco[0][4])
    return render_template('comfirm.html')

@app.route('/login', methods=('GET', 'POST')) # 접속하는 url
def login():
    if request.method == "POST":
        
        # 아이디 확인 후 로그인 과정
        
        return render_template('index.html')
        
        
    return render_template('login.html')
@app.route('/join', methods=['GET']) # 접속하는 url
def join():
    return render_template('join.html')
@app.route('/statistic', methods=['GET']) # 접속하는 url
def statistic():
    return render_template('statistic.html')



if __name__ == '__main__':
    
    
    app.run(host='0.0.0.0',port=5000)
    #app.run()
    
    #set FLASK_APP=app
    #set FLASK_ENV=development
    # ngrok.exe http 5000
    #ssl_context='adhoc'

