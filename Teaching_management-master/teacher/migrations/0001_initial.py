# Generated by Django 2.1 on 2017-12-27 14:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('announce_title', models.CharField(max_length=200, null=True)),
                ('announce_content', models.TextField(null=True)),
                ('announce_time', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CourseInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_name', models.CharField(max_length=50)),
                ('course_syllabus', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CourseTime',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_date', models.DateField(null=True)),
                ('course_time', models.CharField(max_length=50, null=True)),
                ('course_assignment', models.CharField(max_length=60, null=True)),
                ('course_position', models.CharField(max_length=30, null=True)),
                ('course_info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teacher.CourseInfo')),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_title', models.CharField(max_length=200, null=True)),
                ('customer_content', models.TextField(null=True)),
                ('customer_time', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ForumList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('forum_title', models.CharField(max_length=300, null=True)),
                ('forum_content', models.TextField(null=True)),
                ('forum_time', models.DateTimeField(null=True)),
                ('forum_course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teacher.CourseInfo')),
            ],
        ),
        migrations.CreateModel(
            name='Homework',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('homework_name', models.CharField(max_length=50, null=True)),
                ('homework_description', models.TextField(null=True)),
                ('homework_edit_time', models.DateTimeField(null=True)),
                ('homework_deadline', models.DateTimeField(null=True)),
                ('homework_score', models.IntegerField(null=True)),
                ('homework_course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teacher.CourseInfo')),
            ],
        ),
        migrations.CreateModel(
            name='HwGrade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade_score', models.IntegerField(null=True)),
                ('grade_homework', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teacher.Homework')),
            ],
        ),
        migrations.CreateModel(
            name='HwOfCourse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_type', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='IsRead',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('read_isread', models.BooleanField(default=False)),
                ('read_announce', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='teacher.Announcement')),
            ],
        ),
        migrations.CreateModel(
            name='ManagerInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('manager_id', models.CharField(max_length=11, null=True)),
                ('manager_name', models.CharField(max_length=20, null=True)),
                ('manager_job', models.CharField(max_length=40, null=True)),
                ('manager_phone', models.CharField(max_length=15, null=True)),
                ('manager_email', models.EmailField(max_length=254, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message_content', models.TextField(null=True)),
                ('message_time', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MultipleChoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice_content', models.TextField(null=True)),
                ('choice_A', models.CharField(max_length=200, null=True)),
                ('choice_B', models.CharField(max_length=200, null=True)),
                ('choice_C', models.CharField(max_length=200, null=True)),
                ('choice_D', models.CharField(max_length=200, null=True)),
                ('choice_answer', models.IntegerField(null=True)),
                ('choice_score', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PostReply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reply_content', models.TextField(null=True)),
                ('reply_time', models.DateTimeField(null=True)),
                ('reply_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teacher.ForumList')),
            ],
        ),
        migrations.CreateModel(
            name='ShortAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short_content', models.TextField(null=True)),
                ('short_answer', models.CharField(max_length=200, null=True)),
                ('short_score', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source_name', models.CharField(max_length=200, null=True)),
                ('source_file', models.FileField(null=True, upload_to='source/')),
                ('source_time', models.DateTimeField(null=True)),
                ('source_course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teacher.CourseInfo')),
            ],
        ),
        migrations.CreateModel(
            name='StudentAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_choice', models.IntegerField(null=True)),
                ('answer_short', models.CharField(max_length=300, null=True)),
                ('answer_score', models.IntegerField(null=True)),
                ('answer_question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answer', to='teacher.HwOfCourse')),
            ],
        ),
        migrations.CreateModel(
            name='StudentInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_id', models.CharField(max_length=11, null=True)),
                ('student_name', models.CharField(max_length=20, null=True)),
                ('student_college', models.CharField(max_length=30, null=True)),
                ('student_class', models.CharField(max_length=30, null=True)),
                ('student_phone', models.CharField(max_length=11, null=True)),
                ('student_email', models.EmailField(max_length=254, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('user_type', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='TeacherInfo',
            fields=[
                ('teacher_info', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='teacher.UserInfo')),
                ('teacher_id', models.CharField(max_length=15, null=True)),
                ('teacher_name', models.CharField(max_length=20, null=True)),
                ('teacher_department', models.CharField(max_length=30, null=True)),
                ('teacher_phone', models.CharField(max_length=15, null=True)),
                ('teacher_email', models.EmailField(max_length=254, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='userinfo',
            name='user_course',
            field=models.ManyToManyField(to='teacher.CourseInfo'),
        ),
        migrations.AddField(
            model_name='studentinfo',
            name='student_info',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='teacher.UserInfo'),
        ),
        migrations.AddField(
            model_name='studentanswer',
            name='answer_student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teacher.UserInfo'),
        ),
        migrations.AddField(
            model_name='source',
            name='source_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teacher.UserInfo'),
        ),
        migrations.AddField(
            model_name='postreply',
            name='reply_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teacher.UserInfo'),
        ),
        migrations.AddField(
            model_name='message',
            name='message_receiver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receiver', to='teacher.UserInfo'),
        ),
        migrations.AddField(
            model_name='message',
            name='message_sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender', to='teacher.UserInfo'),
        ),
        migrations.AddField(
            model_name='managerinfo',
            name='manager_info',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='teacher.UserInfo'),
        ),
        migrations.AddField(
            model_name='isread',
            name='read_message',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='teacher.Message'),
        ),
        migrations.AddField(
            model_name='isread',
            name='read_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teacher.UserInfo'),
        ),
        migrations.AddField(
            model_name='hwofcourse',
            name='question_choice',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='choice', to='teacher.MultipleChoice'),
        ),
        migrations.AddField(
            model_name='hwofcourse',
            name='question_short',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='short', to='teacher.ShortAnswer'),
        ),
        migrations.AddField(
            model_name='hwgrade',
            name='grade_student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teacher.UserInfo'),
        ),
        migrations.AddField(
            model_name='forumlist',
            name='forum_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teacher.UserInfo'),
        ),
        migrations.AddField(
            model_name='announcement',
            name='announce_course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teacher.CourseInfo'),
        ),
        migrations.AddField(
            model_name='announcement',
            name='announce_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teacher.UserInfo'),
        ),
    ]
