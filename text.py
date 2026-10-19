1,python manage.py startapp accounts
2,project/settings.py  ---> add app : app_name='accounts'
3,project/urls.py: path('accounts/',include('accounts.urls'))
4,accounts/urls.py   app_name='accounts'    path("",include('django.contrib.auth.urls)
5,make new file: Blog/accounts/registrations/login.html:
    {% extends 'blogs_app/base.html' %}
    {% block content %}
{% if form.errors %}
<p>the name or password is not match.try again.</p>
{% endif %}
<form action="{% url 'accounts:login' %}" method='post'>
{% csrf_token %}
{{ form.as_div }}
<button type='submit'>login please</button>
</form>
{% endblock content %}



{% extends 'blogs_app/base.html' %}
{% block content %}

<p>你将删除掉一片辛苦写下的博客--{{blog.text}}</p>

<form action="{% url 'blogs_app:del_blog' blog_id=blog.id %}" method='post'>
    {% csrf_token %}
    <button type='submit'>确认删除</button>
    <a href="{% url 'blogs_app:blog' blog_id=blog.id %}">取消删除</a>
</form>
<form action="{% url 'blogs_app:blog' blog_id=blog.id %}">
<button type='submit'>cancle</button>
</form>

{% endblock content %}




def register(request):
    if request.method != 'POST':
        form=UserCreationForm()
    else:
        from=UserCreationForm(data=request.POST)
        if form.is_valid():
#如果合法，让form.save()存入数据库，并把实例赋值给new_user,django自动登录。
#如果直接form.save()，django不会登录，回到主页，让刚刚注册的用户登录，体验不好。
            new_from=form.save()
            login(request,new_user)
           # form.save()
            return redirect('blogs_app:index')
    context={"form":form}
    return render(request,'registration/register.html',context)
#注意这是registration下的register.html,不要写成accounts,或者其他的。
