# telegram-subscription-bot

Telegram-бот(ы) с проверкой подписки на канал.

## Что изменилось

Теперь конфигурация вынесена из кода в JSON-файл:
- список ботов (любой длины),
- ID канала и ссылка-приглашение,
- все пользовательские тексты/кнопки.

## 1) Создайте конфиг

Скопируйте пример:

```bash
cp bot_settings.json.example bot_settings.json
```

Отредактируйте `bot_settings.json`.

Пример:

```json
{
  "channel": {
    "id": -1002634329403,
    "invite_link": "https://t.me/+XXXXXXXXXXXX"
  },
  "bots": [
    {
      "name": "Sales Bot",
      "token_env": "SALES_BOT_TOKEN"
    },
    {
      "name": "Support Bot",
      "token_env": "SUPPORT_BOT_TOKEN"
    }
  ],
  "messages": {
    "success": "✅ Отлично! {bot_name} готов к работе.",
    "subscribe_prompt": "Для работы с {bot_name} подпишитесь на канал и нажмите «Проверить подписку».",
    "not_subscribed_alert": "❌ Вы всё ещё не подписаны.",
    "subscribe_button": "📣 Подписаться на канал",
    "check_button": "✅ Проверить подписку"
  }
}
```

`{bot_name}` в сообщениях автоматически заменяется на имя бота из `bots[].name`.

## 2) Задайте токены в переменных окружения

```bash
export SALES_BOT_TOKEN=123456:ABC...
export SUPPORT_BOT_TOKEN=123456:DEF...
```

## 3) Запустите

```bash
python bot_loader.py
```

Процесс поднимет всех ботов из `bots` (у которых найдены токены).


## Как применить исправление (если уже были подписанные пользователи)

1. Подтяните изменения с ветки/репозитория, где есть фикс.
2. Перезапустите процесс бота (`python bot_loader.py` или ваш systemd/pm2/supervisor restart).
3. Убедитесь, что бот добавлен в канал и имеет доступ к информации об участниках.
4. Проверьте конкретного пользователя через скрипт:

```bash
BOT_TOKEN=<TOKEN_БОТА> USER_ID=<ID_ПОЛЬЗОВАТЕЛЯ> python scripts/check_subscription.py
```

Если пользователь в канале и имеет Telegram-статус `restricted` с `is_member=true`, он теперь должен проходить проверку как подписанный.

## Дополнительно

- Путь к конфигу можно поменять переменной `BOT_CONFIG_FILE`.
- Для разовой проверки подписки:

```bash
BOT_TOKEN=<YOUR_BOT_TOKEN> USER_ID=<TELEGRAM_USER_ID> python scripts/check_subscription.py
```


## Ошибка TelegramConflictError при деплое

Если в логах есть `Conflict: terminated by other getUpdates request`, значит один и тот же токен опрашивается в нескольких местах одновременно.

Что проверить:

1. Запущен только **один** процесс `python bot_loader.py` (или один инстанс сервиса) на токен.
2. Нет второго деплоя этого же проекта (другая VM/контейнер/Render service) с теми же переменными токенов.
3. В переменных окружения нет одинаковых значений для разных `token_env` (дубли токенов).
4. Не запущен параллельно webhook-процесс на те же токены.

В этом проекте добавлена защита: при старте дубли токенов автоматически пропускаются с предупреждением в логах.
