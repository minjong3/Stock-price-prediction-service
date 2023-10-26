from flask import Flask
import mysql.connector
import pandas as pd

app = Flask(__name__)

# MySQL 연결 설정
db_config = {
"host": "172.31.13.248",
"user": "stock_user",
"password": "1234asde",
"database": "realdb"
}

conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()
# 연결이 제대로 설정되었는지 확인
if conn.is_connected():
    print("MySQL 데이터베이스에 연결되었습니다.")
else:
    print("MySQL 데이터베이스에 연결에 실패했습니다.")

# Flask 애플리케이션 엔드포인트
@app.route('/')
def get_all_data():
    query = "SELECT * FROM stocks WHERE itmsNm = '삼성전자' AND basDt = '2023-10-17';"
    cursor.execute(query)
    data = cursor.fetchall()

    columns = [column[0] for column in cursor.description]
    df = pd.DataFrame(data, columns=columns)  # 데이터를 데이터 프레임으로 변환

    text_data = df.to_string(index=False)  # 데이터 프레임을 문자열로 변환
    return text_data

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
