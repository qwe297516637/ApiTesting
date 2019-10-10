import logging
import time
import pystache as pystache
import requests
from weixin.contact.token import Weixin
from weixin.contact.user import User
from weixin.contact.utiks import Utils


class TestUser:
    depart_id=1

    @classmethod
    def setup_class(cls):
        # todo:create depart
        cls.user = User()

    # 创建成员
    def test_create(self):
        uid = "Tom"+str(time.time())
        data = {
            "userid": uid,
            "name": uid,
            "department": [self.depart_id],
            "email": uid+"@163.com"
        }
        r = self.user.create(data)
        logging.debug(r)
        assert r["errcode"] == 0

    # 目前创建的数据很简单，不符合日常需要，所以要创建复杂的数据结构
    # 引入模板
    def test_creat_by_template(self):
        uid = "arlen_" + str(time.time())
        # 通过时间戳生成手机号（去除小数点取前 11 位）
        mobile = str(time.time()).replace(".", "")[0:11]
        data = str(Utils.parse("user_create.json", {
                                    "name": uid,
                                    "title": "人事",
                                    "email": mobile+"@163.com",
                                    "mobile": mobile
                                }))
        data = data.encode("UTF-8")

        r = self.user.create(data=data)
        logging.debug(r)
        assert r["errcode"] == 0

    # 获取部门成员
    def test_list(self):
        r = self.user.list()
        logging.debug(r)

        r = self.user.list(department_id=5)
        logging.debug(r)

    def mobandemo(self):
        print(pystache.render("hello{{name}} {{#has}} word {{value}} {{/has}}",
                              {"name": "hogwarts",
                               "has":[{"value":1},{"value":2},{"value":3}],
                               }))



