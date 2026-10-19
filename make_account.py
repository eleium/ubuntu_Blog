"""
1,python manage.py startapp accounts
2,将这个app添加到blog_project/settings.py  中
3,把accounts的url,挂到blog_project/urls.py 中，注意path('accounts/',include('accounts.urls)),前缀要用'accounts'跟其他的主路由区分开。

4，现在要让用户login,logout,password,register,change_password设置等等，引用django.contrib.auth.urls,其中就有这些操作的url.
在app accounts中新建urls.py,首先要确定命名空间： app_name='accounts',
另外要注意，path("",include('django.contrib.auth.urls))，前缀千万不能再写'accounts/'了，会出现重复前缀的错误。
如果自己写，就还是path("",views.login,name='login'),
但是丧失了django提供的安全，完备(多个操作：login,logout,password,register)，方便(密码更改，邮箱验证等等），
连续性（后续的装饰器@login_required, request.user等等）

5，编写login.html模板。身份验证的视图默认在registration中寻找login.html模板，所以在accounts/templates/registration下新建login.html

6,因为是django提供的views.login,所以要手动指出，登陆后跳转到的哪里：
settings.py:  LOGIN_REDIRECT_URL='blogs_app:index'

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


"""
