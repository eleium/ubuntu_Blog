from blogs_app.admin import admin
from django.urls import path, views
from django.shortcuts import render, redirect
from blogs_app.models import Blog, Post
from django.urls import include
from blogs_app.form import BlogForm, PostForm
from django.db import models

from django import forms




"""
练习 博客 新建一个Django项目，命名为Blog.
创建一个名为blog的应用程序，再创建两个分别表示博客和博文的模型，并让这些模型包含合适的字段。
为这个项目创建一个超级用户，并使用管理网站创建一个博客和几篇简短的博文。
创建一个主页，在其中按恰当的顺序，显示所有的博文。
创建三个页面，分别用于创建博客、发布新博文，和编辑现有的博文。尝试使用这些页面，确认它们能正确的工作。


我的理解：
这个网站的结构应该是如下：
blogs_app/base.html: 
父模板 除了有欢迎界面，还有链接： <a href="{% url 'blogs_app:index' %}"> 回到主页</a>
这样每一个子模版都可以跳转回主页.（不过主页也有这个链接，挺傻的。）

进入主页：url: path("",views.index,name='index')<--->对应 http://localhost:8000
这个主页里面包含链接，可以跳转到blogs --->http://localhost:8000/blogs 


blogs列表页面 包含这些项： blog_id =1 洛阳，blog_id=2 许昌。 blog_id=3 大连用无序<ul>排法，排列所有的blog
url: path('blogs/',views.blogs,name='blogs'),
还有一个添加新博客的链接：<a href ="{% 'url blogs_app: new_blog'}">添加新博客</a>
url: path('new_blog/',views.new_blog,name='new_blog')


在博客详情页面：一个具体的blog_id , --->http://localhost:8000/blogs/1或2
url:path("blogs/<int:blog_id>/",views.blog,name='blog')
又包含posts 即具体的多个post ---->http://localhost:8000/blogs/1跳转后，显示无序排列的post

现在可以在每个blog_id的博客详情页面，添加跳转链接：增加post，编辑post链接
增加post: url : path('new_post/<int：blog_id>/',views.new_post,name='new_post')
编辑post url: path('edit_post/<int:post_id>/',views.edit_post,name='edit_post')


#----------------------------------------------------------------------------------------------------------------
实操如下：

新建一个文件夹，名字：Blog.
创建 python manage.py startproject . blog_project,和python manage.py startapp blog_app两个文件。其中blog_app是应用程序。

然后创建模型 class Blog(models.Model) 和class Blog_font(model.Model),分别是博客和博文的模型。
创建后在admin.py中注册这两个模型： admin.site.register(Blog/Post),不注册django管理网站不认识模型。

在python manage.py shell 中 createsuperuser: elei 
可以在shell中创建一个博客： Blog.create('旅游') ,创建博文：blog_font.create('洛阳是一个十分适合旅游的城市')
也可在管理网站中add Blog和post.

urls.py 中，开始
path("blogs/",views.blogs,name='blogs')-->blogs.html 
path('blogs/'<int:blog_id>/,views.blog,name='blog')--->blog.html


views.py 定义def blogs(request) 
....

核心口诀：模型 → 迁移 → admin 注册 → 视图 → 模板 → URL。 
先写 models.py，定义好数据结构
makemigrations + migrate
注册到 admin.py，进管理后台加几条测试数据
再写 views.py，从数据库取数据
然后写 templates/，把数据展示出来
最后配 urls.py，把视图和 URL 绑定
先有数据，再有逻辑，最后有入口。 这才是 Django 开发的正确姿势。
"""

# 一，环境搭建：
# 1，虚拟环境，python -m venv b_venv -->b_venv/Scripts/activate
# --->pip install django --->django-admin startproject blog_project .

# --->python manage.py startapp blog_app ---> settings.py: add app:blogs_app
# --->models.py: class Blog/Post(models.Model)
# --->python manage.py makemigrations --->python manage.py migrate
#  --->admin.py: admin.site.register(Blog/Post)(放到最后，是因为要form .models import Blog,Post)
# --->python manage.py createsuperuser :elei
# --->python manage.py runserver
# ---python manage.py shell --->Blog.objects.create(text='洛阳'/'许昌')
# --->b1=Blog.objects.get(id=1) 洛阳,b2=Blog.objects.get(id=2) 许昌
# --->Post.objects.create(blog=b1,text='洛阳有三条大河，廛河是。。。。)

# 以上完成了网站的架设。下面开始给网站添加网页。

# -----------------------------------------------------------------------------------------------------------------

# 定义模型，后面的所有动作都是围绕这些模型运动的。
# 博客网站的两大要素就是博客名blog和博客内容post,因此定义这两个模型就好。

# 在models.py 中：
class Blog(models.Model):
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text


class Post(models.Model):
    text = models.TextField()
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    # Post 有一个外键 blog，指向 Blog
    # 当 Blog 被删除时，所有关联的 Post 也会被删除（整个对象，不只是某个属性

    # blog 是外键，所以：
    # post.blog → 得到整个 Blog 对象
    # post.blog_id → 得到Blog 的 id（整数）
    # post.blog.text → 得到所属博客的文本
    # post.blog.post_set → 反向查询该博客下所有 Post
    # text 只是普通字段，没有这些“额外能力”。blog 是外键字段，能关联到 Blog 对象

    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "posts"

    def __str__(self):
        return f"{self.text[:50]}..."


# 将这两个模型在admin.py中注册：
admin.site.register(Blog)
admin.site.register(Post)

#新建form.py，在其中创建表单类：
#这里的两个表单类，都需要写Meta来配。

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['text']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['text']

# 添加url到urls.py 中,不要忘了 命名空间 不然不知道是哪个app的。
name = "blogs_app"

urlpatterns = [
    path("", views.index, name="index"),
]

# 二，把这个app的urls都要挂到主urs下，也就是project/urls.py:
path("", include("blogs_app.urls"))


# ------------------------------------------------------------------------------------------
# 在views.py 中添加首页的视图函数：
def index(request):
    return render(request, "blogs_app/index.html")


# 新建 index.html:
# 在blogs_app下创建templates/blogs_app文件夹。以后的这个blogs_app的html文件都存放于此：
# 1,先给blogs_app建立一个base.html 父模板
# base.html:
"""
<p><a href="{% url 'blogs_app:index" %}> 欢迎来到博客世界</a></p>
此时这个链接，其实指向的还是首页。加不加都没啥变化，点击后又回到本页。
因为path('',views.index, name='index')其实就是url：http://localhost:8000,就是index.html渲染的页面。

{% block content %}{% endblock content %}
这是父模板的需要子模版填的坑。有几个子模版要挂进来，就要几个坑。坑的形式不一样。

更进一步延申：base.html的存在的意义就是这个应用程序的众多网页有公用的部分。如果没有公用的，base.html都可以不存在。

# 新建index.html:

{% extends 'blogs_app/base.html %}
{% block content %}
<p>欢迎来到我的博客世界的主页</p>

<a href="{% url 'blogs_app:blogs'}"> 点击此处，去查看所有的博客</a>
{% endblock content %}

"""
# ----------------------------------------------------------------------------------
# 在应用程序的urls.py中添加博客列表的 url,:
path("blogs/", views.blogs, name="blogs")


# views.py添加视图函数
def blogs(request):
    blogs = Blog.objects.order_by("date_added")
    context = {"blogs": blogs}
    return render(request, "blogs_app/blogs.html",context)


# blogs.html:博客列表主页，展示出所有的博客：
"""
{% extends 'blogs_app/base.html' %}
{% block content %}
<p>欢迎来到博客世界</p>
<ul>
{% for blog in blogs %}
<li>

{{ blog.text }}
<a href ="{% url 'blogs_app:blog' blog.id %}">跳到具体的一个博客去</a>
</li>
{% empty %}
<li>还没有创建博客主题呢</li>

{% endfor %}

<a href="{% url 'blogs_app:index'}">回到主页</a>
{% endblock content %}
"""

# -----------------------------------------------------------------------------------------
# urls.py 添加url，特定的一个博客：
path("blogs/<int:blog_id>/", views.blog, name="blog")


# views.py 中添加blog视图函数：
def blog(request, blog_id):
    blog = Blog.objects.get(id=blog_id)
    posts = blog.post_set.order_by("-date_added")
    context = {"blog": blog, "posts": posts}
    return render(request, "blogs_app/blog.html", context)


# ---------------------------------------------------------------------------------------

# 有了blog页面，这里展示的是已有的博客。现在还可以添加新的blog博客了。
# urls.py:添加新博客url:
path("new_blog/", views.new_blog, name="new_blog")


# views.py:添加新博客的视图函数.这里就要用到表单了。因为新增加博客主题，是用户在增加。
def new_blog(request):
    blog=Blog.objects.get(id=blog_id)
    
    if request.method != "POST":
        form = BlogForm()

    else:
        form = BlogForm(data=request.POST)

        if form.is_valid():
            form.save()
            return redirect('blogs_app:blogs')
    context = {"form": form}
    return render(request, "blogs_app/new_blog.html", context)


# 📌 不同视图里，context 装的东西不同
# 视图	         context	                             模板里怎么用
# index	        可能没有，或 {'posts': posts}	         {{ posts }}
# blogs	        {'blogs': blogs}	                     {% for blog in blogs %}
# blog	        {'blog': blog, 'posts': posts}	         {{ blog.text }}、{% for post in posts %}
# new_blog    	{'form': form}	                         {{ form.as_p }}
# new_post	    {'form': form, 'blog': blog}	         {{ form.as_p }}、{{ blog.text }}
# edit_post	    {'form': form, 'post': post}	         {{ form.as_p }}、{{ post.text }}
# 看出规律了吗？
# context 里装什么，取决于“这个模板需要什么”

# context 不“千变万化”，它只有一个作用：把视图里的数据传给模板。
# 至于里面装什么，取决于模板需要什么。需要几样就传几样，需要什么类型就传什么类型。
# 你的核心理解是对的：context 就是视图和模板之间的“数据桥梁”。


# 新建new_blog.html模板
"""
{% extends 'blogs_app/base.html %'}
{% block content %}

<p>请写下新的博客</p>

<form action="{% url 'blogs_app:new_blog' %}" method='post'>
{ csrf_token }
{{ form.as_div }}
<button name='sbmmit'>在这提交</button>
</form>

<a href="{% url 'blogs_app:blogs' %}"> 回到博客主页</a>
{% endblock content %}
"""
# ------------------------------------------------------------------------------------------------
# 添加新博文： 在urls.py 中添加新的url:
path("blogs/<int:blog_id>/new_post/", views.new_post, name="new_post")


# 编辑视图函数，新增： new_post()函数：
def new_post(request, blog_id):
    blog = Blog.objects.get(id=blog_id)

    if request.method != "POST":
        form = PostForm()

    else:
        form = PostForm(data=request.POST)

        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.blog = blog
            new_post.save()
            return redirect("blogs_app:blog", blog_id=blog.id)
    context = {"form": form, "blog": blog}
    return render(request, "blogs_app/new_post.html", context)


# 这个blog来自于本函数的blog=Blog.objects.get(id=blog_id),是Blog模型的一个实例。
# 可以这么调用： 直接调用blog.text, blog.date_added ,这是取得Blog的属性。
# 而Blog的返回值，是__str__():return self.text,是Blog类的text属性。所以如果直接调取 blog,那么就是使用Blog类的返回值：text

# {{ blog }} 不是“取属性”，而是“把对象转成字符串”，转的规则由 __str__() 决定。
# 你的 __str__() 只返回 text，所以只显示 text。
# 想显示 date_added，就写 {{ blog.date_added }}。
# 不是“不体现 date_added”，是 __str__() 里没写它。


# 新建一个new_post.html
"""
{% extends 'blogs_app/base.html' %}
{% block content %}

<p>一个欢迎新增博文的页面</p>

<form action="{% url 'blogs_app:new_post' blog.id %}" method='post'>
{ csrf_token }
{{ form.as_div }}
<button name='submit'>保存上交</button>
</form>
<a href="{% url 'blogs_app:blogs' %}">回到博客列表的页面</a>
{% endblock content %}
"""
# ---------------------------------------------------------------------------------------------------------------
# 编辑博文：urls.py 中增加：用于编辑已有的一个blog的其中的一个post:
path("blogs/<int:blog_id>/edit_post/<int:post_id>/", views.edit_post, name="edit_post")


# 编辑视图函数： edit_post():
def edit_post(request,blog_id,post_id):
    post = Post.objects.get(id=post_id)
    blog = post.blog

    if request.method != "POST":
        form = PostForm(instance=post)

    else:
        form = PostForm(instance=post, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("blogs_app:blog", blog_id=blog.id)

    context = {"form": form, "blog": blog, "post": post}
    return render(request, "blogs_app/edit_post.html", context)


#编写edit_post.html
"""
{% extends 'blogs_app/base.html' %}
{% block content %}

<form action="{% url 'blogs_app:edit_post' blog.id post.id %}" method='post'>
{% csrf_token %}
{{ form.as_div }}
<button name='submit'>保存</button>
</form>
{% endblock content %}

"""

#把这个页面链接添加到blog页面的每一个post中：
    # <p><a href="{% url 'blogs_app:edit_post' blog.id post.id %}"> 编辑博文</a></p>
    # 放到列表中
"""
{% extends 'blogs_app/base.html' %}
{%block content%}

<p> 已经写好的博客，博客详情之一：{{ blog.text }}</p>

<p>博文：</p>

<ul>
{% for post in posts %}
<li> 
    <p>{{ post.date_added|date:'M d,Y H:i'}}</p>
    <p>{{ post.text|linebreaks }}</p>
    <p><a href="{% url 'blogs_app:edit_post' blog.id post.id %}"> 编辑博文</a></p>

</li>
{% empty %}
<li>还没有给这个博客添加博文</li>

{% endfor %}
</ul>
    <p><a href="{% url 'blogs_app:new_post' blog.id %}">增加新博文</a></p>
{% endblock content %}
"""

#至此，完成一个完整的博客网站。