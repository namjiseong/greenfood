from msilib.schema import Environment
from tabnanny import filename_only
from flask import Flask, render_template, request, flash, jsonify
from werkzeug.utils import secure_filename
import pymysql
import os
import detect
import detect2
import random
import food_detect
from datetime import datetime
import json
import joblib
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import numpy as np

#DB선언
conn = pymysql.connect(host='localhost', user="root", password="qsdrwe159", db='food_data', charset='utf8')


app = Flask(__name__)
app.secret_key = '1234'
UPLOAD_FOLDER = './static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['id'] = ""


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
            p_list[i] = 66 - p_list[i]
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
        id = request.form['userId']
        pw = request.form['userPw']
        curs = conn.cursor()
        sql="select * from user where id=\'"+id+"\';"
        conn.ping()
        curs.execute(sql)
        rows = curs.fetchall()
        if len(rows) > 0:
            if rows[0][1] == pw:
                print('로그인 성공')
                flash('로그인 성공')
                app.config['id'] = id
                return render_template('index.html')
        else:
            print('로그인 실패')
            flash('로그인 실패')
        return render_template('login.html')
        
        
    return render_template('login.html')
@app.route('/join', methods=('GET', 'POST')) # 접속하는 url
def join():
    if request.method == "POST":
        # 회원 아이디 비번 DB에 저장
        id = request.form['userId']
        pw = request.form['userPw']
        print(id, pw)
        curs = conn.cursor()
        sql="insert into user values( \'" + id + "\', \'" + pw + "\' );"
        
        
        conn.ping()
        curs.execute(sql)
        conn.commit() # 실제 DB에 적용
        
        return render_template('index.html')
    return render_template('join.html')




@app.route('/statistic', methods=('GET', 'POST')) # 접속하는 url
def statistic():
    
    if app.config['id']:
        print(app.config['id'])
        curs = conn.cursor()
        
        if request.method == "POST":
            print(request.form['date'])
            # DB에서 찾아서 json으로 리턴
            box = []
            
            sql="select food_name, count from date_food where now_id=\'"+app.config['id']+"\' and  date_time=\'"+request.form['date']+"\';"
            sql = "select food_name, count, 칼로리, 탄수화물, 단백질, 지방 FROM date_food, food_data where now_id=\'"+app.config['id']+"\' and  date_time=\'"+request.form['date']+"\' and date_food.food_name=food_data.음식명;"
            conn.ping()
            curs.execute(sql)
            rows = curs.fetchall()
            
            return  jsonify(rows)
        
        sql = "select sum(count * 칼로리) as 칼로리_, sum(count * 탄수화물) as 탄수화물_ , sum(count*단백질) as 단백질_, sum(count * 지방) as 지방_ , sum(count * 나트륨) as 나트륨_ , sum(count * 콜레스테롤) as 콜레스테롤_, sum(count * 포화지방산) as 포화지방산_ , sum(count * 총당류) as 총당류_, sum(count * 칼륨) as 칼륨_, sum(count * 칼슘) as 칼슘_ FROM date_food, food_data where now_id=\'"+app.config['id']+"\' and date_food.food_name=food_data.음식명;"
        conn.ping() # 
        curs.execute(sql)
        rows = curs.fetchall()
        print(rows)
        sum_kal = 0
        sum_tan = 0
        sum_dan = 0
        sum_ji = 0
        if len(rows) > 0:
            sum_kal = rows[0][0]
            sum_tan = rows[0][1]
            sum_dan = rows[0][2]
            sum_ji = rows[0][3]
            sum_na = rows[0][4]
            sum_col = rows[0][5]
            sum_fo = rows[0][6]
            sum_dag = rows[0][7]
            sum_kr = rows[0][8]
            sum_ks = rows[0][9]
        sql = "select count(*) from date_food where now_id=\'"+app.config['id']+"\'group by date_time;"
        conn.ping()
        curs.execute(sql)
        rows = curs.fetchall()    
        divi = len(rows)
        avg_kal = sum_kal/divi
        avg_tan = sum_tan/divi
        avg_dan = sum_dan/divi
        avg_ji = sum_ji/divi
        avg_na = sum_na/divi
        avg_col = sum_col/divi
        avg_fo = sum_fo/divi
        avg_dag = sum_dag/divi
        avg_kr = sum_kr/divi
        avg_ks = sum_ks/divi
        
        test = [avg_kal, avg_tan, avg_dan, avg_ji, avg_na, avg_col, avg_fo, avg_dag, avg_kr, avg_ks]
        test = pd.DataFrame(data = [(avg_kal, avg_tan, avg_dan, avg_ji, avg_na, avg_col, avg_fo, avg_dag, avg_kr, avg_ks)])
        
        # 미리 진단 하고 결과만 보내놓기
        #####
        go_model = joblib.load('./go_rpmodel.pkl')
        be_model = joblib.load('./be_rpmodel.pkl')
        dag_model = joblib.load('./dag_rpmodel.pkl')
        go_p = go_model.predict_proba(test)
        be_p = be_model.predict_proba(test)
        dag_p = dag_model.predict_proba(test)
        per = [int(go_p[0][1] * 100), int(be_p[0][1] * 100), int(dag_p[0][1] * 100)]
        
        
        return render_template('statistic.html', avg_kal = avg_kal, avg_tan = avg_tan, avg_dan = avg_dan, avg_ji = avg_ji, per = per)
    else:
        flash('로그인이 필요합니다')
        return render_template('index.html')

@app.route('/date_add', methods=('GET', 'POST')) # 접속하는 url
def date_add():
    
    date_food = request.form['date_food']
    date_count = request.form['date_count']
    date_food_list = list(date_food.split())
    date_count_list = list(date_count.split())
    print(date_food_list)
    print(date_count_list)
    for i in range(len(date_food_list)):
        
        #DB에 저장
        curs = conn.cursor()
        sql="insert into date_food values(\'"+app.config['id']+"\', \'"+ datetime.today().strftime("%Y-%m-%d") +"\', \'"+date_food_list[i]+"\', "+date_count_list[i]+");"
        
        
        conn.ping()
        curs.execute(sql)
        conn.commit() # 실제 DB에 적용
    
    flash('통계 저장 성공')
    return render_template('index.html')


@app.route('/test', methods=('GET', 'POST')) # 접속하는 url
def test():
    if request.method == "POST":
        print(request.form['per_list'])
        go, be, dag = map(int, request.form['per_list'].split(","))
        print(request.form['avg_list'])
        avg_kal, avg_tan, avg_dan, avg_ji = map(float, request.form['avg_list'].split(','))
        return render_template('test.html', avg_kal = avg_kal, avg_tan = avg_tan, avg_dan = avg_dan, avg_ji = avg_ji, go=go, be=be, dag=dag)
    return render_template('test.html')

if __name__ == '__main__':
    
    
    app.run(host='0.0.0.0',port=5000)
    #app.run()
    
    #set FLASK_APP=app
    #set FLASK_ENV=development
    # ngrok.exe http 5000
    #ssl_context='adhoc'

