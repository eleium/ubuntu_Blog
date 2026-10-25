from django import forms

from .models import Blog, Post


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ["text"]
        labels = {"text": "新的博客"}


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["text"]
        labels = {"text": ""}
        #'text'就是定义模型Blog时： text=model.CharField(max_length=200)
        # fields 是模型里的字段名（代码用），labels 是显示给用户看的文字（界面用）。
        # 两者一个管“数据”，一个管“展示”，互不影响。

        widgets = {"text": forms.Textarea(attrs={"cols": 80})}  # noqa: RUF012


# 表单与模型的📌 本质区别
# 对比	                     模型	                        表单
# 是否需要Meta            	❌ 可选	                       ✅ 必须
# Meta 里放什么	            排序、表名、复数名等	        model、fields、labels、widgets
# 不写的后果	            正常跑	                        直接报错
# 模型的 Meta 是“额外配置”，表单的 Meta 是“核心配置”。

# 🎯 一句话总结
# 模型的 class Meta 可选，因为字段直接在类里定义。
# 表单的 class Meta 必须写，因为 ModelForm 必须知道基于哪个模型、包含哪些字段，否则没法生成表单。

# 继承 forms.ModelForm → 获得表单的内置方法（is_valid()、save()）。
# class Meta → 告诉表单基于哪个模型、包含哪些字段。
# 一个管“能力”，一个管“配置”，两者缺一不可，不是“为了用方法才写 Meta”
