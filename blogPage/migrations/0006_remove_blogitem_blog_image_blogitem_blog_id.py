# Generated by Django 4.2.1 on 2023-05-14 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogPage', '0005_alter_blogitem_blog_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogitem',
            name='blog_image',
        ),
        migrations.AddField(
            model_name='blogitem',
            name='blog_id',
            field=models.CharField(blank=True, max_length=60, null=True, unique=True),
        ),
    ]
