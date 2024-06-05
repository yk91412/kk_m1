## Numpy

대규모 배열과 행렬 연산에 필요한 다양한 함수 제공

- NumPy 배열 생성 및 조작

      np.array(): 리스트나 튜플로부터 배열 생성
  
      np.arange(), np.linspace(): 연속된 값으로 배열 생성
  
      배열의 형태 변경: reshape(), flatten() 등


* 속성 탐색

  array.shape : 배열의 크기

  array.size : 배열의 총 요소 수

  array.dtype : 배열 요소의 데이터 유형

  

  - 연산

    array (-,+,/,*) array 2 연산 가능


  - 슬라이싱, 인덱싱
 
    2차원 배열이라면 array[1,2]로 1행의 2열에 있는 수를 출력할 수 있다

    행 하나만 출력시 [2] 가능, 열 하나만 출력시 [:,2] => :를 사용해야 오류가 발생하지 않음
