from django.urls import path

from . import views

app_name = "blogs_app"

urlpatterns = [
    path("", views.index, name="index"),
    path("blogs/", views.blogs, name="blogs"),
    path("blogs/<int:blog_id>/", views.blog, name="blog"),
    path("new_blog/", views.new_blog, name="new_blog"),
    path("blogs/<int:blog_id>/edit_blog/", views.edit_blog, name="edit_blog"),
    path("blogs/<int:blog_id>/del_blog/", views.del_blog, name="del_blog"),
    path("blogs/<int:blog_id>/new_post/", views.new_post, name="new_post"),
    path(
        "blogs/<int:blog_id>/edit_post/<int:post_id>/",
        views.edit_post,
        name="edit_post",
    ),
    path(
        "blogs/<int:blog_id>/del_post/<int:post_id>/", views.del_post, name="del_post"
    ),
]

#'new_blog/'	    URL 模式	    浏览器访问时匹配的路径
# views.new_blog	视图函数	    URL 匹配后，调用哪个函数
# name='new_blog'	URL 的名字	    给模板 {% url %} 反向解析用

# “匹配 URL”和“反向解析 URL”是两件相反的事：
# 匹配：浏览器发来一个 URL，Django 找哪条 path() 能接住 → 看 'new_blog/'
# 反向解析：模板里写 {% url 'blogs_app:new_blog' %}，Django 找哪条 path() 的 name 是这个 → 看 name='new_blog'
