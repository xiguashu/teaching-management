# Generated by Django 2.0.2 on 2018-03-05 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0011_courseinfo_course_exam'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseinfo',
            name='course_credits',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='courseinfo',
            name='course_depart',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='courseinfo',
            name='course_id',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
