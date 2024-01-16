# H&M 데이터 파이프라인 구축
---

**프로젝트 기간 :** 2023.09.26 ~ 2023.11.02
**프로젝트 인원 :** 개인 프로젝트


### 프로젝트 개요

* 급변하는 국내 주식 시장에서 신속하게 변화하는 데이터에 대응하여 투자자들이 보다 더 효과적인 의사 결정을 내릴 수 있도록 하는 것이 이 프로젝트의 핵심 목표입니다. 
이 프로젝트는 국내 상위 11개 주식 데이터를 수집, 가공, 저장하고, 이를 시각적으로 표현하여 사용자들에게 직관적이고 유용한 정보를 제공하는 데 중점을 두고 있습니다. 또한 효율적이고 신뢰성 있는 데이터 수집과 처리, 직관적이며 유연한 시각화를 목표로 하고 있습니다.

### 사용된 스킬

- **언어**
  ![Static Badge](https://img.shields.io/badge/Python%20-%23003057)
- **AWS**
  ![Static Badge](https://img.shields.io/badge/EC2%20-%23003057)
- **컨테이너화**
  ![Static Badge](https://img.shields.io/badge/Docker%20-%23003057)
- **모니터링 및 시각화**
  ![Static Badge](https://img.shields.io/badge/Grafana%20-%23003057)
- **데이터 워크플로우 자동화**
  ![Static Badge](https://img.shields.io/badge/Apache%20Airflow%20-%23003057)
- **커뮤니티 도구**
  ![Static Badge](https://img.shields.io/badge/Git%20hub%20-%23003057)
- **웹 프레임워크**
  ![Static Badge](https://img.shields.io/badge/Flask%20-%23003057)
- **데이터 베이스**
  ![Static Badge](https://img.shields.io/badge/MySQL%20-%23003057)

### 프로젝트 구현 세부정보

1. 공공 api를 통해 데이터를 받아 MySQL DB에 저장합니다.
2. LSTM으로 다음날 시가를 예측 후 MySQL DB에 저장합니다.
3. Grafana로 주식 데이터를 시각화 합니다.
4. Flask를 이용해 다음날 시가를 예측하는 서비스를 배포합니다.
5. Airflow를 통해 데이터 파이프라인을 자동화 시켜줍니다.
   
![image](https://github.com/minjong3/Stock-price-prediction-service/assets/131952523/2273261b-8361-4c01-9aca-c53548a498f6)

### 프로젝트 리뷰

- Kafka, Sapark, hadoop을 사용해서 더 안정적인 데이터 파이프라인을 만들고 싶습니다.
- 주식 데이터이다 보니 뉴스나 재무제표도 영향을 받는데 그런 것 들도 추가 해서 ML을 만들면 더 좋은 서비스가될 것 같습니다.



