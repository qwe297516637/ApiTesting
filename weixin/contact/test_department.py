import datetime
import json

import pytest
import requests
from weixin.contact.token import Weixin
import logging

from weixin.contact.utiks import Utils


class TestDepartment:
    # 递归层级新建5 个部门
    def test_create_depth(self, token):
        parentid = 1
        for i in range(5):
            # 每个部门后面增加时间戳来辨识
            data = {
                "name": "one_Arlen" + str(parentid) + str(datetime.datetime.now().timestamp()),
                "parentid": parentid,
            }
            r = requests.post("https://qyapi.weixin.qq.com/cgi-bin/department/create",
                              params={"access_token": token},
                              json=data
                              ).json()
            logging.debug(r)
            parentid = r["id"]
            assert r["errcode"] == 0

    # 通过 pytest 参数化，校验不同国语言是否能创建 name，一般日韩阿拉伯检测都能成功就是标准编码，基本支持所有国际语言
    @pytest.mark.parametrize("name",[
        "广州研发中心",
        "東京アニメ研究所",
        "서울연구소"
    ])
    def test_create_order(self, name, token):
        data = {
            "name": name+Utils.udid(),
            "parentid": 1,
            "order": 1,
        }

        r=requests.post("https://qyapi.weixin.qq.com/cgi-bin/department/create",
                        params={"access_token": token},
                        json=data
                        ).json()
        logging.debug(r)
        assert r["errcode"] == 0

    def test_get(self, token):
        r=requests.get("https://qyapi.weixin.qq.com/cgi-bin/department/list",
                       params={"access_token": token},
                       ).json()
        logging.info(json.dumps(r, indent=2))