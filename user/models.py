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
    # 第三方平台的icon
    plt_icon = models.CharField(max_length=256, default='')
    # 用户年龄
    age = models.IntegerField(default=18)
    # 性别
    sex = models.CharField(max_length=8, choices=SEX)

    @property
    def avatar(self):
        return self.icon.url if self.icon else self.plt_icon