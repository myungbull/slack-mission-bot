# send_mission_now.py
import os, random, json, requests
from datetime import datetime

TOKEN = os.getenv("SLACK_BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("환경변수 SLACK_BOT_TOKEN 이 설정되지 않았습니다. (GitHub Secrets에 등록했는지 확인)")

USERS = ["U09RGBZSMUK", "U09S1LYSUV7"]  # DM을 보낼 Slack User ID들

MISSIONS = [
    "창문 열고 오늘 날씨 인증샷 📷","물 한 컵 마시고 컵 인증샷 🥛","밖 풍경 찍기 🌄","침대 정리 인증샷 🛏",
    "세수 후 거울 셀카 🪞","양치도구와 함께 셀카 🪥","현관/문 앞 사진 🚪","하늘 사진 찍기 🌤","아침 스트레칭 인증샷 🧘",
    "주먹 쥐고 파이팅 셀카 ✊","손가락 V 인증샷 ✌","건강식 아침 인증샷 🍎","샤워 후 수건 인증샷 🚿","커피/차 준비 인증샷 ☕",
    "휴지통 비운 사진 🗑","책상 정리 인증샷 🧹","날씨 앱 화면 인증샷 📱","침대 이불 정리 사진","냉장고 재료 인증샷 🥗","과일 씻은 사진 🍇",
    "스쿼트 자세 인증샷","팔굽혀펴기 후 바닥 인증샷","아침 인사 셀카 🙋","아침 독서 사진 📖","시계/달력과 함께 인증샷 ⏰",
    "Good Morning 메모 + 셀카","오늘 옷차림 인증샷 👕","가방 준비 사진 🎒","플래너/일기장 펴고 사진 ✍","냉수 세안 후 셀카 ❄",
    "싱크대 정리 인증샷","창문 닦는 인증샷","집안일 인증샷 🧽","식물 물주기 🌱","커튼 열고 햇빛 사진 ☀","오늘 목표 3개 쓰고 사진",
    "간단 요가 인증샷","냉장고 정리 인증샷","바닥에 발 찍기 (기상 인증)","불 켜진 화장실 인증샷 🚽","침대에서 내려온 발 인증샷",
    "세탁기 돌리기 인증샷 🧺","테이블 닦는 중 인증샷","오늘 마실 음료 인증샷","책상 앞에서 셀카","귀여운 표정 셀카 😆",
    "양손 번쩍 셀카 🙌","문 밖 산책 인증샷 🚶‍♂️","운동화 신고 인증샷 👟","아침 기지개 셀카 🧍"
]

# requests 세션: 프록시 무시 + 타임아웃 + ASCII UA
s = requests.Session()
s.trust_env = False
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json; charset=utf-8",
    "User-Agent": "wake-mission-bot/1.0",
}

def slack_api(method: str, payload: dict) -> dict:
    url = f"https://slack.com/api/{method}"
    r = s.post(url, headers=HEADERS, data=json.dumps(payload).encode("utf-8"), timeout=15)
    r.raise_for_status()
    data = r.json()
    if not data.get("ok"):
        raise RuntimeError(f"{method} error: {data.get('error')}")
    return data

def open_dm(user_id: str) -> str:
    return slack_api("conversations.open", {"users": user_id})["channel"]["id"]

def post_message(channel: str, text: str):
    slack_api("chat.postMessage", {"channel": channel, "text": text})

def send_mission_now():
    mission = random.choice(MISSIONS)
    text = f"🌅 *오늘의 아침 미션!* 🌅\n👉 `{mission}`\n사진 인증으로 완료해주세요!"
    for uid in USERS:
        ch = open_dm(uid)
        post_message(ch, text)
        print(f"[{datetime.now()}] sent to {uid}")

if __name__ == "__main__":
    # 인증 체크(원하면 주석 처리 가능)
    print(slack_api("auth.test", {}))
    send_mission_now()
