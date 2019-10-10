import logging
import time

import pystache as pystache
import requests

from weixin.contact.token import Weixin


class TestUser:
    depart_id=1
    @classmethod
    def setup_class(cls):
        #todo:create depart
        pass

    # 创建成员
    def test_create(self):
        uid=str(time.time())
        data={
            "userid": uid,
            "name": uid,
            "department": [self.depart_id],
            "email": uid+"@163.com"
        }
        r=requests.post("https://qyapi.weixin.qq.com/cgi-bin/user/create",
                        params={"access_token": Weixin.get_token()},
                        json=data

                        ).json()
        logging.debug(r)
        assert r["errcode"] == 0

    # 目前创建的数据很简单，不符合日常需要，所以要创建复杂的数据结构
    # 引入模板
    def test_creat_by_template(self):
        uid = "arlen_" + str(time.time())
        # 通过时间戳生成手机号（去除小数点取前 11 位）
        mobile = str(time.time()).replace(".", "")[0:11]
        data = str(self.get_user({
                                    "name": uid,
                                    "title": "人事",
                                    "email": uid+"@163.com",
                                    "mobile": mobile
                                }))
        data = data.encode("UTF-8")
        r=requests.post("https://qyapi.weixin.qq.com/cgi-bin/user/create",
                        params={"access_token": Weixin.get_token()},
                        data=data,
                        headers={"content-type": "application/json"}
                        ).json()
        logging.debug(r)
        assert r["errcode"] == 0

    def mobandemo(self):
        print(pystache.render("hello{{name}} {{#has}} word {{value}} {{/has}}",
                              {"name": "hogwarts",
                               "has":[{"value":1},{"value":2},{"value":3}],
                               }))

    # 获取部门成员
    def test_list(self):
        r=requests.get("https://qyapi.weixin.qq.com/cgi-bin/user/simplelist",
                       params={"access_token": Weixin.get_token(),
                               "department_id": 1,
                               "fetch_child": 1}
                       ).json()
        logging.debug(r)

    def get_user(self, dict):
        template="".join(open("user_create.json").readlines())
        logging.debug(template)
        return pystache.render(template, dict)

    def test_get_user(self):
        logging.debug(self.get_user({"name": "arlen", "title": "人事", "email": "1@163.com"}))