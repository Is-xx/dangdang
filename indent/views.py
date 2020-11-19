import random
import string
import time

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from user.models import TAddress, TUser, TOrder, TCart, TBook, TOrderBook


# 订单
def indent(request):
    username = request.session['username']
    user_id = TUser.objects.filter(username=username)[0].id
    addr = TAddress.objects.filter(user_id=user_id)
    cart = request.session.get('cart')
    if cart:
        for i in cart:
            exit_book = TCart.objects.filter(book_id=i.id, user_id=user_id)
            if exit_book:
                exit_book[0].number += i.count
            else:
                TCart.objects.create(book_id=i.id, user_id=user_id, number=i.count)
        del request.session['cart']
    login_cart = TCart.objects.filter(user_id=user_id)
    num_list = []
    for j in login_cart:
        num_list.append(j.number)
    cart_books = []
    sum = count = 0
    index = 0
    for i in login_cart:
        book = TBook.objects.filter(id=i.book_id)[0]
        book.count = num_list[index]
        book.amount = round(book.d_price * book.count)
        sum += book.d_price * book.count
        count += book.count
        cart_books.append(book)
        index += 1
    content = {
        'addr': list(addr),
        'cart_books': cart_books,
        'sum': sum,
        'username': username,
    }
    return render(request, 'indent.html', content)


# 提交订单成功
def indent_ok(request):
    username = request.session['username']
    ad_count = request.GET.get('count')
    order_id = request.GET.get('order_id')
    sum = request.GET.get('sum')
    add_name = request.GET.get('name')
    content = {
        'ad_count': ad_count,
        'order_id': order_id,
        'sum': sum,
        'add_name': add_name,
        'username': username,
    }
    return render(request, 'indent ok.html', content)


# 用户退出
def exit(request):
    del request.session['username']
    return redirect('index:index')


# 订单提交
def indent_submit(request):
    address_detail = request.GET.get('address')
    name = request.GET.get('name')
    code = request.GET.get('code')
    phone = request.GET.get('phone')
    call = request.GET.get('call')
    username = request.session.get('username')
    user_id = TUser.objects.filter(username=username)[0].id
    flag = True
    for i in TAddress.objects.filter(user_id=user_id):
        if address_detail == i.detail_address:
            flag = False
    # 创建收货地址
    if flag:
        if phone:
            TAddress.objects.create(name=name, post_code=code, detail_address=address_detail, phone=phone,
                                    user_id=user_id)
        else:
            TAddress.objects.create(name=name, post_code=code, detail_address=address_detail, phone=call,
                                    user_id=user_id)
    address_id = TAddress.objects.filter(detail_address=address_detail)[0].id
    t_id = True
    while t_id:
        order_id = random.sample(string.digits, 6)
        order_id = ''.join(order_id)
        order = TOrder.objects.filter(order_id=order_id)
        if not order:
            t_id = False
    login_cart = TCart.objects.filter(user_id=user_id)
    num_list = []
    for j in login_cart:
        num_list.append(j.number)
    cart_books = []
    sum = count = 0
    index = 0
    # 订单总价及数量
    for i in login_cart:
        book = TBook.objects.filter(id=i.book_id)[0]
        book.count = num_list[index]
        sum += book.d_price * book.count
        count += book.count
        cart_books.append(book)
        index += 1
    TOrder.objects.create(order_id=order_id, order_time=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
                          order_money=sum,
                          address_id=address_id, user_id=user_id)
    for book in cart_books:
        TOrderBook.objects.create(order_id=order_id, book_id=book.id, number=book.count)
    TCart.objects.all().delete()
    content = {
        'ad_count': count,
        'order_id': order_id,
        'sum': sum,
        'add_name': name,
    }
    return JsonResponse(content)


# 选择地址
def select(request):
    detail_addr = request.GET.get('addr')
    addr = TAddress.objects.filter(detail_address=detail_addr)[0]
    content = {
        'name': addr.name,
        'phone': addr.phone,
        'code': addr.post_code,
    }
    return JsonResponse(content)
