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

