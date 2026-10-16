from django.contrib import admin
from .models import Blog,Post
# Register your models here.

# 注册模型的目的，是把模型“挂到”Django 自带的 admin 后台，让你可以在浏览器里管理数据。
# 不注册，admin 后台就看不到这个模型。

# 📌 两个概念要分清
# 操作                   	 目的	                          位置
# import	                在代码里使用模型	              views.py、forms.py 等
# admin.site.register	    把模型挂到 admin 后台	          admin.py
# import                    是给程序用的，register 是给“管理界面”用的。两者用途完全不同


admin.site.register(Blog)
admin.site.register(Post)