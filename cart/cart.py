from user.models import TBook


# 书籍类
class Book:
    def __init__(self, id, count):
        book = TBook.objects.filter(id=id)[0]
        self.id = id  # id
        self.count = int(count)  # 数量
        self.name = book.name  # 书名
        self.d_price = float(book.d_price)  # 折扣价
        self.picture = book.picture  # 书籍图片


# 购物车类
class Cart:
    def __init__(self):
        self.book_list = []
        self.__index = 0

    # 迭代器
    def __iter__(self):
        return self

    # 迭代方法
    def __next__(self):
        if self.__index < len(self.book_list):
            item = self.book_list[self.__index]
            self.__index += 1
            return item
        else:
            self.__index = 0
            raise StopIteration

    # 获取书籍对象
    def get_book(self, id):
        for book in self.book_list:
            if book.id == id:
                return book

    # 添加书籍
    def add_books(self, id, count=1):
        book = self.get_book(id)
        if book:
            book.count = int(book.count) + int(count)
        else:
            book = Book(id=id, count=count)
            self.book_list.append(book)

    # 删除一本书籍
    def del_book(self, id):
        book = self.get_book(id)
        if int(book.count) > 1:
            book.count = int(book.count) - 1

    # 清空购物车
    def remove_book(self, id):
        book = self.get_book(id)
        self.book_list.remove(book)
