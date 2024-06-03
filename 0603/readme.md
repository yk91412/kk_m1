##  과제풀이

- 업로드된 파일을 데이터프레임으로 읽기

  업로드된 파일들 중 첫 번째 파일의 이름 가져오기
  
  딕셔너리의 키를 리스트로 반환 -> 이 리스트에서 첫 번째 키를 가져오는 것
  
  file_path = list(uploaded.keys())[0]
  
  df = pd.read_csv(file_path)

- 중복 제외 고유한 값 출력

    df명.컬럼명.unique()

    ex) df.horsepower.unique() => 숫자형일 것 같은데 object형일 때 어떤 값 때문에 object가 되었는지 판단 가능

        => horsepower 안에 숫자와 ?가 같이 있어서 object형이 됨

        => replace로 값을 변환할 수도 있지만 애매하다면 np.nan으로 바꾸어 dropna() 실행

- heatmap

  sns.heatmap(df.corr(), annot=True, cmap='coolwarm',center = 0)
  
  center = 0 => 색상 맵의 중앙값이 0, 0을 기준으로 cool/warm으로 나누겠다

- 파생 변수 생성시 종속 변수 사용x

  독립 변수끼리로만 파생 변수 만들기

- 회귀

  Mean Squared Error
  
  실제 값과 모델이 예측한 값 간의 평균 제곱 차이를 측정
  
  Root Mean Squared Error
  
  평균 제곱 오차(MSE)의 제곱근으로, 예측 값과 실제 값 사이의 평균 제곱 차이
  
  R-squared

  모델이 설명하는 종속 변수의 총 변동 중에서 설명되는 부분의 비율을 의미

  적합성을 평가하는 데 유용



========================================================================

## pandas 날짜



날짜 변환 : to_datetime, to_timestamp, to_period

날짜 생성 : date_range, period_range, date_range




            ---- 파이썬 datetime 모듈 ----


  (date, time, datetime, timedelta, tzinfo)을 제공

      '2021-03-16' => date 클래스

      '2021-03-16 12:34:21' => datetime 클래스

  특정 날짜를 생성하거나 날짜 간의 차이를 계산 등...

        strftime() => 날짜를 문자열로 변환

        strptime() => 문자열을 날자로 변환



                          ---- 판다스 모듈 ----


    시계열 데이터 처리에 특화, 대량의 날짜 데이터를 빠르고 효율적으로 처리 가능

    to_datetime() 함수로 다양한 형식의 날짜 문자열을 datetime 객체로 변환 가능


        pd.to_datetime(str,list...)

========================================================================

** 날짜

      * pd.date_range 함수

      start =, periods = ~ or end = ~, freq = ~

      freq = 'D' 일 단위
      
              'B' 주말을 뺀 평일 단위
              
              'W' 주 단위

        pandas에서 제공하지만 내부적으로 numpy의 날짜/시간 타입인 datetime64를 사용
        
        일정한 간격으로 날짜 범위를 생성하는데 사용

        date_range = pd.date_range(start = '2022-01-1', end = '2022-01-10')

        => atetimeIndex(['2022-01-01', '2022-01-02', '2022-01-03', '2022-01-04',
               '2022-01-05', '2022-01-06', '2022-01-07', '2022-01-08',
               '2022-01-09', '2022-01-10'],
              dtype='datetime64[ns]', freq='D')


      * 날짜를 인덱스로 설정하여 데이터프레임을 구성하면 날짜를 기준으로 데이터 조작이 용이
      
        data = {'date':['2022-01-01','2022-01-02','2022-01-03'], 'value':[1,2,3]}

    
       ex) 특정 날짜의 데이터 선택
       
          print(df.loc['2022-01-02'])

        ex) 날짜 범위 슬라이싱
        
          print(df['2022-01-01':'2022-01-02'])


        ex) 불리언 조건식을 사용하여 날짜 범위를 필터링

        date_range = pd.date_range(start = '2020-01-01', end = '2020-01-10')
        
        date_series = pd.Series(date_range)
        
        fd = date_series[(date_series >= '2020-01-01') & (date_series <= '2020-01-03')]


      * resample 함수 (df에서만 가능)

      주어진 주기(일,월,분기 등) 에 따라 다양한 방법으로 데이터 집계하는 기능

      df명.resample(~).sum()

        => ~별로 합계

        'M' 달별로

        'Q' 분기별로


        * dt 접근자

        pandas에서 날짜와 시간 형식의 Series 또는 DataFrame 열에 접근하여
        해당 열의 값에 대해 날짜 및 시간 관련 작업을 수행하는 데 사용

          df['컬럼명'].dt.year / month / day / dayofweek ....


========================================================================

## 실습

        import pandas as pd
        from google.colab import files
        uploaded = files.upload()
        
        file_path = list(uploaded.keys())[0]
        df = pd.read_csv(file_path)

      => keys를 사용해 list를 묶어서 [0]을 하게되면
      굳이 파일 이름을 알아낼 필요가 없음


      1. df.info()를 확인하여 null값이나 type유형 파악

      2. 필요없는 열 제거

      3. 결측치 확인해서 제거

      4. 파생 변수 생성

      5. 범주형 변수를 만들어서 데이터 처리


    * 범주형 변수 만들기

    bins = 나눌 구간

    labels = 구간마다의 라벨이름

    df['만들 컬럼명'] = pd.cut(df['사용할 컬럼'], bins = bins, labels = labels)

    * get_dummies

    범주형 데이터를 처리하는 방법 중 하나
    
    문자열 데이터를 숫자형으로 변환하고,

    더미 변수는 정보를 표현하는 새로운 열을 만든다
