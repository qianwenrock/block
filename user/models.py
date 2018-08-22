from django.db import models

# Create your models here.
class User(models.Model):
    SEX = (
        ('M', '男性'),
        ('F', '女性'),
        ('U', '未知'),
    )
    # 用户昵称
    nickname = models.CharField(max_length=32, unique=True)
    # 用户密码
    password = models.CharField(max_length=128)
    # 用户图像
    icon = models.ImageField()
    # 用户年龄
    age = models.IntegerField()
    # 性别
    sex = models.CharField(max_length=8, choices=SEX)
