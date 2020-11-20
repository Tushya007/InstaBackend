# Generated by Django 3.0.5 on 2020-11-20 13:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='maincommentmodel',
            name='sub_comment',
        ),
        migrations.RemoveField(
            model_name='postmodel',
            name='comments',
        ),
        migrations.AddField(
            model_name='maincommentmodel',
            name='main_post',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='posts.PostModel'),
        ),
        migrations.AddField(
            model_name='subcommentmodel',
            name='mainComment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='posts.MainCommentModel'),
        ),
    ]