from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import auth
from teacher.models import UserInfo, TeacherInfo, StudentInfo, ManagerInfo, CourseInfo, \
                           CourseTime, Homework, MultipleChoice, ShortAnswer, HwOfCourse, \
                           StudentAnswer, HwGrade, ForumList, PostReply, Source, Message, \
                           Announcement, Customer, IsRead,Liuyan
from django.contrib.auth.models import User
from django.db import models
import time

def admincheck(user):
    try:
        if user.userinfo.user_type == 3:
            return True
    except:
        return False
    return False


@user_passes_test(admincheck, login_url="/login")
def index(request):
    tmp = []
    # 通知列表设有一个标志位来标志是否已读，0为未读，1为已读，前端点击了通知详情按钮后，应该到后台将状态设置为已读

    GlobalNoticeList = [['1', '操作系统课程有新通知', '2017/12/12, 20:00:00', '作业1已发布，ddl为今晚10点'],
                        ['1', '计算机网络课程有新通知', '2017/12/13, 20:00:00', '作业2已发布，ddl为今晚10点'],
                        ['0', '软件需求工程课程有新通知', '2017/12/14, 20:00:00', '作业3已发布，ddl为今晚10点'],
                        ['0', '操作系统课程有新通知', '2017/12/14, 20:00:00', '作业4已发布，ddl为今晚10点']]
    unreadGlobalNotice = 0
    for i in GlobalNoticeList:
        if i[0] == '0':
            unreadGlobalNotice += 1

    coursesall=CourseInfo.objects.all()
    counts=coursesall.count()
    CoursesList=[[0 for i in range(6)] for i in range(counts)]
    k=0
    i=0
    for course in coursesall:
        CoursesList[i][0]=course.course_name
        CoursesList[i][1]=course.course_teacher
        CoursesList[i][2]=course.course_time
        CoursesList[i][3]=course.course_pos
        CoursesList[i][4]=course.course_type
        CoursesList[i][5]=course.course_exam
        i+=1


    CoursesPage = Paginator(CoursesList, 10)
    CoursesPaginator = []
    for i in range(1, CoursesPage.num_pages + 1):
        for j in CoursesPage.page(i):
            tmp.append(CoursesPage.page(i))
        CoursesPaginator.append(tmp)
        tmp = []
    liuyanall=Liuyan.objects.all()
    counts=liuyanall.count()
    liuyanList=[[0 for i in range(6)] for i in range(counts)]

    k=0

    for item in liuyanall:
        if liuyanall[k].role==1:
            role='学生'
            img='/static/Semantic-UI-master/examples/assets/images/avatar/tom.jpg'
        elif liuyanall[k].role==2:
            role='教师'
            img='/static/Semantic-UI-master/examples/assets/images/avatar/nan.jpg'
        elif liuyanall[k].role==3:
            role='管理员'
            img='/static/Semantic-UI-master/examples/assets/images/avatar/tom.jpg'
        else:
            img='/static/Semantic-UI-master/examples/assets/images/avatar/tom.jpg'
            role='游客'
        liuyanList[k]=[img,liuyanall[k].name,role,liuyanall[k].content,
                       liuyanall[k].datetime,k+1,liuyanall[k].id]
        k+=1

    liuyanPage = Paginator(liuyanList, 10)
    liuyanPaginator = []
    for i in range(1, liuyanPage.num_pages + 1):
        for j in liuyanPage.page(i):
            tmp.append(liuyanPage.page(i))
        liuyanPaginator.append(tmp)
        tmp = []
    # 用户表
    userall=User.objects.all()
    counts=userall.count()
    UserList=[[0 for i in range(4)] for i in range(counts)]

    k=0
    for item in userall:
        UserList[k]=[item.id,item.username,item.email,item.date_joined]
        k=k+1

    UserPage = Paginator(UserList, 10)
    UserPaginator = []
    for i in range(1, UserPage.num_pages + 1):
        for j in UserPage.page(i):
            tmp.append(UserPage.page(i))
        UserPaginator.append(tmp)
        tmp = []
    return render(request, 'administrator/index.html', {'GlobalNoticeList': GlobalNoticeList,
                                                        'unreadGlobalNotice': unreadGlobalNotice,
                                                        'CoursesList': CoursesList,
                                                        'liuyanPage': liuyanPage, 'liuyanPaginator': liuyanPaginator,
                                                        'CoursesPage': CoursesPage,
                                                        'CoursesPaginator': CoursesPaginator,
                                                        'UserPage': UserPage, 'UserPaginator': UserPaginator})


@user_passes_test(admincheck, login_url="/login")
def courses(request,id):

    course=CourseInfo.objects.get(course_name=id)
    CourseInfomation=[course.course_id,course.course_name,course.course_depart,course.course_credits,course.course_teacher]
    # 课程信息表，包括课程号，课程名，开课学院，开班数，本班教师

    # 课程开班表，包括教师，学期，上课时间，上课地点，教学方式，考试时间
    CoursesList = [
        [['陈纯', '冯雁'], '春夏', ['周二第7,8节', '周一第3,4,5节'], ['玉泉曹光彪西-503', '玉泉教7-304(多)'], '2018/01/20, 08:00:00'],
        [['王强'], '春夏', ['周二第7,8节', '周一第3,4,5节'], ['玉泉曹光彪西-503', '玉泉曹光彪二期-202(多)'], '2018/01/20, 08:00:00'],
        [['路东明'], '春夏', ['周日第11,12节', '周一第3,4,5节'], ['玉泉曹光彪西-503', '玉泉教7-304(多)'], '2018/01/20, 08:00:00'],
        [['陈纯'], '春夏', ['周二第7,8节', '周一第3,4,5节'], ['玉泉曹光彪西-503', '玉泉曹光彪二期-202(多)'], '2018/01/20, 08:00:00'], ]

    #courseall=CourseInfo.objects.get()
    #counts=courseall.count()
    #liuyanList = [[0 for i in range(6)] for i in range(counts)]
    # 教师信息表
    # 包括教工号，姓名，职称，学院，邮箱，联系电话
    TeacherList = [['215010', '邢卫', '教授', '计算机科学与技术学院', '10086@zju.edu.cn', '18888888888'],
                   ['215011', '卫', '教授', '计算机科学与技术学院', '10086@zju.edu.cn', '18888888888'],
                   ]
    # 学生信息表
    # 包括学号，姓名，年级，学院，专业，邮箱，联系电话
    StudentList = [['315010', '邢卫', '2015', '计算机科学与技术学院', '计算机科学与技术', '10086@zju.edu.cn', '18888888888'],
                   ['316011', '卫', '2016', '计算机科学与技术学院', '软件工程', '10086@zju.edu.cn', '18888888888'],
                   ['315010', '邢卫', '2015', '计算机科学与技术学院', '计算机科学与技术', '10086@zju.edu.cn', '18888888888'],
                   ['316011', '卫', '2016', '计算机科学与技术学院', '软件工程', '10086@zju.edu.cn', '18888888888'],
                   ['315010', '邢卫', '2015', '计算机科学与技术学院', '计算机科学与技术', '10086@zju.edu.cn', '18888888888'],
                   ['316011', '卫', '2016', '计算机科学与技术学院', '软件工程', '10086@zju.edu.cn', '18888888888'],
                   ['315010', '邢卫', '2015', '计算机科学与技术学院', '计算机科学与技术', '10086@zju.edu.cn', '18888888888'],
                   ['316011', '卫', '2016', '计算机科学与技术学院', '软件工程', '10086@zju.edu.cn', '18888888888'],
                   ['315010', '邢卫', '2015', '计算机科学与技术学院', '计算机科学与技术', '10086@zju.edu.cn', '18888888888'],
                   ['316011', '卫', '2016', '计算机科学与技术学院', '软件工程', '10086@zju.edu.cn', '18888888888'],
                   ['315010', '邢卫', '2015', '计算机科学与技术学院', '计算机科学与技术', '10086@zju.edu.cn', '18888888888'],
                   ['316011', '卫', '2016', '计算机科学与技术学院', '软件工程', '10086@zju.edu.cn', '18888888888'],
                   ['315010', '邢卫', '2015', '计算机科学与技术学院', '计算机科学与技术', '10086@zju.edu.cn', '18888888888'],
                   ['316011', '卫', '2016', '计算机科学与技术学院', '软件工程', '10086@zju.edu.cn', '18888888888'],
                   ]
    return render(request, 'administrator/administrator_courses.html', {'TeacherList': TeacherList,
                                                                        'StudentList': StudentList,
                                                                        'CourseInfo': CourseInfomation,
                                                                        'CoursesList': CoursesList})


@user_passes_test(admincheck, login_url="/login")
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/")

def liuyan(request):
    print(request.user.userinfo.user_type)
    Liuyan.objects.create(content=request.POST['comment'],datetime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) ,role=request.user.userinfo.user_type,name=request.user.username)
    return HttpResponseRedirect("/administrator/")

def deleteliuyan(request,id):
    Liuyan.objects.filter(id=id).delete()
    return HttpResponseRedirect("/administrator/")

def resetpass(request,id):
    us=User.objects.get(id=id)
    us.set_password('123456')
    us.save();
    return HttpResponseRedirect("/administrator/")
