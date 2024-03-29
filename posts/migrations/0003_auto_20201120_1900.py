# Generated by Django 3.0.5 on 2020-11-20 13:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_auto_20201120_1857'),
    ]

    operations = [
        migrations.AlterField(
            model_name='maincommentmodel',
            name='main_post',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='posts.PostModel'),
        ),
        migrations.AlterField(
            model_name='subcommentmodel',
            name='mainComment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='posts.MainCommentModel'),
        ),
    ]
