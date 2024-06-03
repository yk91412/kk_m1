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

** 날짜

날짜 변환 : to_datetime, to_timestamp, to_period

날짜 생성 : date_range, period_range, date_range

