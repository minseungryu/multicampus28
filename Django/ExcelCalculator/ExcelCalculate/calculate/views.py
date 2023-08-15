from django.shortcuts import render, redirect
from django.http import HttpResponse
import pandas as pd
import json


def calculate(request):
    file = request.FILES['fileInput']
    print("사용자가 등록한 파일 이름: ", file)
    df = pd.read_excel(file, sheet_name="Sheet1", header=0)
    print(df.head())

    #grade 별 value 리스트 만들기
    grade_dic = {}                #빈 딕셔너리 생성
    total_row_num = len(df.index)
    #print(total_row_num)

    for i in range(total_row_num):
        data = df.loc[i, :]
        if not data.grade in grade_dic.keys():
            grade_dic[data.grade] = [data.value]
        else:
            grade_dic[data.grade].append(data.value)     
    print(grade_dic)

    # grade별 최솟값 최댓값 평균값 구하기
    grade_calculate_dic = {}
    for key in grade_dic.keys():
        grade_calculate_dic[key] = {}
        grade_calculate_dic[key]['min'] = min(grade_dic[key])   #각 Grade별 최소값
        grade_calculate_dic[key]['max'] = max(grade_dic[key])
        grade_calculate_dic[key]['avg'] = float(sum(grade_dic[key])) / len(grade_dic[key])
    
    #결과출력
    grade_list = list(grade_calculate_dic.keys())
    grade_list.sort()

    for key in grade_list:
        print("# grade: ", key)
        print("min:", grade_calculate_dic[key]['min'], end="")
        print("/ max:", grade_calculate_dic[key]['max'], end="")
        print("/ avg:", grade_calculate_dic[key]['avg'], end="\n\n")
        
    #이메일 주소 도메인별 인원 구하기
    email_domain_dic = {}
    for i in range(total_row_num):
        data = df.loc[i, :]
        #print(data.email)

        email_domain = data['email'].split("@")[1]
        if not email_domain in email_domain_dic.keys():
            email_domain_dic[email_domain] = 1
        else:
            email_domain_dic[email_domain] += 1
    
    #딕셔너리 내림차순 : html 개별 과제
    # sorted_email_domain_dic = sorted(email_domain_dic.items(), key=lambda x: x[1], reverse=True)
    # email_domain_dic = dict(sorted_email_domain_dic)
    # print("email 도메인별 사용인원: ")

    for key in email_domain_dic.keys():
        print("#", key, ":", email_domain_dic[key], "명")

    # 결과 값을 세션에 추가 / Pandas 데이터타입을 파이썬 기본데이터 타입으로 변환필요
    grade_calculate_dic_to_session = {}
    for key in grade_list:
        grade_calculate_dic_to_session[int(key)] = {}
        grade_calculate_dic_to_session[int(key)]['max'] = float(grade_calculate_dic[key]['max'])
        grade_calculate_dic_to_session[int(key)]['avg'] = float(grade_calculate_dic[key]['avg'])
        grade_calculate_dic_to_session[int(key)]['min'] = float(grade_calculate_dic[key]['min'])
    
    request.session['grade_calculate_dic'] = grade_calculate_dic_to_session
    request.session['email_domain_dic'] = email_domain_dic

    # pandas 로 해결하는 경우 (등급별 value 값 요약)
    grade_df = df.groupby('grade')['value'].agg(["min", "max", "mean"]).reset_index().rename(columns = {"mean": "avg"})
    grade_df = grade_df.astype({"min":"int", "max":"int", "avg": "float"})
    print(grade_df.dtypes)

    grade_df = grade_df.style.hide(axis="index").set_table_attributes('class ="table table-dark"')
    grade_calculate_pd_to_session = {'grade_df' : grade_df.to_html(justify='center')}
    request.session['grade_calculate_pd_dic'] = grade_calculate_pd_to_session
    print("")


    # pandas 로 해결하는 경우 (이메일도메인별 count)
    df['domain'] = df['email'].apply(lambda x : x.split("@")[1])
    email_df = df.groupby('domain')['value'].agg("count").sort_values(ascending=False).reset_index()
    email_df = email_df.style.hide(axis='index').set_table_attributes('class="table table-dark"')
    email_calculate_pd_to_session = {'email_df' : email_df.to_html(justify='center')}
    request.session['email_calculate_pd_dic'] = email_calculate_pd_to_session
    print(email_df)

    return redirect("/result")




    # 요청 > 바로 다음 함수 지정할 때 'name' // > 다른 화면(html) 보여줘야할 때 'path'
    # return redirect("/result")
"""
    # 과제 : 위 코드 결과 값을 pandas 문법으로 변환해서 2개 task 완료하기
    # 내가 써본 답 (아래)

def calculate(request):
    # 파일 받아오기
    file = request.FILES['fileInput']
    print("사용자가 등록한 파일 이름: ", file)
    df = pd.read_excel(file, sheet_name="Sheet1", header=0)
    
    #파일을 데이터프레임으로, 데이터 2개 복사
    df = pd.DataFrame(df)
    df1 = df.copy()
    df2 = df.copy()

    #grade 별 최소, 최대, 평균 구하기 (pivot table 해보기)
    grouped_grade = df1.pivot_table(index='grade', values= 'value', aggfunc=('max', 'min', 'mean'))
    grouped_grade = grouped_grade.reset_index()
    print(grouped_grade.head())

    # grouped_df = {}
    # grouped_max = df1.groupby('grade')['value'].max()
    # grouped_min = df1.groupby('grade')['value'].min()
    # grouped_avg = df1.groupby('grade')['value'].mean()

    # grouped_df['min'] = grouped_min
    # grouped_df['max'] = grouped_max
    # grouped_df['avg'] = grouped_avg
    # grouped_df = pd.DataFrame(grouped_df)

    # print(grouped_df.head())
    # print("")

    # # domain 별 value_count
    df2['email_domain'] = df2['email'].str.split('@').str[1]
    domain_counts = df2['email_domain'].value_counts()

    domain_counts = pd.DataFrame(domain_counts)
    domain_counts.columns = ['value']
    domain_counts = domain_counts.rename_axis('domain')
    domain_counts = domain_counts.sort_values(by="value", ascending=False)
    domain_counts = domain_counts.reset_index()
    print(domain_counts.head())
"""
    
