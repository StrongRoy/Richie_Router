from django.db import models


# Create your models here.

class UserType(models.Model):
    title = models.CharField(max_length=32)

    class Meta:
        verbose_name_plural = '用户类型'

    def __str__(self):
        return self.title


class Role(models.Model):
    caption = models.CharField(max_length=32)
    user_type = models.ForeignKey(to=UserType)

    class Meta:
        verbose_name_plural = '用户角色'

    def __str__(self):
        return self.caption


class UserInfo(models.Model):
    name = models.CharField(max_length=32,verbose_name='用户名')
    email = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    role = models.ManyToManyField(to=Role)

    class Meta:
        verbose_name_plural = '用户信息'

    def __str__(self):
        return self.name
