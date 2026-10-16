from django.db import models

# Create your models here.
class Blog(models.Model):
    text=models.CharField(max_length=200)
    date_added=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text


class Post(models.Model):
    blog=models.ForeignKey(Blog,on_delete=models.CASCADE)
    text=models.TextField()
    date_added=models.DateTimeField(auto_now_add=True)  
    class Meta:
          verbose_name_plural = "posts"
          #这个Meta可选的。因为post的复数形式就是posts.
          #如果有其他的元条件，才需要Meta
          
# 📌模型中 什么时候需要 class Meta？
# 场景	                     是否需要 Meta
# 设置排序	                ✅ 需要，ordering = ['-date_added']
# 设置复数名	            ✅ 需要，verbose_name_plural = '...'
# 设置单数名	            ✅ 需要，verbose_name = '...'
# 设置数据库表名	        ✅ 需要，db_table = '...'
# 普通模型，什么都不改	     ❌ 不需要
# 如果你的模型不需要额外配置，完全可以不写 class Meta。
    
    def __str__(self):
        return f"{self.text[:50]}..."
    
#模型与表单的📌 本质区别
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