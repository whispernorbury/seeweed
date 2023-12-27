# SEEWEED
The fairy tale maker AI
## Install
1. setup Virtual environment:
    ```
    py -3.10 -m venv env
2. turn on virtual environment:
    ```
    env\Scripts\activate.bat
4. import libraries:
    ```
    pip install -r requirements.txt
5. Modify \Lib\site-packages\librosa\core\constantq.py
    ```
    Ln 1059: complex -> complex128(1)
5. DB migrate and run server:
    ```
    python manage.py migrate
    python manage.py runserver
## Add Your voice!
* Import `<YourGlowTTS>.tar` to
```
/TTS/data/glowtts-v2/
```
* Import `<YourHifigan>.tar` to
```
/TTS/data/hifigan-v2/
```
### **NOTE**
1. The ```SeeWeed``` is available only on Window OS...
2. You have to poss your own OpenAI API Key!!
## REFERENCE
[Openai](https://openai.com): for `GPT-4, Dalle`  
[SCE-TTS](https://sce-tts.github.io/#/v2/index): for `TTS(customizable)`  
[Contest Info](https://sites.google.com/yonsei.ac.kr/genaicontest): about `Yonsei genAI contest`  
## LICENSE
##### MIT © TeamDahe
