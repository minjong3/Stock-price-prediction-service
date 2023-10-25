import time
import pandas as pd
import requests
import mysql.connector
from datetime import date
import json

# MySQL 연결 설정
db_config = {
"host": "localhost",
"user": "stock_user",
"password": "1234asde",
"database": "realdb"
}

conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

# 데이터 가져오는 코드 추가
headers = {'Content-Type': 'application/json', 'charset': 'UTF-8', 'Accept': '*/*'}
url = "https://apis.data.go.kr/1160100/service/GetStockSecuritiesInfoService/getStockPriceInfo"

key = '9+xsULVVtkmcT9/of4fUpyEz4wLCUNLexYSxxX1KI8yeVtKaNIw2698qQ+ymG5I1ibMzd3nN7AZkA/r2brLmVg=='
# 원하는 항목들을 리스트로 정의
items = ['삼성전자', 'SK하이닉스', '삼성바이오로직스', '삼성SDI',
        'LG화학', '현대차', 'NAVER', '카카오', 'KB금융', '현대모비스', '셀트리온']

for i in items:
    # 항목들을 쉼표로 구분된 문자열로 변환
    

    # params에 itmsNm을 추가
    params = {
        'serviceKey': key,
        'numOfRows': 10000,
        'pageNo': 1,
        'resultType': 'json',
        'beginBasDt': '20200101',
        'itmsNm': i  # itmsNm을 문자열로 전달
    }
    
    
    df = pd.DataFrame()
    temp_df = pd.DataFrame()
# 첫 번째 페이지 데이터를 가져와서 DataFrame으로 변환
    errorCount = 1
    total_count = 0
    #while errorCount <= 10 :
        # try:
        #     print("test")
    response = requests.get(url=url, headers=headers, params=params)
    total_count = response.json()['response']['body']['totalCount']
    api_data = response.json()["response"]["body"]["items"]["item"]
    df = pd.DataFrame(api_data)
        #     break
        # except Exception:
        #     errorCount = 11
        #     sleep(5)
        #     break
                        
        # 다음 페이지 데이터를 반복적으로 가져와서 DataFrame에 추가
    if total_count > params['numOfRows']:
        for i in range(2,total_count//10000+1):
            params['pageNo'] = i
            errorCount = 1
            while errorCount <= 10 :
                try:
                    response = requests.get(url=url, headers=headers, params=params)
                    data = response.json()["response"]["body"]["items"]["item"]
                    temp_df = pd.DataFrame(data)
                    df = pd.concat([df, temp_df], ignore_index=True)
                    print('123')
                    break
                except requests.exceptions.JSONDecodeError:
                    time.sleep(5)
                    print(f'error:{errorCount}')
                except Exception:
                    errorCount = 11
                    break
                    
            time.sleep(1)


    # 데이터프레임을 리스트 딕셔너리로 변환
    data_list = df.to_dict(orient='records')

    # 데이터베이스에 데이터 삽입 또는 업데이트
    for data in data_list:
        srtnCd = data['srtnCd']
        insert_query = """
            INSERT INTO stocks (srtnCd, isinCd, itmsNm, lstgStCnt, mrktTotAmt, basDt, trqu, trPrc, clpr, vs, fltRt, mkp, hipr, lopr)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
            isinCd = VALUES(isinCd),
            itmsNm = VALUES(itmsNm),
            lstgStCnt = VALUES(lstgStCnt),
            mrktTotAmt = VALUES(mrktTotAmt),
            basDt = VALUES(basDt),
            trqu = VALUES(trqu),
            trPrc = VALUES(trPrc),
            clpr = VALUES(clpr),
            vs = VALUES(vs),
            fltRt = VALUES(fltRt),
            mkp = VALUES(mkp),
            hipr = VALUES(hipr),
            lopr = VALUES(lopr)
        """
        values = (data['srtnCd'], data['isinCd'], data['itmsNm'], data['lstgStCnt'], data['mrktTotAmt'], data['basDt'],data['trqu'], data['trPrc'], data['clpr'], data['vs'], data['fltRt'], data['mkp'], data['hipr'], data['lopr'])
        cursor.execute(insert_query, values)

    conn.commit()  # 데이터베이스에 변경 내용 저장

cursor.close()
conn.close()