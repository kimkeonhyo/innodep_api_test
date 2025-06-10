import argparse
import os
import threading
import time
from pathlib import Path

import pandas as pd

from utils.VCA_api import VCA
from utils.logger import set_logger

def get_main_parser() -> argparse.ArgumentParser:
    """메인 파서를 생성하고 서브 파서를 추가합니다."""
    parser = argparse.ArgumentParser(description="RTSP 녹화 및 Vurix 연동 도구")

    subparsers = parser.add_subparsers(
        dest="command", help="명령어를 선택하세요: VCA"
    )
    
    #VCA 서브 명령어용 파서
    VCA_parser = subparsers.add_parser(
        "VCA", help="VCA 이벤트를 전송합니다."
    )
    VCA_parser.add_argument(
        "-vu","--vurix-url", required=True, help="Vurix API base URL."
    )
    VCA_parser.add_argument(
        "-vi", "--vurix-id", required=True, help="Vurix API ID."
    )
    VCA_parser.add_argument(
        "-vp", "--vurix-pwd", required=True, help="Vurix API Password."
    )
    
    return parser

def VCA_main(args: argparse.Namespace) -> None:
    """VCA 이벤트를 전송합니다."""
    
    logger = set_logger("logs/VCA.log")
    
    try:
        # logger.info(args.data)
        
        vca = VCA(args.vurix_url)
        vca.login(args.vurix_id, args.vurix_pwd)
        
        vca.send_event()
    
    except Exception as e:
        logger.error(f"VCA 처리 중 오류 발생: {e}")
        print(f"[오류] VCA 실행 실패: {e}")
    
    
    
def main() -> None:

    parser = get_main_parser()
    args = parser.parse_args()

    if args.command == "VCA":
        VCA_main(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()