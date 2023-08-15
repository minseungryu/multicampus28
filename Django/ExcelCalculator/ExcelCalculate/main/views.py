from django.shortcuts import render, redirect
from random import *
from .models import *
from sendEmail.views import *
import pandas as pd

# Create your views here.
def index(request):
    # 로그인된 사용자만 접근
    # 조건문 : 사용자 정보가 세션에 존재하면 메인화면으로 출력 (로그인 action 이 있어야 세션에 사용자 정보 저장됨!)
    #          만약, 사용자 정보가 세션에 없으면, 로그인 화면으로 출력
    if 'user_name' in request.session.keys():
        return render(request, "main/index.html")       # 사용자 세션 정보가 담긴 index.html
    else:
        return redirect("main_signin")

    # return render(request, "main/index.html")    ->아무 세션정보가 없는 index.html

def signup(request):
    return render(request, "main/signup.html")

def join(request):
    print(request)
    name = request.POST['signupName']
    email = request.POST['signupEmail']
    pw = request.POST['signupPW']
    user = User(user_name = name, user_email = email, user_password = pw)
    user.save()
    print("사용자 정보 저장 완료됨(확인용코드)")

    # 인증코드 생성
    code = randint(1000, 9000)
    print("인증코드 생성 ---------", code)  #서버가 보낸 코드, 쿠키와 세션

    response = redirect("main_verifyCode")  #응답을 객체로 저장함
    response.set_cookie('code', code)   #인증코드
    response.set_cookie('user_id', user.id)
    print("응답 객체 완성 ------------")

    # 이메일 발송하는 함수 만들기
    # 이메일 주소 2개 준비
    send_result = send(email, code)
    if send_result:
        print("main > views.py > 이메일 발송 중 완료된 거 같음..!")
        return response
    else:
        return HttpResponse("이메일 발송 실패!")
    

def signin(request):
    return render(request, "main/signin.html")

def login(request):
    # 로그인된 사용자만 이용할 수 있도록 구현
    # 현재 사용자가 로그인된 사용자인지 판단하기 위해 세션 사용 (verify 함수에서 만든 세션)
    # 세션 처리 진행
    loginEmail = request.POST['loginEmail']
    loginPW = request.POST['loginPW']

    # 로그인 시도 시: user 모델에 접근 후, 사용자가 입력한 이메일로 탐색 시도
    # 회원 미가입 또는 비번 틀릴 경우 : 에러 발생/이상한 페이지
    # >> 예외처리
    try:
        user = User.objects.get(user_email=loginEmail)
    except:
        return redirect("main_loginFail")
    
    if loginPW == user.user_password:
        request.session['user_name'] = user.user_name       #사용자가 회원가입시 입력한 정보
        request.session['user_email'] = user.user_email     #사용자가 회원가입시 입력한 정보(>>로그인 상태 유지)
        return redirect('main_index')
    else:
        # 로그인 실패, 정보가 다름
        print("매칭 실패")
        return redirect("main_loginFail")


def loginFail(request):
    return render(request, 'main/loginFail.html')


def verifyCode(request):
    return render(request, "main/verifyCode.html")

def verify(request):
    # 1. 사용자가 입력한 code 값을 받아야 함
    user_code = request.POST['verifyCode']
    # 2. 쿠키에 저장되어 있는 code 값을 가져오기 (join 함수 확인)
    cookie_code = request.COOKIES.get('code')
    print("두 코드 체크 :", user_code, cookie_code)

    # 3. 두 개 코드 일치 여부 확인
    if user_code == cookie_code:
        # 회원가입 완료
        user = User.objects.get(id = request.COOKIES.get('user_id'))
        user.user_validate = 1      # True = 1, False = 0
        user.save()
        print("DB에 user_validate 업데이트 완료---------------")

        response = redirect('main_index')

        #저장되어 있는 쿠키 삭제
        response.delete_cookie('code')
        response.delete_cookie('user_id')
        #response.set_cookie('user', user)

        # 사용자 정보를 세션에 저장
        request.session['user_name'] = user.user_name       ##로그인 화면 구현시 활용 >> 요청
        request.session['user_email'] = user.user_email     ##로그인 화면 구현시 활용

        return response
    
    else:
        # 인증코드 화면으로 돌아가야함
        return redirect('verifyCode')

    #return redirect('main_index') #인증이 완료되면 메인 화면으로 보내줌

def result(request):
    if 'user_name' in request.session.keys():
        #보안을 위해 새로운 객체에 저장
        content = {}
        content['grade_calculate_dic'] = request.session['grade_calculate_dic']
        content['email_domain_dic'] = request.session['email_domain_dic']
        content['grade_calculate_pd_dic'] = request.session['grade_calculate_pd_dic']
        content['email_calculate_pd_dic'] = request.session['email_calculate_pd_dic']

        #print(content['grade_calculate_pd_dic'])
        #print(content['email_calculate_pd_dic'])

        #기존 세션 삭제
        del request.session['grade_calculate_dic']
        del request.session['email_domain_dic']
        del request.session['grade_calculate_pd_dic']
        del request.session['email_calculate_pd_dic']

        return render(request, "main/result.html", content)     #사용자 세션 정보가 담긴 상태에서의 result.html
    else:
        return redirect('main_signin')
    
def logout(request):
    # 로그아웃 = 세션 종료 >> 세션 정보 삭제
    # 파이썬에서 객체 삭제
    del request.session['user_name']
    del request.session['user_email']
    return redirect('main_signin')

