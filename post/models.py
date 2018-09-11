from django.db import models
from user.models import User
# Create your models here.
class Post(models.Model):
    # 不使用外键关联,通过定义字段
    uid = models.IntegerField()
    title = models.CharField(max_length=64)
    created = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    @property
    def auth(self):
        # 使用单例模式来让他不会重复创建同样的东西
        if not hasattr(self,'_auth'):
            self._auth = User.objects.get(id=self.uid)
        return self._auth

    def comment(self):
        return Comment.objects.filter(post_id=self.id).order_by('-id')

class Comment(models.Model):
    uid = models.IntegerField()
    post_id = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    @property
    def auth(self):
        # 使用单例模式来让他不会重复创建同样的东西
        if not hasattr(self, '_auth'):
            self._auth = User.objects.get(id=self.uid)
        return self._auth

    @property
    def post(self):
        # 使用单例模式来让他不会重复创建同样的东西
        if not hasattr(self, '_post'):
            self._post = Post.objects.get(id=self.post_id)
        return self._post