import os, django, random
import string
from datetime import datetime

from django.test import TestCase

# Create your tests here.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dangdang.settings")
django.setup()

from user.models import TBook

# first_name = ["王", "李", "张", "刘", "赵", "蒋", "孟", "陈", "徐", "杨", "沈", "马", "高", "殷", "上官", "钟", "常"]
# second_name = ["伟", "华", "建国", "洋", "刚", "万里", "爱民", "牧", "陆", "路", "昕", "鑫", "兵", "硕", "志宏", "峰", "磊", "雷", "文","明浩", "光", "超", "军", "达"]
#
# for i in range(20):
#     book = TBook.objects.create(
#         name=random.choice(second_name) + random.choice(first_name),
#         price=random.randint(10, 50),
#         d_price=random.randint(10, 50),
#         picture='',
#         author=random.choice(first_name) + random.choice(second_name),
#         press=random.choice(second_name)+'出版社',
#         date=datetime.now().strftime('%Y-%m-%d'),
#         introduction=''.join(random.sample(string.ascii_lowercase, 20)),
#         book_isbn=''.join(random.sample(string.digits, 8)),
#         world_count=random.randint(500, 20000),
#         page_count=random.randint(100,300),
#         open_type='16k',
#         book_paper='白纸',
#         menu=''.join(random.sample(string.ascii_lowercase, 20)),
#         socre=random.randint(0, 10),
#         stock=random.randint(1, 500),
#         sales=random.randint(1, 500),
#         review=''.join(random.sample(string.ascii_lowercase, 20)),
#     )
