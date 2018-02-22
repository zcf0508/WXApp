#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'zhoucaifa'

import os
import json
import urllib
import binascii
import base64
from Crypto.Cipher import AES
import logging
import time
#logging.basicConfig(filename='logs/flask '+str(time.strftime("%Y-%m-%d",time.localtime(int(time.time()))))+'.log', filemode="a", format='%(asctime)s - %(levelname)s - %(message)s',level=logging.INFO)

class WXApp(object):

    __WX_APPID=''
    __WX_SECRET=''
    token=None

    #初始化类，设置appid及secret
    def __init__(self, appid=None,secret=None):
        if appid is not None and secret is not None:
            self.__WX_APPID=appid
            self.__WX_SECRET=secret
            self.token = self.Token(appid, secret)
        else:
            raise Exception("appid或secret为空")

    #js_code换取session_key、openid及unionid
    def code2session(self,code):
        # header_dict = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko'}
        # header_dict = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko'}
        url = 'https://api.weixin.qq.com/sns/jscode2session?appid=' + self.__WX_APPID + '&secret=' + self.__WX_SECRET + '&js_code=' + code + '&grant_type=authorization_code'
        req = urllib.request.Request(url=url)
        res = urllib.request.urlopen(req)
        res = res.read()
        resJson = json.loads(res.decode('utf-8'))
        logging.info(resJson)
        if resJson.__contains__('openid'):
            if resJson.__contains__('unionid'):
                return {
                    'openid': resJson['openid'],
                    'session_key': resJson['session_key'],
                    'unionid':resJson['unionid']
                }
            return {
                'openid':resJson['openid'],
                'session_key':resJson['session_key']
            }
        else:
            return {
                'errcode':resJson['errcode'],
                'errmsg':resJson['errmsg']
            }

    #解密encryptedData获取openId及unionId
    def decrypt(self, session_key, encrypted_data, iv):
        # base64 decode
        session_key = base64.b64decode(session_key)
        encrypted_data = base64.b64decode(encrypted_data)
        iv = base64.b64decode(iv)

        cipher = AES.new(session_key, AES.MODE_CBC, iv)

        def _unpad(self, s):
            return s[:-ord(s[len(s) - 1:])]

        decrypt_data = _unpad(cipher.decrypt(encrypted_data))
        decrypted = json.loads(decrypt_data.decode())

        if decrypted['watermark']['appid'] != self.__WX_APPID:
            raise Exception('Invalid Buffer')

        return decrypted

    #获取Token
    class Token(object):
        accesstoken = ""
        lastdate = 0
        __appid=''
        __secret=''

        def __init__(self,appid,secret):
            self.__appid=appid
            self.__secret=secret

        def getToken(self):
            if(self.__appid=='' or self.__secret==''):
                raise Exception("appid或secret为空")
            if (self.accesstoken == "" or self.lastdate <= time.time()):
                header_dict = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko'}
                url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=' + self.__appid + '&secret=' + self.__secret
                req = urllib.request.Request(url=url, headers=header_dict)
                res = urllib.request.urlopen(req)
                res = res.read()
                resJson = json.loads(res.decode('utf-8'))
                print(resJson)
                if resJson.__contains__('access_token'):
                    self.accesstoken = resJson['access_token']
                    self.lastdate = time.time() + resJson['expires_in']
                return self.accesstoken
            else:
                return self.accesstoken

    #发送模板消息
    class SendTemplate(object):
        def __init__(self,token):
            self.accesstoken=token

        def send(self, data):
            print(str(json.dumps(data)))
            header_dict = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
                'Content-Type': 'application/json'
            }
            url = 'https://api.weixin.qq.com/cgi-bin/message/wxopen/template/send?access_token=' + self.accesstoken
            req = urllib.request.Request(url=url, data=str(json.dumps(data)).encode('utf-8'), headers=header_dict)
            res = urllib.request.urlopen(req)
            res = res.read()
            resJson = json.loads(res.decode('utf-8'))
            print(resJson)
            if (resJson['errcode'] == 0):
                return True
            else:
                return False

    def gen_3rd_session_key(self):
        """ 生成长度为 32 位的 hex 字符串，用于第三方 session 的 key"""
        return binascii.hexlify(os.urandom(16)).decode()