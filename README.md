1. setup Virtual environment:
    ```
    py -3.10 -m venv env
2. turn on virtual environment:
    ```
    env\Scripts\activate.bat
4. import libraries:
    ```
    pip install -r requirements.txt
5. \Lib\site-packages\librosa\core\constantq.py
    ```
    Ln 1059: complex -> complex128(1)
6. run server:
    ```
    python manage.py runserver
