from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import auth
from django.contrib.auth.models import User
from django.db.models import Q
from teacher.models import UserInfo, TeacherInfo, StudentInfo, ManagerInfo, CourseInfo, \
                           CourseTime, Homework, MultipleChoice, ShortAnswer, HwOfCourse, \
                           StudentAnswer, HwGrade, ForumList, PostReply, Source, Message, \
    Announcement, Customer, IsRead, HwSubmit
import time, json

def studentcheck(user):
    try:
        if user.userinfo.user_type == 1:
            return True
    except:
        return False
    return False

# Create your views here.
@user_passes_test(studentcheck, login_url="/login")
def index(request):
    
    # 加载课程列表
    userCourse = request.user.userinfo.user_course.all()
    CoursesList = []
    for i in userCourse:
        singleCourse = [i.course_name, i.course_teacher.split(';'), i.course_time.split(
            ';'), i.course_pos.split(';'), i. course_type, '1', '2', '3', i.id]
        CoursesList.append(singleCourse)

    #### 缺少一个数量的统计
    # a = []
    # for i in userCourse:
    #     announcement = Announcement.objects.filter(announce_course = i)
    #     #a.append(len(announcement))
    #     for j in announcement:
    #         print(j.isread_set.all().filter(read_user=request.user.userinfo))
    #for i in a:
        #print(i)

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
    
    liuyanList = []
    leftmessage = Customer.objects.all()
    j = 1
    for i in leftmessage:
        liuyanList.append(
            ['/static/Semantic-UI-master/examples/assets/images/avatar/tom.jpg', '游客', '游客', i.customer_title + i.customer_content, i.customer_time.strftime("%Y-%m-%d %H:%M:%S"), j])
        j += 1

    tmp = []
    # 通知列表设有一个标志位来标志是否已读，0为未读，1为已读，前端点击了通知详情按钮后，应该到后台将状态设置为已读
    # GlobalNoticeList = [['1', '操作系统课程有新通知', '2017/12/12, 20:00:00', '作业1已发布，ddl为今晚10点'],
    #                     ['1', '计算机网络课程有新通知', '2017/12/13, 20:00:00', '作业2已发布，ddl为今晚10点'],
    #                     ['0', '软件需求工程课程有新通知', '2017/12/14, 20:00:00', '作业3已发布，ddl为今晚10点'],
    #                     ['0', '操作系统课程有新通知', '2017/12/14, 20:00:00', '作业4已发布，ddl为今晚10点']]
    unreadGlobalNotice = 0
    for i in GlobalNoticeList:
        if i[0] == '0':
            unreadGlobalNotice += 1
    # 课程表，应统计每门课程未读通知、未完成作业、未阅读课件的数量
    # CoursesList = [['软件需求工程', ['邢卫', '刘玉生'], ['周一6，7，8'], ['玉泉曹光彪西-503', '玉泉教7-304(多)'], '专业课', '2', '1', '1'],
    #                ['操作系统原理', ['伍赛'], ['周一6，7，8'], ['玉泉曹光彪西-503', '玉泉教7-304(多)'], '专业课', '1', '2', '2'],
    #                ['软件工程管理', ['金波'], ['周一，7，8'], ['玉泉曹光彪西-503', '玉泉教7-304(多)'], '专业课', '1', '3', '3'],
    #                ['计算机网络', ['陆魁军'], ['周一6，7，8'], ['玉泉曹光彪西-503', '玉泉教7-304(多)'], '专业课', '0', '4', ' 2'],
    #                ['计算机网络', ['陆魁军'], ['周一，7，8'], ['玉泉曹光彪西-503', '玉泉教7-304(多)'], '专业课', '0', '5', '3'],
    #                ['计算机网络', ['陆魁军'], ['周一，7，8'], ['玉泉曹光彪西-503', '玉泉教7-304(多)'], '专业课', '0', '6', '3'],
    #                ['计算机网络', ['陆魁军'], ['周一6，7，8'], ['玉泉曹光彪西-503', '玉泉教7-304(多)'], '专业课', '0', '7', '5'], ]
    # liuyanList = [['/static/Semantic-UI-master/examples/assets/images/avatar/tom.jpg', '邢卫', '教师', '垃圾网站',
    #                '2017/12/12, 20:00:00', '1'],
    #               ['/static/Semantic-UI-master/examples/assets/images/avatar/tom.jpg', '邢卫', '教师', '垃圾网站',
    #                '2017/12/12, 20:00:00', '2'],
    #               ['/static/Semantic-UI-master/examples/assets/images/avatar/tom.jpg', '游客', '游客', '垃圾网站',
    #                '2017/12/12, 20:00:00', '3'],
    #               ['/static/Semantic-UI-master/examples/assets/images/avatar/tom.jpg', '邢卫', '游客', '垃圾网站',
    #                '2017/12/12, 20:00:00', '4'],
    #               ['/static/Semantic-UI-master/examples/assets/images/avatar/tom.jpg', '邢卫', '教师', '垃圾网站',
    #                '2017/12/12, 20:00:00', '5'],
    #               ['/static/Semantic-UI-master/examples/assets/images/avatar/tom.jpg', '邢卫', '教师', '垃圾网站',
    #                '2017/12/12, 20:00:00', '6'],
    #               ['/static/Semantic-UI-master/examples/assets/images/avatar/tom.jpg', '游客', '游客', '垃圾网站',
    #                '2017/12/12, 20:00:00', '7'],
    #               ['/static/Semantic-UI-master/examples/assets/images/avatar/tom.jpg', '邢卫', '游客', '垃圾网站',
    #                '2017/12/12, 20:00:00', '7'],
    #               ['/static/Semantic-UI-master/examples/assets/images/avatar/tom.jpg', '邢卫', '教师', '垃圾网站',
    #                '2017/12/12, 20:00:00', '9'],
    #               ['/static/Semantic-UI-master/examples/assets/images/avatar/tom.jpg', '邢卫', '教师', '垃圾网站',
    #                '2017/12/12, 20:00:00', '10'],
    #               ['/static/Semantic-UI-master/examples/assets/images/avatar/tom.jpg', '游客', '游客', '垃圾网站',
    #                '2017/12/12, 20:00:00', '11'],
    #               ['/static/Semantic-UI-master/examples/assets/images/avatar/tom.jpg', '邢卫', '游客', '垃圾网站',
    #                '2017/12/12, 20:00:00', '12'],
    #               ]
    liuyanPage = Paginator(liuyanList, 10)
    liuyanPaginator = []
    for i in range(1, liuyanPage.num_pages + 1):
        for j in liuyanPage.page(i):
            tmp.append(liuyanPage.page(i))
        liuyanPaginator.append(tmp)
        tmp = []
    return render(request, 'student/index.html', {'GlobalNoticeList': GlobalNoticeList,
                                                  'unreadGlobalNotice': unreadGlobalNotice,
                                                  'CoursesList': CoursesList,
                                                  'liuyanPage': liuyanPage, 'liuyanPaginator': liuyanPaginator})


@user_passes_test(studentcheck, login_url="/login")
def course(request, id):
    # id = request.GET['id']
    course = CourseInfo.objects.get(id=id)
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
    #### 缺少一个最后回复的显示
    tmp = []
    # 论坛贴子列表
    # PostList = [['摸鱼求约', '邢卫', '2017/12/12, 20:00:00', '', '', '0'],
    #             ['摸鱼求约', '邢卫', '2017/12/12, 20:00:00', '', '', '0'],
    #             ['摸鱼求约', '邢卫', '2017/12/12, 20:00:00', '', '', '0'],
    #             ['摸鱼求约', '邢卫', '2017/12/12, 20:00:00', '', '', '0'],
    #             ['摸鱼求约', '邢卫', '2017/12/12, 20:00:00', '', '', '0'],
    #             ['摸鱼求约', '邢卫', '2017/12/12, 20:00:00', '', '', '0'],
    #             ['摸鱼求约', '邢卫', '2017/12/12, 20:00:00', '', '', '0'],
    #             ['摸鱼求约', '邢卫', '2017/12/12, 20:00:00', '', '', '0'],
    #             ['摸鱼求约', '邢卫', '2017/12/12, 20:00:00', '', '', '0'],
    #             ['摸鱼求约', '邢卫', '2017/12/12, 20:00:00', '', '', '0'],
    #             ['摸鱼', '邢卫', '2017/12/12, 20:00:00', '', '', '0'],
    #             ['摸鱼', '邢卫', '2017/12/12, 20:00:00', '', '', '0'],
    #             ]
    PostPage = Paginator(PostList, 10)
    PostPaginator = []
    for i in range(1, PostPage.num_pages + 1):
        for j in PostPage.page(i):
            tmp.append(PostPage.page(i))
        PostPaginator.append(tmp)
        tmp = []

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

    #### 缺少对应课程的通知

    # NoticeList = [['1', '作业1已发布', '2017/12/12, 20:00:00', '作业1已发布，ddl为今晚10点'],
    #               ['1', '作业2已发布', '2017/12/13, 20:00:00', '作业2已发布，ddl为今晚10点'],
    #               ['0', '作业3已发布', '2017/12/14, 20:00:00', '作业3已发布，ddl为今晚10点'],
    #               ['0', '作业4已发布', '2017/12/14, 20:00:00', '作业4已发布，ddl为今晚10点']]
    unreadNotice = 0
    for i in NoticeList:
        if i[0] == '0':
            unreadNotice += 1
    # 作业列表设有一个标志位来标志是否已提交，0为未提交，1为已提交，前端提交作业后，应该到后台将状态设置为已提交
    # 应能正确指导前端进行页面跳转
    
    HwList = []
    homework = course.homework_set.all()
    for i in homework:
        try:
            status = i.hwgrade_set.get(id=i.id)
            HwList.append(['1', i.homework_name, i.homework_deadline, i.id])
        except:
            HwList.append(['0', i.homework_name, i.homework_deadline, i.id])

    # HwList = [['1', '作业1', '2017/12/12, 20:00:00'],
    #           ['1', '作业2', '2017/12/13, 20:00:00'],
    #           ['0', '作业3', '2017/12/14, 20:00:00']]

    unsubmitHw = 0
    for i in HwList:
        if i[0] == '0':
            unsubmitHw += 1
    
    TeacherList = []
    teacher = course.userinfo_set.filter(user_type=2)
    for i in teacher:
        TeacherList.append([i.teacherinfo.teacher_name, '教授',
                            '计算机科学与技术学院', i.teacherinfo.teacher_email, i.teacherinfo.teacher_phone, i.user.id])

    # 教师信息表
    # TeacherList = [['邢卫', '教授', '计算机科学与技术学院', '10086@zju.edu.cn', '18888888888'],
    #                ['邢卫', '教授', '计算机科学与技术学院', '10086@zju.edu.cn', '18888888888'],
    #                ]
    # 资源列表

    PPTList = []
    source = course.source_set.filter(source_type=1).all()
    for i in source:
        PPTList.append([i.source_name, i.source_user.name,
                        i.source_time.strftime("%Y-%m-%d %H:%M:%S")])
    # PPTList = [['uml.ppt', '刘玉生', '2017/12/12, 20:00:00'],
    #            ['5.ppt', '刘玉生', '2017/12/12, 20:00:00'],
    #            ['操作系统概念.ppt', '王泽杰', '2017/12/12, 20:00:00'],
    #            ['软件需求.ppt', '邢卫', '2017/12/12, 20:00:00'],
    #            ['作业成绩.ppt', '邢卫', '2017/12/12, 20:00:00'],
    #            ['uml.ppt', '刘生', '2017/12/12, 20:00:00'],
    #            ['5.ppt', '刘生', '2017/12/12, 20:00:00'],
    #            ['操作系统概念.ppt', '王泽杰', '2017/12/12, 20:00:00'],
    #            ['软件需求.ppt', '邢卫', '2017/12/12, 20:00:00'],
    #            ['作业成绩.ppt', '邢卫', '2017/12/12, 20:00:00']]
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
    # PDFList = [['uml.pdf', '刘玉生', '2017/12/12, 20:00:00'],
    #            ['5.pdf', '刘玉生', '2017/12/12, 20:00:00'],
    #            ['操作系统概念.pdf', '王泽杰', '2017/12/12, 20:00:00'],
    #            ['软件需求.pdf', '邢卫', '2017/12/12, 20:00:00'],
    #            ['作业成绩.pdf', '邢卫', '2017/12/12, 20:00:00'],
    #            ['作业成绩.pdf', '邢卫', '2017/12/12, 20:00:00']]
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
    # MediaList = [['uml.mp4', '刘玉生', '2017/12/12, 20:00:00'],
    #              ['5.mp4', '刘玉生', '2017/12/12, 20:00:00'],
    #              ['操作系统概念.mp4', '王泽杰', '2017/12/12, 20:00:00'],
    #              ['软件需求.mp4', '邢卫', '2017/12/12, 20:00:00'],
    #              ['作业成绩.mp4', '邢卫', '2017/12/12, 20:00:00']]
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
    # OthersList = [['uml.doc', '刘玉生', '2017/12/12, 20:00:00'],
    #               ['5.docx', '刘玉生', '2017/12/12, 20:00:00'],
    #               ['操作系统概念.doc', '王泽杰', '2017/12/12, 20:00:00'],
    #               ['软件需求.xls', '邢卫', '2017/12/12, 20:00:00'],
    #               ['作业成绩.docx', '邢卫', '2017/12/12, 20:00:00']]
    OthersPage = Paginator(OthersList, 5)
    OthersPaginator = []
    for i in range(1, OthersPage.num_pages + 1):
        for j in OthersPage.page(i):
            tmp.append(OthersPage.page(i))
            OthersPaginator.append(tmp)
        tmp = []
    return render(request, 'student/student_courses.html', {'PostList': PostList,
                                                            'PostPage': PostPage, 'PostPaginator': PostPaginator,
                                                            'NoticeList': NoticeList, 'unreadNotice': unreadNotice,
                                                            'HwList': HwList, 'unsubmitHw': unsubmitHw,
                                                            'TeacherList': TeacherList,
                                                            'PPTPage': PPTPage, 'PPTPaginator': PPTPaginator,
                                                            'PDFPage': PDFPage, 'PDFPaginator': PDFPaginator,
                                                            'MediaPage': MediaPage, 'MediaPaginator': MediaPaginator,
                                                            'OthersPage': OthersPage,
                                                            'OthersPaginator': OthersPaginator,
                                                            'time': json.dumps(coursetime)})


@user_passes_test(studentcheck, login_url="/login")
def hw(request, hwid):
    # 提交记录显示某次提交或保存的时间，保存为0，提交为1

    SubmitRecord = []
    homework = Homework.objects.get(id=hwid)
    submit = homework.hwsubmit_set.filter()
    for i in submit:
        SubmitRecord.append([i.submit_time.strftime("%Y-%m-%d %H:%M:%S"), i.submit_status])
    # SubmitRecord = [['2017/12/12, 20:00:00', 0],
    #                 ['2017/12/13, 20:00:00', 0],
    #                 ['2017/12/14, 20:00:00', 1]]
    return render(request, 'student/student_hw.html', {'SubmitRecord': SubmitRecord})


@user_passes_test(studentcheck, login_url="/login")
def forum(request, id):
    tmp = []

    post = ForumList.objects.get(id=id)
    reply = post.postreply_set.all()

    PostName = post.forum_title
    j = 0
    PostList = []
    for i in reply:
        j += 1
        if i.reply_user.user_type == 1:
            identity = '学生'
        elif i.reply_user.user_type == 2:
            identity = '教师'
        PostList.append(
            ['/static/Semantic-UI-master/examples/assets/images/avatar/tom.jpg', i.reply_user.name, identity, i.reply_content, i.reply_time.strftime("%Y-%m-%d %H:%M:%S"), j])
    # PostList = [['/static/Semantic-UI-master/examples/assets/images/avatar/tom.jpg', '邢卫', '教师', '垃圾网站',
    #              '2017/12/12, 20:00:00', '1'],
    #             ['/static/Semantic-UI-master/examples/assets/images/avatar/tom.jpg', '邢卫', '教师', '垃圾网站',
    #              '2017/12/12, 20:00:00', '2'],
    #             ['/static/Semantic-UI-master/examples/assets/images/avatar/tom.jpg', '游客', '游客', '垃圾网站',
    #              '2017/12/12, 20:00:00', '3'],
    #             ['/static/Semantic-UI-master/examples/assets/images/avatar/tom.jpg', '邢卫', '游客', '垃圾网站',
    #              '2017/12/12, 20:00:00', '4'],
    #             ['/static/Semantic-UI-master/examples/assets/images/avatar/tom.jpg', '邢卫', '教师', '垃圾网站',
    #              '2017/12/12, 20:00:00', '5'],
    #             ['/static/Semantic-UI-master/examples/assets/images/avatar/tom.jpg', '邢卫', '教师', '垃圾网站',
    #              '2017/12/12, 20:00:00', '6'],
    #             ['/static/Semantic-UI-master/examples/assets/images/avatar/tom.jpg', '游客', '游客', '垃圾网站',
    #              '2017/12/12, 20:00:00', '7'],
    #             ['/static/Semantic-UI-master/examples/assets/images/avatar/tom.jpg', '邢卫', '游客', '垃圾网站',
    #              '2017/12/12, 20:00:00', '7'],
    #             ['/static/Semantic-UI-master/examples/assets/images/avatar/tom.jpg', '邢卫', '教师', '垃圾网站',
    #              '2017/12/12, 20:00:00', '9'],
    #             ['/static/Semantic-UI-master/examples/assets/images/avatar/tom.jpg', '邢卫', '教师', '垃圾网站',
    #              '2017/12/12, 20:00:00', '10'],
    #             ['/static/Semantic-UI-master/examples/assets/images/avatar/tom.jpg', '游客', '游客', '垃圾网站',
    #              '2017/12/12, 20:00:00', '11'],
    #             ['/static/Semantic-UI-master/examples/assets/images/avatar/tom.jpg', '邢卫', '游客', '垃圾网站',
    #              '2017/12/12, 20:00:00', '12'],
    #             ]
    PostPage = Paginator(PostList, 10)
    PostPaginator = []
    for i in range(1, PostPage.num_pages + 1):
        for j in PostPage.page(i):
            tmp.append(PostPage.page(i))
        PostPaginator.append(tmp)
        tmp = []
    return render(request, 'student/student_forum.html', {'PostPage': PostPage,
                                                          'PostPaginator': PostPaginator,
                                                          'PostName': PostName})


@user_passes_test(studentcheck, login_url="/login")
def student_resource_comment(request):
    tmp = []


    ResourceName = 'uml.pdf'  #对应资源的名称
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
    return render(request, 'student/student_resource_comment.html', {'ResourceName': ResourceName,
                                                                     'CommentPage': CommentPage,
                                                                     'CommentPaginator': CommentPaginator,
                                                                     'id': id})


@user_passes_test(studentcheck, login_url="/login")
def message(request, messageid):

    user1 = User.objects.get(id=messageid)
    id1 = UserInfo.objects.get(user=user1)
    id2 = request.user.userinfo
    name = User.objects.get(id=messageid).userinfo.name
    messages = Message.objects.filter(Q(message_sender=id1, message_receiver=id2) | Q(message_receiver=id1, message_sender=id2)).order_by("message_time")
    History = []
    # name = '吴朝晖'  #私信的对象
    for i in messages:
        if i.message_sender == id1:
            History.append(['/static/Semantic-UI-master/examples/assets/images/avatar/tom.jpg', id1.name,
                        i.message_time.strftime("%Y-%m-%d %H:%M:%S"), i.message_content])
        else:
            History.append(['/static/img/kk.png', id2.name,
                        i.message_time.strftime("%Y-%m-%d %H:%M:%S"), i.message_content])
    # History = [['/static/img/kk.png', '吴朝晖', '2017/12/12, 20:00:00', '网吧走起网吧走起网吧走起网吧走起网吧走起网吧走起网吧走起网吧走起网吧走起网吧走起网吧走起网吧走起网吧走起网吧走起'],
    #            ['/static/img/zju.jpg', '王泽杰', '2017/12/14, 20:00:00', '不去']]
    return render(request, 'student/message.html', {'name': name,
                                                    'History': History})


@user_passes_test(studentcheck, login_url="/login")
def ret(request):
    return render(request, 'tmp.html')


@user_passes_test(studentcheck, login_url="/login")
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/")
