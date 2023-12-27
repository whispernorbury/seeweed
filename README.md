1. setup Virtual environment, GoTo env:
    py -3.10 -m venv env
    env\Scripts\activate.bat
2. import libraries:
    pip install -r requirements.txt
3. \Lib\site-packages\librosa\core\constantq.py
    Ln 1059: complex -> complex128(1)
4. run server:
    python manage.py runserver