# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


# 收货地址
class TAddress(models.Model):
    name = models.CharField(max_length=20, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=50, blank=True, null=True)
    detail_address = models.CharField(max_length=100, blank=True, null=True)
    user = models.ForeignKey('TUser', models.DO_NOTHING, blank=True, null=True)
    post_code = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_address'


# 书籍类
class TBook(models.Model):
    name = models.CharField(max_length=20, blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    d_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    picture = models.CharField(max_length=100, blank=True, null=True)
    author = models.CharField(max_length=20, blank=True, null=True)
    press = models.CharField(max_length=20, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    category = models.ForeignKey('TCategory', models.DO_NOTHING, blank=True, null=True)
    introduction = models.CharField(max_length=500, blank=True, null=True)
    book_isbn = models.CharField(max_length=64, blank=True, null=True)
    world_count = models.IntegerField(blank=True, null=True)
    page_count = models.IntegerField(blank=True, null=True)
    open_type = models.CharField(max_length=20, blank=True, null=True)
    book_paper = models.CharField(max_length=20, blank=True, null=True)
    menu = models.CharField(max_length=500, blank=True, null=True)
    score = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    stock = models.IntegerField(blank=True, null=True)
    sales = models.IntegerField(blank=True, null=True)
    review = models.CharField(max_length=500, blank=True, null=True)

    # 折扣
    @property
    def discount(self):
        return round(self.d_price / self.price * 10, 2)

    class Meta:
        managed = False
        db_table = 't_book'


# 购物车类
class TCart(models.Model):
    user = models.ForeignKey('TUser', models.DO_NOTHING, blank=True, null=True)
    book = models.ForeignKey(TBook, models.DO_NOTHING, blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_cart'


# 书籍类别
class TCategory(models.Model):
    class_name = models.CharField(max_length=20, blank=True, null=True)
    level = models.IntegerField(blank=True, null=True)
    category_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_category'


# 订单类
class TOrder(models.Model):
    order_id = models.IntegerField(blank=True, null=True)
    order_time = models.DateTimeField(blank=True, null=True)
    order_money = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    payment_method = models.CharField(max_length=20, blank=True, null=True)
    address = models.ForeignKey(TAddress, models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('TUser', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_order'


# 订单项
class TOrderBook(models.Model):
    order = models.ForeignKey(TOrder, models.DO_NOTHING, blank=True, null=True)
    book = models.ForeignKey(TBook, models.DO_NOTHING, blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_order_book'


# 用户
class TUser(models.Model):
    username = models.CharField(max_length=20, blank=True, null=True)
    userpwd = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_user'
