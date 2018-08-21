from django.shortcuts import render,redirect
from post.models import Post
# 向上取整
from math import ceil
# Create your views here.
# 帖子列表操作
def post_list(request):
    # 获取到当前的页码
    page = int(request.GET.get('page',1))
    # 获取所有的帖子总数
    total = Post.objects.count()
    # 每页显示的帖子数
    per_page = 10
    # 显示的所有页数
    pages = ceil(total/per_page)
    # 按照索引进行分页
    start = (page - 1) * per_page
    end = start + per_page
    posts = Post.objects.all().order_by('-id')[start:end]
    # int 不能进行遍历，需要用range()转化下
    return render(request, 'post_list.html' ,{'posts':posts, 'pages':range(pages)})

# 创建帖子的操作
def create_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        # 根据title和content创建帖子
        post = Post.objects.create(title=title, content=content)
        # 创建完成之后跳转到阅读页面
        return redirect('/post/read/?post_id=%s' %post.id)
    return render(request, 'create_post.html')

# 修改帖子的操作
def edit_post(request):
    if request.method == 'POST':
        # 先获取要修改的数据(通过hidden里面要提交的post_id获取的)
        post_id = int(request.POST.get('post_id'))
        post = Post.objects.get(id=post_id)
        # 将要修改的内容存入数据库
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        post.save()
        return redirect('/post/read/?post_id=%s' %post.id)
    else:
        post_id = int(request.GET.get('post_id'))
        post = Post.objects.get(id=post_id)
        return render(request, 'edit_post.html', {'post':post})

# 阅读帖子的操作
def read_post(request):
    # 获取post_id
    post_id = int(request.GET.get('post_id'))
    # 根据请求参数所携带的post_id查找到对应的post
    post = Post.objects.get(id=post_id)
    return render(request, 'read_post.html', {'post':post})

# 搜索帖子的操作
def search_post(request):
    if request.method == 'POST':
    # 获取关键字
        keyword = request.POST.get('keyword')
        # 根据关键字查询到所有符合条件的文章
        posts = Post.objects.get(content__contains=keyword)
        return render(request, 'search.html', {'posts':posts})
    return render(request, 'search.html', {})
