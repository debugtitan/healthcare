# Generated by Django 4.2.1 on 2023-05-14 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogPage', '0003_alter_blogitem_blog_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogitem',
            name='blog_description',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='blogitem',
            name='blog_title',
            field=models.CharField(max_length=180, unique=True),
        ),
    ]
