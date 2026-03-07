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

## Дополнительно

- Путь к конфигу можно поменять переменной `BOT_CONFIG_FILE`.
- Для разовой проверки подписки:

```bash
BOT_TOKEN=<YOUR_BOT_TOKEN> USER_ID=<TELEGRAM_USER_ID> python scripts/check_subscription.py
```
