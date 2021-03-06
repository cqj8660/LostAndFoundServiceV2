from django.http import HttpResponse, JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt


class BaseView(View):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.res={'code':0,'msg':'success','data':[]}

    def check(self,check):
        for name in self.params:
            if name not in check:
                return {'code': -1, 'msg': 'unexpected params!',
                                     'data': {'required': check, 'unexpected': name}}
        for name in check:
            if check[name].get('required',False) and (name not in self.params):
                return {'code': -1, 'msg': 'params required not satisfied!',
                                     'data': {'required': check, 'expected': name}}
        return {'code':0}

    def get(self, request):
        return JsonResponse({'code': 0, 'msg': 'use post,please.', 'data': []})

    @csrf_exempt
    def post(self, request):
        # <view logic>
        self.request=request
        self.params=request.POST.dict()
        return JsonResponse(self.res)

    def response(self):
        return  JsonResponse(self.res)

def check(check,params):
    for name in params:
        if name not in check:
            return {'code': -1, 'msg': 'unexpected params!',
                    'data': {'required': check, 'unexpected': {name:params[name]}}}
    for name in check:
        if check[name].get('required', False) and (name not in params):
            return {'code': -1, 'msg': 'params required not satisfied!',
                    'data': {'required': check, 'expected': {name:check[name]}}}
    return {'code': 0}

def formatQuerySet(qset):
    res=[]
    for obj in qset:
        row=obj.format()
        res.append(row)
    return res