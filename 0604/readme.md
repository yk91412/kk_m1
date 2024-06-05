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

    df[::2] , df+df1[::2] 이런식으로도 가능




    - datetime vs timestamp

        datetime은 Python 표준 라이브러리에서 제공
      
        Timestamp는 pandas 라이브러리에서 제공
      
        TImestamp는 pandas의 다른 데이터 구조와의 호환성이 좋으며, 시계열 데이터를 다룰 때 유리
      
        Timestamp는 datetime 객체의 기능을 확장하여 시계열 분석에 필요한 추가 기능을 제공


        ts['20110110'] / ts['1/10/2011'] => pandas는 이러한 형식들을 자동으로 인식하고 적절한 날짜로 변환


    - series.index[2] => 2번째 인덱스

   ================================================================================================

  - trunctate
 
    
