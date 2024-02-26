import http.client, hashlib, urllib, random, json


def tran(text):

    from pip._vendor.distlib.compat import raw_input

    # 百度appid和密钥需要通过注册百度【翻译开放平台】账号后获得
    appid = '20230513001676327'  # 填写你的appid
    secretKey = 'hstve9MgTdUatauhzfnP'  # 填写你的密钥

    httpClient = None
    myurl = '/api/trans/vip/translate'  # 通用翻译API HTTP地址

    fromLang = 'auto'  # 原文语种
    toLang = 'en'  # 译文语种
    salt = random.randint(32768, 65536)
    # 手动录入翻译内容，q存放
    q = text
    sign = appid + q + str(salt) + secretKey
    sign = hashlib.md5(sign.encode()).hexdigest()
    myurl = myurl + '?appid=' + appid + '&q=' + urllib.parse.quote(q) + '&from=' + fromLang + \
            '&to=' + toLang + '&salt=' + str(salt) + '&sign=' + sign

    # 建立会话，返回结果
    try:
        httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', myurl)
        # response是HTTPResponse对象
        response = httpClient.getresponse()
        result_all = response.read().decode("utf-8")
        result = json.loads(result_all)

        return result["trans_result"][0]["dst"]

    except Exception as e:
        print(e)
    finally:
        if httpClient:
            httpClient.close()


if __name__ == '__main__':
    print(tran("			修改邮箱密码提醒		您的邮箱（lc_y2001@163.com）已于 2023年05月02日 15:44:43 成功修改密码。		检测到您正在使用第三方邮件客户端登录网易邮箱，为了保障您的帐号信息安全，我们建议您重新设置POP3/IMAP协议（前往网页版邮箱-设置-POP3/SMTP/IMAP-关闭后重新开启）。		我们推荐您使用网易邮箱官方客户端“网易邮箱大师”。邮箱大师使用专属协议传输邮件，无需开启客户端协议，能有效避免邮件泄露等潜在安全风险。			"))

