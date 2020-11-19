from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from user.models import TCategory
from user.models import TBook


# 首页
def index(request):
    request.session['u'] = 'index'
    username = request.session.get('username')
    cate1 = TCategory.objects.filter(level=1)
    care2 = TCategory.objects.filter(level=2)
    new_books = TBook.objects.all().order_by('-date')[:8]
    recommend = TBook.objects.all().order_by('-score')[:8]
    sales = TBook.objects.all().order_by('-sales')[:5]
    sales2 = TBook.objects.all().order_by('-sales')[:10]
    content = {
        'username': username,
        'cates1': cate1,
        'cates2': care2,
        'new_books': new_books,
        'recommend': recommend,
        'sales': sales,
        'sales2': sales2,
    }
    return render(request, 'index.html', content)


# 书籍信息
def detail(request):
    username = request.session.get('username')
    id = request.GET.get('id')
    request.session['u'] = 'Book details'
    request.session['u_id'] = id
    book = TBook.objects.get(id=id)
    discount = round(book.d_price / book.price, 2)
    cate2 = TCategory.objects.filter(tbook__id=id)[0]
    cate1 = TCategory.objects.filter(id=cate2.category_id)[0]
    content = {
        'username': username,
        'book': book,
        'discount': discount,
        'cate1': cate1,
        'cate2': cate2,
    }
    return render(request, 'Book details.html', content)


# 书籍分类
def list(request):
    username = request.session.get('username')
    num = request.GET.get('num', 1)
    cate1 = TCategory.objects.filter(level=1)
    care2 = TCategory.objects.filter(level=2)
    level = request.GET.get('level')
    id = request.GET.get('id')
    request.session['u'] = 'booklist'
    request.session['u_id'] = id
    request.session['u_level'] = level
    if level == '1':
        catetit1 = TCategory.objects.filter(id=id)[0]
        catetit2 = ''
        books = TBook.objects.filter(category__category_id=id)
    else:
        catetit2 = TCategory.objects.filter(id=id)[0]
        catetit1 = TCategory.objects.filter(id=catetit2.category_id)[0]
        books = TBook.objects.filter(category_id=id)
    cont = books.count()
    pagtor = Paginator(books, per_page=3)
    page = pagtor.page(num)
    content = {
        'username': username,
        'catetit1': catetit1,
        'catetit2': catetit2,
        'cont': cont,
        'level': level,
        'id': id,
        'page': page,
        'cates1': cate1,
        'cates2': care2,
    }
    return render(request, 'booklist.html', content)


# 用户退出
def quit(request):
    u_level = request.session.get('u_level')
    u_id = request.session.get('u_id')
    content = {
        'u_level': u_level,
        'u_id': u_id,
    }
    res = JsonResponse(content)
    del request.session['username']
    res.set_cookie('username', max_age=0)
    res.set_cookie('userpwd', max_age=0)
    return res
