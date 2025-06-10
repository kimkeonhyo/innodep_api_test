import json
import os
import platform
import subprocess

from utils.logger import set_logger
from datetime import datetime

def check_os():
    os_name = platform.system()

    if os_name == "Windows":
        return "win"
    elif os_name == "Darwin":
        return "mac"
    else:
        return os_name
    
    
class VCA:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.auth_token = None
        self.api_serial = None
        self.logger = set_logger("logs/vca.log")

    # TODO :  'x-account-pass:{pwd}' 구문이 mac과 윈도우 다르게 먹음 분리해야함
    # option import sys로 os별로 명령어 다르게 ->
    def login(self, id: str, pwd: str):

        if check_os() == "mac":
            print("맥입니다")
            command = f"""
            curl -v -X GET "{self.base_url}/api/login?force-login=false" \
            -H "x-account-id:{id}" \
            -H 'x-account-pass:{pwd}' \
            -H "x-account-group:group1" \
            -H "x-license:licVCA" \
            --max-time 30
            """
        elif check_os() == "win":
            print("윈도우 입니다")
            command = f'curl -v -X GET "{self.base_url}/api/login?force-login=false" -H "x-account-id:{id}" -H "x-account-pass:{pwd}" -H "x-account-group:group1" -H "x-license:licNormalClient" --max-time 30'

        result = subprocess.run(
            command, shell=True, capture_output=True, text=True, encoding="utf-8"
        )  # 인코딩 에러 남(현재 윈도우), 윈도우와 맥 호환이 다르니 예외처리 추가
        if result.returncode == 0:
            # Extract the JSON part from the response
            json_start_index = result.stdout.find("{")
            json_end_index = result.stdout.rfind("}") + 1
            json_response = result.stdout[json_start_index:json_end_index]

            try:
                response_dict = json.loads(json_response)
                self.logger.info(f"응답 JSON: {response_dict}")
                self.auth_token = response_dict["results"]["auth_token"]
                self.api_serial = response_dict["results"]["api_serial"]
                self.logger.info(f"Auth Token: {self.auth_token}")
                self.logger.info(f"API Serial: {self.api_serial}")
            except (json.JSONDecodeError, KeyError) as e:
                self.logger.error(f"Failed to parse JSON response: {e}")
        else:
            self.logger.error(f"Command failed with return code {result.returncode}")
            self.logger.error(f"Error output: {result.stderr}")
            
    def send_event(self):
        event_num = int(input("이벤트 번호를 입력하세요 : "))
        event_msg = input("이벤트 메시지를 입력하세요 : ")
        print(f"입력된 이벤트 번호 : {event_num} \n 이벤트 메시지 : {event_msg}")
        
        ## 현재 시간 문자열 생성
        event_time = datetime.now().strftime("%y-%m-%d %H:%M:%S.%f")[:-3]
        print(f"이벤트 발생 시간 : {event_time}")
        ## post API body json
        json_payload = json.dumps({
            "dev_serial": 100004,
            "dch_ch": 1,
            "event_id": event_num,
            "event_time": event_time,
            "event_msg": event_msg,
            "event_status": 1
        })
        
        if check_os() == "mac":
            
            command = f"""
            curl -v -X POST "{self.base_url}/api/event/send-vca" \
            -H "Content-Type: application/json" \
            -H "x-auth-token:{self.auth_token}" \
            -H "x-api-serial:{self.api_serial}" \
            -d '{json_payload}'
            """
        elif check_os() == "win":
            command = f'curl -v -X POST "{self.base_url}/api/event/send-vca" -H "Content-Type: application/json" -H "x-auth-token: {self.auth_token}" -H "x-api-serial: {self.api_serial}" -d "{json_payload}"'
        else:
            self.logger.error("Unsupported OS")
            return
            
        print("이벤트 전송 중...")
        
        result = subprocess.run(
            command, shell=True, capture_output=True, text=True, encoding="utf-8"
        )
        
        if result.returncode == 0:
            self.logger.info(f"event send complete")
            print("이벤트 전송 성공!")
        else:
            self.logger.error(f"command failed with return code {result.returncode}")
            self.logger.error(f"stderr: {result.stderr}")
            print("이벤트 전송 실패")