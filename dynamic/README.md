## user相关接口   
* [x] <a href='#categories'>categories</a>   
* [x] <a href='#create'>create</a>   
* [x] <a href='#list'>list</a>   
* [x] <a href='#delete'>delete</a>   
* [x] <a href='#update'>update</a>   
* [x] <a href='#apply'>apply</a>   
* [x] <a href='#confirm'>confirm</a>    
* [x] <a href='#reject'>reject</a>    
* [x] <a href='#ocrPrintedText'>ocrPrintedText</a>    

## 接口文档   
domain=‘http(s)://lostandfoundv2.yiwangchunyu.wang’   
 
请注意！：用户在服务端的唯一标识为user_id，不是opendi or stu_id   

### <a name='categories'>categories</a> 获取类别列表   
url = {domain}/service/dynamic/categories   
method = post   
params:   

return:
```json
{
    "code": 0,
    "msg": "success",
    "data": [
        {
            "id": 1,
            "status": 1,
            "ctime": "2020-03-26 11:34:04",
            "mtime": "2020-03-26 11:34:15",
            "name": "校园卡"
        },
        {
            "id": 2,
            "status": 1,
            "ctime": "2020-03-26 11:34:29",
            "mtime": "2020-03-26 11:34:35",
            "name": "雨伞"
        },
        {
            "id": 3,
            "status": 1,
            "ctime": "2020-03-26 15:18:00",
            "mtime": "2020-03-26 15:18:27",
            "name": "其他"
        }
    ]
}
```

### <a name='create'>create</a> 创建动态   
url = {domain}/service/dynamic/create   
method = post   
params:   


|   名称  | 类型 | 必须 | 备注 |
| :-----| ----: | :----: | :----: |
|user_id | int | Y |  |
|type | int | Y | 1:lost 2:found |
|category | int | Y |  |
|title | string | Y |  物品名称（保留字段，可传''）|
|desc | string | Y |  物品描述|
|images | json_string | N | 建议先调用接口上传图片(upload/dynamicImg)，成功填此接口；或者先创建，再上传图片，再更新此字段（不建议） |
|location | json_string | N | 地理位置信息 |
|meta | string | N | 捡到校园卡，传校园卡卡号 |

return:
```json
{
    "code": 0,
    "msg": "success",
    "data": []
}
```

### <a name='list'>list</a> 查询动态列表   
url = {domain}/service/dynamic/list   
method = post   
params:   


|   名称  | 类型 | 必须 | 备注 |
| :-----| ----: | :----: | :----: |
|id | int | n |  |
|user_id | int | n |  |
|type | int | n |  |
|category | int | n |  |
|title | string | n |  物品名称（保留字段，可传''）|
|desc | string | n |  物品描述|
|meta | string | n | 捡到校园卡，传校园卡卡号 |
|state | int | n | 1:待申领，2：待确认，3：申领成功 |
|belongsTo | int | n | 申领人 |
|page | int | n | 0 |
|size | int | n | 10 |

我发布的：传user_id
我申领的：传belongsTo

return:
```json
{
    "code": 0,
    "msg": "success",
    "data": {
        "cnt": 2,
        "dynamics": [
            {
                "id": 1,
                "status": 1,
                "ctime": "2020-03-26 14:55:20",
                "mtime": "2020-03-26 14:55:28",
                "user_id": 1,
                "type": 1,
                "category": 1,
                "title": "",
                "desc": "丢失",
                "images": [],
                "location": {},
                "meta": null,
                "belongsTo": 1,
                "state": "待申领",
                "user_info": {
                    "id": 1,
                    "status": 1,
                    "ctime": "2020-03-20 08:53:49",
                    "mtime": "2020-03-20 10:49:53",
                    "stu_id": "10152150127",
                    "nick_name": "yiwangchunyu",
                    "name": "汪春雨",
                    "avatar": "http://127.0.0.1:8000/media/avatar/1_20200320184953.jpg",
                    "gender": 1,
                    "phone": "18918053907",
                    "role": 2
                }
            },
            {
                "id": 2,
                "status": 1,
                "ctime": "2020-03-26 16:53:28",
                "mtime": "2020-03-26 16:53:28",
                "user_id": 1,
                "type": 1,
                "category": 1,
                "title": "",
                "desc": "",
                "images": [],
                "location": {},
                "meta": "",
                "belongsTo": 1,
                "state": "待申领",
                "user_info": {
                    "id": 1,
                    "status": 1,
                    "ctime": "2020-03-20 08:53:49",
                    "mtime": "2020-03-20 10:49:53",
                    "stu_id": "10152150127",
                    "nick_name": "yiwangchunyu",
                    "name": "汪春雨",
                    "avatar": "http://127.0.0.1:8000/media/avatar/1_20200320184953.jpg",
                    "gender": 1,
                    "phone": "18918053907",
                    "role": 2
                }
            }
        ]
    }
}
```


### <a name='delete'>delete</a> 删除动态   
url = {domain}/service/dynamic/delete   
method = post   
params:   


|   名称  | 类型 | 必须 | 备注 |
| :-----| ----: | :----: | :----: |
|id | int | Y | 动态id|
|user_id | int | Y |  |

return:
```json
{
    "code": 0,
    "msg": "success",
    "data": []
}
```


### <a name='apply'>update</a> 更新动态   
url = {domain}/service/dynamic/apply   
method = post   
params:   


|   名称  | 类型 | 必须 | 备注 |
| :-----| ----: | :----: | :----: |
|id | int | Y |  |
|user_id | int | N |  |
|type | int | N |  |
|category | int | N |  |
|title | string | N |  物品名称（保留字段，可传''）|
|desc | string | N |  物品描述|
|images | json_string | N | 建议先调用接口上传图片(upload/dynamicImg)，成功填此接口；或者先创建，再上传图片，再更新此字段（不建议） |
|location | json_string | N | 地理位置信息 |
|meta | string | N | 捡到校园卡，传校园卡卡号 |

return:
```json
{
    "code": 0,
    "msg": "success",
    "data": []
}
```

### <a name='apply'>apply</a> 申领   
url = {domain}/service/dynamic/apply   
method = post   
params:   


|   名称  | 类型 | 必须 | 备注 |
| :-----| ----: | :----: | :----: |
|id | int | Y |  |
|user_id | int | Y |  |

return:
```json
{
    "code": 0,
    "msg": "success",
    "data": {
        "user_info": {
            "id": 1,
            "status": 1,
            "ctime": "2020-03-20 08:53:49",
            "mtime": "2020-03-20 10:49:53",
            "stu_id": "10152150127",
            "nick_name": "yiwangchunyu",
            "name": "汪春雨",
            "avatar": "http://127.0.0.1:8000/media/avatar/1_20200320184953.jpg",
            "gender": 1,
            "phone": "18918053907",
            "role": 2
        }
    }
}
```

### <a name='confirm'>confirm</a> 确认   
url = {domain}/service/dynamic/confirm   
method = post   
params:   


|   名称  | 类型 | 必须 | 备注 |
| :-----| ----: | :----: | :----: |
|id | int | Y |  |
|user_id | int | Y |  |

return:
```json
{
    "code": 0,
    "msg": "success",
    "data": {
    }
}
```

### <a name='reject'>reject</a> 拒绝   
url = {domain}/service/dynamic/reject   
method = post   
params:   


|   名称  | 类型 | 必须 | 备注 |
| :-----| ----: | :----: | :----: |
|id | int | Y |  |
|user_id | int | Y |  |


return:
```json
{
    "code": 0,
    "msg": "success",
    "data": {
    }
}
```

### <a name='ocrPrintedText'>ocrPrintedText</a> OCR   
url = {domain}/service/dynamic/reject   
method = post   
params:   


|   名称  | 类型 | 必须 | 备注 |
| :-----| ----: | :----: | :----: |
|img_url | string | Y | 要检测的图片 url，传这个则不用传 img 参数。 |
|img | FormData | Y |  form-data 中媒体文件标识，有filename、filelength、content-type等信息，传这个则不用传 img_url。|

[测试图片](https://lostandfoundv2.yiwangchunyu.wang/media/dynamic/2020/3/30/20200330190833_52537.jpg)

return:
```json
{
    "code": 0,
    "msg": "success",
    "data": {
        "errcode": 0,
        "errmsg": "ok",
        "items": [
            {
                "text": "姓名",
                "pos": {
                    "left_top": {
                        "x": 35,
                        "y": 43
                    },
                    "right_top": {
                        "x": 89,
                        "y": 43
                    },
                    "right_bottom": {
                        "x": 89,
                        "y": 65
                    },
                    "left_bottom": {
                        "x": 35,
                        "y": 65
                    }
                }
            },
            {
                "text": "爱新觉罗 · 玄烨",
                "pos": {
                    "left_top": {
                        "x": 95,
                        "y": 38
                    },
                    "right_top": {
                        "x": 282,
                        "y": 37
                    },
                    "right_bottom": {
                        "x": 282,
                        "y": 66
                    },
                    "left_bottom": {
                        "x": 95,
                        "y": 66
                    }
                }
            },
            {
                "text": "性别",
                "pos": {
                    "left_top": {
                        "x": 35,
                        "y": 85
                    },
                    "right_top": {
                        "x": 85,
                        "y": 85
                    },
                    "right_bottom": {
                        "x": 86,
                        "y": 107
                    },
                    "left_bottom": {
                        "x": 35,
                        "y": 107
                    }
                }
            },
            {
                "text": "男",
                "pos": {
                    "left_top": {
                        "x": 96,
                        "y": 85
                    },
                    "right_top": {
                        "x": 125,
                        "y": 85
                    },
                    "right_bottom": {
                        "x": 126,
                        "y": 110
                    },
                    "left_bottom": {
                        "x": 96,
                        "y": 110
                    }
                }
            },
            {
                "text": "民族满",
                "pos": {
                    "left_top": {
                        "x": 158,
                        "y": 84
                    },
                    "right_top": {
                        "x": 236,
                        "y": 83
                    },
                    "right_bottom": {
                        "x": 235,
                        "y": 107
                    },
                    "left_bottom": {
                        "x": 158,
                        "y": 107
                    }
                }
            },
            {
                "text": "出生",
                "pos": {
                    "left_top": {
                        "x": 36,
                        "y": 127
                    },
                    "right_top": {
                        "x": 83,
                        "y": 127
                    },
                    "right_bottom": {
                        "x": 83,
                        "y": 148
                    },
                    "left_bottom": {
                        "x": 36,
                        "y": 148
                    }
                }
            },
            {
                "text": "1654年5月4日",
                "pos": {
                    "left_top": {
                        "x": 99,
                        "y": 127
                    },
                    "right_top": {
                        "x": 286,
                        "y": 126
                    },
                    "right_bottom": {
                        "x": 286,
                        "y": 149
                    },
                    "left_bottom": {
                        "x": 100,
                        "y": 149
                    }
                }
            },
            {
                "text": "住址",
                "pos": {
                    "left_top": {
                        "x": 35,
                        "y": 172
                    },
                    "right_top": {
                        "x": 86,
                        "y": 173
                    },
                    "right_bottom": {
                        "x": 85,
                        "y": 193
                    },
                    "left_bottom": {
                        "x": 35,
                        "y": 193
                    }
                }
            },
            {
                "text": "北京市东城区景山前街4号",
                "pos": {
                    "left_top": {
                        "x": 96,
                        "y": 171
                    },
                    "right_top": {
                        "x": 345,
                        "y": 170
                    },
                    "right_bottom": {
                        "x": 346,
                        "y": 196
                    },
                    "left_bottom": {
                        "x": 96,
                        "y": 194
                    }
                }
            },
            {
                "text": "紫禁城乾清宫",
                "pos": {
                    "left_top": {
                        "x": 96,
                        "y": 206
                    },
                    "right_top": {
                        "x": 221,
                        "y": 206
                    },
                    "right_bottom": {
                        "x": 221,
                        "y": 231
                    },
                    "left_bottom": {
                        "x": 96,
                        "y": 231
                    }
                }
            },
            {
                "text": "公民身份证号码",
                "pos": {
                    "left_top": {
                        "x": 37,
                        "y": 280
                    },
                    "right_top": {
                        "x": 167,
                        "y": 280
                    },
                    "right_bottom": {
                        "x": 168,
                        "y": 303
                    },
                    "left_bottom": {
                        "x": 37,
                        "y": 303
                    }
                }
            },
            {
                "text": "000003165405049842",
                "pos": {
                    "left_top": {
                        "x": 186,
                        "y": 282
                    },
                    "right_top": {
                        "x": 462,
                        "y": 282
                    },
                    "right_bottom": {
                        "x": 462,
                        "y": 303
                    },
                    "left_bottom": {
                        "x": 185,
                        "y": 303
                    }
                }
            }
        ],
        "img_size": {
            "w": 544,
            "h": 336
        }
    }
}
```