import json
import traceback

import requests
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from LostAndFoundServiceV2.settings import URL_PREFIX
from lib.utils import log
weapp={
        'appid':'wxd8d5a2f6fa7f1878',
        'secret':'c1377133ab2c26acf453a0d7ed877710',
    }

def studentLogin(stu_id, stu_pwd):
    try:
        url = 'http://202.120.82.2:8081/ClientWeb/pro/ajax/login.aspx'
        params = {"id":stu_id,"pwd":stu_pwd,"act":'login'}
        r=requests.post(url, data=params,timeout=5).json()
        log('DEBUG','client studentLogin','request res',data=r)
        r['code']=1-r['ret']
    except Exception as e:
        traceback.print_exc()
        log('ERROE','@client studentLogin',e.__str__())
        return {'code':-2,'msg':e.__str__(),'data':[]}
    return r

def getOpenid(code):
    data={
        'appid':'wxd8d5a2f6fa7f1878',
        'secret':'c1377133ab2c26acf453a0d7ed877710',
        'grant_type':'authorization_code',
        'js_code':code
    }
    url='https://api.weixin.qq.com/sns/jscode2session'
    try:
        print(data)
        r=requests.post(url,data=data)
    except:
        traceback.print_exc()
        return {'code':-1,'msg':'timeout | getopenid failed!','data':[]}
    return {'code':0, 'msg':'success','data':json.loads(r.text)}

def authGetAccessToken():
    data = {
        'appid': 'wxd8d5a2f6fa7f1878',
        'secret': 'c1377133ab2c26acf453a0d7ed877710',
        'grant_type': 'client_credential',
    }
    try:
        r = requests.get('https://api.weixin.qq.com/cgi-bin/token',params=data)
        r=r.json()
    except Exception as e:
        log("ERROR",'@client authGetAccessToken',e.__str__(),data=[data])
        r={}
    finally:
        if 'access_token' in r:
            return {'code':0,'msg':'success','data':r}
        else:
            return {'code': -2, 'msg': 'failed to get access_token', 'data': []}


def ocrPrintedText(params):
    if 'access_token' not in params:
        at_res=authGetAccessToken()
        if at_res is None or at_res['code']!=0:
            return at_res
        params['access_token']=at_res['data']['access_token']
    try:
        r = requests.post('https://api.weixin.qq.com/cv/ocr/comm', data=params)
        r = r.json()
        res = {
            'code': 0,
            'msg': 'success',
            'data': r
        }
    except Exception as e:
        log("ERROR",'@client ocrPrintedText',e.__str__(),data=[params])
        res = {
            'code': -2,
            'msg': 'failed to call ocrPrintedText',
            'data': {}
        }
    return res

def rpc(fc,data):
    url = URL_PREFIX+'/service/' + fc
    res={'code':-2,'msg':'error in rpc','data':[]}
    #尝试本地
    try:
        r=requests.post(url=url,data=data).json()
        log('DEBUG', '@client rpc', data=[url,r])
    except Exception as e:
        log('ERROR','@client rpc',e,data=url)
        res['msg']=e
        return res
    return r