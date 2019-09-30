import requests
import logging
import json


class TestRe(object):
    # 配置 logging（用来打印）
    # 因为 logging 默认的等级比较高，所以需要配置m默认等级才能打印出来
    logging.basicConfig(level=logging.INFO)

    def test_get(self):
        r = requests.get("https://testerhome.com/api/v3/topics.json?limit=2")
        # 打印 r
        logging.info(r)
        # 打印 r 文本
        logging.info(r.text)
        # 返回 json
        logging.info(r.json())
        # 对 打印对象进行json序列化展示（indent=2:格式缩进 2 格）
        logging.info(json.dumps(r.json(), indent=2))
