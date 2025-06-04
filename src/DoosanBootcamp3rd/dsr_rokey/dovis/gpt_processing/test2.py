from pathlib import Path
import openai
import os
from ament_index_python.packages import get_package_share_directory
from dotenv import load_dotenv
from playsound import playsound

current_dir = os.path.dirname(os.path.abspath(__file__))
resource_path = os.path.join(current_dir, "../resource")
dotenv_path = os.path.join(resource_path, ".env")

# .env 로드
is_load = load_dotenv(dotenv_path=dotenv_path)

# 키 불러오기
api_key = os.getenv("OPENAI_API_KEY2")
speech_file_path = os.path.join(resource_path, "output.mp3")
client = openai(api_key=api_key)
# 음성 생성 요청 (streaming X, 일반 파일 저장 방식)
response = client.audio.speech.create(
    model="tts-1",  # 또는 "tts-1-hd"
    voice="ash",   # coral, nova, shimmer 등 사용 가능
    input="저는 두비스입니다. 한국말 잘못해요. 잘부탁드립니다."
)

# 결과 저장
with open(speech_file_path, "wb") as f:
    f.write(response.content)

playsound(os.path.join(resource_path, "output.mp3"))
