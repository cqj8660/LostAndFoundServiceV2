import json
import os
import sys

import requests

from lib.utils import log


def sync_user():

    url='https://lostandfound.yiwangchunyu.wang/service/user/getById'
    for i in range(10,700):
        r = requests.post(url,data={'id':i,'user_id':10152150127}).json()
        data=r['data']
        payload = {
            'phone':'',
            'gender':1,
            'stu_id' : data['user_id'],
            'nick_name': data['nick_name'],
            'avatar': data['avatar_url'],

        }
        if data['contact_type']=='手机号':
            payload['phone']=data['contact_value']
        payload['ctime']=data['ctime'].replace('T',' ').replace('Z','')

        r=requests.post('https://lostandfoundv2.yiwangchunyu.wang/service/user/insert',data=payload)
        print(r.json())

def sync_dynamic():
    r = requests.post('https://lostandfoundv2.yiwangchunyu.wang/service/dynamic/categories',data={'size':100}).json()
    categories=r['data']
    name2id={}
    for cat in categories:
        name2id[cat['name']]=cat['id']

    r = requests.post('https://lostandfound.yiwangchunyu.wang/service/dynamic/show',data={'size':100}).json()
    # print('cnt',r['data']['count'],r)
    for id,row in enumerate(reversed(r['data']['dynamics'])):
        print(id,r['data']['count'],row)
        params={
            'user_id':'',
            'type':'',
            'category':'',
            'title':'',
            'desc':row['content'],
            'images':'',
            'location':json.dumps(row['location']),
            'ctime':row['ctime'].replace('T',' ').replace('Z','')
        }
        if row['type']=='lost':
            params['type']=1
        else:
            params['type'] = 2

        if row['category'] in name2id:
            params['category']=name2id[row['category']]
        else:
            params['category']=name2id['其他']

        user_res = requests.post('https://lostandfoundv2.yiwangchunyu.wang/service/user/get',
                          data={'stu_id': row['user_id']}).json()
        # log('INFO', '@dynamic insert get user info', '', data=user_res)
        if user_res is None or user_res['code'] != 0:
            log('ERROR', '@dynamic insert get user info failed', '', data=[row['user_id'], user_res])
            continue
        params['user_id'] = user_res['data']['id']

        images=[]
        for url in row['images']:
            img_res = requests.post('https://lostandfoundv2.yiwangchunyu.wang/service/upload/dynamicImgByUrl',
                                     data={'img_url': url}).json()
            if img_res is None or img_res['code']!=0:
                log('ERROR', '@upload dynamic image failed', '', data=[url,img_res])
                continue
            images.append(img_res['data'])
        params['images']=json.dumps(images)

        dynamic_res=requests.post('https://lostandfoundv2.yiwangchunyu.wang/service/dynamic/create',
                      data=params).json()
        if dynamic_res is None or dynamic_res['code'] != 0:
            log('ERROR', '@create dynamic failed', '', data=[params, dynamic_res])
            continue

if __name__=='__main__':
    # sync_user()
    sync_dynamic()