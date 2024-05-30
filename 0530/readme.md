## 과제풀이

- lambda 함수는 elif 불가능 => 복잡한 연산이라면 사용자 정의함수를 이용하는 것이 좋다

- Series를 사용할 땐 map을 사용하는 것이 좋다(간단한 연산이라면)

- transform : 기존은 유지하고 새로운 열에 함수를 적용하여 출력하고 싶을 때 사용

** apply vs map

apply는 DataFrame의 행이나 열 단위로 함수를 적용할 수 있지만, map은 Series의 각 요소에만 함수를 적용

Series의 각 요소를 변환하는 간단한 작업에는 map이 적합하고,
더 복잡한 변환이 필요한 경우나 DataFrame 전체를 다룰 때는 apply가 유용

** apply vs applymap

=> 되도록이면 apply 사용

df.apply는 DataFrame의 각 행(row) 또는 열(column)에 함수를 적용

기본적으로 axis=0으로 설정되어 있어 열 단위로 함수를 적용

각 행 또는 열 자체가 Series로 전달되며, 이 Series 전체에 대해 함수를 적용하려고 한다.

applymap은 DataFrame의 모든 요소에 대해 함수를 적용하므로, 전체 DataFrame에 대한 변환이 필요할 때 유용

===============================================================

## 연산 및 탐색

** pivot

  구성

  index: 새로운 DataFrame에서 인덱스로 사용할 기존 열 또는 열들의 이름
  
  columns: 새로운 DataFrame에서 열로 사용할 기존 열 또는 열들의 이름

  values: 피벗할 때 사용할 값이 있는 열의 이름

  기능

  긴 형식의 데이터를 넓은 형식으로 변환하여 특정 차원에서 데이터를 재구성
  
  피벗된 데이터를 통해 시간 경과에 따른 변화나 여러 카테고리의 비교를 쉽게 할 수 있다
  
  넓은 형식의 데이터는 시각화 도구에서 더 쉽게 다룰 수 있다

  - pivot, pivot_table 둘 다 사용 가능

    aggfunc 사용하려면 pivot_table을 사용해야함
    
  pandas.pivot_table(data
  
                      * 반드시 알고 있어야 하는 정보
                     , index=None  ## 각 행(row)는 무엇으로 정의할지
                     , columns=None ## 각 열(column)은 무엇으로 정의할지
                     , values=None ## 각 Cell을 어떤 숫자로 계산할지
                     , aggfunc='mean', 'sum', 'nunique' 등 ## 계산을 어떻게 할지
                   
                    더 알고 있으면 좋은 정보
                   , fill_value=None => Nan이 나올 때 채울 값
                   , margins=False
                   , dropna=True
                   , margins_name='All'
                   , observed=False
                   , sort=True
                  )


    ** 결합 탐색

      1.merge 함수

      기준이 되는 열이나 인덱스를 키라고 부름

      키가 되는 열이나 인덱스는 반드시 양쪽 데이터프레임에 모두 존재

      pd.merge(df1,df2,on='키가 될 컬럼',how='inner/outer/left/right')

      => default = inner


      2. join 함수

      merge와 기본 작동 방식이 비슷

      행 인덱스를 기준으로 결합

      df1.join(df2,lsuffix = ~, rsuffix = ~, how ='inner/outer/left/right')

      => default left

      join시 set_index를 사용하는 이유는 연산을 보다 효율 적이고 명확하게 수행

      
      3. concat 함수

  ===============================================================

  - 인덱스 재배치

    ignore_index = True : 0부터 다시 인덱스해준다

  ---- 데이터 불러오기 ----

    1. 구글 마운트 사용
    
    file = '파일 경로 복사'

    df = pd.read_excel(file, engine = 'openpyxl', index_col = ~)

    2. 파일 업로드 이용

      from google.colab import files

      uploaded = files.upload()

      업로드 실행

      import pandas as pd

      file_path = 파일명

      df = pd.read_csv(file_path)

      
  - bool 시리즈에선 or연산자 불가능 | & 으로 사용해야한다

  - .index
    
    df명.index[0] => 인덱스가 0인 부분

    df명[df명.a >10].index => 조건식을 만족하는 부분에 인덱스

  - rename과 딕셔너리를 이용해 컬럼 이름 재배치

    *** astype과 딕셔너리를 이용해서 자료형 변경도 가능

    ex) rename(columns = {'a':1,'b':2}) => a는 1로 b는 2로 컬럼명 변경
    
  - replace를 이용해 값 변경

    ex) .replace(['a','b'],[1,0]) => a는 1로 b는 0으로 변경

  - 칼럼 대/소문자로 변경

    ex) df명.rename(str.upper/lower, axis = 'columns')

  - value_counts()

    df명.특정컬럼명.value_counts() => 특정 컬럼의 값 구성 체크

  - unique()

    df명.특정컬럼명.unique() => 특정 컬럼의 고유 구성 요소
    
  ===============================================================

  ** 범주형 데이터 -> 수치형 데이터

  from sklearn.preprocessing import LabelEncoder

  fit_transform
  
  데이터를 전처리할 때 사용되며, 변환기(transformer)를 데이터에 맞게 적합시키고, 그 적합에 따라 데이터를 변환
  
  1. Label Encoding
    
     각 범주형 값을 고유한 정수로 변환

     범주형 변수에 순서나 순위가 있을 때 유용
     
  2. One-Hot Encoding
    
     각 범주형 값을 이진 벡터로 변환(0,1)

     범주형 변수에 순서나 순위가 없을 때 유용

  별도의 열을 만들고, 해당 범주에 해당하는 경우 1, 그렇지 않은 경우 0

                이제는 true,false로 나온다
                
  ex) color_ blue  color_red ...
      0              0
      0              1
      1              0
      0              0

  - get_dummies() 함수

  범주형 데이터를 원-핫 인코딩(One-Hot Encoding) 방식으로 변환

  ex) pd.get_dummies(df명)
  
  ===============================================================

  ** 시각화

  import matplotlib.pyplot as plt

 - plot(): 기본적인 시각화 함수를 제공하며, 다양한 종류의 그래프를 그릴 수 있다.

      kind 매개변수를 통해 그래프의 종류를 지정할 수 있다

      (line, bar, barh, hist, box, kde, density, area, pie, scatter, hexbin 등)

  plt.figure(figsize=(12,5))

  => 그래프의 크기 설정

  plt.subplot(1,2,1)

  => 1행 2열 그리드에 1번째 위에 서브플롯을 추가
  
  plt.tight_layout()

  => 서브플롯 간의 간격을 자동으로 조정하여 겹치지 않도록
  
- hist(): 히스토그램을 생성.

  alpha 투명도, bins 구간
  
- boxplot(): 박스 플롯을 생성.

- scatter_matrix(): 여러 변수 간의 산점도 행렬을 생성.

- plot.scatter(): 산점도를 생성.

- plot.bar(): 막대 그래프를 생성.

- plot.kde(): 커널 밀도 추정 그래프를 생성.
