import logging
from telegram import Update
from telegram.ext import ContextTypes
from langchain_core.messages import HumanMessage
from app.agents.router.graph import app as router_app

logger = logging.getLogger(__name__)


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    welcome_message = (
        f"Hi {user.mention_html()}! 👋\n\n"
        "I'm your Cashflow Assistant. I can help you manage your expenses and income.\n\n"
        "Just send me a message like:\n"
        "• 'Add an expense of $50 for groceries'\n"
        "• 'List my expenses'\n"
        "• 'Show my income'\n\n"
        "Type /help for more information."
    )
    await update.message.reply_html(welcome_message)


async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    help_message = (
        "🤖 <b>Cashflow Assistant Help</b>\n\n"
        "<b>Expense Management:</b>\n"
        "• Add expense: 'Add $50 expense for groceries'\n"
        "• List expenses: 'Show all my expenses'\n"
        "• Update expense: 'Update expense #1 amount to $60'\n"
        "• Delete expense: 'Delete expense #1'\n\n"
        "<b>Income Management:</b>\n"
        "• Coming soon!\n\n"
        "Just chat naturally - I'll understand what you need!"
    )
    await update.message.reply_html(help_message)


async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text
    user = update.effective_user

    logger.info(f"Received message from {user.username}: {user_message}")

    try:
        await update.message.chat.send_action("typing")

        result = router_app.invoke({
            "messages": [HumanMessage(content=user_message)]
        })

        response_message = result["messages"][-1]
        response_text = response_message.content

        logger.info(f"Sending response: {response_text}")

        await update.message.reply_text(response_text)

    except Exception as e:
        logger.error(f"Error processing message: {e}", exc_info=True)
        await update.message.reply_text(
            "Sorry, I encountered an error processing your request. Please try again."
        )
