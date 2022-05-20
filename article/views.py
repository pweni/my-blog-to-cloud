from django.shortcuts import render, redirect
from django.http import HttpResponse
# 导入数据库模型 ArticlePost
from .models import ArticlePost
# 引入刚才定义的ArticlePostForm表单类
from .forms import ArticlePostForm
# 引入User模型
from django.contrib.auth.models import User
# 引入markdown模块
import markdown
from django.contrib.auth.decorators import login_required
# 引入分页器
from django.core.paginator import Paginator
# from django.core.paginator import *


# # 我的paginator
# class MyPaginator(Paginator):
#     def get_page(self, number):
#         """
#         Return a valid page, even if the page argument isn't a number or isn't
#         in range.
#         """
#         try:
#             number = self.validate_number(number)
#         except PageNotAnInteger:
            # 自由设置
#             number = 2
#         except EmptyPage:
#             number = self.num_pages
#         return self.page(number)


def article_list(request):
    """文章列表"""
    # 根据GET请求中查询条件
    # 返回不同排序的对象数组
    if request.GET.get('order') == 'total_views':
        articles_list = ArticlePost.objects.all().order_by('-total_views')
        order = 'total_views'
    else:
        articles_list = ArticlePost.objects.all()
        order = 'normal'

    paginator = Paginator(articles_list, 6)
    page = request.GET.get('page')
    articles = paginator.get_page(page)

    # 修改此行
    context = {'articles': articles, 'order': order}

    return render(request, 'article/list.html', context)


def article_detail(request, id):
    """文章详情"""
    # 取出相应的文章
    article = ArticlePost.objects.get(id=id)
    # 浏览量 +1
    article.total_views += 1
    article.save(update_fields=['total_views'])
    # 将markdown语法渲染成html格式
    article.body = markdown.markdown(article.body, extensions=[
        # 包含 缩写、表格等常用拓展
        'markdown.extensions.extra',
        # 语法高亮拓展
        'markdown.extensions.codehilite',
    ])
    # 需要传递给模板对象
    context = {
        'article': article
    }
    # 载入模板，返回context对象
    return render(request, 'article/detail.html', context=context)


@login_required(login_url='/userprofile/login/')
def article_create(request):
    """写、发表文章"""
    # 判断用户是否提交数据
    if request.method == "POST":
        # 将提交的数据赋值到表单实列中
        article_post_form = ArticlePostForm(data=request.POST)
        # 判断提交的数据是否满足模型的要求
        if article_post_form.is_valid():
            # 保存数据但暂时不提交，因为author未指定
            new_article = article_post_form.save(commit=False)
            new_article.author = User.objects.get(id=request.user.id)
            # 将新文章保存到数据库
            new_article.save()
            # 完成后返回到文章履历列表
            return redirect('article:article_list')
        else:
            return HttpResponse('表单有误请重新填写')
    # 如果用户请求获取数据，就是显示写文章页面
    else:
        # 创建表单类实例
        article_post_form = ArticlePostForm()
        # 赋值上下文
        context = {
            'article_post_form': article_post_form
        }
        return render(request, 'article/create.html', context=context)


# def article_delete(request, id):
#     """不安全的删除"""
#     article = ArticlePost.objects.get(id=id)
#     article.delete()
#     return redirect('article:article_list')
@login_required(login_url='/userprofile/login/')
def article_safe_delete(request, id):
    """安全的删除，防止xss攻击"""
    if request.method == 'POST':
        article = ArticlePost.objects.get(id=id)
        # 判断文章是不是属于当前用户
        if request.user.id == article.author_id:
            article.delete()
        else:
            return HttpResponse('这不是你的文章你没有权限删除！')
        return redirect('article:article_list')
    else:
        return HttpResponse("仅允许post请求")


@login_required(login_url='/userprofile/login/')
def article_update(request, id):
    """编辑更新文章"""
    # 获取要更新的文章
    article = ArticlePost.objects.get(id=id)
    print(request.user.id)
    print(article.author)
    print(article.author_id)
    # 判断当前用户是否能修改文章（文章得属于自己）
    if request.user.id == article.author_id:
        # 判断当前的状态，准备提交就是post，需要保存到数据库
        if request.method == 'POST':
            # 将提交的数据赋值到表单实例中
            article_post_form = ArticlePostForm(data=request.POST)
            # 判断合法性
            if article_post_form.is_valid():
                # 保存新写入的 title、body 数据并保存
                article.title = request.POST['title']
                article.body = request.POST['body']
                article.save()
                return redirect('article:article_detail', id=id)
                # 如果数据不合法，返回错误信息
            else:
                return HttpResponse("表单内容有误，请重新填写。")

        # 如果是get请求
        # 创建表单类实例
        article_post_form = ArticlePostForm()
        # 赋值上下文，将 article 文章对象也传递进去，以便提取旧的内容
        context = {'article': article, 'article_post_form': article_post_form}
        # 将响应返回到模板中
        return render(request, 'article/update.html', context)
        # return render(request, 'article/update.html')
    return HttpResponse('不是你的文章你没有权限编辑！')
