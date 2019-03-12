from django.shortcuts import render, redirect, HttpResponseRedirect, Http404
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse

# Create your views here.


def register(request):
    # 从 get 或者 post 请求中获取 next 参数值
    # get 请求中，next 通过 url 传递，即 /?next=value
    # post 请求中，next 通过表单传递，即 <input type="hidden" name="next" value="{{ next }}"/>
    redirect_to = request.POST.get('next', request.GET.get('next', ''))
    # 只有当请求为 POST 时，才表示用户提交了注册信息
    if request.method == 'POST':
        # request.POST 是一个类字典数据结构，记录了用户提交的注册信息
        # 这里提交的就是用户名（username）、密码（password）、邮箱（email）
        # 用这些数据实例化一个用户注册表单
        form = RegisterForm(request.POST)

        # 验证数据的合法性
        if form.is_valid():
            # 如果提交数据合法，调用表单的 save 方法将用户数据保存到数据库
            form.save()

            if redirect_to:
                return redirect(redirect_to)
            else:
                # 注册成功，跳转回首页
                return redirect('/')
    else:
        # 请求不是 POST，表明用户正在访问注册页面，展示一个空的注册表单给用户
        form = RegisterForm()

    # 渲染模板
    # 如果用户正在访问注册页面，则渲染的是一个空的注册表单
    # 如果用户通过表单提交注册信息，但是数据验证不合法，则渲染的是一个带有错误信息的表单
    return render(request, 'users/register.html', context={'form': form, 'next': redirect_to})


@login_required(login_url='login')
def shelf(request):
    book_list = request.user.favorates.all()
    page_name = 'My Shelf'
    return render(request, 'novel/index.html', context={
        'book_list': book_list,
        'page_name': page_name
    })


@login_required(login_url='login')
def add_to_favorate(request, book_id, slug):
    book = book_id
    if (slug == 'add'):
        request.user.favorates.add(book)
        return HttpResponseRedirect(reverse('book_detail', args=(book_id,)))
    elif(slug == 'drop'):
        request.user.favorates.remove(book)
        return HttpResponseRedirect(reverse('book_detail', args=(book_id,)))
    else:
        raise Http404("Request Error")
