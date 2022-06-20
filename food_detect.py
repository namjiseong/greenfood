import pymysql
import detect
import detect2
import random
import os
#DB선언
conn = pymysql.connect(host='jiseongdb.cthzjzmgoiad.ap-northeast-2.rds.amazonaws.com', user="admin", password="qsdrwe159", db='food_data', charset='utf8')



    
def boxbox(Img):
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
    
    answer = [food_list, kal, tan, dan, ji]
    return answer