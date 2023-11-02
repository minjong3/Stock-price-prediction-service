import numpy as np
import pandas as pd
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.optimizers import Adam
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import mysql.connector
from datetime import datetime, timedelta
from airflow.models import Variable

def connect_to_database():
    
    mysql_pw = Variable.get("mysql_pw")
    
    db_config = {
        "host": "172.31.13.248",
        "user": "stock_user",
        "password": mysql_pw,
        "database": "realdb"
    }

    # 데이터베이스 연결
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    
        # 연결이 제대로 설정되었는지 확인
    if conn.is_connected():
        print("MySQL 데이터베이스에 연결되었습니다.")
    else:
        print("MySQL 데이터베이스에 연결에 실패했습니다.")
        
    return conn, cursor

def insert_prediction_to_db(conn, cursor, stock_name, prediction_date, predicted_open):
    try:
        # 현재 날짜 계산
        today = datetime.now().date()
        
        # 예측하려는 날짜 계산 (예를 들어, 다음날 날짜로 설정)
        prediction_date = today + timedelta(days=1)
        
        # 데이터베이스에 삽입할 데이터 준비
        insert_query = "INSERT INTO predicted (basDt, itmsNm, predicted_mkp) VALUES (%s, %s, %s)"
        data = (prediction_date, stock_name, predicted_open)
        
        # 데이터 삽입
        cursor.execute(insert_query, data)
        conn.commit()
        
    except Exception as e:
        print(f"데이터베이스에 데이터를 삽입하는 중 오류 발생: {e}")
        
mysql_pw = Variable.get("mysql_pw")
        
# MySQL 데이터베이스 연결 설정
db_config = {
    "host": "172.31.13.248",
    "user": "stock_user",
    "password": mysql_pw,
    "database": "realdb"
}

# 데이터베이스 연결
conn = mysql.connector.connect(**db_config)

# 데이터를 가져올 쿼리
query = """
SELECT *
FROM stocks
"""

# 쿼리 실행 및 결과를 데이터 프레임으로 읽기
df = pd.read_sql(query, conn)

# 연결 닫기
conn.close()

# 불필요한 열 삭제
df.drop(['srtnCd', 'isinCd', 'lstgStCnt', 'mrktTotAmt', 'trPrc', 'vs', 'fltRt'], axis=1, inplace=True)

# 열 이름 변경
df.rename(columns={'basDt': '일자', 'itmsNm': '종목', 'clpr': '종가', 'mkp': '시가', 
                   'hipr': '고가', 'lopr': '저가', 'trqu': '거래량'}, inplace=True)


grouped_data = df.groupby('종목')
individual_dfs = {}  # 종목별 DataFrame을 저장할 딕셔너리

for name, group in grouped_data:
    individual_dfs[name] = group

# 결과 저장을 위한 딕셔너리
results = {}

# 모든 종목에 대해 루프 실행
for stock_name, data in grouped_data:
    # 데이터프레임 선택
    dates = data['일자']
    cols = list(data)[3:8]
    stock_data = data[cols].astype(float)
    
    # 데이터 정규화
    scaler = StandardScaler()
    scaler = scaler.fit(stock_data)
    stock_data_scaled = scaler.transform(stock_data)
    
    # 학습 데이터와 테스트 데이터 분리
    n_train = int(0.9 * stock_data_scaled.shape[0])
    train_data_scaled = stock_data_scaled[0:n_train]
    train_dates = dates[0:n_train]

    test_data_scaled = stock_data_scaled[n_train:]
    test_dates = dates[n_train:]
    
    # LSTM 입력 데이터 준비
    pred_days = 1
    seq_len = 14
    input_dim = 5

    trainX = []
    trainY = []
    testX = []
    testY = []

    for i in range(seq_len, n_train - pred_days + 1):
        trainX.append(train_data_scaled[i - seq_len:i, 0:train_data_scaled.shape[1]])
        trainY.append(train_data_scaled[i + pred_days - 1:i + pred_days, 0])

    for i in range(seq_len, len(test_data_scaled) - pred_days + 1):
        testX.append(test_data_scaled[i - seq_len:i, 0:test_data_scaled.shape[1]])
        testY.append(test_data_scaled[i + pred_days - 1:i + pred_days, 0])

    trainX, trainY = np.array(trainX), np.array(trainY)
    testX, testY = np.array(testX), np.array(testY)
    # LSTM 모델 정의
    model = Sequential()
    model.add(LSTM(64, input_shape=(trainX.shape[1], trainX.shape[2]), return_sequences=True))
    model.add(LSTM(32, return_sequences=False))
    model.add(Dense(trainY.shape[1]))

    # 학습률 지정
    learning_rate = 0.01
    optimizer = Adam(learning_rate=learning_rate)

    # 모델 컴파일
    model.compile(optimizer=optimizer, loss='mse')


    history = model.fit(trainX, trainY, epochs=30, batch_size=32, validation_split=0.1, verbose=1)


    # Prediction
    prediction = model.predict(testX)

    # Generate array filled with means for prediction
    mean_values_pred = np.repeat(scaler.mean_[np.newaxis, :], prediction.shape[0], axis=0)
    mean_values_pred[:, 0] = np.squeeze(prediction)

    # Inverse transform
    y_pred = scaler.inverse_transform(mean_values_pred)[:, 0]

    # Generate array filled with means for testY
    mean_values_testY = np.repeat(scaler.mean_[np.newaxis, :], testY.shape[0], axis=0)
    mean_values_testY[:, 0] = np.squeeze(testY)

    # Inverse transform
    testY_original = scaler.inverse_transform(mean_values_testY)[:, 0]

    # 결과를 results 딕셔너리에 저장
    results[stock_name] = (test_dates, testY_original, y_pred)

    history = model.fit(trainX, trainY, epochs=30, batch_size=32, validation_split=0.1, verbose=1)
    # 예측
    prediction = model.predict(testX)
    #print(prediction.shape, testY.shape)
    # 예측값의 평균으로 채워진 배열 생성
    mean_values_pred = np.repeat(scaler.mean_[np.newaxis, :], prediction.shape[0], axis=0)

    # 예측값을 첫 번째 열에 대입
    mean_values_pred[:, 0] = np.squeeze(prediction)

    # 역변환
    y_pred = scaler.inverse_transform(mean_values_pred)[:, 0]
    #print(y_pred.shape)

    # 실제값의 평균으로 채워진 배열 생성
    mean_values_testY = np.repeat(scaler.mean_[np.newaxis, :], testY.shape[0], axis=0)

    # 실제값을 첫 번째 열에 대입
    mean_values_testY[:, 0] = np.squeeze(testY)

    # 역변환
    testY_original = scaler.inverse_transform(mean_values_testY)[:, 0]
    

# 데이터베이스 연결
conn, cursor = connect_to_database()

# 모든 종목에 대해 루프 실행
for stock_name in results:
    # 해당 종목의 결과 데이터 가져오기
    test_dates, actual_open, predicted_open = results[stock_name]
    
    # 모레 예측값을 추출 (현재 날짜에 2일을 더합니다)
    prediction_date = datetime.now().date() + timedelta(days=1)
    
    # 모델로부터 모레의 예측값 추출 (이전 코드에서 이미 다음날의 값을 추출하는 부분을 사용하면 됩니다)
    predicted = predicted_open[-1]
    
    # 결과를 데이터베이스에 추가
    insert_prediction_to_db(conn, cursor, stock_name, prediction_date, predicted)



# 연결 닫기
conn.close()

print('저장완료')