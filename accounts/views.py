from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render


# Create your views here.
def register(request):
    """注册新用户"""
    if request.method != "POST":
        form = UserCreationForm()
    else:
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            # form.save()
            new_user = form.save()
            login(request, new_user)
            return redirect("blogs_app:index")
    context = {"form": form}
    # 千万注意：这里是accounts的app。必须是registration文件夹下。
    return render(request, "registration/register.html", context)
