# Generated by Django 3.2.15 on 2023-02-04 03:54

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_id', models.CharField(max_length=128, unique=True, verbose_name='アカウントID')),
                ('email', models.CharField(max_length=128, unique=True, verbose_name='メールアドレス')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='作成日時')),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='更新日時')),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='updated_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='更新日時'),
        ),
        migrations.AddField(
            model_name='post',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='app.user', verbose_name='ユーザー'),
            preserve_default=False,
        ),
    ]
