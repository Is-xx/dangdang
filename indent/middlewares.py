from django.shortcuts import render
from django.utils.deprecation import MiddlewareMixin


class MyMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        super().__init__(get_response)

    # view处理请求前执行
    def process_request(self, request):
        # 强制登陆
        if "indent" in request.path:
            session = request.session
            if session.get("username"):
                pass
            else:
                return render(request, "login.html")

    # 在process_request之后View之前执行
    def process_view(self, request, view_func, view_args, view_kwargs):
        pass

    # view执行之后，响应之前执行
    def process_response(self, request, response):
        return response

    # 如果View中抛出了异常
    def process_exception(self, request, ex):
        pass
