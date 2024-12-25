import json
from curl_cffi import requests
from typing import Dict, Any
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


from curl_cffi import requests
#
# # 测试不同的浏览器版本
# test_browsers = [
#     "chrome99",
#     "chrome100",
#     "chrome101",
#     "chrome104",
#     "chrome107",
#     "chrome110",
#     "safari15",
#     "safari16",
#     "firefox99",
#     "firefox100",
#     "firefox101",
#     "firefox102"
# ]
#
# def test_browser_support():
#     for browser in test_browsers:
#         try:
#             session = requests.Session()
#             session.impersonate = browser
#             print(f"✓ {browser} is supported")
#         except Exception as e:
#             print(f"✗ {browser} is not supported: {str(e)}")
#
# if __name__ == "__main__":
#     print("Testing browser support...")
#     test_browser_support()

def send_request(url: str, headers: Dict[str, str], payload: Dict[str, Any], proxy: str = None):
    try:
        # 配置CURL选项
        impersonate = "chrome110"

        # 创建session
        session = requests.Session()
        session.impersonate = impersonate

        # 设置代理
        if proxy:
            session.proxies = {
                'http': proxy,
                'https': proxy
            }

        # 发送请求
        response = session.post(
            url,
            headers=headers,
            json=payload,
            verify=False
        )

        # 返回响应
        return response.text

    except Exception as e:
        logger.error(f"Error during request: {str(e)}")
        raise


def main():
    url = "https://hungerstation.com/api/v2/vendors"
    headers = {
        'Accept-Language': 'en',
        'Connection': 'WIFI',
        'Device': 'Xiaomi 22021211RG',
        'Content-Type': 'application/json',
        'DEVICE-UID': '183b16c5-56a8-4f2a-a367-ad3f48edcf5a76e6fde1c79b143c',
        'User-Agent': 'HungerStation/1200 (Android 12)',
        'authorization': '',
        'perseus-client-id': '1720592469375.390334775292845453.Fb1d0NUj39',
        'perseus-session-id': '1735117151000.207839494948152051.7gTUUsgiVv',
        'Google-Client-Id': '183b16c5-56a8-4f2a-a367-ad3f48edcf5a76e6fde1c79b143c',
        'build-flavor': 'gms',
        'Adjust-ID': '9c1b72a530b9a4a1d25b2c74ffd2419c'
    }

    payload = {
        "pagination": {"limit": 50, "page": 0},
        "location": {
            "latitude": 24.684972586413583,
            "longitude": 46.65699664503336,
            "locale_id": 749
        },
        "search_query": "",
        "filters": [],
        "home_module_id": 1,
        "sorting_key": "DEFAULT",
        "locale_id": 749,
        "expedition_type": "delivery"
    }

    proxy = "http://127.0.0.1:7890"

    try:
        print("Sending request...")
        response = send_request(url, headers, payload, proxy)
        print("Response received:")
        print(response)

        # 尝试解析JSON响应
        try:
            json_response = json.loads(response)
            print("\nParsed JSON response:")
            print(json.dumps(json_response, indent=2, ensure_ascii=False))
        except json.JSONDecodeError:
            print("Could not parse response as JSON")

    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()