from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.
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
    # 课程表，应统计每门课程未读通知+未提交的作业数量
    CoursesList = [['软件需求工程', ['邢卫', '刘玉生'], ['周一6，7，8'], ['玉泉曹光彪西-503', '玉泉教7-304(多)'], '专业课', '2', '1', '1'],
                   ['操作系统原理', ['伍赛', '邢卫'], ['周一6，7，8'], ['玉泉曹光彪西-503', '玉泉教7-304(多)'], '专业课', '1', '2', '2'],
                   ['软件工程管理', ['金波', '邢卫'], ['周一6，7，8'], ['玉泉曹光彪西-503', '玉泉教7-304(多)'], '专业课', '1', '3', '3'],
                   ['计算机网络', ['陆魁军', '邢卫'], ['周一6，7，8'], ['玉泉曹光彪西-503', '玉泉教7-304(多)'], '专业课', '0', '4', ' 2'], ]
    liuyanList = [['/static/Semantic-UI-master/examples/assets/images/avatar/tom.jpg', '邢卫', '教师', '垃圾网站',
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
    liuyanPage = Paginator(liuyanList, 10)
    liuyanPaginator = []
    for i in range(1, liuyanPage.num_pages + 1):
        for j in liuyanPage.page(i):
            tmp.append(liuyanPage.page(i))
        liuyanPaginator.append(tmp)
        tmp = []
    return render(request, 'ta/index.html', {'GlobalNoticeList': GlobalNoticeList,
                                                  'unreadGlobalNotice': unreadGlobalNotice,
                                                  'CoursesList': CoursesList,
                                                  'liuyanPage': liuyanPage, 'liuyanPaginator': liuyanPaginator})


def course(request):
    tmp = []
    PostList = [['摸鱼求约', '邢卫', '2017/12/12, 20:00:00', '', '', '0'],
                ['摸鱼求约', '邢卫', '2017/12/12, 20:00:00', '', '', '0'],
                ['摸鱼求约', '邢卫', '2017/12/12, 20:00:00', '', '', '0']]
    # 通知列表设有一个标志位来标志是否已读，0为未读，1为已读，前端点击了通知详情按钮后，应该到后台将状态设置为已读
    NoticeList = [['1', '作业1ddl已到', '2017/12/12, 20:00:00', '作业1ddl已到，请您及时批改'],
                  ['1', '作业2ddl已到', '2017/12/13, 20:00:00', '作业2ddl已到，请您及时批改'],
                  ['0', '作业3ddl已到', '2017/12/14, 20:00:00', '作业3ddl已到，请您及时批改'],
                  ['0', '作业4ddl已到', '2017/12/14, 20:00:00', '作业4ddl已到，请您及时批改']]
    unreadNotice = 0
    for i in NoticeList:
        if i[0] == '0':
            unreadNotice += 1
    # 作业列表设有一个标志位来标志是否已批改，0为未提交，1为已提交，前端批改作业后，应该到后台将状态设置为已提交；
    # 应能正确指导前端进行页面跳转
    HwList = [['1', '作业1', '2017/12/12, 20:00:00'],
              ['1', '作业2', '2017/12/13, 20:00:00'],
              ['0', '作业3', '2017/12/14, 20:00:00']]
    unsubmitHw = 0
    for i in HwList:
        if i[0] == '0':
            unsubmitHw += 1
    # 资源列表
    PPTList = [['uml.ppt', '刘玉生', '2017/12/12, 20:00:00'],
               ['5.ppt', '刘玉生', '2017/12/12, 20:00:00'],
               ['操作系统概念.ppt', '王泽杰', '2017/12/12, 20:00:00'],
               ['软件需求.ppt', '邢卫', '2017/12/12, 20:00:00'],
               ['作业成绩.ppt', '邢卫', '2017/12/12, 20:00:00'],
               ['uml.ppt', '刘生', '2017/12/12, 20:00:00'],
               ['5.ppt', '刘生', '2017/12/12, 20:00:00'],
               ['操作系统概念.ppt', '王泽杰', '2017/12/12, 20:00:00'],
               ['软件需求.ppt', '邢卫', '2017/12/12, 20:00:00'],
               ['作业成绩.ppt', '邢卫', '2017/12/12, 20:00:00']]
    PPTPage = Paginator(PPTList, 5)
    PPTPaginator = []
    for i in range(1, PPTPage.num_pages + 1):
        for j in PPTPage.page(i):
            tmp.append(PPTPage.page(i))
        PPTPaginator.append(tmp)
        tmp = []
    PDFList = [['uml.pdf', '刘玉生', '2017/12/12, 20:00:00'],
               ['5.pdf', '刘玉生', '2017/12/12, 20:00:00'],
               ['操作系统概念.pdf', '王泽杰', '2017/12/12, 20:00:00'],
               ['软件需求.pdf', '邢卫', '2017/12/12, 20:00:00'],
               ['作业成绩.pdf', '邢卫', '2017/12/12, 20:00:00'],
               ['作业成绩.pdf', '邢卫', '2017/12/12, 20:00:00']]
    PDFPage = Paginator(PDFList, 5)
    PDFPaginator = []
    for i in range(1, PDFPage.num_pages + 1):
        for j in PDFPage.page(i):
            tmp.append(PDFPage.page(i))
        PDFPaginator.append(tmp)
        tmp = []
    MediaList = [['uml.mp4', '刘玉生', '2017/12/12, 20:00:00'],
                 ['5.mp4', '刘玉生', '2017/12/12, 20:00:00'],
                 ['操作系统概念.mp4', '王泽杰', '2017/12/12, 20:00:00'],
                 ['软件需求.mp4', '邢卫', '2017/12/12, 20:00:00'],
                 ['作业成绩.mp4', '邢卫', '2017/12/12, 20:00:00']]
    MediaPage = Paginator(MediaList, 5)
    MediaPaginator = []
    for i in range(1, MediaPage.num_pages + 1):
        for j in MediaPage.page(i):
            tmp.append(MediaPage.page(i))
            MediaPaginator.append(tmp)
        tmp = []
    OthersList = [['uml.doc', '刘玉生', '2017/12/12, 20:00:00'],
                  ['5.docx', '刘玉生', '2017/12/12, 20:00:00'],
                  ['操作系统概念.doc', '王泽杰', '2017/12/12, 20:00:00'],
                  ['软件需求.xls', '邢卫', '2017/12/12, 20:00:00'],
                  ['作业成绩.docx', '邢卫', '2017/12/12, 20:00:00']]
    OthersPage = Paginator(OthersList, 5)
    OthersPaginator = []
    for i in range(1, OthersPage.num_pages + 1):
        for j in OthersPage.page(i):
            tmp.append(OthersPage.page(i))
            OthersPaginator.append(tmp)
        tmp = []
    StudentNum = 50 #本班学生总数
    StudentList = [['315010', '王泽杰', '2015', '计算机科学与技术学院', '软件工程', '18888@qq.com', '10086'],
                   ['315010', '王泽杰', '2015', '计算机科学与技术学院', '软件工程', '18888@qq.com', '10086'],
                   ['315010', '王泽杰', '2015', '计算机科学与技术学院', '软件工程', '18888@qq.com', '10086'],
                   ['315010', '王泽杰', '2015', '计算机科学与技术学院', '软件工程', '18888@qq.com', '10086'],]
    return render(request, 'ta/ta_course.html', {'PostList': PostList,
                                                           'NoticeList': NoticeList, 'unreadNotice': unreadNotice,
                                                           'HwList': HwList, 'unsubmitHw': unsubmitHw,
                                                           'PPTPage': PPTPage, 'PPTPaginator': PPTPaginator,
                                                           'PDFPage': PDFPage, 'PDFPaginator': PDFPaginator,
                                                           'MediaPage': MediaPage, 'MediaPaginator': MediaPaginator,
                                                           'OthersPage': OthersPage,
                                                           'OthersPaginator': OthersPaginator,
                                                           'StudentNum': StudentNum, 'StudentList': StudentList})


def hw(request):
    StudentNum = 50 #学生总数
    SubmitNum = 20 #已提交人数
    return render(request, 'teacher/teacher_hw.html', {'StudentNum': StudentNum,
                                                       'SubmitNum': SubmitNum})
def message(request):
    History = [['/static/img/kk.png', '吴朝晖', '2017/12/12, 20:00:00', '网吧走起网吧走起网吧走起网吧走起网吧走起网吧走起网吧走起网吧走起网吧走起网吧走起网吧走起网吧走起网吧走起网吧走起'],
               ['/static/img/zju.jpg', '王泽杰', '2017/12/14, 20:00:00', '不去']]
    return render(request, 'ta/message.html', {'History': History})

def new_hw(request):
    return render(request, 'ta/new_hw.html')


def mark_hw(request):
    return render(request, 'ta/mark_hw.html')


def ta_forum(request):
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
    return render(request, 'ta/ta_forum.html', {'PostPage': PostPage,
                                                          'PostPaginator': PostPaginator,
                                                          'PostName': PostName})


def ta_resource_comment(request):
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
    return render(request, 'ta/ta_resource_comment.html', {'ResourceName': ResourceName,
                                                                     'CommentPage': CommentPage,
                                                                     'CommentPaginator': CommentPaginator})
