# 微信小程序接口实现

参考： [小程序官方文档](https://mp.weixin.qq.com/debug/wxadoc/dev/api/api-login.html)

## 使用

- 初始化

```python
from WXApp import WXAPP
wxapp=WXAPP(appid,secret)
```

- 通过code换取openid和session_key

```python
wxapp.code2session(code)
```

返回值(dict)说明

| 参数          | 说明                                       |
| ----------- | ---------------------------------------- |
| openid      | 用户的唯一标识                                  |
| session_key | 会话密钥                                     |
| unionid     | [特定情况返回](https://mp.weixin.qq.com/debug/wxadoc/dev/api/uinionID.html) |

- 解密encryptedData

```python
wxapp.decrypt(session_key, encrypted_data, iv)
```

返回如下

```json
{
    "openId": "OPENID",
    "nickName": "NICKNAME",
    "gender": GENDER,
    "city": "CITY",
    "province": "PROVINCE",
    "country": "COUNTRY",
    "avatarUrl": "AVATARURL",
    "unionId": "UNIONID",
    "watermark":
    {
        "appid":"APPID",
        "timestamp":TIMESTAMP
    }
}
```

- 发送模板消息

```python
wxapp.SendTemplate(wxapp.token.getToken()).send({
    'touser':"OPENID",
    'template_id':"TEMPLATE_ID",
    'form_id':"FORMID",
    'data':{
      'keyword1':{
        'value':"value1"
      },
       'keyword2':{
        'value':"value2"
      },
    }
})
```

模板消息[格式参考](https://mp.weixin.qq.com/debug/wxadoc/dev/api/notice.html#%E5%8F%91%E9%80%81%E6%A8%A1%E6%9D%BF%E6%B6%88%E6%81%AF)

- 3rd_session

```python
wxapp.gen_3rd_session_key()
```

可用于与小程序端的客户认证