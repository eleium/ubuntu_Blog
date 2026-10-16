"""
# 博客网站结构说明

你这个思路非常对：**先把网站结构和页面流程画清楚，再动手写代码**。这是专业开发的做法。
我按你的理解，给你一份完整的网站内容说明书。

## 一、页面层级图

http://localhost:8000/                        主页（index）
    │
    ├── 链接 → http://localhost:8000/blogs/               博客列表页（blogs）
    │               │
    │               ├── 链接 → /new_blog/                 新建博客页（new_blog）
    │               │
    │               └── 每个博客 → /blogs/<blog_id>/      博客详情页（blog）
    │                                     │
    │                                     ├── 链接 → /blogs/<id>/new_post/          新建博文页（new_post）
    │                                     │
    │                                     └── 每篇博文 → /blogs/<id>/edit_post/<post_id>/   编辑博文页（edit_post）
    │
    └── 导航栏链接（base.html 提供，所有页面共用）
            ├── 主页
            └── 所有博客


## 二、页面清单

| 页面          | URL                                          | 视图函数         | 模板                  | 作用 |
| 主页          | `/`                                          | `index`          | `index.html`          | 网站入口 |
| 博客列表      | `/blogs/`                                    | `blogs`          | `blogs.html`          | 显示所有博客 |
| 博客详情      | `/blogs/<blog_id>/`                          | `blog`           | `blog.html`           | 显示某博客及其博文 |
| 新建博客      | `/new_blog/`                                 | `new_blog`       | `new_blog.html`       | 表单：创建新博客 |
| 新建博文      | `/blogs/<blog_id>/new_post/`                 | `new_post`       | `new_post.html`       | 表单：在某博客下发博文 |
| 编辑博文      | `/blogs/<blog_id>/edit_post/<post_id>/`      | `edit_post`      | `edit_post.html`      | 表单：修改已有博文 |

---

## 三、每个页面的具体内容

### 1. 父模板 `base.html`

**作用**：所有页面的公共外框。

**内容**：
- 网站标题（欢迎来到博客世界）
- 导航栏：
  - 主页 → `/`
  - 所有博客 → `/blogs/`
- `{% block content %}{% endblock %}`：留给子模板填充内容

**所有子模板通过 `{% extends 'blogs_app/base.html' %}` 继承它。**

---

### 2. 主页 `index.html`

**URL**：`http://localhost:8000/`

**内容**：
- 一句欢迎语（国庆节快乐）
- 一个链接 → 跳转到博客列表页

**示例**：

```html
{% extends 'blogs_app/base.html' %}
{% block content %}
<p>国庆节快乐。</p>
<a href="{% url 'blogs_app:blogs' %}">查看所有博客</a>
{% endblock %}
```

---

### 3. 博客列表页 `blogs.html`

**URL**：`http://localhost:8000/blogs/`

**内容**：
- 显示所有博客（无序列表）
- 每个博客是一个链接，点击进入该博客详情页
- 一个“添加新博客”的链接

**示例**：

```html
{% extends 'blogs_app/base.html' %}
{% block content %}
<p>所有的 blog 主题都在这啦！</p>

<ul>
    {% for blog in blogs %}
    <li>
        <a href="{% url 'blogs_app:blog' blog.id %}">{{ blog.text }}</a>
    </li>
    {% empty %}
    <li>还没有创建博客主题呢</li>
    {% endfor %}
</ul>

<a href="{% url 'blogs_app:new_blog' %}">添加新博客</a>
{% endblock %}
```

---

### 4. 博客详情页 `blog.html`

**URL**：`http://localhost:8000/blogs/1/`

**内容**：
- 显示当前博客的标题
- 显示该博客下所有博文（无序列表）
- 每篇博文有“编辑”链接
- 一个“发布新博文”的链接

**示例**：

```html
{% extends 'blogs_app/base.html' %}
{% block content %}
<h2>{{ blog.text }}</h2>

<a href="{% url 'blogs_app:new_post' blog.id %}">+ 发布新博文</a>

<ul>
    {% for post in posts %}
    <li>
        <p>{{ post.date_added|date:'M d, Y H:i' }}</p>
        <p>{{ post.text|linebreaks }}</p>
        <a href="{% url 'blogs_app:edit_post' blog.id post.id %}">编辑</a>
    </li>
    {% empty %}
    <li>还没有给这个博客添加博文</li>
    {% endfor %}
</ul>
{% endblock %}
```

---

### 5. 新建博客页 `new_blog.html`

**URL**：`http://localhost:8000/new_blog/`

**内容**：
- 一个表单，让用户输入博客标题
- 提交按钮

**示例**：

```html
{% extends 'blogs_app/base.html' %}
{% block content %}
<p>添加新博客：</p>

<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">创建博客</button>
</form>
{% endblock %}
```

---

### 6. 新建博文页 `new_post.html`

**URL**：`http://localhost:8000/blogs/1/new_post/`

**内容**：
- 显示当前是给哪个博客添加博文
- 一个表单，让用户输入博文内容
- 提交按钮

**示例**：

```html
{% extends 'blogs_app/base.html' %}
{% block content %}
<p>为「{{ blog.text }}」添加新博文：</p>

<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">发布博文</button>
</form>
{% endblock %}
```

---

### 7. 编辑博文页 `edit_post.html`

**URL**：`http://localhost:8000/blogs/1/edit_post/1/`

**内容**：
- 一个表单，预填当前博文内容
- 用户修改后提交
- 提交按钮

**示例**：

```html
{% extends 'blogs_app/base.html' %}
{% block content %}
<p>编辑博文：</p>

<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">保存修改</button>
</form>
{% endblock %}
```

---

## 四、页面跳转流程

```
主页 /
  │
  └─→ 博客列表 /blogs/
        │
        ├─→ 新建博客 /new_blog/  （提交后返回博客列表）
        │
        └─→ 博客详情 /blogs/1/
              │
              ├─→ 新建博文 /blogs/1/new_post/  （提交后返回博客详情）
              │
              └─→ 编辑博文 /blogs/1/edit_post/1/  （提交后返回博客详情）
```

---

## 五、数据模型

```python
class Blog(models.Model):
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)

class Post(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
```

**关系**：

- 一个 Blog 可以有多个 Post
- 一个 Post 属于一个 Blog

---

## 六、表单

```python
class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['text']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['text']
```

---

## 七、开发顺序建议

| 步骤       | 做什么 |
| 1          | 写 `models.py`，迁移数据库 |
| 2          | 写 `forms.py` |
| 3          | 写 `views.py`（7 个视图函数） |
| 4          | 写 `urls.py`（7 条路由） |
| 5          | 写 `base.html` |
| 6          | 写 `index.html` |
| 7          | 写 `blogs.html` |
| 8          | 写 `blog.html` |
| 9          | 写 `new_blog.html` |
| 10         | 写 `new_post.html` |
| 11         | 写 `edit_post.html` |
| 12         | 测试所有页面 |
| 13         | 写 CSS 美化 |
| 14         | 部署 |

---

## 八、一句话总结

> **先画结构图，再写代码。**
> 你已经把结构图画清楚了，接下来就是按顺序填文件：模型 → 表单 → 视图 → URL → 模板 → 测试 → 美化 → 部署。

**这份说明就是你项目的“施工图”，按它一步步走，不会乱。**
"""

# 1.哪个链接挂到哪个链接里
# 2.<form action=...必须有{% csrf_token %}
# 3.url 有参数的，html里面就加上关键字参数。
# 4.html要规范：各个元素符号的用法，语句的顺序，闭合
# 5.views.py 导入是一个还没解决的问题。从哪里导入啥。
# 6.有post/get请求，也就是用户与网页互动，就要用form.分两种：直接form.save()的，和form.save(commit=False)的。要区别开。
# 7.models.py 中，啥时候需要class Meta 的。
