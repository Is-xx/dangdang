from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from cart.cart import Cart
from user.models import TCart, TUser, TBook


# 展示购物车
def cart(request):
    request.session['u'] = 'cart'
    login = request.session.get('username')
    cart = request.session.get('cart')
    # 检查登陆状态
    if login:
        user_id = TUser.objects.filter(username=login)[0].id
        # 未登录状态下的购物车
        if cart:
            for i in cart:
                exit_book = TCart.objects.filter(book_id=i.id, user_id=user_id)
                if exit_book:
                    exit_book[0].number += i.count
                else:
                    TCart.objects.create(book_id=i.id, user_id=user_id, number=i.count)
            del request.session['cart']
        # 用户对应的购物车表
        login_cart = TCart.objects.filter(user_id=user_id)
        num_list = []
        for j in login_cart:
            num_list.append(j.number)
        cart_books = []
        sum = count = 0
        index = 0
        # 购物车总价及数量
        for i in login_cart:
            book = TBook.objects.filter(id=i.book_id)[0]
            book.count = num_list[index]
            book.amount = round(book.d_price * book.count)
            sum += book.d_price * book.count
            count += book.count
            cart_books.append(book)
            index += 1
        # 前端接收数据
        login_content = {
            'username': login,
            'login_cart': cart_books,
            'count': count,
            'sum': sum,
        }
        return render(request, 'car.html', login_content)
    sum = count = 0
    if cart:
        for i in cart:
            total = i.d_price * int(i.count)
            sum += total
            count += int(i.count)
    content = {
        'count': count,
        'sum': sum,
        'cart': cart,
        'username': login,
    }
    return render(request, 'car.html', content)


# 添加购物车
def add_cart(request):
    id = request.GET.get('id')
    count = request.GET.get('count')
    login = request.session.get('username')
    # 检查登录
    if login:
        user_id = TUser.objects.filter(username=login)[0].id
        exit_book = TCart.objects.filter(book_id=id, user_id=user_id)
        # 检查购物车中是否有该书
        if exit_book:
            exit_book[0].number += int(count)
        else:
            TCart.objects.create(book_id=id, user_id=user_id, number=count)
        return HttpResponse('ok')
    cart = request.session.get('cart')
    if not cart:
        # 创建一个临时购物车
        cart = Cart()
    cart.add_books(id, count)
    request.session['cart'] = cart
    return HttpResponse('ok')


# 购物车减一
def sub_cart(request):
    id = request.GET.get('id')
    cart = request.session.get('cart')
    cart.del_book(id)
    request.session['cart'] = cart
    return HttpResponse('ok')


# 书籍总价
def total_book(request):
    id = request.GET.get('id')
    books = request.session.get('cart')
    book = books.get_book(id)
    total = book.d_price * book.count
    return HttpResponse(total)


# 清空购物车
def del_cart(request):
    id = request.GET.get('id')
    cart = request.session.get('cart')
    cart.remove_book(id)
    request.session['cart'] = cart
    return HttpResponse('ok')


# 计算购物车总价
def big_total(request):
    login = request.session.get('username')
    # 检查登录
    if login:
        login_cart = TCart.objects.all()
        num_list = []
        for j in login_cart:
            num_list.append(j.number)
        cart_books = []
        sum = count = 0
        index = 0
        for i in login_cart:
            book = TBook.objects.filter(id=i.book_id)[0]
            book.count = num_list[index]
            sum += book.d_price * book.count
            count += book.count
            cart_books.append(book)
            index += 1
    else:
        books = request.session.get('cart')
        sum = 0
        count = 0
        for i in books:
            total = i.d_price * int(i.count)
            sum += total
            count += int(i.count)
    content = {
        'sum': sum,
        'count': count,
    }
    return JsonResponse(content)


# 书籍加一
def add_login_cart(request):
    id = request.GET.get('id')
    login = request.session.get('username')
    user_id = TUser.objects.filter(username=login)[0].id
    book = TCart.objects.filter(book_id=id, user_id=user_id)[0]
    book.number = book.number + 1
    book.save()
    return HttpResponse('ok')


# 书籍减一
def sub_login_cart(request):
    id = request.GET.get('id')
    login = request.session.get('username')
    user_id = TUser.objects.filter(username=login)[0].id
    book = TCart.objects.filter(book_id=id, user_id=user_id)[0]
    book.number = book.number - 1
    book.save()
    return HttpResponse('ok')


# 书籍总价
def total_login_book(request):
    id = request.GET.get('id')
    login = request.session.get('username')
    user_id = TUser.objects.filter(username=login)[0].id
    num = TCart.objects.filter(book_id=id, user_id=user_id)[0].number
    price = TBook.objects.filter(id=id)[0].d_price
    total = num * price
    return HttpResponse(total)


# 删除书籍
def del_login_cart(request):
    id = request.GET.get('id')
    login = request.session.get('username')
    user_id = TUser.objects.filter(username=login)[0].id
    TCart.objects.filter(book_id=id, user_id=user_id)[0].delete()
    return HttpResponse('ok')
