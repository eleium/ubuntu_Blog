from django.contrib.auth.decorators import login_required

from django.shortcuts import get_object_or_404, redirect, render
from .forms import BlogForm, PostForm
from .models import Blog, Post
from django.http import Http404


# Create your views here.
def index(request):
    # context={'text':text}
    return render(request, "blogs_app/index.html")


@login_required
def blogs(request):
    # blogs = Blog.objects.order_by("date_added")
    # 从笼统的objects转到objects.filter,过滤一下，只有拥有者是请求的用户的blog。
    blogs = Blog.objects.filter(owner=request.user).order_by("date_added")
    context = {"blogs": blogs}
    return render(request, "blogs_app/blogs.html", context)


@login_required
def blog(request, blog_id):
    blog = Blog.objects.get(id=blog_id)
    # 添加如果不是登录的用户，返回404错误
    if blog.owner != request.user:
        raise Http404

    posts = blog.post_set.order_by("-date_added")
    context = {"blog": blog, "posts": posts}
    return render(request, "blogs_app/blog.html", context)


@login_required
def new_blog(request):
    if request.method != "POST":
        form = BlogForm()
    else:
        form = BlogForm(data=request.POST)
        # 创建一个BlogForm()表单类的实例。
        # data 是 BlogForm（继承自 ModelForm → BaseForm）构造函数的一个参数，用来接收用户提交的数据。
        # request.POST: 用户提交的数据，以POST的方式。
        # 用户填了表单，点提交 → 浏览器把数据打包成 POST 请求 → Django 把它放进 request.POST。

        if form.is_valid():
            new_blog = form.save(commit=False)
            new_blog.owner = request.user
            new_blog.save()
            # form.save()
            return redirect("blogs_app:blogs")
    context = {"form": form}
    # form 是一个表单实例，它里面包含一个 text 字段，这个字段对应 Blog 模型里的 text 字段。
    # 用户在这个 text 字段里填的内容（比如“洛阳”），验证通过后会被保存到 Blog 对象的 text 属性里。
    # form 不是字段本身，而是“字段的容器”。

    # BlogForm 里的 fields = ['text']，决定了表单里有一个 text 字段。
    # 这个 text 字段，对应 Blog 模型里的 text 字段。
    # 用户填的“洛阳”，就是这个字段的值。
    # form 是“包含这个字段的表单实例”，不是字段本身。
    return render(request, "blogs_app/new_blog.html", context)


@login_required
def edit_blog(request, blog_id):
    # 更安全的写法：用户输入不存在的id，不会崩溃
    blog = get_object_or_404(Blog, id=blog_id)
    if blog.owner != request.user:
        raise Http404

    if request.method != "POST":
        form = BlogForm(instance=blog)
    else:
        form = BlogForm(instance=blog, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("blogs_app:blog", blog_id=blog.id)
    context = {"form": form, "blog": blog}
    return render(request, "blogs_app/edit_blog.html", context)


@login_required
def del_blog(request, blog_id):
    # 更安全的写法：用户输入不存在的id，不会崩溃
    blog = get_object_or_404(Blog, id=blog_id)
    if blog.owner != request.user:
        raise Http404

    if request.method == "POST":
        blog.delete()
        return redirect("blogs_app:blogs")
    context = {"blog": blog}
    return render(request, "blogs_app/del_blog.html", context)


@login_required
def new_post(request, blog_id):
    # 1. 根据 URL 传来的 blog_id，查出要加博文的博客
    blog = Blog.objects.get(id=blog_id)
    if blog.owner != request.user:
        raise Http404

    if request.method != "POST":
        # 2. GET 请求：创建一个空表单，给用户填
        form = PostForm()
    else:
        # 3. POST 请求：用用户提交的数据创建表单
        form = PostForm(data=request.POST)
        if form.is_valid():
            # 4. 验证通过，先不保存到数据库
            new_post = form.save(commit=False)
            # 5. 把这篇博文关联到当前博客
            new_post.blog = blog
            # 6. 现在才保存到数据库
            new_post.save()
            # 7. 跳回当前博客的详情页,目的：防止用户按 F5 重复提交表单。
            return redirect("blogs_app:blog", blog_id=blog.id)

    context = {"form": form, "blog": blog}
    # context所需要传递给new_post.html的内容，一定来自本视图函数：
    # blog = Blog.objects.get(id=blog_id) 和 form = PostForm(data=request.POST)

    # {{ blog }} 到底显示什么，取决于 Blog 模型的 __str__() 方法。
    # 📌 为什么只显示 text，不显示 date_added？
    # 因为 {{ blog }} 调用的是 Blog.__str__()，而你（或教程）只让 __str__() 返回 text。
    # 所以 {{ blog }} 就只显示 text，不显示 date_added。

    # 📌 如果想显示 date_added，怎么办？
    # 方法 1：直接取属性
    # {{ blog.text }}
    # {{ blog.date_added }}
    return render(request, "blogs_app/new_post.html", context)


# PostForm 实例有 is_valid()、save() 等方法
# 它的字段是 text，对应 Post 模型的 text 字段,是TextField,是长文本，没有字数强制的限制。
# labels 和 model 不在实例上，它们在 Meta 里，是“配置”（BlogForm/PostForm 都有必须的Meta.)
# 更准确的说法：
# 这个实例包含 text 字段，以及验证、保存等方法。labels 和 model 是 PostForm.Meta 里的配置，控制表单怎么显示、基于哪个模型。

"""
现在新建了form, (form=PostForm(data=request.POST)。这是一个新表单，带有数据。用户已经编写了新的博文。
那么new_post又是啥？关联到blog，实际上是什么动作？目的是成为这个blog的一个post,怎么实现的呢？


你问到了 `form.save(commit=False)` 最核心的机制。我一步步拆开。

### 📌 先分清两个东西

| 名字                 | 是什么 |
| `form`               | `PostForm` 实例，**用户填的数据 + 验证逻辑** |
| `new_post`           | `Post` 模型实例，**准备存进数据库的记录** ,调用了 form.save()，Django 在背后执行了创建动作

**`form` 是“表单”，`new_post` 是“数据库记录”。**

### 📌 `form.save(commit=False)` 做了什么？
new_post = form.save(commit=False)

**这一句，Django 做了两件事：**

1. **根据 `form` 里用户填的数据，创建一个 `Post` 对象**(这个对象就是new_post)
2. **但暂时不把它存进数据库**

**`new_post` 就是这个 `Post` 对象。**
它的 `text` 字段已经有用户输入的内容：Post模型有text=model.TextField(),字数不受限制（比如“洛阳有三条大河”），但：

- **它还没有 `id`**（因为没存数据库，Django 还没分配主键）
- **它的 `blog_id` 还是空的**（因为 `PostForm` 里只包含 `text` 字段，没有 `blog` 字段）

### 📌 `new_post.blog = blog` 是什么动作？
new_post.blog = blog
**这是 Python 的“属性赋值”。**

- `new_post` 是一个 `Post` 实例
- `blog` 是一个 `Blog` 实例
- `new_post.blog` 是 `Post` 的**外键字段**
- **赋值后，`new_post` 就知道自己属于哪个 `Blog` 了**

**数据库层面，这个动作相当于：**
> 把 `new_post` 的 `blog_id` 设为 `blog.id`
**比如 `blog.id = 1`，那 `new_post.blog_id` 就变成 `1`。**

### 📌 `new_post.save()` 做了什么？
new_post.save()
**这时才真正写入数据库：**

- Django 给 `new_post` 分配一个 `id`（比如 3）
- 把 `text`、`blog_id`、`date_added` 一起写入数据库
**数据库里就多了一条 Post 记录：**

id=3, text='洛阳有三条大河', blog_id=1, date_added=...
**这条记录的 `blog_id=1`，说明它属于 id=1 的那个博客。**

### 📌 怎么实现“成为这个 blog 的一个 post”？
**靠的就是外键。**
`Post` 模型里：
blog = models.ForeignKey(Blog, on_delete=models.CASCADE)

**这个外键，在数据库里就是 `blog_id` 这一列。**

- `new_post.blog = blog` → 设置 `blog_id`
- `new_post.save()` → 把 `blog_id` 写入数据库

**数据库里，只要 `Post` 的 `blog_id` 等于某个 `Blog` 的 `id`，它就“属于”那个博客。**

### 📌 为什么必须用 `commit=False`？
**如果不写 `commit=False`：**
new_post = form.save()   # 直接存数据库
**会报错：**
IntegrityError: NOT NULL constraint failed: blogs_app_post.blog_id
**因为 `Post` 的 `blog` 字段是必填的（NOT NULL），但表单里没有 `blog` 字段，Django 不知道填什么，数据库拒绝插入。**

**用了 `commit=False`：**
1. 先创建对象，不存数据库
2. 手动补上 `blog`
3. 再 `save()`，这时数据完整了

### 🎯 一句话总结
> **`form.save(commit=False)` 创建 Post 对象但不存数据库，`new_post.blog = blog` 设置外键，`new_post.save()` 才真正写入。**
> **“成为某个 blog 的 post”，就是靠 `blog_id` 这一列。** 只要 `Post.blog_id` 指向某个 `Blog.id`，数据库里它们就关联上了。

**`commit=False` 的意义：给你一个机会，在保存前补上表单里没有的字段（比如外键）。**
"""


@login_required
def edit_post(request, blog_id, post_id):
    # 定义编辑博文函数，接收 URL 传来的 blog_id 和 post_id
    post = Post.objects.get(id=post_id)
    # 根据 post_id 查出要编辑的博文
    blog = post.blog
    # 取出这篇博文所属的博客（通过外键 post.blog）
    if blog.owner != request.user:
        raise Http404

    if request.method != "POST":
        # GET 请求：显示带原有数据的表单
        form = PostForm(instance=post)
    else:
        # POST 请求：用用户提交的数据，更新这个已有对象
        form = PostForm(instance=post, data=request.POST)
        if form.is_valid():
            # 验证通过，保存更新
            form.save()
            # 跳回该博客的详情页
            return redirect("blogs_app:blog", blog_id=blog.id)

    # 把表单、博文、博客都传给模板
    context = {"form": form, "post": post, "blog": blog}
    # 渲染 edit_post.html
    return render(request, "blogs_app/edit_post.html", context)


@login_required
def del_post(request, blog_id, post_id):
    blog = get_object_or_404(Blog, id=blog_id)
    post = get_object_or_404(Post, blog=blog, id=post_id)
    if blog.owner != request.user:
        raise Http404
    if request.method == "POST":
        post.delete()
        return redirect("blogs_app:blog", blog_id=blog.id)
    context = {"blog": blog, "post": post}
    return render(request, "blogs_app/del_post.html", context)
