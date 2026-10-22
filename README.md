# Практическая работа №3 — GitHub Actions CI/CD

## Приложение
Консольный калькулятор личных средств на Python. Доходы и расходы сохраняются в `transactions.json`, который не включается в Git и не перезаписывается при деплое. Для демонстрации: `python3 app.py --demo`.

## Локальные тесты

```sh
python3 -m pip install -r requirements-dev.txt
python3 -m pytest -v
python3 app.py --demo
```

## Конфигурация GitHub
1. Создать репозиторий GitHub и загрузить проект в ветку `main`.
2. В GitHub открыть **Settings → Actions → Runners → New self-hosted runner**, выбрать Linux и архитектуру ВМ, выполнить команды установки и регистрации на Linux, показанные GitHub. Не публиковать временный токен.
3. На Linux выполнить команды из GitHub для запуска `./run.sh` или (после регистрации) установки systemd-сервиса `sudo ./svc.sh install && sudo ./svc.sh start`.
4. Проверить в Settings → Actions → Runners, что runner отображается как Online.
5. При каждом push в `main` сначала запускается job **Run pytest** на GitHub-hosted Ubuntu. Только при успехе job **Deploy to Linux VM** запускается на Linux машине с self-hosted runner.
6. Деплой копирует `app.py` в `$HOME/finance-app` и записывает короткий SHA в `$HOME/finance-app/version.txt`. Учётные данные приложения не используются. Запуск deployed app: `python3 ~/finance-app/app.py --demo`.

**Важно:** Linux VM с runner должна иметь выход в интернет *во время получения GitHub Actions заданий и деплоя*. После отключения адаптера NAT runner станет Offline, если другого маршрута к GitHub нет. Восстановление адаптера для защиты позволяет продолжить CI/CD.

## Демонстрация сбоя тестов на защите
1. Убедиться, что последний workflow зелёный, а SHA соответствует `cat ~/finance-app/version.txt` на Linux.
2. В `app.py` изменить `balance = incomes - expenses` на `balance = incomes + expenses`, сделать commit/push в `main`.
3. Тесты `test_expense_reduces_balance` и `test_multiple_transactions` упадут; `Deploy to Linux VM` не выполнится; `version.txt` останется прежним.
4. Вернуть `balance = incomes - expenses`, сделать commit/push в `main`: тесты будут зелёными и новая версия автоматически развернётся на Linux.

Проект содержит базовое задание (test + deploy), без необязательных усложнений (линтер, Docker).
