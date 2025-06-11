# Vurix VCA Event send Tool
Vurix API를 사용하여 CCTV 로그에 따른 VCA 이벤트를 전송하는 기능을 제공

## 1. Requirements
Create a virtual environment
```bash
conda create -n {env.name} python=3.11
conda activate {env.name}
```
Install the requirements.txt
```bash
pip install -r reuirements.txt
```

## 2. 실행방법
VCA.py를 이용하여 실행할 수 있다.
```bash
python VCA.py VCA \
   -vu {Vurix API URL} \
   -vi {Vurix ID} \
   -vp {Vurix Password}
```