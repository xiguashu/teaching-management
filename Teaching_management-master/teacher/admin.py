from django.contrib import admin
from teacher.models import UserInfo, TeacherInfo, StudentInfo, ManagerInfo, CourseInfo, \
                    CourseTime, Homework, MultipleChoice, ShortAnswer, HwOfCourse, \
                    StudentAnswer, HwGrade, ForumList, PostReply, Source, Message, \
                    Announcement, Customer, IsRead, HwSubmit,Liuyan

# Register your models here.
admin.site.register([UserInfo, TeacherInfo, StudentInfo, ManagerInfo, CourseInfo, \
                    CourseTime, Homework, MultipleChoice, ShortAnswer, HwOfCourse, \
                    StudentAnswer, HwGrade, ForumList, PostReply, Source, Message, \
                    Announcement, Customer, IsRead, HwSubmit,Liuyan])
