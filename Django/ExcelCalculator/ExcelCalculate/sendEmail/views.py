from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string

# Create your views here.
def send(receiverEmail, verifyCode):
    # receiverEmail : 사용자가 회원가입 할 때 입력한 이메일 주소
    # verifyCode : 인증코드

    # 인증코드 발송은 에러가 날 가능성이 존재
    # try-except 구문 사용 : google 이용 <===개발자가 통제할 수 있는 영역이 아님(특히, 외부 API 사용시!)
    try:
        content = {'verifyCode' : verifyCode}
        msg_html = render_to_string("sendEmail/email_format.html", content)
        msg = EmailMessage(subject="인증 코드 발송 메일",
                           body=msg_html,
                           from_email="ryuminseung96@gmail.com",
                           bcc=[receiverEmail])
        msg.content_subtype="html"
        msg.send()

        print("sendEmail > views.py > send 함수 임무 완료-----------")
        return True 
    except:
        print("sendEmail > views.py > send 함수 임무 실패(점검 필요)-----------")
        return False

    #return HttpResponse("sendEmail, send Function!")
