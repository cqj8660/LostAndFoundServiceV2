import datetime
import json
import traceback

from django.http import HttpResponse, JsonResponse

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from lib import client
from lib.client import studentLogin, rpc
from lib.utils import log
from lib.view import check
from user.models import UserOpenid, User


@csrf_exempt
def getOpenid(request):
    required = {'js_code'}
    if not required.issubset(set(request.POST.keys())):
        return HttpResponse(json.dumps({'code': -1, 'msg': 'unexpected params!',
                                        'data': {'required': list(required), 'yours': request.POST.dict()}}))
    res=client.getOpenid(request.POST['js_code'])
    return JsonResponse(res)

@csrf_exempt
def loginByOpenid(request):
    res={'code':0, 'msg':'success', 'data':[]}
    required={'openid'}
    if not required.issubset(set(request.POST.keys())):
        return HttpResponse(json.dumps({'code': -1, 'msg': 'unexpected params!', 'data': {'required':list(required),'yours':request.POST.dict()}}))
    try:
        openid=request.POST['openid']
        user_openid=UserOpenid.objects.get(openid=openid, status=1)
        user_info=User.objects.get(id=user_openid.user_id)
        res['data']=user_info.format()
    except Exception as e:
        res={'code':-2, 'msg':e.__str__(), 'data':[]}
    return HttpResponse(json.dumps(res))

@csrf_exempt
def login(request):
    res={'code':0, 'msg':'success', 'data':[]}
    required={'openid','stu_id','password','phone','avatar','gender','nick_name'}
    if not required.issubset(set(request.POST.keys())):
        return JsonResponse({'code': -1, 'msg': 'unexpected params!', 'data': {'required':list(required),'yours':request.POST.dict()}})
    try:
        #鉴权：
        login_res=studentLogin(request.POST['stu_id'],request.POST['password'])
        if login_res['code']!=0:
            return JsonResponse(login_res)
        else:
            #鉴权通过
            #注册或更新用户信息
            stu_id=request.POST['stu_id']
            dict=request.POST.dict().copy()
            update={
                'nick_name':dict['nick_name'],
                'name':login_res['data']['name'],
                'gender':dict['gender'],
                'phone':dict['phone'],
                'avatar':dict['avatar'],
                'status':1
            }
            user,created=User.objects.update_or_create(stu_id=stu_id,defaults=update)
            # 更新openid
            obj, created = UserOpenid.objects.update_or_create(
                openid=request.POST['openid'], user_id=user.id,
                defaults={'status': 1}
            )
            #将头像存在本地
            rpc_res=rpc(fc='upload/avatar',data={'avatar':user.avatar,'user_id':user.id})
            if rpc_res['code']!=None:
                if rpc_res['code']==0:
                    user.avatar = rpc_res['data']['avatar']
                    user.save()
                else:
                    log('ERROR','user login','faild to save avatar',data=user.avatar)

            res['data']=user.format()

    except Exception as e:
        res={'code':-2, 'msg':e.__str__(), 'data':[]}
        log('ERROR','user login last exception',e.__str__())
    return JsonResponse(res)

@csrf_exempt
def logout(request):
    res={'code':0, 'msg':'success', 'data':[]}
    required={'user_id'}
    if not required.issubset(set(request.POST.keys())):
        return JsonResponse({'code': -1, 'msg': 'unexpected params!',
                             'data': {'required': list(required), 'yours': request.POST.dict()}})
    try:
        user_id=request.POST['user_id']
        UserOpenid.objects.filter(user_id=user_id).update(status=0)
    except Exception as e:
        res={'code':-2, 'msg':e.__str__(), 'data':[]}
    return JsonResponse(res)

@csrf_exempt
def update(request):
    res = {'code': 0, 'msg': 'success', 'data': []}
    required = {'user_id','update'}
    if not required.issubset(set(request.POST.keys())):
        return JsonResponse(
            {'code': -1, 'msg': 'unexpected params!', 'data': {'required': list(required), 'yours': request.POST.dict()}})
    try:
        user_id = request.POST['user_id']
        update = request.POST['update']
        try:
            if isinstance(update,str):
                update=json.loads(update)
            if not isinstance(update,dict):
                return JsonResponse({'code': -3, 'msg':'field "update" shoud be a JSON object or JSON string', 'data': []})
        except Exception as e:
            return JsonResponse({'code': -4, 'msg':e.__str__(), 'data': 'json unserilized error'})
        User.objects.filter(id=user_id).update(**update)
    except Exception as e:
        res = {'code': -2, 'msg': e.__str__(), 'data': []}
    return JsonResponse(res)

@csrf_exempt
def get(request):
    res = {'code': 0, 'msg': 'success', 'data': []}
    params=request.POST.dict()
    required = {
        'id':{},
        'stu_id':{}
    }
    check_res = check(required, params)
    if check_res is None or check_res['code'] != 0:
        return JsonResponse(check_res)
    try:
        user=User.objects.get(**params)
        res['data']=user.format()
    except User.DoesNotExist:
        res = {'code': -2, 'msg': 'DoesNotExist', 'data': []}
    except User.MultipleObjectsReturned:
        res = {'code': -2, 'msg': 'MultipleObjectsReturned', 'data': []}
    except Exception as e:
        res = {'code': -2, 'msg': e.__str__(), 'data': []}
    return JsonResponse(res)

@csrf_exempt
def insert(request):
    res = {'code': 0, 'msg': 'success', 'data': []}
    params=request.POST.dict()
    stu_id=params['stu_id']
    params.pop('stu_id')
    params['ctime']=datetime.datetime.strptime(params['ctime'], "%Y-%m-%d %H:%M:%S")
    try:
        user,cteated=User.objects.update_or_create(stu_id=stu_id,defaults=params)

        # 将头像存在本地
        rpc_res = rpc(fc='upload/avatar', data={'avatar': user.avatar, 'user_id': user.id})
        if rpc_res['code'] != None:
            if rpc_res['code'] == 0:
                user.avatar = rpc_res['data']['avatar']
                user.save()
            else:
                log('ERROR', 'user login', 'faild to save avatar', data=user.avatar)

        res['data'] = user.format()
    except Exception as e:
        res = {'code': -2, 'msg': e.__str__(), 'data': []}
        log('ERROR','@user inster',e.__str__())
    return JsonResponse(res)