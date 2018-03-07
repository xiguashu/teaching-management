from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import auth
from django.contrib import auth
from django.contrib.auth.models import User
from django.db.models import Q
from teacher.models import UserInfo, TeacherInfo, StudentInfo, ManagerInfo, CourseInfo, \
    CourseTime, Homework, MultipleChoice, ShortAnswer, HwOfCourse, \
    StudentAnswer, HwGrade, ForumList, PostReply, Source, Message, \
    Announcement, Customer, IsRead, HwSubmit
import json

def teachercheck(user):
    try:
        if user.userinfo.user_type == 2:
            return True
    except:
        return False
    return False

# Create your views here.
@user_passes_test(teachercheck, login_url="/login")
def index(request):
    tmp = []
    # 通知列表设有一个标志位来标志是否已读，0为未读，1为已读，前端点击了通知详情按钮后，应该到后台将状态设置为已读
    userMessage = request.user.userinfo.isread_set.all()
    GlobalNoticeList = []
    for i in userMessage:
        if i.read_isread == True:
            flag = '1'
        else:
            flag = '0'
        if i.read_message != None:
            singleMessage = [flag, i.read_message.message_sender.name,
                             i.read_message.message_time.strftime("%Y-%m-%d %H:%M:%S"), i.read_message.message_content]
        else:
            singleMessage = [flag, i.read_announce.announce_title,
                             i.read_announce.announce_time.strftime("%Y-%m-%d %H:%M:%S"), i.read_announce.announce_content]
        GlobalNoticeList.append(singleMessage)
    unreadGlobalNotice = 0
    for i in GlobalNoticeList:
        if i[0] == '0':
            unreadGlobalNotice += 1
    # 课程表，应统计每门课程未读通知+未提交的作业数量

    userCourse = request.user.userinfo.user_course.all()
    CoursesList = []
    for i in userCourse:
        singleCourse = [i.course_name, i.course_teacher.split(';'), i.course_time.split(
            ';'), i.course_pos.split(';'), i. course_type, '1', '2', '3', i.id]
        CoursesList.append(singleCourse)

    liuyanList = []
    leftmessage = Customer.objects.all()
    j = 1
    for i in leftmessage:
        liuyanList.append(
            ['/static/Semantic-UI-master/examples/assets/images/avatar/tom.jpg', '游客', '游客', i.customer_title + i.customer_content, i.customer_time.strftime("%Y-%m-%d %H:%M:%S"), j])
        j += 1
    liuyanPage = Paginator(liuyanList, 10)
    liuyanPaginator = []
    for i in range(1, liuyanPage.num_pages + 1):
        for j in liuyanPage.page(i):
            tmp.append(liuyanPage.page(i))
        liuyanPaginator.append(tmp)
        tmp = []

    return render(request, 'teacher/index.html', {'GlobalNoticeList': GlobalNoticeList,
                                                  'unreadGlobalNotice': unreadGlobalNotice,
                                                  'CoursesList': CoursesList,
                                                  'liuyanPage': liuyanPage, 'liuyanPaginator': liuyanPaginator})


@user_passes_test(teachercheck, login_url="/login")
def course(request, courseid):
    tmp = []
    course = CourseInfo.objects.get(id=courseid)
    forum = course.forumlist_set.all()
    PostList = []
    re = 0
    for i in forum:
        posts = i.postreply_set.all()
        for j in posts:
            re += 1
            lastname = j.reply_user.name
            lasttime = j.reply_time.strftime("%Y-%m-%d %H:%M:%S")
        PostList.append([i.forum_title, i.forum_user.name, i.forum_time.strftime("%Y-%m-%d %H:%M:%S"), lastname, lasttime, re, i.id])
        
    time = course.coursetime_set.all()
    coursetime = []
    for i in time:
        coursetime.append([i.course_date.strftime("%Y-%m-%d"), i.course_time, i.course_assignment, i.course_position])

    # 通知列表设有一个标志位来标志是否已读，0为未读，1为已读，前端点击了通知详情按钮后，应该到后台将状态设置为已读
    userMessage = request.user.userinfo.isread_set.all()
    NoticeList = []
    for i in userMessage:
        if i.read_isread == True:
            flag = '1'
        else:
            flag = '0'
        if i.read_message != None:
            singleMessage = [flag, i.read_message.message_sender.name,
                             i.read_message.message_time.strftime("%Y-%m-%d %H:%M:%S"), i.read_message.message_content]
        else:
            singleMessage = [flag, i.read_announce.announce_title,
                             i.read_announce.announce_time.strftime("%Y-%m-%d %H:%M:%S"), i.read_announce.announce_content]
        NoticeList.append(singleMessage)
    unreadNotice = 0
    for i in NoticeList:
        if i[0] == '0':
            unreadNotice += 1
    # 作业列表设有一个标志位来标志是否已批改，0为未提交，1为已提交，前端批改作业后，应该到后台将状态设置为已提交；
    # 应能正确指导前端进行页面跳转
    HwList = []
    homework = course.homework_set.all()
    for i in homework:
        try:
            status = i.hwgrade_set.get(id=i.id)
            HwList.append(['1', i.homework_name, i.homework_deadline, i.id])
        except:
            HwList.append(['0', i.homework_name, i.homework_deadline, i.id])
    unsubmitHw = 0
    for i in HwList:
        if i[0] == '0':
            unsubmitHw += 1
    # 资源列表
    PPTList = []
    source = course.source_set.filter(source_type=1).all()
    for i in source:
        PPTList.append([i.source_name, i.source_user.name,
                        i.source_time.strftime("%Y-%m-%d %H:%M:%S")])
    PPTPage = Paginator(PPTList, 5)
    PPTPaginator = []
    for i in range(1, PPTPage.num_pages + 1):
        for j in PPTPage.page(i):
            tmp.append(PPTPage.page(i))
        PPTPaginator.append(tmp)
        tmp = []
    PDFList = []
    source = course.source_set.filter(source_type=2).all()
    for i in source:
        PDFList.append([i.source_name, i.source_user.name,
                        i.source_time.strftime("%Y-%m-%d %H:%M:%S")])
    PDFPage = Paginator(PDFList, 5)
    PDFPaginator = []
    for i in range(1, PDFPage.num_pages + 1):
        for j in PDFPage.page(i):
            tmp.append(PDFPage.page(i))
        PDFPaginator.append(tmp)
        tmp = []
    MediaList = []
    source = course.source_set.filter(source_type=3).all()
    for i in source:
        MediaList.append([i.source_name, i.source_user.name,
                          i.source_time.strftime("%Y-%m-%d %H:%M:%S")])
    MediaPage = Paginator(MediaList, 5)
    MediaPaginator = []
    for i in range(1, MediaPage.num_pages + 1):
        for j in MediaPage.page(i):
            tmp.append(MediaPage.page(i))
            MediaPaginator.append(tmp)
        tmp = []
    OthersList = []
    source = course.source_set.filter(source_type=4).all()
    for i in source:
        OthersList.append([i.source_name, i.source_user.name,
                           i.source_time.strftime("%Y-%m-%d %H:%M:%S")])
    OthersPage = Paginator(OthersList, 5)
    OthersPaginator = []
    for i in range(1, OthersPage.num_pages + 1):
        for j in OthersPage.page(i):
            tmp.append(OthersPage.page(i))
            OthersPaginator.append(tmp)
        tmp = []
    
    StudentNum = 4  # 本班学生总数
    StudentList = []
    students = course.userinfo_set.filter(user_type=1).all()

    StudentList = [['3150100654', '薛伟', '2015', '计算机科学与技术学院', '软件工程', '645658325@qq.com', '18143465569'],
                   ['3150101234', '王泽杰', '2015', '计算机科学与技术学院',
                       '软件工程', '789452405@qq.com', '18143485594'],
                   ['3150105248', '陈立华', '2015', '计算机科学与技术学院',
                       '软件工程', '548123475@qq.com', '18143465587'],
                   ['3150102259', '梁杰', '2015', '计算机科学与技术学院', '软件工程', '785425910@qq.com', '18143454424'], ]
    
    TaList = [['3140101111', '李刚', '计算机科学与技术学院', '软件工程', '789524512@qq.com', '1504158534'],
              ['3140102222', '李明', '计算机科学与技术学院', '软件工程', '18888@qq.com', '18547186253'],
              ['3140103333', '小明', '计算机科学与技术学院', '软件工程', '18888@qq.com', '13357628512'], ]
    return render(request, 'teacher/teacher_course.html', {'PostList': PostList,
                                                           'NoticeList': NoticeList, 'unreadNotice': unreadNotice,
                                                           'HwList': HwList, 'unsubmitHw': unsubmitHw,
                                                           'PPTPage': PPTPage, 'PPTPaginator': PPTPaginator,
                                                           'PDFPage': PDFPage, 'PDFPaginator': PDFPaginator,
                                                           'MediaPage': MediaPage, 'MediaPaginator': MediaPaginator,
                                                           'OthersPage': OthersPage,
                                                           'OthersPaginator': OthersPaginator,
                                                           'StudentNum': StudentNum, 'StudentList': StudentList,
                                                           'TaList': TaList,
                                                           'courseid': courseid,
                                                           'time': json.dumps(coursetime)})


@user_passes_test(teachercheck, login_url="/login")
def hw(request, courseid):
    StudentNum = 50  # 学生总数
    SubmitNum = 20  # 已提交人数
    return render(request, 'teacher/teacher_hw.html', {'StudentNum': StudentNum,
                                                       'SubmitNum': SubmitNum})

@user_passes_test(teachercheck, login_url="/login")
def message(request, courseid):
    History = [['/static/img/kk.png', '吴朝晖', '2017/12/12, 20:00:00',
                '网吧走起网吧走起网吧走起网吧走起网吧走起网吧走起网吧走起网吧走起网吧走起网吧走起网吧走起网吧走起网吧走起网吧走起'],
               ['/static/img/zju.jpg', '王泽杰', '2017/12/14, 20:00:00', '不去']]
    return render(request, 'teacher/message.html', {'History': History})


@user_passes_test(teachercheck, login_url="/login")
def new_hw(request, courseid):
    return render(request, 'teacher/new_hw.html')


@user_passes_test(teachercheck, login_url="/login")
def mark_hw(request):
    return render(request, 'teacher/mark_hw.html')


@user_passes_test(teachercheck, login_url="/login")
def teacher_forum(request):
    tmp = []
    PostName = '摸鱼求约'  # 对应资源的名称
    PostList = [['/static/Semantic-UI-master/examples/assets/images/avatar/tom.jpg', '邢卫', '教师', '垃圾网站',
                 '2017/12/12, 20:00:00', '1'],
                ['/static/Semantic-UI-master/examples/assets/images/avatar/tom.jpg', '邢卫', '教师', '垃圾网站',
                 '2017/12/12, 20:00:00', '2'],
                ['/static/Semantic-UI-master/examples/assets/images/avatar/tom.jpg', '游客', '游客', '垃圾网站',
                 '2017/12/12, 20:00:00', '3'],
                ['/static/Semantic-UI-master/examples/assets/images/avatar/tom.jpg', '邢卫', '游客', '垃圾网站',
                 '2017/12/12, 20:00:00', '4'],
                ['/static/Semantic-UI-master/examples/assets/images/avatar/tom.jpg', '邢卫', '教师', '垃圾网站',
                 '2017/12/12, 20:00:00', '5'],
                ['/static/Semantic-UI-master/examples/assets/images/avatar/tom.jpg', '邢卫', '教师', '垃圾网站',
                 '2017/12/12, 20:00:00', '6'],
                ['/static/Semantic-UI-master/examples/assets/images/avatar/tom.jpg', '游客', '游客', '垃圾网站',
                 '2017/12/12, 20:00:00', '7'],
                ['/static/Semantic-UI-master/examples/assets/images/avatar/tom.jpg', '邢卫', '游客', '垃圾网站',
                 '2017/12/12, 20:00:00', '7'],
                ['/static/Semantic-UI-master/examples/assets/images/avatar/tom.jpg', '邢卫', '教师', '垃圾网站',
                 '2017/12/12, 20:00:00', '9'],
                ['/static/Semantic-UI-master/examples/assets/images/avatar/tom.jpg', '邢卫', '教师', '垃圾网站',
                 '2017/12/12, 20:00:00', '10'],
                ['/static/Semantic-UI-master/examples/assets/images/avatar/tom.jpg', '游客', '游客', '垃圾网站',
                 '2017/12/12, 20:00:00', '11'],
                ['/static/Semantic-UI-master/examples/assets/images/avatar/tom.jpg', '邢卫', '游客', '垃圾网站',
                 '2017/12/12, 20:00:00', '12'],
                ]
    PostPage = Paginator(PostList, 10)
    PostPaginator = []
    for i in range(1, PostPage.num_pages + 1):
        for j in PostPage.page(i):
            tmp.append(PostPage.page(i))
        PostPaginator.append(tmp)
        tmp = []
    return render(request, 'teacher/teacher_forum.html', {'PostPage': PostPage,
                                                          'PostPaginator': PostPaginator,
                                                          'PostName': PostName})


@user_passes_test(teachercheck, login_url="/login")
def teacher_resource_comment(request):
    tmp = []
    ResourceName = 'uml.pdf'  # 对应资源的名称
    CommentList = [['/static/Semantic-UI-master/examples/assets/images/avatar/tom.jpg', '邢卫', '教师', '垃圾网站',
                    '2017/12/12, 20:00:00', '1'],
                   ['/static/Semantic-UI-master/examples/assets/images/avatar/tom.jpg', '邢卫', '教师', '垃圾网站',
                    '2017/12/12, 20:00:00', '2'],
                   ['/static/Semantic-UI-master/examples/assets/images/avatar/tom.jpg', '游客', '游客', '垃圾网站',
                    '2017/12/12, 20:00:00', '3'],
                   ['/static/Semantic-UI-master/examples/assets/images/avatar/tom.jpg', '邢卫', '游客', '垃圾网站',
                    '2017/12/12, 20:00:00', '4'],
                   ['/static/Semantic-UI-master/examples/assets/images/avatar/tom.jpg', '邢卫', '教师', '垃圾网站',
                    '2017/12/12, 20:00:00', '5'],
                   ['/static/Semantic-UI-master/examples/assets/images/avatar/tom.jpg', '邢卫', '教师', '垃圾网站',
                    '2017/12/12, 20:00:00', '6'],
                   ['/static/Semantic-UI-master/examples/assets/images/avatar/tom.jpg', '游客', '游客', '垃圾网站',
                    '2017/12/12, 20:00:00', '7'],
                   ['/static/Semantic-UI-master/examples/assets/images/avatar/tom.jpg', '邢卫', '游客', '垃圾网站',
                    '2017/12/12, 20:00:00', '7'],
                   ['/static/Semantic-UI-master/examples/assets/images/avatar/tom.jpg', '邢卫', '教师', '垃圾网站',
                    '2017/12/12, 20:00:00', '9'],
                   ['/static/Semantic-UI-master/examples/assets/images/avatar/tom.jpg', '邢卫', '教师', '垃圾网站',
                    '2017/12/12, 20:00:00', '10'],
                   ['/static/Semantic-UI-master/examples/assets/images/avatar/tom.jpg', '游客', '游客', '垃圾网站',
                    '2017/12/12, 20:00:00', '11'],
                   ['/static/Semantic-UI-master/examples/assets/images/avatar/tom.jpg', '邢卫', '游客', '垃圾网站',
                    '2017/12/12, 20:00:00', '12'],
                   ]
    CommentPage = Paginator(CommentList, 10)
    CommentPaginator = []
    for i in range(1, CommentPage.num_pages + 1):
        for j in CommentPage.page(i):
            tmp.append(CommentPage.page(i))
        CommentPaginator.append(tmp)
        tmp = []
    return render(request, 'teacher/teacher_resource_comment.html', {'ResourceName': ResourceName,
                                                                     'CommentPage': CommentPage,
                                                                     'CommentPaginator': CommentPaginator})


@user_passes_test(teachercheck, login_url="/login")
def addta(request):
    return render(request, 'teacher/add_ta.html')

@user_passes_test(teachercheck, login_url="/login")
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/")
