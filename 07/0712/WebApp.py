from flask import Flask, render_template, request, send_file, make_response
from wtforms import StringField, SelectField, DateField, SubmitField
import pandas as pd
import matplotlib.pyplot as plt
import mpld3
from markupsafe import Markup
from flask_assets import Environment, Bundle
import matplotlib.font_manager as fm
import os
from datetime import date
from flask_wtf.csrf import CSRFProtect
from flask_wtf import FlaskForm  # FlaskForm 추가
import zipfile
from io import BytesIO

app = Flask(__name__)
app.config.from_pyfile('config.py')

csrf = CSRFProtect(app)

# 폼 클래스 정의
class SearchForm(FlaskForm):
    application_fields = StringField('Application Fields')
    filter_type = SelectField('필터', choices=[('patent', '특허실용신안'), ('applicant', '출원인')])
    search_keyword = StringField('search_keyword')
    start_date = DateField('출원일자', format='%Y-%m-%d', default=date(2013, 1, 1))
    end_date = DateField('~', format='%Y-%m-%d', default=date.today())
    submit = SubmitField('검색')
    download = SubmitField('다운로드')

current_directory = os.getcwd()
font_path = os.path.join(current_directory, 'NanumBarunGothic.ttf')

if os.path.exists(font_path):
    fm.fontManager.addfont(font_path)
    font_prop = fm.FontProperties(fname=font_path)
    plt.rc("font", family=font_prop.get_name())
    plt.rcParams['axes.unicode_minus'] = False

plt.switch_backend('Agg')

assets = Environment(app)

css = Bundle('css/style.css', output='gen/packed.css', filters='cssmin')
js = Bundle('js/scripts.js', output='gen/packed.js', filters='jsmin')

assets.register('css_all', css)
assets.register('js_all', js)

css.build()
js.build()

df_patents = pd.read_excel('result_mod_30June2024.xlsx')
df_papers = pd.read_excel('Papers_Arxiv.xlsx')

df_patents['application_date'] = pd.to_datetime(df_patents['application_date'], errors='coerce')
filtered_data_patents = pd.DataFrame()
filtered_data_papers = pd.DataFrame()


categories = {
    '제너럴': ['인공 지능','인공지능','뉴럴 네트워크','chat gpt','챗 gpt','챗 지피티','제미나이','메타 라마','ILSVRC','이미지넷','이미지 넷','알렉스넷','알렉스 넷','추론','신경망','신경 망','학습','훈련방법','ai','지능형','훈련 방법','지도방법','지도 방법','학습방법','학습 방법','머신러닝','머신 러닝','딥러닝','딥 러닝','패턴인식','패턴 인식','블록체인','블록 체인','이미지인식','이미지 인식','비전','자연어 처리','자연어처리','챗봇','기계학습','기계 학습','심층학습','심층 학습','제스처 인식','제스쳐 인식','피사체 인식','객체 인식','오브젝트 인식','동작 인식','모션 인식','안면 인식','거대 언어','거대언어','생성형','일반 인공지능','일반 인공 지능','일반 ai','자율 인공지능','자율 ai','자율 학습'],
    '의료':['의료','항체','헬스','치료','항체','건강','유전자','병원','유도체','환자','동물','의료기기','의료 기기','의료정보','의료 정보','바이오의료','바이오 의료','의학','약물','수술','재활','임상','의사','간호','응급','진단','면역','질환','질병','치료제','보건','헬스케어','생체'],
    '전자상거래서비스': ['상거래','상품','주문','맞춤 서비스','클라이언트','배송','판매','결제','공급망','공급 망','판매망','판매 망','서비스','전자상거래플랫폼','전자 상거래 플랫폼','전자상거래 플랫폼','온라인쇼핑','온라인 쇼핑','온라인 거래','디지털결제','디지털 결제','온라인서비스','온라인 서비스','온라인 플랫폼','온라인플랫폼','인터넷 거래','인터넷거래','인터넷 서비스','인터넷서비스','고객','구매자','트래픽','방문자','페이지뷰','세션 시간','세션시간','이메일 구독','이메일구독','마케팅','광고','QR','연관 상품','연관상품','통관','관세','환율'],
    '자동차': ['자동차','주행','진입','변속기','자율주행','자율 주행','도로','차량','충돌','교통','비행','보행자','차선','신호등','전기차','하이브리드','내연기관','커넥티드카','커넥티드 카','스마트카','스마트 카','운전 보조 시스템','운전보조 시스템','운전보조시스템','ADAS','차량용센서','차량센서','차량 센서','차량용 센서','모빌리티','운송','운전','주차','헤드업 디스플레이','헤드업디스플레이','내비게이션'],
    '금융': ['금융','코인','트레이딩','투자','신용','자산','블록체인','블록 체인','디지털자산','디지털 자산','간편결제','자동결제','입금','출금','재정','은행','보험','경제','자산','부채','대출','이자','지불','결제','송금','환율','외환','주식','채권','증권','펀드','연금','퇴직금','저축','예금','지급 보증','핀테크','온라인 뱅킹','온라인뱅킹','인터넷 뱅킹','인터넷뱅킹','크라우드 펀딩','크라우드펀딩','크립토커런시','비트코인','알트코인','캐피털'],
    '교육': ['교육','강의','교육용','시험','성적','학생','학습관리','학습 관리','자기주도학습','학교','대학','강의','교수','교실','e러닝','이러닝','에듀테크','가상 교실','가상 수업','디지털 교과서','교사','교육자'],
    '농업': ['농업','농사','작황','작물','스마트농업','스마트 농업','농작물','농약','수확','스마트팜','품종'],
    '엔터테인먼트': ['콘텐츠','컨텐츠','증강 현실','증강현실','게임','미디어','사용자인터페이스','가상현실','음성인식','가상현실콘텐츠','엔터테인먼트','영화','드라마','애니메이션','뮤지컬','공연','콘서트','음악','음원','음반','뮤직비디오','뮤직 비디오','라디오','팟캐스트','팟 캐스트','오디오북','오디오 북','웹툰','웹소설','웹 소설','스트리밍','넷플릭스','디즈니','아마존','유튜브','트위치','틱톡','페이스북','인스타그램','전시회'],
    '보안': ['보안','침입','탐지','데이터보호','데이터 보호','위협예측','위협 예측','인증','암호화','암호','안전기술','위험','방화벽','바이러스','스파이','랜섬웨어','피싱','스팸','해독','디지털 서명','디지털서명','디지털 인증서','디지털인증서','토큰','보안 프로토콜','보안프로토콜','위협 방지','위협 분석','위협 대응','위협 완화','위협 모니터링','위협 방어','위협 평가','위협 예측','위협 방어','위협 차단','위협 관리','침해 탐지','침해 방지','침해 분석','침해 대응','침해 완화','침해 모니터링','침해 평가','침해 예측','침해 방어','침해 차단','침해 관리'],
    '자동화시스템': ['자동화','로봇자동화','로봇 자동화','제어시스템','제어 시스템','IoT','로봇제어','로봇 제어','스마트시스템','스마트 시스템','온라인서비스','온라인 서비스'],
    '반도체': ['뉴로모픽', '인공지능 반도체', 'ai 반도체', 'npu', '양자 소자','양자 컴퓨팅','양자 알고리즘']
} 


# categories = {
#     '제너럴': ['artificial intelligence', 'neural network', 'chat gpt', 'gemini', 'meta llama', 'ilsvrc', 'imagenet', 'alexnet', 'inference', 'learning', 'training methods', 'ai', 'intelligent', 'training method', 'supervised methods', 'learning methods', 'machine learning', 'deep learning', 'pattern recognition', 'blockchain', 'image recognition', 'vision', 'natural language processing', 'chatbot', 'gesture recognition', 'object recognition', 'motion recognition', 'facial recognition', 'large language models', 'generative', 'general ai', 'autonomous ai', 'autonomous learning'],
#     '의료': ['healthcare', 'antibody', 'health', 'treatment', 'wellness', 'gene', 'hospital', 'derivative', 'patient', 'animal', 'medical device', 'medical information', 'bio-medical', 'medicine', 'drug', 'surgery', 'rehabilitation', 'clinical', 'doctor', 'nurse', 'emergency', 'diagnosis', 'immune', 'disease', 'disorder', 'therapy', 'public health', 'biometrics'],
#     '전자상거래서비스': ['commerce', 'product', 'order', 'customized services', 'client', 'delivery', 'sales', 'payment', 'supply chain', 'service', 'e-commerce platform', 'online shopping', 'online transaction', 'digital payment', 'online service', 'online platform', 'internet transaction', 'internet service', 'customer', 'buyer', 'traffic', 'visitor', 'page view', 'session time', 'email subscription', 'marketing', 'advertisement', 'qr', 'related products', 'customs clearance', 'tariff', 'exchange rate'],
#     '자동차': ['automobile', 'driving', 'entry', 'transmission', 'autonomous driving', 'road', 'vehicle', 'collision', 'traffic', 'flight', 'pedestrian', 'lane', 'traffic light', 'electric vehicle', 'hybrid', 'internal combustion engine', 'connected car', 'smart car', 'driver assistance system', 'adas', 'vehicle sensor', 'mobility', 'transportation', 'parking', 'head-up display', 'navigation'],
#     '금융': ['finance', 'coin', 'trading', 'investment', 'credit', 'asset', 'blockchain', 'digital asset', 'easy payment', 'automatic payment', 'deposit', 'withdrawal', 'bank', 'insurance', 'economy', 'liability', 'loan', 'interest', 'remittance', 'exchange rate', 'foreign exchange', 'stock', 'bond', 'securities', 'fund', 'pension', 'retirement fund', 'savings', 'guarantee', 'fintech', 'online banking', 'internet banking', 'crowdfunding', 'cryptocurrency', 'bitcoin', 'altcoin', 'capital'],
#     '교육': ['education', 'lecture', 'educational', 'exam', 'grade', 'student', 'learning management', 'self-directed learning', 'school', 'university', 'professor', 'classroom', 'e-learning', 'edutech', 'virtual classroom', 'virtual class', 'digital textbook', 'teacher', 'educator'],
#     '농업': ['agriculture', 'farming', 'crop', 'smart agriculture', 'agricultural products', 'pesticide', 'harvest', 'smart farm', 'varieties'],
#     '엔터테인먼트': ['content', 'augmented reality', 'game', 'media', 'user interface', 'virtual reality', 'voice recognition', 'vr content', 'entertainment', 'movie', 'drama', 'animation', 'musical', 'performance', 'concert', 'music', 'music source', 'album', 'music video', 'radio', 'podcast', 'audiobook', 'webtoon', 'web novel', 'streaming', 'netflix', 'disney', 'amazon', 'youtube', 'twitch', 'tiktok', 'facebook', 'instagram', 'exhibition'],
#     '보안': ['security', 'intrusion', 'detection', 'data protection', 'threat prediction', 'authentication', 'encryption', 'safe technology', 'risk', 'firewall', 'virus', 'spyware', 'ransomware', 'phishing', 'spam', 'decryption', 'digital signature', 'digital certificate', 'token', 'security protocol', 'threat prevention', 'threat analysis', 'threat response', 'threat mitigation', 'threat monitoring', 'threat defense', 'threat assessment', 'intrusion detection', 'intrusion prevention', 'intrusion analysis', 'intrusion response', 'intrusion mitigation', 'intrusion monitoring', 'intrusion assessment'],
#     '자동화시스템': ['automation', 'robotic automation', 'control system', 'iot', 'robot control', 'smart system', 'online service'],
#     '반도체': ['neuromorphic', 'ai semiconductor', 'npu', 'quantum device', 'quantum computing', 'quantum algorithm']
# }


@app.route('/')
def index():
    form = SearchForm()
    return render_template('Web.html', date=date, form=form)

@app.route('/search', methods=['POST'])
@csrf.exempt
def search():
    global filtered_data_patents
    global filtered_data_papers

    form = SearchForm()
    if form.validate_on_submit():
        application_fields = request.form.getlist('application_fields')
        filter_type = form.filter_type.data
        search_keyword = form.search_keyword.data
        start_date = form.start_date.data.strftime('%Y-%m-%d')
        end_date = form.end_date.data.strftime('%Y-%m-%d')
        
        try:
            # 특허 데이터 필터링
            field_conditions = [(df_patents[field] == 1) for field in application_fields]
            filtered_df_patents = df_patents[pd.concat(field_conditions, axis=1).any(axis=1)]

            if filter_type == 'applicant':
                filtered_df_patents = filtered_df_patents[filtered_df_patents['applicant'].str.contains(search_keyword, na=False)]
            else:
                filtered_df_patents = filtered_df_patents[(filtered_df_patents['title'].str.contains(search_keyword, na=False)) | 
                                                          (filtered_df_patents['summary'].str.contains(search_keyword, na=False))]

            filtered_df_patents = filtered_df_patents[(filtered_df_patents['application_date'] >= start_date) & (filtered_df_patents['application_date'] <= end_date)]

            filtered_df_patents = filtered_df_patents.rename(columns={
                'status': 'Status',
                'title': 'Title',
                'ap_num': 'Application Number',
                'application_date': 'Application Date',
                'applicant': 'Applicant'
            })

             # Add hyperlink to Application Number in patent table
            filtered_df_patents['Application Number'] = filtered_df_patents.apply(
                lambda row: f'<a href="https://patents.google.com/?q=KR{row["Application Number"]}" target="_blank">{row["Application Number"]}</a>',
                axis=1
            )
            filtered_data_patents = filtered_df_patents

            if filtered_df_patents.empty:
                return render_template('Web.html', table="No data available after filtering", plot="", top3_table="", top5_table="", paper_table="", date=date, form=form)

            
            # 논문 데이터 필터링
            if filter_type == 'patent':
                paper_conditions = []
                for field in application_fields:
                    for keyword in categories.get(field, []):
                        paper_conditions.append((df_papers['title'].str.contains(keyword, na=False)) | 
                                                (df_papers['Abstract'].str.contains(keyword, na=False)))
                if paper_conditions:
                    filtered_df_papers = df_papers[pd.concat(paper_conditions, axis=1).any(axis=1)]
                    filtered_df_papers = filtered_df_papers[(filtered_df_papers['title'].str.contains(search_keyword, na=False)) | 
                                                            (filtered_df_papers['Abstract'].str.contains(search_keyword, na=False))]
                    filtered_data_papers = filtered_df_papers
                else:
                    filtered_data_papers = pd.DataFrame()

                if not filtered_data_papers.empty:
                    paper_table_html = filtered_df_papers[['title', 'Abstract', 'submit_date']].to_html(index=False, classes="table", escape=False)
                else:
                    paper_table_html = ""
            else:
                paper_table_html = ""

            table_html = filtered_df_patents[['Application Number', 'Application Date', 'Applicant', 'Title', 'Status']].to_html(index=False, classes="table", escape=False)

            # 플롯 데이터를 준비
            filtered_df_patents['application_year'] = filtered_df_patents['Application Date'].dt.year
            filtered_counts = filtered_df_patents.groupby(['application_year', 'applicant_lgrp']).size().unstack(fill_value=0)

            years = list(filtered_counts.index)
            fig, ax = plt.subplots(figsize=(12, 6))
            filtered_counts.plot(kind='bar', stacked=True, ax=ax)
            ax.set_title('Patent Counts by Year')
            ax.set_xlabel('Year', fontsize=14)
            ax.set_ylabel('Patent Counts', fontsize=14)
            ax.set_xticks(range(len(years)))
            ax.set_xticklabels(years, rotation=45, ha='right', fontsize=12)
            ax.tick_params(axis='y', labelsize=12)
            plot_html = mpld3.fig_to_html(fig)
            plt.close(fig)

            top3_df = filtered_df_patents['Applicant'].value_counts().head(3).reset_index()
            top3_df.columns = ['Applicant', 'Patent Count']
            top3_table = top3_df.to_html(index=False, classes="table", escape=False)

            # Define the stopwords
            stopwords = [' 주식회사', '주식회사 ', '주식회사', '(주)']

            # Function to remove stopwords
            def remove_stopwords(name, stopwords):
                for stopword in stopwords:
                    name = name.replace(stopword, '')
                return name.strip()            
            filtered_df_etc_domestic = filtered_df_patents[filtered_df_patents['applicant_lgrp'].isin(['etc', '국내기업'])]
            top5_df = filtered_df_etc_domestic['Applicant'].value_counts().head(10).reset_index()
            top5_df.columns = ['Applicant', 'Patent Count']
            top5_df['Applicant'] = top5_df.apply(
                lambda row: f'<a href="https://www.wanted.co.kr/search?query={remove_stopwords(row["Applicant"], stopwords)}&tab=company" target="_blank">{row["Applicant"]}</a>',
                axis=1
            )
            top5_table = top5_df.to_html(index=False, classes="table", escape=False)
            
            return render_template('Web.html', table=Markup(table_html), plot=Markup(plot_html), 
                                   top3_table=Markup(top3_table), top5_table=Markup(top5_table),
                                   paper_table=Markup(paper_table_html),
                                   application_fields=application_fields, filter_type=filter_type,
                                   search_keyword=search_keyword, start_date=start_date, end_date=end_date, date=date, form=form)

        except Exception as e:
            return render_template('Web.html', table="An error occurred: {}".format(e), plot="", top3_table="", top5_table="", paper_table="", date=date, form=form)

    return render_template('Web.html', date=date, form=form)

@app.route('/download', methods=['POST'])
@csrf.exempt
def download():
    global filtered_data_patents
    global filtered_data_papers

    # 특허 데이터 컬럼 선택
    patent_columns = ['Application Number', 'Application Date', 'Applicant', 'Title', 'Status']
    if not filtered_data_patents.empty:
        filtered_patent_data = filtered_data_patents[patent_columns]
        patent_csv = filtered_patent_data.to_csv(index=False)
    else:
        patent_csv = "No data available for patents"

    # 논문 데이터 컬럼 선택
    paper_columns = ['title', 'Abstract', 'submit_date']
    if not filtered_data_papers.empty:
        filtered_paper_data = filtered_data_papers[paper_columns]
        paper_csv = filtered_paper_data.to_csv(index=False)
    else:
        paper_csv = "No data available for papers"

    # 메모리 내에서 압축 파일 생성
    memory_file = BytesIO()
    with zipfile.ZipFile(memory_file, 'w') as zf:
        zf.writestr("filtered_patents.csv", patent_csv)
        zf.writestr("filtered_papers.csv", paper_csv)

    memory_file.seek(0)
    
    # 응답 데이터 생성
    response = make_response(memory_file.read())
    response.headers["Content-Disposition"] = "attachment; filename=filtered_data.zip"
    response.headers["Content-Type"] = "application/zip"

    return response

@app.route('/plot')
@csrf.exempt
def plot():
    global filtered_data_patents
    if filtered_data_patents.empty:
        return "No data available for plotting"

    if 'Application Date' not in filtered_data_patents.columns:
        return "Column 'Application Date' not found in filtered_data"

    filtered_data_patents['application_year'] = filtered_data_patents['Application Date'].dt.year
    filtered_counts = filtered_data_patents.groupby(['application_year', 'applicant_lgrp']).size().unstack(fill_value=0)

    fig, ax = plt.subplots(figsize=(7, 4))
    filtered_counts.plot(kind='bar', stacked=True, ax=ax)
    ax.set_title('Patent Counts by Year')
    ax.set_xlabel('Year', fontsize=16)
    ax.set_ylabel('Patent Counts', fontsize=16)
    ax.set_xticks(range(len(filtered_counts.index)))
    ax.set_xticklabels(filtered_counts.index, rotation=45, ha='right', fontsize=12)
    ax.tick_params(axis='y', labelsize=12, direction='in')
    ax.tick_params(axis='x', labelsize=12, direction='in')

    from matplotlib.patches import Rectangle
    rect = Rectangle((ax.get_xlim()[0], ax.get_ylim()[0]), 
                     ax.get_xlim()[1] - ax.get_xlim()[0], 
                     ax.get_ylim()[1] - ax.get_ylim()[0], 
                     fill=False, color='black', linewidth=1.2)
    ax.add_patch(rect)

    plt.tight_layout()
    plot_html = mpld3.fig_to_html(fig)
    plt.close(fig)

    return render_template('plot.html', plot=Markup(plot_html))

if __name__ == '__main__':
    app.run(debug=True)
