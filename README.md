# telegram-subscription-bot
Telegram bot with subscription check for a channel
## Subscription check script
Run a one-off check against your channel using environment variables:

```bash
BOT_TOKEN=<YOUR_BOT_TOKEN> USER_ID=<TELEGRAM_USER_ID> python scripts/check_subscription.py
