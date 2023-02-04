from django.db import models
from django.utils import timezone


class User(models.Model):
    account_id = models.CharField(verbose_name="アカウントID", max_length=128, unique=True)
    email = models.CharField(verbose_name="メールアドレス", max_length=128, unique=True)
    created_at = models.DateTimeField(verbose_name="作成日時", default=timezone.now)
    updated_at = models.DateTimeField(verbose_name="更新日時", default=timezone.now)


class Post(models.Model):
    user = models.ForeignKey(User, verbose_name="ユーザー", on_delete=models.CASCADE)
    channel_name = models.CharField("チャンネル名", max_length=255)
    caption = models.TextField("キャプション")
    video_url = models.URLField("動画URL", max_length=255)
    music_name = models.CharField("曲名", max_length=255)
    updated_at = models.DateTimeField(verbose_name="更新日時", default=timezone.now)
    created_at = models.DateTimeField(verbose_name="作成日", auto_now_add=True)

    class Meta:
        verbose_name = "投稿"
        verbose_name_plural = "投稿"

        def __str__(self):
            return self.channel_name
