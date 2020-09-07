import hashlib
import re
import time

import requests

from cqu_jxgl.config import config
from cqu_jxgl.exceptions import ValidationError
from cqu_jxgl.utils import check_user, log, reset_error_count


class Student(object):
    def __encrypt_passwd(self):
        def _md5(string):
            m = hashlib.md5()
            m.update(string.encode("utf-8"))
            return m.hexdigest()

        string = self.username + _md5(self.password).upper()[:30] + "10611"
        res = _md5(string).upper()[:30]
        return res

    def login(self, headers=None) -> requests.Response:
        def _get_session():
            session = requests.Session()
            session.headers.update(
                {
                    "Accept": str(config["headers"]["Accept"]),
                    "Connection": str(config["headers"]["Connection"]),
                    "User-Agent": str(config["headers"]["User-Agent"]),
                    "Accept-Encoding": str(config["headers"]["Accept-Encoding"]),
                    "Accept-Language": str(config["headers"]["Accept-Language"]),
                    "Upgrade-Insecure-Requests": str(
                        config["headers"]["Upgrade-Insecure-Requests"]
                    ),
                }
            )
            return session

        def _login(student):
            session = _get_session()
            payload = {
                "Sel_Type": "STU",
                "__VIEWSTATE": student.vs,
                "__VIEWSTATEGENERATOR": student.vsg,
                "aerererdsdxcxdfgfg": "",
                "efdfdfuuyyuuckjg": student.__encrypt_passwd(),
                "pcInfo": "",
                "txt_dsdfdfgfouyy": "",
                "txt_dsdsdsdjkjkjc": student.username,
                "txt_ysdsdsdskgf": "",
                "typeName": "",
            }
            response = session.post(
                student.base_url + "/_data/index_login.aspx",
                data=payload,
                headers=headers,
                proxies=student.proxies,
            )
            if "账号或密码不正确！请重新输入。" in response.text:
                raise ValidationError("账号或密码不正确！请重新输入。")
            return response, session

        res, s = _login(self)
        while res.status_code != 200 and config["behavior"]["unlimited_retry"]:
            log(
                f"Get code-{res.status_code} when trying to login, retrying...",
                error=True,
            )
            res, s = _login(self)

        self.session = s
        reset_error_count()
        return res

    def get(self, url, params=None, headers=None) -> requests.Response:
        """
        Note: Any dictionaries that you pass to a request method will be merged with the session-level values that are
        set. The method-level parameters override session parameters.
        """
        res = self.session.get(self.base_url + url, params=params, headers=headers)

        try:
            dsafeid = re.findall("DSafeId=.+?;", res.text)[0][8:-1]
        except IndexError:
            pass
        else:
            # Add the cookie to current session
            cookie_obj = requests.cookies.create_cookie(
                domain=config["network"]["host"], name="DSafeId", value=dsafeid
            )
            self.session.cookies.set_cookie(cookie_obj)

            # Waiting for 0.68s. This is MANDATORY.
            time.sleep(0.68)

            # Then Get again. The real website is revealed.
            res = self.session.get(self.base_url + url, params=params, headers=headers)

        while res.status_code != 200 and config["behavior"]["unlimited_retry"]:
            log(
                f"Get code-{res.status_code} when post to {url}, retrying...",
                error=True,
            )
            res = self.session.get(self.base_url + url, params=params, headers=headers)
        reset_error_count()
        return res

    def post(self, url, data=None, headers=None) -> requests.Response:
        """
        Note: Any dictionaries that you pass to a request method will be merged with the session-level values that are
        set. The method-level parameters override session parameters.
        """
        res = self.session.post(self.base_url + url, data=data, headers=headers)
        while res.status_code != 200 and config["behavior"]["unlimited_retry"]:
            log(
                f"Get code-{res.status_code} when post to {url}, retrying...",
                error=True,
            )
            res = self.session.post(self.base_url + url, data=data, headers=headers)
        reset_error_count()
        return res

    def __init__(self, username=None, password=None):
        if None in (username, password):
            self.username, self.password = check_user()
        else:
            self.username, self.password = username, password

        self.base_url = "http://" + config["network"]["host"]
        self.vs = config["network"]["vs"]
        self.vsg = "CAA0A5A7"
        self.proxies = config["network"]["proxies"]
        self.session = None
