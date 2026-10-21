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



<!doctpyt html>
<html lang='zh-cn'>
<head>
<meta charset='utf-8'>
<meta name='viewport' content='width=device-width,initial-scale=1'>
<title>我的博客</title>

{% load django-bootstrap5 %}
{% bootstrap_css %}
{% bootstrap_javascript %}<!-- 浏览器标签页最上方的标题 -->
<title>我的博客我做主</title>          → 🔴 图上浏览器标签页文字"我的博客我做主"

<!-- ============ 以下全部在导航栏那条灰色横条里 ============ -->

<!-- 整块导航栏容器（占据图片最上方灰色横条） -->
<nav class="navbar navbar-expand-md navbar-light bg-light mb-4 border">
                                        ↑bg-light就是那条浅灰底色  ↑border是灰色边框  ↑mb-4是下面那条细黑线（下边距+边框重合）

    <!-- ↓ 里面的"内容宽度"容器，决定左右不贴边 -->
    <div class="container-fluid">

        <!-- ①最左边的"我的博客"大字（品牌位） -->
        <a class="navbar-brand" href="{% url 'blogs_app:index' %}">我的博客</a>
           ↑navbar-brand让字号变大、加粗、有内边距
           对应图上🔵 "我的博客" （左侧大字）

        <!-- ②汉堡按钮（只有手机小屏才出现，你这屏幕够宽所以隐藏了） -->
        <button class="navbar-toggler" type="button"
                data-bs-toggle="collapse" data-bs-target="#navbarCollapse">
            <span class="navbar-toggler-icon"></span>
        </button>
        → 你截图里**看不到这个**，因为屏幕宽度 >768px，`navbar-expand-md` 把它藏起来了。缩小浏览器窗口到手机宽度才会出现三条横线

        <!-- ③折叠容器，大屏下强制展开 -->
        <div class="collapse navbar-collapse" id="navbarCollapse">

            <!-- ↓ 导航链接组 -->
            <ul class="navbar-nav me-auto mb-2 mb-md-0">
                                  ↑me-auto 把右边空间推走，让后面元素靠右

                <!-- ④列表项 -->
                <li class="nav-item">
                    <!-- ⑤导航链接（当前页，Bootstrap会自动加active高亮） -->
                    <a class="nav-link" href="{% url 'blogs_app:blogs' %}">博客列表</a>
                       ↑nav-link给了内边距、鼠标悬停变色
                       对应图上🟢 "博客列表" （右侧链接，因为me-auto推过去了）
                </li>
            </ul>

        </div>
    </div>
</nav>
<!-- ============ 导航栏结束 ============ -->

<!-- 下面是页面正文（block content 渲染的内容） --><!-- 浏览器标签页最上方的标题 -->
<title>我的博客我做主</title>          → 🔴 图上浏览器标签页文字"我的博客我做主"

<!-- ============ 以下全部在导航栏那条灰色横条里 ============ -->

<!-- 整块导航栏容器（占据图片最上方灰色横条） -->
<nav class="navbar navbar-expand-md navbar-light bg-light mb-4 border">
                                        ↑bg-light就是那条浅灰底色  ↑border是灰色边框  ↑mb-4是下面那条细黑线（下边距+边框重合）

    <!-- ↓ 里面的"内容宽度"容器，决定左右不贴边 -->
    <div class="container-fluid">

        <!-- ①最左边的"我的博客"大字（品牌位） -->
        <a class="navbar-brand" href="{% url 'blogs_app:index' %}">我的博客</a>
           ↑navbar-brand让字号变大、加粗、有内边距
           对应图上🔵 "我的博客" （左侧大字）

        <!-- ②汉堡按钮（只有手机小屏才出现，你这屏幕够宽所以隐藏了） -->
        <button class="navbar-toggler" type="button"
                data-bs-toggle="collapse" data-bs-target="#navbarCollapse">
            <span class="navbar-toggler-icon"></span>
        </button>
        → 你截图里**看不到这个**，因为屏幕宽度 >768px，`navbar-expand-md` 把它藏起来了。缩小浏览器窗口到手机宽度才会出现三条横线

        <!-- ③折叠容器，大屏下强制展开 -->
        <div class="collapse navbar-collapse" id="navbarCollapse">

            <!-- ↓ 导航链接组 -->
            <ul class="navbar-nav me-auto mb-2 mb-md-0">
                                  ↑me-auto 把右边空间推走，让后面元素靠右

                <!-- ④列表项 -->
                <li class="nav-item">
                    <!-- ⑤导航链接（当前页，Bootstrap会自动加active高亮） -->
                    <a class="nav-link" href="{% url 'blogs_app:blogs' %}">博客列表</a>
                       ↑nav-link给了内边距、鼠标悬停变色
                       对应图上🟢 "博客列表" （右侧链接，因为me-auto推过去了）
                </li>
            </ul>

        </div>
    </div>
</nav>
<!-- ============ 导航栏结束 ============ -->

<!-- 下面是页面正文（block content 渲染的内容） --><!-- 浏览器标签页最上方的标题 -->
<title>我的博客我做主</title>          → 🔴 图上浏览器标签页文字"我的博客我做主"

<!-- ============ 以下全部在导航栏那条灰色横条里 ============ -->

<!-- 整块导航栏容器（占据图片最上方灰色横条） -->
<nav class="navbar navbar-expand-md navbar-light bg-light mb-4 border">
                                        ↑bg-light就是那条浅灰底色  ↑border是灰色边框  ↑mb-4是下面那条细黑线（下边距+边框重合）

    <!-- ↓ 里面的"内容宽度"容器，决定左右不贴边 -->
    <div class="container-fluid">

        <!-- ①最左边的"我的博客"大字（品牌位） -->
        <a class="navbar-brand" href="{% url 'blogs_app:index' %}">我的博客</a>
           ↑navbar-brand让字号变大、加粗、有内边距
           对应图上🔵 "我的博客" （左侧大字）

        <!-- ②汉堡按钮（只有手机小屏才出现，你这屏幕够宽所以隐藏了） -->
        <button class="navbar-toggler" type="button"
                data-bs-toggle="collapse" data-bs-target="#navbarCollapse">
            <span class="navbar-toggler-icon"></span>
        </button>
        → 你截图里**看不到这个**，因为屏幕宽度 >768px，`navbar-expand-md` 把它藏起来了。缩小浏览器窗口到手机宽度才会出现三条横线

        <!-- ③折叠容器，大屏下强制展开 -->
        <div class="collapse navbar-collapse" id="navbarCollapse">

            <!-- ↓ 导航链接组 -->
            <ul class="navbar-nav me-auto mb-2 mb-md-0">
                                  ↑me-auto 把右边空间推走，让后面元素靠右

                <!-- ④列表项 -->
                <li class="nav-item">
                    <!-- ⑤导航链接（当前页，Bootstrap会自动加active高亮） -->
                    <a class="nav-link" href="{% url 'blogs_app:blogs' %}">博客列表</a>
                       ↑nav-link给了内边距、鼠标悬停变色
                       对应图上🟢 "博客列表" （右侧链接，因为me-auto推过去了）
                </li>
            </ul>

        </div>
    </div>
</nav>
<!-- ============ 导航栏结束 ============ -->
<!-- 浏览器标签页最上方的标题 -->
<title>我的博客我做主</title>          → 🔴 图上浏览器标签页文字"我的博客我做主"

<!-- ============ 以下全部在导航栏那条灰色横条里 ============ -->

<!-- 整块导航栏容器（占据图片最上方灰色横条） -->
<nav class="navbar navbar-expand-md navbar-light bg-light mb-4 border">
                                        ↑bg-light就是那条浅灰底色  ↑border是灰色边框  ↑mb-4是下面那条细黑线（下边距+边框重合）

    <!-- ↓ 里面的"内容宽度"容器，决定左右不贴边 -->
    <div class="container-fluid">

        <!-- ①最左边的"我的博客"大字（品牌位） -->
        <a class="navbar-brand" href="{% url 'blogs_app:index' %}">我的博客</a>
           ↑navbar-brand让字号变大、加粗、有内边距
           对应图上🔵 "我的博客" （左侧大字）

        <!-- ②汉堡按钮（只有手机小屏才出现，你这屏幕够宽所以隐藏了） -->
        <button class="navbar-toggler" type="button"
                data-bs-toggle="collapse" data-bs-target="#navbarCollapse">
            <span class="navbar-toggler-icon"></span>
        </button>
        → 你截图里**看不到这个**，因为屏幕宽度 >768px，`navbar-expand-md` 把它藏起来了。缩小浏览器窗口到手机宽度才会出现三条横线

        <!-- ③折叠容器，大屏下强制展开 -->
        <div class="collapse navbar-collapse" id="navbarCollapse">

            <!-- ↓ 导航链接组 -->
            <ul class="navbar-nav me-auto mb-2 mb-md-0">
                                  ↑me-auto 把右边空间推走，让后面元素靠右

                <!-- ④列表项 -->
                <li class="nav-item">
                    <!-- ⑤导航链接（当前页，Bootstrap会自动加active高亮） -->
                    <a class="nav-link" href="{% url 'blogs_app:blogs' %}">博客列表</a>
                       ↑nav-link给了内边距、鼠标悬停变色
                       对应图上🟢 "博客列表" （右侧链接，因为me-auto推过去了）
                </li>
            </ul>

        </div>
    </div>
</nav>
<!-- ============ 导航栏结束 ============ -->

<!-- 下面是页面正文（block content 渲染的内容） --><!-- 浏览器标签页最上方的标题 -->
<title>我的博客我做主</title>          → 🔴 图上浏览器标签页文字"我的博客我做主"

<!-- ============ 以下全部在导航栏那条灰色横条里 ============ -->

<!-- 整块导航栏容器（占据图片最上方灰色横条） -->
<nav class="navbar navbar-expand-md navbar-light bg-light mb-4 border">
                                        ↑bg-light就是那条浅灰底色  ↑border是灰色边框  ↑mb-4是下面那条细黑线（下边距+边框重合）

    <!-- ↓ 里面的"内容宽度"容器，决定左右不贴边 -->
    <div class="container-fluid">

        <!-- ①最左边的"我的博客"大字（品牌位） -->
        <a class="navbar-brand" href="{% url 'blogs_app:index' %}">我的博客</a>
           ↑navbar-brand让字号变大、加粗、有内边距
           对应图上🔵 "我的博客" （左侧大字）

        <!-- ②汉堡按钮（只有手机小屏才出现，你这屏幕够宽所以隐藏了） -->
        <button class="navbar-toggler" type="button"
                data-bs-toggle="collapse" data-bs-target="#navbarCollapse">
            <span class="navbar-toggler-icon"></span>
        </button>
        → 你截图里**看不到这个**，因为屏幕宽度 >768px，`navbar-expand-md` 把它藏起来了。缩小浏览器窗口到手机宽度才会出现三条横线

        <!-- ③折叠容器，大屏下强制展开 -->
        <div class="collapse navbar-collapse" id="navbarCollapse">

            <!-- ↓ 导航链接组 -->
            <ul class="navbar-nav me-auto mb-2 mb-md-0">
                                  ↑me-auto 把右边空间推走，让后面元素靠右

                <!-- ④列表项 -->
                <li class="nav-item">
                    <!-- ⑤导航链接（当前页，Bootstrap会自动加active高亮） -->
                    <a class="nav-link" href="{% url 'blogs_app:blogs' %}">博客列表</a>
                       ↑nav-link给了内边距、鼠标悬停变色
                       对应图上🟢 "博客列表" （右侧链接，因为me-auto推过去了）
                </li>
            </ul>

        </div>
    </div>
</nav>
<!-- ============ 导航栏结束 ============ -->

<!-- 下面是页面正文（block content 渲染的内容） -->
<!-- 下面是页面正文（block content 渲染的内容） -->
</head>


<!-- 浏览器标签页最上方的标题 -->
<title>我的博客我做主</title>          → 🔴 图上浏览器标签页文字"我的博客我做主"

<!-- ============ 以下全部在导航栏那条灰色横条里 ============ -->

<!-- 整块导航栏容器（占据图片最上方灰色横条） -->
<nav class="navbar navbar-expand-md navbar-light bg-light mb-4 border">
                                        ↑bg-light就是那条浅灰底色  ↑border是灰色边框  ↑mb-4是下面那条细黑线（下边距+边框重合）

    <!-- ↓ 里面的"内容宽度"容器，决定左右不贴边 -->
    <div class="container-fluid">

        <!-- ①最左边的"我的博客"大字（品牌位） -->
        <a class="navbar-brand" href="{% url 'blogs_app:index' %}">我的博客</a>
           ↑navbar-brand让字号变大、加粗、有内边距
           对应图上🔵 "我的博客" （左侧大字）

        <!-- ②汉堡按钮（只有手机小屏才出现，你这屏幕够宽所以隐藏了） -->
        <button class="navbar-toggler" type="button"
                data-bs-toggle="collapse" data-bs-target="#navbarCollapse">
            <span class="navbar-toggler-icon"></span>
        </button>
        → 你截图里**看不到这个**，因为屏幕宽度 >768px，`navbar-expand-md` 把它藏起来了。缩小浏览器窗口到手机宽度才会出现三条横线

        <!-- ③折叠容器，大屏下强制展开 -->
        <div class="collapse navbar-collapse" id="navbarCollapse">

            <!-- ↓ 导航链接组 -->
            <ul class="navbar-nav me-auto mb-2 mb-md-0">
                                  ↑me-auto 把右边空间推走，让后面元素靠右

                <!-- ④列表项 -->
                <li class="nav-item">
                    <!-- ⑤导航链接（当前页，Bootstrap会自动加active高亮） -->
                    <a class="nav-link" href="{% url 'blogs_app:blogs' %}">博客列表</a>
                       ↑nav-link给了内边距、鼠标悬停变色
                       对应图上🟢 "博客列表" （右侧链接，因为me-auto推过去了）
                </li>
            </ul>

        </div>
    </div>
</nav>
<!-- ============ 导航栏结束 ============ -->

<!-- 下面是页面正文（block content 渲染的内容） -->
