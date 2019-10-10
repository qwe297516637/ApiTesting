import requests
import logging
import json
import jsonpath
from hamcrest import *
from jsonschema import validate


class TestRequests(object):
    # 配置 logging（用来打印）
    # 因为 logging 默认的等级比较高，所以需要配置m默认等级才能打印出来
    logging.basicConfig(level=logging.INFO)
    url = "https://testerhome.com/api/v3/topics.json?limit=2"

    def test_get(self):
        r = requests.get(self.url)
        # 打印 r
        logging.info(r)
        # 打印 r 文本
        logging.info(r.text)
        # 返回 json
        logging.info(r.json())
        # 对 打印对象进行json序列化展示（indent=2:格式缩进 2 格）
        logging.info(json.dumps(r.json(), indent=2))

    def test_post(self):
        r=requests.post(self.url,
                        params={"a": 1, "b": "aaaa"},
                        json={"hh": "你好", "vv": "aa"},
                        headers={"aa": "ss", "bb": "ccc"},
                        # 增加代理，能从 Charles 提取到数据
                        proxies={"https": "192.168.3.16:8888"},
                        # 不校验证书
                        verify=False
                        )
        # 检查 url
        logging.info(r.url)
        # 检查文本
        logging.info(r.text)
        # 对 打印对象进行json序列化展示（indent=2:格式缩进 2 格）
        logging.info(json.dumps(r.json(), indent=2))

    def test_cookies(self):
        r=requests.get("http://47.95.238.18:8090/cookies",
                       cookies={"a": "11", "b": "22"})
        logging.info(r.text)

    def test_xueqiu_quote(self):
        url = "https://stock.xueqiu.com/v5/stock/portfolio/stock/list.json?"
        r = requests.get(url,
                         cookies={"xq_a_token": "8690ceb72296848c7231df0a19a78a3b14bb6899",
                                  "u": "3314078945"},
                         headers={"User-Agent": "Xueqiu Android 11.19"},
                         # 通过判断，这个是指定的页面数，所以是必要写进来
                         params={"category": "1"}
                         )
        logging.info(json.dumps(r.json(), indent=2))
        # 增加断言，查返回的数据中data下 category 是不是等于 1
        assert r.json()["data"]["category"] == 1
        assert r.json()["data"]["stocks"][0]["name"] == "招商银行"

        a = jsonpath.jsonpath(r.json(), "$.data.stocks[0].name")
        logging.info(a)

        b = jsonpath.jsonpath(r.json(), "$.data.stocks[?(@.symbol == 'SH600036')].name")[0]
        logging.info(b)
        # 常用来做断言，例如当股票码为 SH600036 时，name 是不是为招商银行
        assert b == "招商银行"
        # 通过断言返回值是否等于"招商银1行"，如果不等于报后面的错误，等同上面的 assert
        assert_that(b, equal_to("招商银行"), "比较上市代码与名字")

        c = jsonpath.jsonpath(r.json(), "$.data.stocks[*].name")
        logging.info(c)

        assert_that(
            c,
            any_of(
                has_item("招商银行"),
                has_item("中国软件")
            ), "没有匹配数据"
        )

    def test_hamcrest(self):
        # 断言 0.1*0.1 结果跟 0.01 比较误差是否超过了给定值
        assert_that(0.1*0.1, close_to(0.01, 0.000000000000000002))
        # 断言 a 存在这组数据中
        assert_that(["a", "b", "c"], has_item("a"))
        # 断言存在多个值
        assert_that(["a", "b", "c"], has_items("c", "b"))
        # 断言任何一个条件，只要一个匹配就是对的，all_of 就是全部都要匹配
        assert_that(
            ["a", "b", "c"],
            any_of(
                has_items("c", "d"),
                has_items("c", "b")
            )
        )

    # schema校验
    def test_xueqiu_list_schema(self):
        url = "https://stock.xueqiu.com/v5/stock/portfolio/stock/list.json?"
        r = requests.get(url,
                         cookies={"xq_a_token": "8690ceb72296848c7231df0a19a78a3b14bb6899",
                                  "u": "3314078945"},
                         headers={"User-Agent": "Xueqiu Android 11.19"},
                         # 通过判断，这个是指定的页面数，所以是必要写进来
                         params={"category": "1"}
                         )
        logging.info(json.dumps(r.json(), indent=2))

        schema=json.load(open("list_schema.json"))
        validate(instance=r.json(), schema=schema)

    def test_schema(self):
        schema = {
            "type": "object",
            "properties": {
                "price": {"type": "number"},
                "name": {"type": "string"},
            },
        }

        validate(instance={"name": "Eggs", "price": 34.99}, schema=schema)