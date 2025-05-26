from datetime import timedelta

from django.http import JsonResponse

from django.contrib.auth import authenticate, login, logout
from datetime import timedelta


# 登录处理
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from django.contrib.sessions.models import Session

def clean_expired_sessions():
    """清理过期的session"""
    # 获取当前时间
    now = timezone.now()
    # 查询所有过期的session并删除它们
    Session.objects.filter(expire_date__lt=now).delete()

def signin(request):
    """处理用户登录"""
    if request.method == 'POST':
        # 清理过期的session
        clean_expired_sessions()

        # 获取用户名和密码
        username = request.POST.get('username')
        password = request.POST.get('password')

        # 验证用户名和密码
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                if user.is_superuser:
                    login(request, user)
                    # 在session中存入用户类型
                    request.session['usertype'] = 'mgr'
                    # 设置session过期时间（这里是1分钟）
                    request.session.set_expiry(timedelta(hours=1))
                    session_id = request.session.session_key
                    if not session_id:
                        # 如果session_id为空，抛出重新登录的提示
                        return JsonResponse({'ret': 1, 'msg': '请重新登录'})
                    # 返回登录成功的结果，并将 session_id 存入返回结果中
                    return JsonResponse({'ret': 0, 'session_id': session_id})
                else:
                    return JsonResponse({'ret': 1, 'msg': '请使用管理员账户登录'})
            else:
                return JsonResponse({'ret': 0, 'msg': '用户已经被禁用'})
        else:
            return JsonResponse({'ret': 1, 'msg': '用户不存在或密码错误'})
    else:
        return JsonResponse({'ret': 1, 'msg': '请求方法不正确'})




# 登出处理
def signout( request):
    # 使用登出方法
    logout(request)
    return JsonResponse({'ret': 0})