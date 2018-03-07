from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.models import User
from teacher.models import UserInfo, TeacherInfo, StudentInfo, ManagerInfo, CourseInfo, \
    CourseTime, Homework, MultipleChoice, ShortAnswer, HwOfCourse, \
    StudentAnswer, HwGrade, ForumList, PostReply, Source, Message, \
    Announcement, Customer, IsRead

# Create your views here.
def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    username = request.POST.get('username')
    password = request.POST.get('password')
    #print(username)
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
    # Correct password, and the user is marked "active"
        auth.login(request, user)
    # Redirect to a success page.
        try:
            if user.userinfo.user_type == 1:
                return HttpResponseRedirect("/student/")
            elif user.userinfo.user_type == 2:
                return HttpResponseRedirect('/teacher/')
            elif user.userinfo.user_type == 3:
                return HttpResponseRedirect('/administrator/')
        except:
            return HttpResponse("请等待管理员为您分配权限！<a href='/'>点此返回</a>")
    else:
    # Show an error page
        print(user)
        return HttpResponse("用户名或密码错误，<a href='/'>点此返回</a>")

def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')

    if not 'username' in request.POST or not request.POST['username']:
        return HttpResponse("用户名不能为空，<a href='/register'>点此返回</a>")
    if not 'password1' in request.POST or not request.POST['password1']:
        return HttpResponse("密码不能为空，<a href='/register'>点此返回</a>")

    username = request.POST.get('username')
    password1 = request.POST.get('password1')
    password2 = request.POST.get('password2')
    
    if len(User.objects.filter(username='username')) > 0:
        return HttpResponse("用户名已经存在，<a href='/register'>点此返回</a>")

    if password1 != password2:
        return HttpResponse("密码不匹配，<a href='/register'>点此返回</a>")

    new_user = User.objects.create_user(username=username, password=password1)
    new_user.save()

    return HttpResponse("注册成功，<a href='/'>返回登录</a>")

