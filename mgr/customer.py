from django.http import JsonResponse
import json


from common.models import Customer

def dispatcher(request):
    # 根据session判断用户是否是登录的管理员用户
    if 'usertype' not in request.session:
        return JsonResponse({
            'ret': 302,
            'msg': '未登录',
            'redirect': '/mgr/sign.html'},
            status=302)

    if request.session['usertype'] != 'mgr' :
        return JsonResponse({
            'ret': 302,
            'msg': '用户非mgr类型',
            'redirect': '/mgr/sign.html'} ,
            status=302)
    # 将请求参数统一放入request 的 params 属性中，方便后续处理
    # GET请求 参数 在 request 对象的 GET属性中
    if request.method == 'GET':
        request.params = request.GET

    # POST/PUT/DELETE 请求 参数 从 request 对象的 body 属性中获取
    elif request.method in ['POST','PUT','DELETE']:
        # 根据接口，POST/PUT/DELETE 请求的消息体都是 json格式
        request.params = json.loads(request.body)


    # 根据不同的action分派给不同的函数进行处理
    action = request.params['action']
    if action == 'list_customer':
        return list_customers(request)
    elif action == 'add_customer':
        return add_customer(request)
    elif action == 'modify_customer':
        return modify_customer(request)
    elif action == 'del_customer':
        return delete_customer(request)

    else:
        return JsonResponse({'ret': 1, 'msg': '不支持该类型http请求'})


def list_customers(request):
    # 返回一个 QuerySet 对象 ，包含所有的表记录
    qs = Customer.objects.values()

    # 将 QuerySet 对象 转化为 list 类型
    # 否则不能 被 转化为 JSON 字符串
    retlist = list(qs)

    return JsonResponse({'ret': 0, 'retlist': retlist})


def add_customer(request):

    info    = request.params['data']

    # 从请求消息中 获取要添加客户的信息
    # 并且插入到数据库中
    # 返回值 就是对应插入记录的对象
    record = Customer.objects.create(name=info['name'] ,
                            phonenumber=info['phonenumber'] ,
                            address=info['address'])


    return JsonResponse({'ret': 0, 'id':record.id})


def modify_customer(request):
    # 从请求消息中 获取修改客户的信息
    # 找到该客户，并且进行修改操作

    customerid = request.params['id']
    newdata = request.params['newdata']

    try:
        # 根据 id 从数据库中找到相应的客户记录
        customer = Customer.objects.get(id=customerid)
    except Customer.DoesNotExist:
        return {
            'ret': 1,
            'msg': f'id 为`{customerid}`的客户不存在'
        }

    if 'name' in newdata:
        customer.name = newdata['name']
    if 'phonenumber' in newdata:
        customer.phonenumber = newdata['phonenumber']
    if 'address' in newdata:
        customer.address = newdata['address']

    # 注意，一定要执行save才能将修改信息保存到数据库
    customer.save()

    return JsonResponse({'ret': 0})


def delete_customer(request):

    customerid = request.params['id']



    try:
        # 根据 id 从数据库中找到相应的客户记录
        customer = Customer.objects.get(id=customerid)
    except Customer.DoesNotExist:
        return  {
                'ret': 1,
                'msg': f'id 为`{customerid}`的客户不存在'
        }

    # delete 方法就将该记录从数据库中删除了
    customer.delete()

    return JsonResponse({'ret': 0})
