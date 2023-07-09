import os
from dotenv import load_dotenv

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from dialog_flow import detect_intent_texts


def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Привет {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def reply(update: Update, context: CallbackContext) -> None:
    project_id = os.getenv("DIALOGFLOW_PROJECT_ID")
    response = detect_intent_texts(project_id, update.effective_chat.id, [update.message.text], "ru")
    update.message.reply_text(response.fulfillment_text)


def main() -> None:
    load_dotenv()
    tg_token = os.getenv("TG_BOT_TOKEN")

    updater = Updater(tg_token)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))

    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, reply))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
