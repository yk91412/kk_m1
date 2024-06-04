## pandas - 날짜

- 새로운 열 추가

  1. dt 접근자 사용

    dt['새로운 컬럼명'] = df['사용할 컬럼명'].dt.year / month / day ...
  
  2. 인덱스 사용

    set_index를 사용해서 날짜를 인덱스로 바꾸고

    df['새로운 컬럼명'] = df.index.year / month / day ...


  - 날짜 기반 슬라이싱
 
    df.loc[~:~] : 인덱스가 날짜 일 경우에 사용

    df.loc[원하는 행, ~:~] : 원하는 행에서 특정 컬럼만 슬라이싱 가능

    
