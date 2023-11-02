from flask import Flask, render_template
import mysql.connector
import pandas as pd

app = Flask(__name__, template_folder='templates')  # 템플릿 디렉토리를 설정


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

@app.route('/predicted_data')
def show_predicted_data():
    # SQL 쿼리 실행
    cursor.execute("SELECT * FROM predicted ORDER BY basDt DESC LIMIT 11;")
    data = cursor.fetchall()
    
    return render_template('predicted_table.html', data=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
