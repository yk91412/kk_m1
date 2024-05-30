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


