import re, email
import pandas as pd
import numpy as np
from urlextract import URLExtract
from collections import Counter
from urllib.parse import urlparse
from utils import translate

class Process():

    def __init__(self, txt, per_data):
        self.data = pd.DataFrame([])
        tran = True
        txt["date"] = txt["date"][0][1:-1]
        if tran:
            self.data["body"] = [translate.tran(txt["body"])]
            self.data["subject"] = [translate.tran(txt["subject"])]
        else:
            self.data["body"] = [txt["body"]]
            self.data["subject"] = [txt["subject"]]
        self.data["Date"] = [self.tran_time(txt["date"])]
        self.per_data = per_data
        print(self.data)

    def tran_time(self, date):
        dict1 = {"星期一": "Monday", "星期二": "Tuesday", "星期三": "Wednesday",
                 "星期四": "Thursday", "星期五": "Friday", "星期六": "Saturday", "星期日": "Sunday"}
        return dict1[date]

    def extract_body(self, text):

        body = ''
        subject = ''
        msg = email.message_from_string(text)
        if msg.is_multipart():
            for payload in msg.get_payload():
                body += str(payload)
            try:
                for sub in msg.get('subject'):
                    subject += str(sub)
            except:
                subject = ''
        else:
            body = msg.get_payload()
            try:
                subject = msg.get("subject")
            except:
                subject = ''
        return body, subject

    def judge_email_time(self, x):
        if x:
            if "Sat" in x or "Sun" in x:
                return 1
            else:
                return 0
        else:
            return 0

    # 1. count of dot
    def url_to_domain(self, url):
        o = urlparse(url)
        domain = o.hostname
        return domain

    # 5. 是否含有端口号
    def ifcontainport(self, urls):
        count = 0
        for url in urls:
            if urlparse(url).port:
                count += 1
        if count > 0:
            return 1
        else:
            return 0

    # 6. 含有端口号的url个数
    def count_urls_contain_post(self, urls):
        count = 0
        for url in urls:
            if urlparse(url).port:
                count += 1
        return count

    # 8. 包含ip的url个数
    def containipinlink(self, urls):
        pattern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
        count = 0
        for url in urls:
            try:
                if pattern.search(url)[0]:
                    count += 1
                else:
                    pass
            except:
                pass
        return count

    def run(self):
        # self.data['body'] = self.data['text']["body"]
        # self.data['subject'] = self.data['text']['subject']
        extractor = URLExtract()
        self.data['urls'] = self.data['body'].apply(lambda x: list(set(extractor.find_urls(x))))
        self.data['date_work'] = self.data['Date'].apply(self.judge_email_time)
        self.data['dot'] = self.data['urls'].apply(lambda xs: sum([Counter(self.url_to_domain(x))['.'] for x in xs]))
        self.data['port'] = self.data['urls'].apply(lambda xs: 1 if list(set([urlparse(x).port for x in xs])) != [None] and len(xs) > 0 else 0)
        self.data['port1'] = self.data['urls'].apply(lambda x: self.count_urls_contain_post(x))
        self.data['ip'] = self.data['urls'].apply(lambda x: self.containipinlink(x))
        self.data['ip1'] = self.data['ip'].apply(lambda x: 1 if x > 0 else 0)
        # 10. 连续使用域名数量
        data = self.data
        data['domain_count'] = data['urls'].apply(lambda xs: len(set([self.url_to_domain(x) for x in xs])))

        # 11.链接数量
        data['urls_count'] = data['urls'].apply(lambda xs: len(xs))

        # 13.14.click here link
        data['click'] = data['urls'].apply(lambda x: 1 if 'click' in ",".join(x).lower() else 0)
        data['here'] = data['urls'].apply(lambda x: 1 if 'here' in ",".join(x).lower() else 0)
        data['link'] = data['urls'].apply(lambda x: 1 if 'link' in ",".join(x).lower() else 0)

        # 1.suspension
        data['suspension'] = data['body'].apply(lambda x: 1 if "suspension" in x.lower() else 0)

        # 2.dear
        data['dear'] = data['body'].apply(lambda x: 1 if "dear" in x.lower() else 0)

        # 3. verify your account
        data['verifyyouraccount'] = data['body'].apply(lambda x: 1 if "verify your account" in x.lower() else 0)

        # 4. HTML
        data['html'] = data['body'].apply(lambda x: 1 if "html" in x.lower() else 0)

        # 7. 邮件正文丰富度 = 词的数量/字符的数量。
        data['w_count'] = data['body'].apply(lambda x: len(x.split(" ")))
        data['str_count'] = data['body'].apply(lambda x: len(x))
        data['body_richness'] = round(data['w_count'] / data['str_count'], 2)

        # 8.account
        data['account_count'] = data['body'].apply(lambda x: Counter(x.split(" "))['account'])

        # 9. suspended
        data['suspended_count'] = data['body'].apply(lambda x: Counter(x.split(" "))['suspended'])

        # 10. 不重复单词个数
        data['word_count'] = data['body'].apply(lambda x: len(set(x.split(" "))))

        # 特殊字符
        # @：在电子邮件地址中使用，用于分隔用户名和域名。
        data['@'] = data['body'].apply(lambda x: 1 if "@" in x.lower() else 0)
        # !：用于增加紧迫感或强调重要性。
        data['!'] = data['body'].apply(lambda x: 1 if "!" in x.lower() else 0)
        # # ：用于标记话题或关键字。
        data['#'] = data['body'].apply(lambda x: 1 if "#" in x.lower() else 0)
        # %：用于表示折扣或优惠。
        data['%'] = data['body'].apply(lambda x: 1 if "%" in x.lower() else 0)
        # &：用于连接两个词或短语。
        data['&'] = data['body'].apply(lambda x: 1 if "&" in x.lower() else 0)
        # +：用于创建假电子邮件地址。
        data['+'] = data['body'].apply(lambda x: 1 if "+" in x.lower() else 0)
        # -：用于创建假网站地址或分隔单词。
        data['-'] = data['body'].apply(lambda x: 1 if "-" in x.lower() else 0)
        # _：用于创建假电子邮件地址。
        data['_'] = data['body'].apply(lambda x: 1 if "_" in x.lower() else 0)
        # $：用于表示货币或价格。
        data['$'] = data['body'].apply(lambda x: 1 if "$" in x.lower() else 0)
        # *：用于强调或突出显示重要部分。
        data['*'] = data['body'].apply(lambda x: 1 if "*" in x.lower() else 0)
        # /：用于创建假网站地址。
        data['/'] = data['body'].apply(lambda x: 1 if "/" in x.lower() else 0)
        # \：用于混淆网址或文件路径
        data['\\'] = data['body'].apply(lambda x: 1 if "\\" in x.lower() else 0)

        # 钓鱼邮件中敏感词
        data['contain_account'] = data['body'].apply(lambda x: 1 if "account" in x.lower() else 0)
        data['contain_password'] = data['body'].apply(lambda x: 1 if "password" in x.lower() else 0)
        data['contain_verify'] = data['body'].apply(lambda x: 1 if "verify" in x.lower() else 0)
        data['contain_reward'] = data['body'].apply(lambda x: 1 if "reward" in x.lower() else 0)
        data['contain_confidentiality'] = data['body'].apply(lambda x: 1 if "confidentiality" in x.lower() else 0)
        data['contain_cancel'] = data['body'].apply(lambda x: 1 if "cancel" in x.lower() else 0)

        # 1.bank
        data['bank'] = data['subject'].apply(lambda x: 1 if x and 'bank' in x.lower() else 0)

        # 3. FW
        data['fw'] = data['subject'].apply(lambda x: 1 if x and 'FW' in x else 0)

        # 4. re
        data['re'] = data['subject'].apply(lambda x: 1 if x and 're:' in x else 0)

        # 5. verify
        data['verify'] = data['subject'].apply(lambda x: 1 if x and 'verify' in x else 0)

        # 6.word count
        data['subject_word_count'] = data['subject'].apply(lambda x: len(str(x).split(" ")) if x else 0)

        # 7.str count
        data['subject_str_count'] = data['subject'].apply(lambda x: len(str(x)) if x else 0)

        # richness
        data['subject_richness'] = round(data['subject_word_count'] / data['subject_str_count'], 2)

        # 是否包含大写字母
        data['upper'] = data['subject'].apply(lambda x: 0 if x and x.islower() else 1)

        data = data.fillna(0)
        data = data.replace([np.inf, -np.inf], 0)

        features = data.iloc[:, 4:]
        features = features.append(self.per_data, ignore_index=True)
        for i in list(features.columns):
            # 获取各个指标的最大值和最小值
            Max = np.max(features[i])
            Min = np.min(features[i])
            features[i] = (features[i] - Min) / (Max - Min)

        return pd.DataFrame(features.iloc[0, 0:]).T


if __name__ == '__main__':
    with open("../finishemail/数据集/monkey数据集/数据集/000/000", 'r')as f:
        txt = f.read()
    per_data = pd.read_csv("../static/data/features.csv")
    p = Process(txt, per_data)
    print(p.run())




