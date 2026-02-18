# Учебный проект для группы QAP22

---

## Содержание

- [Установка Python](#установка-python)
- [Установка PyCharm](#установка-pycharm)
- [Создание проекта и venv](#создание-проекта-и-venv)
- [Установка Git](#установка-git)
- [Установка всех пакетов](#установка-всех-пакетов)
- [Запуск первого теста](#запуск-первого-теста)
- [Запуск первого теста с разными ключами](#запуск-первого-теста-с-разными-ключами)

---

## Установка Python

**Проверка наличия:**

```bash
python --version
# или
python3 --version
```

**Windows**

1. Скачайте Python 3.11+ с официального сайта.
2. В инсталляторе поставьте галочку **“Add Python to PATH”**.
3. Проверьте:

```powershell
python --version
pip --version
```

**macOS / Linux**
Часто Python уже есть. Если нет — установите из менеджера пакетов или с сайта Python.

```bash
python3 --version
python3 -m pip --version
```

---

## Установка PyCharm

1. Скачайте **PyCharm Community**.
2. В настройках выберите интерпретатор Python (из установленного Python или из виртуального окружения проекта).
3. Опционально включите предпросмотр Markdown и автосохранение.

---

## Создание проекта и venv

```bash
# macOS/Linux
mkdir qa-project && cd qa-project
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip

# Windows PowerShell
mkdir qa-project; cd qa-project
python -m venv .venv
. .\.venv\Scripts\activate
python -m pip install --upgrade pip
```
---

## Установка Git

**Проверка:**

```bash
git --version
```

**Установка:**

* Windows: установите Git for Windows (Git Bash или PowerShell).
* macOS: `xcode-select --install` или установщик Git.
* Linux (Ubuntu): `sudo apt-get install git`.

**Быстрая настройка:**

```bash
git config --global user.name "Ваше Имя"
git config --global user.email "you@example.com"
```

**Клонирование проекта**
```bash
git clone https://github.com/qahelping/qap22_python_project
```
---

## Установка всех пакетов

Создайте `requirements.txt` в корне проекта или скачайте из этого репозитория:

```
pytest
selenium
webdriver-manager
```

Установите всё разом:

```bash
pip install -r requirements.txt
```

---

## Запуск первого теста

Запуск тестов:

```bash
pytest -q
```

## Запуск первого теста с разными ключами

**Базовые:**

```bash
pytest          # стандартный вывод
pytest -v       # подробные имена тестов
pytest -q       # тихий режим
pytest tests/test_pytest/test_intro.py -v -s --cache-clear --tb=short  # пример
```

Полезные флаги на практике
```bash
#-s — не захватывать stdout/stderr (удобно для дебага print)
#--lf — запустить только “упавшие” на прошлом прогоне
#--ff — сначала упавшие, потом остальные
#--durations=10 — показать 10 самых долгих тестов
```bash

**Отбор тестов:**

```bash
pytest tests/test_python_org_wait.py   # один файл
pytest tests -k search                 # по подстроке в имени
pytest -k "not e2e"                    # исключить
```

**Маркеры:**

```python
import pytest

@pytest.mark.e2e
def test_something():
    ...
```

Запуск по маркеру:

```bash
pytest -m e2e
```

**Поведение при падениях и отчёты:**

```bash
pytest -x            # стоп на первом фейле
pytest --maxfail=1   # то же
pytest -ra           # причины skip/xfail
pytest -s            # показать print()/stdout
```


```bash
allure serve allure-results

allure generate allure-results -o allure-report --clean
allure serve
```
