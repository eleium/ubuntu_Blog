"""
1,python manage.py startapp accounts
2,将这个app添加到blog_project/settings.py  中
3,把accounts的url,挂到blog_project/urls.py 中，注意path('accounts/',include('accounts.urls'),前缀要用'accounts'跟其他的主路由区分开。

4，现在要让用户login,logout,password,change_password设置等等，引用django.contrib.auth.urls,其中就有这些操作的url.
在app accounts中新建urls.py,首先要确定命名空间： app_name='accounts',
另外要注意，path("",include('django.contrib.auth.urls')，前缀千万不能再写'accounts/'了，会出现重复前缀的错误。
如果自己写，就还是path("",views.login,name='login'),
但是丧失了django提供的安全，完备(多个操作：login,logout,password)，方便(密码更改，邮箱验证等等），
连续性（后续的装饰器@login_required, request.user等等）

5，编写login.html模板。身份验证的视图默认在registration中寻找login.html模板，所以在accounts/templates/registration下新建login.html

6,因为是django提供的views.login,所以要手动指出，登陆后跳转到的哪里：
settings.py:  LOGIN_REDIRECT_URL='blogs_app:index'
 LOGIN_URL 正好默认对上了，但值得写进笔记
`@login_required` 未登录时跳到`settings.LOGIN_URL` ， 默认值就是`/accounts/login/` 。
你的前缀刚好是`accounts/` ，所以不用配也能用。
如果前缀改了（比如改成`auth/` ），就必须显式写`LOGIN_URL = 'accounts:login'` 。

 7,补充views.py-->del_blog,edit_blog,del_post,所有的视图函数齐全了。

8,编写上述视图函数对应的html模板。

9，添加一个注册页面。
9-1，accounts/urls.py path('register/',views.register,name='register')
9-2,views.py:
def register(request):
    if request.method != 'POST':
        form=UserCreationForm()
    else:
        form=UserCreationForm(data=request.POST)
        if form.is_valid():
            new_user=form.save()
            login(request,new_user)
            return redirect('blogs_app:index')
    context={'form':form}
    return render(request,'registration/register.html',context)

9-3,register.html:
{% extends 'blogs_app/base.html' %}
{% block content %}

<p>欢迎注册</p>
<form action="{% url 'accounts:register' %}" method='post'>
{% csrf_token %}
{{ form.as_div }}
<button type='submit'>注册</button>
</form>
{% endblock content %}

9-4,在blogs_app/base.html中添加关于注册的链接：
<a href="{% url 'accounts:register' %}">请注册</a>


10,给各个页面指定权限，谁能看。
用到装饰器 @login_required限制访问
现在看来，只需要把accounts:register和 blogs_app: index和accounts:login 供所有人使用，其他的所有页面都用@login_required限制起来
from django.contrib.auth.decorators import login_required      (decorator: 装饰器)
在其他的函数前面都加上装饰器： @login_required ,让django先执行login_required函数，查验是否登录用户。


11，引入owner。
from django.contrib.auth.models import User
找出本博客中，最高层的是啥？是博客详情:blog,基本上所有的操作都是围绕blog进行的：增删改查.这是模型，不是具体的实例
所以对 blogs_app/models.py 进行修改：
class Blog(models.Model):
    text=models.CharField(max_length=200)
    date_added=models.DateTimeField(auto_now_add=True)
    owner=models.User.ForeignKey(User,on_delete=models.CASCADE)

   def __str__(self):

        return self.text

12,查看本应用已经注册了多少人，拿到名单和id --->python manage.py shell  from django.contrib.auth.models import User
for user in User.objects.all():
    print(user,user.id)
然后 quit()shell， python manage.py makemigrations blogs_app-->选择1：提供默认值。--->1,选择把所有blogs关联到id=1的用户。（一般id=1的是超级用户，
但是不是超级用户也可也。id一定要真实存在。）
python manage.py migrate 完成数据迁徙。只有在模型被真正改变的，比如这次的增加了owner=Usre.ForeignKey(User,on_delete=models.CASCADE)才需要迁徙.


13,更改views.py 中的blogs()视图函数

def blogs(request):
    # blogs=Blog.objects.get(id=blog_id)
    blogs=Blog.objects.filter(owner=request.user).order_by('date_added')
    context={'blogs':blogs,}
    return render(request,'blogs_app/blogs.html',context)

14.更改blog()函数，保护用户的博客：
def blog(request,blog_id):
    blog=Blog.objects.get(id=blog_id)
    if owner != request.user:
        raise Http404
    posts=blog.post_set.order_by('-date_added')
    context={"blog":blog,"posts":posts}
    return render(request,'blogs_app/blog.html',context)



只要是修改、删除、编辑已有的blog或post的，都需要if owner != request.user ----> raise Http404
新增的，不需要，但是要明确属于谁。新增的也就是new_blog,而new_post同样需要判断blog.owner是否是登录的用户的。
if owner!=request.user:
    raise Http404
blog():
def blog(request,blog_id):
    blog=Blog.objects.get(id=blog_id)
    posts=blog.post_set.order_by("-date_added")
    if owner!= request.user:
        raise Http404
    context={"blog":blog,'posts':post}
    return render(request,'blogs_app/blog.html',context)
至此，所有的网页被关联到具体的登录用户。

下面开始用django-bootstrap5的样式来装饰网页，让网页生动漂亮。
ubuntu 下面 pip install django-bootstrap5
setting.py ，在installed 中添加： ’django_bootstrap5',位置必须在我自己填的几个app，和django默认自带的app之间。
首先从base.html开始：

<!doctype html>
<html lang='zh-cn'>
<head>
<meta charset='utf-8'>
<meta name='viewport' content='width=device-width,initial-scale=1'>
<title>'我的博客'</title>

{% load django_bootstrap5 %}
{% bootstrap_css %}
{% bootstrap_javascript %}
</head>
以上是一个标准的设定：网页是中文，翻译、视听按中文来。编码是utf-8. 视口随设备。网页标签：title
导入django-bootstrap5，以及其中的css样式库和javascript脚本。

<!doctype html>
<html lang="zh">
<head>
<meta charset='utf-8'>
<meta name='viewport',content='width=device-width,initail-scale=1'>
<title>webpage</title>

{% load django_bootstrap5 %}
{% bootstrap_css %}
{% bootstrap_javascript %}
</head>
<body>

<nav class ="navbar navbar-expand-md mb-4 navbar-light bg-light border round=3">
表明这是导航栏，随设备展开，设备>=768,展开。否则，折叠。下行距4 导航栏、背景都为浅色，有边框，圆角。
<div class='container-fluid' >
以下是一个块区域，像容器流动一样充满。
<a class='navbar-brand' herf="{% url 'blogs_app:index' %}">回到主页</a>
大字号 的招牌、logo:链接回到主页
<
"""
