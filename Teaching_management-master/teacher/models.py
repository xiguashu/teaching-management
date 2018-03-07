from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.
class UserInfo(models.Model):

    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, null=True)
    user_type = models.IntegerField()
    user_course = models.ManyToManyField('CourseInfo')

    def __str__(self):
        return "{}:{}".format(self.user, self.user_type)

    @classmethod
    def get_type(user_type):
        if user_type == 1:
            return "学生"
        elif user_type == 2:
            return "老师"
        elif user_type == 3:
            return "管理员"

class TeacherInfo(models.Model):

    teacher_info = models.OneToOneField(UserInfo, primary_key=True, on_delete=models.CASCADE)
    teacher_id = models.CharField(max_length=15, null=True)
    teacher_name = models.CharField(max_length=20, null=True)
    teacher_department = models.CharField(max_length=30, null=True)
    teacher_phone = models.CharField(max_length=15, null=True)
    teacher_email = models.EmailField(null=True)

    def __str__(self):
        return "teacher info:{},id:{},name:{},department:{},phone:{},email:{}".format(self.teacher_info, self.teacher_id, self.teacher_name, self.teacher_department, self.teacher_phone, self.teacher_email)

class StudentInfo(models.Model):

    student_info = models.OneToOneField(UserInfo, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=11, null=True)
    student_name = models.CharField(max_length=20, null=True)
    student_college = models.CharField(max_length=30, null=True)
    student_class = models.CharField(max_length=30, null=True)
    student_phone = models.CharField(max_length=11, null=True)
    student_email = models.EmailField(null=True)

    def __str__(self):
        return "student info:{}, id:{}, name:{}, college:{}, class:{}, phone:{}, email:{}".format(self.student_info, self.student_id, self.student_name, self.student_college, self.student_class, self.student_phone, self.student_email)

class ManagerInfo(models.Model):

    manager_info = models.OneToOneField(UserInfo, on_delete=models.CASCADE)
    manager_id = models.CharField(max_length=11, null=True)
    manager_name = models.CharField(max_length=20, null=True)
    manager_job = models.CharField(max_length=40, null=True)
    manager_phone = models.CharField(max_length=15, null=True)
    manager_email = models.EmailField(null=True)

    def __str__(self):
        return "manager info:{}, id:{}, name:{}, job:{}, phone:{}, email:{}".format(self.manager_info, self.manager_id, self.manager_name, self.manager_job, self.manager_phone, self.manager_email)

class CourseInfo(models.Model):

    course_name = models.CharField(max_length=50, null=True)
    course_syllabus = models.TextField(null=True)
    course_teacher = models.CharField(max_length=50, null=True)
    course_type = models.CharField(max_length=50, null=True)
    course_time = models.CharField(max_length=30, null=True)
    course_pos = models.CharField(max_length=30, null=True)
    course_exam=models.DateTimeField(null=True)
    course_id=models.CharField(max_length=100,null=True)
    course_depart=models.CharField(max_length=20,null=True)
    course_credits=models.FloatField(null=True)


class CourseTime(models.Model):

    course_info = models.ForeignKey('CourseInfo', on_delete=models.CASCADE)
    course_date = models.DateField(null=True)
    course_time = models.CharField(max_length=50, null=True)
    course_assignment = models.CharField(max_length=60, null=True)
    course_position = models.CharField(max_length=30, null=True)

    def __str__(self):
        return "coursetime info:{}, date:{}, time:{}, assign:{}, pos:{}".format(self.course_info, self.course_date, self.course_time, self.course_assignment, self.course_position)

class Homework(models.Model):

    homework_name = models.CharField(max_length=50, null=True)
    homework_description = models.TextField(null=True)
    homework_course = models.ForeignKey('CourseInfo', on_delete=models.CASCADE)
    homework_edit_time = models.DateTimeField(null=True)
    homework_deadline = models.DateTimeField(null=True)
    homework_score = models.IntegerField(null=True)

    def __str__(self):
        return "homework name:{}, description:{}, course:{}, edit:{}, deadline:{}, score:{}".format(self.homework_name, self.homework_description, self.homework_course, self.homework_edit_time, self.homework_deadline, self.homework_score)

class MultipleChoice(models.Model):

    choice_content = models.TextField(null=True)
    choice_A = models.CharField(max_length=200, null=True)
    choice_B = models.CharField(max_length=200, null=True)
    choice_C = models.CharField(max_length=200, null=True)
    choice_D = models.CharField(max_length=200, null=True)
    choice_answer = models.IntegerField(null=True)
    choice_score = models.IntegerField(null=True)

    def __str__(self):
        return "choice content:{}, A:{}, B:{}, C:{}, D:{}, answer:{}, score:{}".format(self.choice_content, self.choice_A, self.choice_B, self.choice_C, self.choice_D, self.choice_answer, self.choice_score)

class ShortAnswer(models.Model):

    short_content = models.TextField(null=True)
    short_answer = models.CharField(max_length=200, null=True)
    short_score = models.IntegerField(null=True)

    def __str__(self):
        return "short content:{}, answer:{}, score:{}".format(self.short_content, self.short_answer, self.short_score)

class HwOfCourse(models.Model):

    question_type = models.IntegerField()
    question_short = models.ForeignKey('ShortAnswer', related_name='short', on_delete=models.CASCADE, null=True, default=None)
    question_choice = models.ForeignKey('MultipleChoice', related_name='choice', on_delete=models.CASCADE, null=True, default=None)

    def __str__(self):
        return "hwofcourse type:{}, short:{}, choice:{}".format(self.question_type, self.question_short, self.question_choice)

class StudentAnswer(models.Model):

    answer_question = models.ForeignKey('HwOfCourse', related_name='answer', on_delete=models.CASCADE)
    answer_student = models.ForeignKey('UserInfo', on_delete=models.CASCADE)
    answer_choice = models.IntegerField(null=True)
    answer_short = models.CharField(max_length=300, null=True)
    answer_score = models.IntegerField(null=True)

    def __str__(self):
        return "answer question:{}, student:{}, choice:{}, short:{}, score:{}".format(self.answer_question, self.answer_student, self.answer_choice, self.answer_short, self.answer_score)

class HwSubmit(models.Model):

    submit_homework = models.ForeignKey('Homework', on_delete=models.CASCADE)
    submit_student = models.ForeignKey('UserInfo', on_delete=models.CASCADE)
    submit_status = models.IntegerField(null=True)
    submit_time = models.DateTimeField(null=True)

class HwGrade(models.Model):

    grade_homework = models.ForeignKey('Homework', on_delete=models.CASCADE)
    grade_student = models.ForeignKey('UserInfo', on_delete=models.CASCADE)
    grade_score = models.IntegerField(null=True)
    grade_submit = models.BooleanField()

    def __str__(self):
        return "grade homework:{}, student:{}, score:{}".format(self.grade_homework, self.grade_student, self.grade_score)

class ForumList(models.Model):

    forum_title = models.CharField(max_length=300, null=True)
    forum_content = models.TextField(null=True)
    forum_time = models.DateTimeField(null=True)
    forum_course = models.ForeignKey('CourseInfo', on_delete=models.CASCADE)
    forum_user = models.ForeignKey('UserInfo', on_delete=models.CASCADE)

    def __str__(self):
        return "forum title:{}, content:{}, time:{}, course:{}, user:{}".format( \
        self.forum_title, self.forum_content, self.forum_time, self.forum_course, self.forum_user)

class PostReply(models.Model):

    reply_user = models.ForeignKey('UserInfo', on_delete=models.CASCADE)
    reply_post = models.ForeignKey('ForumList', on_delete=models.CASCADE)
    reply_content = models.TextField(null=True)
    reply_time = models.DateTimeField(null=True)

    def __str__(self):
        return "reply user:{}, post:{}, content:{}, time:{}".format(self.reply_user, self.reply_post, self.reply_content, self.reply_time)

class Source(models.Model):

    source_name = models.CharField(max_length=200, null=True)
    source_file = models.FileField(upload_to='source/', null=True)
    source_course = models.ForeignKey('CourseInfo', on_delete=models.CASCADE)
    source_user = models.ForeignKey('UserInfo', on_delete=models.CASCADE)
    source_time = models.DateTimeField(null=True)
    source_type = models.IntegerField(null=True)

    def __str__(self):
        return "source name:{}, file:{}, course:{}, user:{}, time:{}".format( \
    self.source_name, self.source_file, self.source_course, self.source_user, self.source_time)

class Message(models.Model):

    message_sender = models.ForeignKey('UserInfo', related_name='sender', on_delete=models.CASCADE)
    message_receiver = models.ForeignKey('UserInfo', related_name='receiver', on_delete=models.CASCADE)
    message_content = models.TextField(null=True)
    message_time = models.DateTimeField(null=True)
    
    def __str__(self):
        return "message sender:{}, receiver:{}, content:{}, time:{}".format( \
        self.message_sender, self.message_receiver, self.message_content, self.message_time)

class Announcement(models.Model):

    announce_title = models.CharField(max_length=200, null=True)
    announce_content = models.TextField(null=True)
    announce_time = models.DateTimeField(null=True)
    announce_user = models.ForeignKey('UserInfo', on_delete=models.CASCADE)
    announce_course = models.ForeignKey('CourseInfo', on_delete=models.CASCADE)

    def __str__(self):
        return "announcement title:{}, content:{}, time:{}, user:{}, course:{}".format \
        (self.announce_title, self.announce_content, self.announce_time, self.announce_user, self.announce_course)

class Customer(models.Model):

    customer_title = models.CharField(max_length=200, null=True)
    customer_content = models.TextField(null=True)
    customer_time = models.DateTimeField(null=True)

    def __str__(self):
        return "customer title:{}, content:{}, time:{}".format( \
        self.customer_title, self.customer_content, self.customer_time)

class IsRead(models.Model):

    read_message = models.ForeignKey('Message', on_delete=models.CASCADE, null=True, default=None, blank=True)
    read_announce = models.ForeignKey('Announcement', on_delete=models.CASCADE, null=True, default=None, blank=True)
    read_user = models.ForeignKey('UserInfo', on_delete=models.CASCADE)
    read_isread = models.BooleanField(default=False)

    def __str__(self):
        return "isread message:{}, announce:{}, user:{}, isread:{}".format( \
        self.read_message, self.read_announce, self.read_user, self.read_isread)

class Liuyan(models.Model):
    content=models.CharField(max_length=400,null=True)
    name=models.CharField(max_length=10)
    role=models.IntegerField()
    datetime=models.DateTimeField()
    item_id=models.IntegerField(null=True)
    def __str__(self):
        return self.name+" : "+self.content
