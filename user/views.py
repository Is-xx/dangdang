from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
import random, string
from user.captcha.image import ImageCaptcha
from user.models import TUser


# 注册
def register(request):
    u = request.GET.get('u')
    request.session['u'] = u
    if u == 'booklist':
        u_level = request.GET.get('level')
        u_id = request.GET.get('id')
        request.session['u_level'] = u_level
        request.session['u_id'] = u_id
    if u == 'Book details':
        u_id = request.GET.get('id')
        request.session['u_id'] = u_id
    return render(request, 'register.html')


# 验证码
def getcaptcha(request):
    image = ImageCaptcha()
    code = random.sample(string.ascii_lowercase + string.ascii_uppercase + string.digits, 4)
    random_code = ''.join(code)
    request.session['captcha'] = random_code
    data = image.generate(random_code)
    return HttpResponse(data, 'image/png')


# 注册逻辑
def register_logic(request):
    code = request.session.get('captcha')
    recode = request.POST.get('txt_vcode')
    if code.lower() == recode.lower():
        name = request.POST.get('txt_username')
        pwd = request.POST.get('txt_password')
        user = TUser.objects.filter(username=name)
        if user:
            return HttpResponse('error1')
        with transaction.atomic():
            TUser.objects.create(username=name, userpwd=pwd)
        return HttpResponse('ok')
    return HttpResponse('error')


# 注册成功
def register_ok(request):
    u = request.session.get('u')
    u_level = request.session.get('u_level')
    u_id = request.session.get('u_id')
    username = request.GET.get('username')
    request.session['username'] = username
    content = {
        'u': u,
        'u_level': u_level,
        'u_id': u_id,
        'username': username,
    }
    return render(request, 'register ok.html', content)


# 登录
def login(request):
    u = request.GET.get('u')
    request.session['u'] = u
    if u == 'booklist':
        u_level = request.GET.get('level')
        u_id = request.GET.get('id')
        request.session['u_level'] = u_level
        request.session['u_id'] = u_id
    if u == 'Book details':
        u_id = request.GET.get('id')
        request.session['u_id'] = u_id
    name = request.COOKIES.get('username')
    if name:
        request.session['username'] = name
        return redirect('index:index')
    return render(request, 'login.html', {'u': u})


# 登录逻辑
def login_logic(request):
    u = request.session.get('u')
    name = request.GET.get('name')
    pwd = request.GET.get('pwd')
    code = request.GET.get('code')
    captcha = request.session.get('captcha')
    user = TUser.objects.filter(username=name)
    if code.lower() != captcha.lower():
        msg = '1'
    else:
        if user:
            if user[0].userpwd == pwd:
                u_level = request.session.get('u_level')
                u_id = request.session.get('u_id')
                content = {
                    'u': u,
                    'u_level': u_level,
                    'u_id': u_id,
                }
                request.session['username'] = name
                res = JsonResponse(content)
                remember = request.GET.get('remember')
                if remember == 'true':
                    res.set_cookie('username', name, max_age=7 * 24 * 60 * 60)
                    res.set_cookie('userpwd', pwd, max_age=7 * 24 * 60 * 60)
                return res
            else:
                msg = '3'
        else:
            msg = '2'
    content = {
        'msg': msg,
    }
    return JsonResponse(content)
