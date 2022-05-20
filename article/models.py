from django.db import models
# 导入内建的User模型
from django.contrib.auth.models import User
# timezone 用于处理时间相关事务
from django.utils import timezone


# 博客文章数据模型
class ArticlePost(models.Model):
    # 文章作者。参数on_delete 用于指定数据删除方式
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='文章作者')

    # 文章标题。models.CharField 为字符串段，用于保存较短的字符串，比如标题
    title = models.CharField(max_length=100, verbose_name='文章标题')

    # 文章正文。保存大量文本使用 TextField
    body = models.TextField(verbose_name='文章正文')

    # 文章创建时间。参数 default=timezone.now 指定其在创建数据时将默认写入当前时间
    created = models.DateTimeField(default=timezone.now, verbose_name='文章创建时间')

    # 文章被浏览次数
    total_views = models.PositiveIntegerField(default=0, verbose_name='浏览数')

    # 文章更新时间。参数auto_now 指定每次数据更新时自动写入当前时间
    updated = models.DateTimeField(auto_now=True, verbose_name='文章更新时间')

    # 内部类 class Meta 用于给 model 定义元数据
    class Meta:
        # ordering 指定模型返回的数据的排列顺序
        # '-created' 表面数据应该以倒序排列
        ordering = ('-created',)

    # 函数 __str__ 定义调用对象的str()方法时的返回值内容
    def __str__(self):
        # 将文章标题返回
        return self.title
