import os
from uuid import uuid4
from django.db import models
from django.utils import timezone
from core.models import Profile


def date_upload_to(instance, filename):
    ymd_path = timezone.now().strftime('%Y/%m/%d')
    uuid_name = uuid4().hex
    extension = os.path.splitext(filename)[-1].lower()
    return '/'.join([ymd_path, uuid_name + extension, ])


class Question(models.Model):
    """
        질문 모델이다.
        관리자가 생성을 하는 질문들을 저장을 하는 용도로 사용이 된다.
    """
    content = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.content


class Post(models.Model):
    """
        유저가 작성하는 포스터이다.
    """
    EMOTION_CHOICES = [
        ('WARM', "따뜻했어요"),
        ('FUN', "즐거웠어요"),
        ('HAPPY', "기뻤어요"),
        ('TOUCHED', "감동이에요"),
        ('EXTRA', "기타")
    ]

    created_at = models.DateField(auto_now_add=True)
    emotion = models.CharField(
        max_length=10, choices=EMOTION_CHOICES, default="WARM")
    question = models.ForeignKey(
        Question, on_delete=models.SET_NULL, null=True)
    detail = models.TextField(blank=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='post')
    image = models.ImageField(
        null=True, upload_to=date_upload_to)
    continuity = models.IntegerField(default=0)

    def __str__(self):
        return "[%d][%s] %s" % (self.id, self.profile, self.created_at)

    class Meta:
        unique_together = ('created_at', 'profile')
        ordering = ('-created_at',)


class UserQuestion(models.Model):
    """
        매일 유저에게 새로운 질문을 매칭을 해주기 위해서, 구현이 되었다.
    """
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    last_login = models.DateField(auto_now=True)
    question = models.ForeignKey(
        Question, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return "[%s][%s] %s" % (self.profile, self.last_login, self.question)
