# Check For PC Status



## 0. Table Of Contents

1. Introduction
2. Installation
3. How to run





## 1. Introduction

카페 및 공공장소에서 자리비움 시 노트북 도난을 방지해주는 솔루션 입니다.

해당 솔루션은 아래 기능을 제공하고 있습니다.

- 주기적으로 AC 전원 어댑터 연결 체크
- 상태이상에 대한 웹캠을 통한 캡쳐기능
- 해당 결과들을 주기적으로 텔레그램 메신저에 전송
- 도난결과에 따라 텔레그램 응답 메시지에 따른 원격 명령 수행(예정)





## 2. Installation

### 2-1. Requirements

```
pip install -r requirements.txt
```





## 3. How to run

### 3-1. Create TelegramBot

우선적으로 텔레그램 메신저를 통해 자신만의 Bot을 생성해야 합니다.

Bot 생성방법은 [How to make TelegramBot?](https://github.com/madfalc0n/TIL/blob/master/Telegram/How_to_make_telegram_bot.md)을 참조하시면 됩니다.

### 3-2. Run main.py

```
python main.py -t <telegrambot token> -p <log direct>
```

#### 3-2-1. Must Required Parameters

1. `--token` or `-t`

   - 위에서 생성한 텔레그램 봇의 토큰 값을 반드시 명시해주어야 합니다.

     ```
     python main.py -t '123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11'
     ```


#### 3-2-2. Sub Required Parameters

1. `--pic_path` or `-lp`

   - 캡쳐한 이미지를 저장하기 위한 경로입니다.

   - 명시하지 않을 경우 `log_pic/`에 저장됩니다.

     ```
     python main.py -t '123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11' -lp 'custom_log_pic/'
     ```

2. `--stat_path` or `-ls`

   - 캡쳐한 이미지를 저장하기 위한 경로입니다.

   - 명시하지 않을 경우 `log_stat/`에 저장됩니다.

     ```
     python main.py -t '123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11' -ls 'custom_log_stat/'
     ```

     