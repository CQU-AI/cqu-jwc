import hashlib

import requests

from cqu_jwc.config import config
from cqu_jwc.utils import check_user, log, reset_error_count


class Student(object):

    def __encrypt_passwd(self):
        def _md5(string):
            m = hashlib.md5()
            m.update(string.encode('utf-8'))
            return m.hexdigest()

        string = self.username + _md5(self.password).upper()[:30] + '10611'
        res = _md5(string).upper()[:30]
        return res

    def login(self) -> requests.Response:
        def _login(student):
            session = requests.Session()
            payload = {
                'Sel_Type': 'STU',
                '__VIEWSTATE': student.vs,
                '__VIEWSTATEGENERATOR': student.vsg,
                'aerererdsdxcxdfgfg': '',
                'efdfdfuuyyuuckjg': student.__encrypt_passwd(),
                'pcInfo': '',
                'txt_dsdfdfgfouyy': '',
                'txt_dsdsdsdjkjkjc': student.username,
                'txt_ysdsdsdskgf': '',
                'typeName': ''
            }
            return session.post(student.base_url + '/_data/index_login.aspx', data=payload, headers=student.headers,
                                proxies=student.proxies), session

        res, s = _login(self)
        while res.status_code != 200 and config['behavior']['unlimited_retry']:
            log(f'Get code-{res.status_code} when trying to login, retrying...', error=True)
            res, s = _login(self)

        self.session = s
        reset_error_count()
        return res

    def get(self, url, params=None, headers=None) -> requests.Response:
        headers = self.check_headers(headers)
        res = self.session.get(self.base_url + url, params=params, headers=headers)
        while res.status_code != 200 and config['behavior']['unlimited_retry']:
            log(f'Get code-{res.status_code} when post to {url}, retrying...', error=True)
            res = self.session.get(self.base_url + url, params=params, headers=headers)
        reset_error_count()
        return res

    def post(self, url, data=None, headers=None) -> requests.Response:
        headers = self.check_headers(headers)
        res = self.session.post(self.base_url + url, data=data, headers=headers)
        while res.status_code != 200 and config['behavior']['unlimited_retry']:
            log(f'Get code-{res.status_code} when post to {url}, retrying...', error=True)
            res = self.session.post(self.base_url + url, data=data, headers=headers)
        reset_error_count()
        return res

    def check_headers(self, headers):
        if headers is None:
            headers = self.session.headers
        headers.update({
            'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/67.0.3396.87 Safari/537.36"})
        return headers

    def __init__(self, username=None, password=None):
        if None in (username, password):
            self.username, self.password = check_user()
        else:
            self.username, self.password = username, password

        self.base_url = "http://" + config['network']['host']
        self.vs = config['network']['vs']
        self.vsg = "CAA0A5A7"
        self.proxies = config['network']['proxies']
        self.session = None
        self.headers = {
            'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36"
        }
