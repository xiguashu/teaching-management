from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.

def index(request):
    tmp = []
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
    # 课程表，应统计每门课程未读通知、未完成作业、未阅读课件的数量
    CoursesList = [['软件需求工程', ['邢卫', '刘玉生'], ['周一6，7，8'], ['玉泉曹光彪西-503', '玉泉教7-304(多)'], '专业课'],
                   ['操作系统原理', ['伍赛'], ['周一6，7，8'], ['玉泉曹光彪西-503', '玉泉教7-304(多)'], '专业课'],
                   ['软件工程管理', ['金波'], ['周一，7，8'], ['玉泉曹光彪西-503', '玉泉教7-304(多)'], '专业课'],
                   ['计算机网络', ['陆魁军'], ['周一6，7，8'], ['玉泉曹光彪西-503', '玉泉教7-304(多)'], '专业课'],
                   ['计算机网络', ['陆魁军'], ['周一，7，8'], ['玉泉曹光彪西-503', '玉泉教7-304(多)'], '专业课'],
                   ['计算机网络', ['陆魁军'], ['周一，7，8'], ['玉泉曹光彪西-503', '玉泉教7-304(多)'], '专业课'],
                   ['计算机网络', ['陆魁军'], ['周一6，7，8'], ['玉泉曹光彪西-503', '玉泉教7-304(多)'], '专业课'],
                   ['软件需求工程', ['邢卫', '刘玉生'], ['周一6，7，8'], ['玉泉曹光彪西-503', '玉泉教7-304(多)'], '专业课'],
                   ['操作系统原理', ['伍赛'], ['周一6，7，8'], ['玉泉曹光彪西-503', '玉泉教7-304(多)'], '专业课'],
                   ['软件工程管理', ['金波'], ['周一，7，8'], ['玉泉曹光彪西-503', '玉泉教7-304(多)'], '专业课'],
                   ['计算机网络', ['陆魁军'], ['周一6，7，8'], ['玉泉曹光彪西-503', '玉泉教7-304(多)'], '专业课'],
                   ['计算机网络', ['陆魁军'], ['周一，7，8'], ['玉泉曹光彪西-503', '玉泉教7-304(多)'], '专业课'],
                   ['计算机网络', ['陆魁军'], ['周一，7，8'], ['玉泉曹光彪西-503', '玉泉教7-304(多)'], '专业课'],
                   ['计算机网络', ['陆魁军'], ['周一6，7，8'], ['玉泉曹光彪西-503', '玉泉教7-304(多)'], '专业课'],
                   ]
    CoursesPage = Paginator(CoursesList, 10)
    CoursesPaginator = []
    for i in range(1, CoursesPage.num_pages + 1):
        for j in CoursesPage.page(i):
            tmp.append(CoursesPage.page(i))
        CoursesPaginator.append(tmp)
        tmp = []
    return render(request, 'visitor/index.html', {'liuyanPage': liuyanPage, 'liuyanPaginator': liuyanPaginator,
                                                  'CoursesList': CoursesList,
                                                  'CoursesPage': CoursesPage, 'CoursesPaginator': CoursesPaginator})

def course(request):
    return render(request, 'visitor/visitor_course.html')
