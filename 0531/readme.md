## 과제풀이

- 파이썬에서는 merge를 사용하는게 기본(sql에서 join인 것처럼)

- 그룹화 된 결과를 reset_index()를 이용해 다시 정규화하여 분석하기 유용하게 만드는 것이 좋다

- 생존을 나타내는 survived 컬럼에서 1이 생존, 0이 사망이라면 이를 평균을 내면 생존율을 알 수 있다

  ex) 0 0 0 1 1 1 0 0 1 1 => 총 10명, 생존자 5명, 평균을 내면 0.5 / 즉 생존율과 같다

- xticks(rotation = 0) => x축 눈금 레이블을 0으로 한다

- grid(axis='y') => y축에 대해 그리드 표시

- sort_values(ascending=False) => value의 값을 내림차순


========================================================================================

## 탐색

  - rand 균등분포 / randn 정규분포
    

  - cut() 함수 : 주어진 데이터를 구간(또는 범주)으로 나누는데 사용

    bins : 나눌 구간의 경계값을 지정

    labels : 매개변수를 사용하여 각 구간에 라벨 지정

    ( 미포함, [ 포함 => 0은 미포함 10은 포함
    
    ex) bins = [0, 30, 50, 100]  # 0~30, 31~50, 51~100 구간으로 나눔
    
    labels = ['Young', 'Middle-aged', 'Senior']  # 각 구간에 대한 라벨

    age_groups = pd.cut(ages, bins=bins, labels=labels)



  *** plot

  plt.figure(figsize=(8, 6)) => 그림 크기 조절 / 가로 8인치 세로 6인치 뜻함

  plt.tight_layout()  => 그래프 간격 조절

  plt.legend() => 범례 추가

  plt.xlabel('Value') => x축 이름
   
  plt.ylabel('Density') => y축 이름

  

  kind = line, bar, hist, box, kde, scater, barh, density, area, pie....

  => (default)선, 막대, 히스토그램, 상자, 밀도, 산점도, 수평막대, 밀도, 영역, 파이
  

  
  ---- subplots ----

    여러 그래프를 동시에 그리고 싶을 때 사용

    fig, ax  = plt.subplots(nrows=~,ncols=~,figsize=~)

fig란 figure로써 - 전체 subplot을 말한다.

ex) 서브플로안에 몇개의 그래프가 있던지 상관없이 그걸 담는 하나

전체 사이즈를 말한다.

ax는 axe로써 - 전체 중 낱낱개를 말한다

ex) 서브플롯 안에 2개(a1,a2)의 그래프가 있다면 a1, a2 를 일컬음



  ---- boxplot ----

데이터의 분포와 이상치를 시각화

    df명.plot.box() => ()안에 특정 컬럼만 넣어서 볼 수 있다
    plt.title(~)
    plt.show()


    
  ---- scatter ----
  
두 변수 간의 관계를 보여주는 그래프

    df.plot.scatter(x='A',y='B')
    plt.title('Scatter Plot')
    plt.show()



    
  ---- KDE ----
  
   커널 밀도 추정
   
   데이터의 분포를 부드럽게 나타내는 그래프


    data['A'].plot.kde(label = 'A')
    data['B'].plot.kde(label = 'B')
    plt.title('Kernel Density Estimate (KDE) Plot')
    
    plt.show()




   ---- histogram ----

     data.plot.hist(bins=30,alpha=0.5,density=True,label='Histogram')

  bins => 구간수

  alpha => 투명도

  density = True => 밀도 정규화 / y축이 상대도수(확률 밀도)로 표시


===================================================================================

seaborn 라이브러리

- countplot
  
성별과 승객(생존,사망) 수

sns.countplot(x='sex',hue = 'survived',data = df)


- histplot

sns.histplot(df, bins=30 , kde=False , color='blue' ,label='Survived')


===================================================================================

## 데이터 전처리 실습

순서

 1) 데이터 불러오기

  -> info() -> 결측치,컬럼 dtype

  -> descrebe() -> 통계적 요약

  2) 변수 선택

1. 중요 변수 탐색

    -> 변수간의 상관 관계(종속 변수와 독립 변수의 관계는 높을수록 좋다)

          => ex) 학생들의 시험 점수를 예측하는 경우
   
                  학생들의 공부 시간은 독립변수

                학생들의 시험 점수는 공부 시간에 의해 영향
   
                  학생들의 시험 점수는 종속변수

      df.corr() or df.corr()[특정 컬럼]

      plot.box()를 이용하여 이상치 확인
   
    -> 변수 분포(독립변수간의 관계는 낮은게 좋다/높으면 중복)

3. 파생 변수

    -> 탐색적 분석 시도

    -> 파생 변수 종속변수의 상관관계

표준화, 정규화

-> 적용할 분석용 데이터 셋

from sklearn.preprocessing import StandardScaler

     scaler = StandardScaler()
