from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import *               # models.py의 클래스를 모두 상속받겠다(모든 것)


# Create your views here.
# 연습용
'''
def index(request) : 
    return HttpResponse('나의 첫번째 페이지')
'''


def index(request):  #request 써주는 이유 : GET/POST를 위해
    #로직 처리 구현
    todos = Todo.objects.all() # DB에 저장된 내용 모두 불러오기
    print("From DB:", todos)    # DB에서 데이터가 잘 넘어오나 확인용
    content = {'todos' : todos}
    return render(request, "my_to_do_app/index.html", content)

def createTodo(request):
    user_input_str = request.POST['todoContent']
    print("todoContent: " + user_input_str)

    # DB에 저장
    new_todo = Todo(content = user_input_str)
    new_todo.save()

    # return HttpResponse("create Todo를 하자! ==> " + user_input_str)
    # 작성 후, 메인페이지로 돌아가기
    return HttpResponseRedirect(reverse('index'))

def deleteTodo(request):
    delete_todo_id = request.GET['todoNum']
    print("삭제할 Todo의 ID", delete_todo_id)
    todo = Todo.objects.get(id= delete_todo_id)
    todo.delete()
    return HttpResponseRedirect(reverse('index'))