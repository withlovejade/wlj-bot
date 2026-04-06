import os
import uuid
from datetime import datetime

from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)

BOT_TOKEN = os.environ["BOT_TOKEN"]
ADMIN_CHAT_ID = int(os.environ["ADMIN_CHAT_ID"])

(
    MENU,
    YOUR_NAME,
    INSTAGRAM,
    TELEGRAM_HANDLE,
    ITEM_TITLE,
    PIECE_TYPE,
    SIZE,
    PRICE,
    PURCHASE_INFO,
    DESCRIPTION,
    FLAWS,
    CERTIFICATIONS,
    DEALING,
    PHOTOS,
    VIDEO,
    CONFIRM,
    REMOVE_POST_LINK,
    REMOVE_SUBMISSION_CODE,
    REMOVE_CONFIRM,
) = range(19)

MENU_KEYBOARD = [
    ["Submit Marketplace Item"],
    ["Remove Sale Post"],
    ["How It Works", "Contact Admin"],
]


def main_menu_markup():
    return ReplyKeyboardMarkup(MENU_KEYBOARD, resize_keyboard=True)


def yes_no_markup():
    return ReplyKeyboardMarkup([["Yes", "No"]], resize_keyboard=True, one_time_keyboard=True)


def safe_text(value):
    if value is None:
        return "None"
    value = str(value).strip()
    return value if value else "None"


def generate_submission_code():
    date_part = datetime.utcnow().strftime("%Y%m%d")
    short_part = uuid.uuid4().hex[:6].upper()
    return "WLJ-{}-{}".format(date_part, short_part)


async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, text=None) -> int:
    if text is None:
        text = (
            "Welcome to WLJ Family Bot.\n\n"
            "Please choose an option from the menu below."
        )

    await update.message.reply_text(
        text,
        reply_markup=main_menu_markup(),
    )
    return MENU


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data.clear()
    return await show_main_menu(update, context)


async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    choice = update.message.text.strip()

    if choice == "Submit Marketplace Item":
        return await start_submission(update, context)

    if choice == "Remove Sale Post":
        return await start_remove_sale_post(update, context)

    if choice == "How It Works":
        await update.message.reply_text(
            "WLJ Marketplace Options:\n\n"
            "1. Submit Marketplace Item\n"
            "   - Answer the listing questions\n"
            "   - Upload up to 5 photos\n"
            "   - Optionally upload 1 video\n"
            "   - Confirm your submission\n"
            "   - Receive your unique submission code\n\n"
            "2. Remove Sale Post\n"
            "   - Submit your Telegram post link\n"
            "   - Submit your marketplace submission code\n"
            "   - Admin will review your removal request"
        )
        return await show_main_menu(
            update,
            context,
            "You’re back at the main menu. Please choose an option.",
        )

    if choice == "Contact Admin":
        await update.message.reply_text(
            "If you need help, please contact the WLJ admin team at @WLJSingapore directly in your usual WLJ channel or group."
        )
        return await show_main_menu(
            update,
            context,
            "You’re back at the main menu. Please choose an option.",
        )

    await update.message.reply_text("Please choose one of the menu options.")
    return MENU


async def start_submission(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data.clear()
    context.user_data["photos"] = []
    context.user_data["submission_code"] = generate_submission_code()

    await update.message.reply_text(
        "Great! I’ll ask you a few questions and send your submission to the admin team for review.\n\n"
        "How do I address you?",
        reply_markup=ReplyKeyboardRemove(),
    )
    return YOUR_NAME


async def your_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["your_name"] = update.message.text.strip()
    await update.message.reply_text(
        "To verify that the item was purchased from WLJ, please provide either your Instagram/Tiktok handle or the item purchase code. If not submitted, this post will not be approved."
    )
    return INSTAGRAM


async def instagram(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["instagram"] = update.message.text.strip()
    await update.message.reply_text(
        "Please indicate your Telegram handle for the buyer to reach out to you. If not submitted, this post will not be approved."
    )
    return TELEGRAM_HANDLE


async def telegram_handle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["telegram_handle"] = update.message.text.strip()
    await update.message.reply_text("What do you want your post title to be?")
    return ITEM_TITLE


async def item_title(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["item_title"] = update.message.text.strip()
    await update.message.reply_text(
        "What item category is it? Such as bangle/earrings/rings/etc."
    )
    return PIECE_TYPE


async def piece_type(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["piece_type"] = update.message.text.strip()
    await update.message.reply_text(
        "What is the size or measurements of the item you are selling?"
    )
    return SIZE


async def size(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["size"] = update.message.text.strip()
    await update.message.reply_text("How much are you selling the item for?")
    return PRICE


async def price(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["price"] = update.message.text.strip()
    await update.message.reply_text(
        "When did you purchase this item from WLJ? A rough date or month will be sufficient."
    )
    return PURCHASE_INFO


async def purchase_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["purchase_info"] = update.message.text.strip()
    await update.message.reply_text(
        "Please write a short description for your item. This will be the description body of your post."
    )
    return DESCRIPTION


async def description(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["description"] = update.message.text.strip()
    await update.message.reply_text("Please describe the flaws or condition.")
    return FLAWS


async def flaws(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["flaws"] = update.message.text.strip()
    await update.message.reply_text(
        "Please indicate if you have any certifications for the item. If none, type None."
    )
    return CERTIFICATIONS


async def certifications(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["certifications"] = update.message.text.strip()
    await update.message.reply_text(
        "Any preferred method of transacting? Such as cash on delivery or mailing? If none, type None."
    )
    return DEALING


async def dealing(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["dealing"] = update.message.text.strip()
    await update.message.reply_text(
        "Now send up to 5 photos of the item.\n"
        "Send them one by one. There may be some delays, so please do not rush.\n\n"
        "When finished, send /done"
    )
    return PHOTOS


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    saved_photos = context.user_data.get("photos", [])

    if len(saved_photos) >= 5:
        await update.message.reply_text(
            "You already uploaded 5 photos. Send /done to continue."
        )
        return PHOTOS

    photo = update.message.photo[-1]
    saved_photos.append(photo.file_id)
    context.user_data["photos"] = saved_photos

    await update.message.reply_text(
        "Saved photo {}/5. Send another photo or /done.".format(len(saved_photos))
    )
    return PHOTOS


async def done_photos(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if len(context.user_data.get("photos", [])) == 0:
        await update.message.reply_text(
            "Please send at least 1 photo before continuing."
        )
        return PHOTOS

    await update.message.reply_text(
        "Now send 1 video if you have one.\n"
        "If you want to skip, send /skip."
    )
    return VIDEO


async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["video"] = update.message.video.file_id
    await update.message.reply_text(
        "Final confirmation:\n"
        "Do you confirm this piece was purchased from WLJ and all details provided are honest and complete?",
        reply_markup=yes_no_markup(),
    )
    return CONFIRM


async def skip_video(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["video"] = None
    await update.message.reply_text(
        "Final confirmation:\n"
        "Do you confirm this piece was purchased from WLJ and all details provided are honest and complete?",
        reply_markup=yes_no_markup(),
    )
    return CONFIRM


async def send_submission_to_admin(
    context: ContextTypes.DEFAULT_TYPE, data: dict, user_id: int, username
) -> None:
    submitted_by = "@{}".format(username) if username else "(no username)"

    details = (
        "New WLJ Marketplace Submission\n\n"
        "Submission Code: {}\n"
        "Submitted by Telegram user: {}\n"
        "User ID: {}\n\n"
        "Name: {}\n"
        "Instagram / Purchase Verification: {}\n"
        "Telegram Handle: {}\n"
        "Item Title: {}\n"
        "Piece Type: {}\n"
        "Size / Measurements: {}\n"
        "Price: {}\n"
        "WLJ Purchase Info: {}\n"
        "Description: {}\n"
        "Flaws / Condition: {}\n"
        "Certifications: {}\n"
        "Dealing: {}\n"
        "Confirmed: Yes"
    ).format(
        safe_text(data.get("submission_code")),
        submitted_by,
        user_id,
        safe_text(data.get("your_name")),
        safe_text(data.get("instagram")),
        safe_text(data.get("telegram_handle")),
        safe_text(data.get("item_title")),
        safe_text(data.get("piece_type")),
        safe_text(data.get("size")),
        safe_text(data.get("price")),
        safe_text(data.get("purchase_info")),
        safe_text(data.get("description")),
        safe_text(data.get("flaws")),
        safe_text(data.get("certifications")),
        safe_text(data.get("dealing")),
    )

    await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=details)

    photos = data.get("photos", [])
    for idx, file_id in enumerate(photos, start=1):
        await context.bot.send_photo(
            chat_id=ADMIN_CHAT_ID,
            photo=file_id,
            caption="Submission Code: {}\nSubmission photo {}/{}".format(
                safe_text(data.get("submission_code")),
                idx,
                len(photos),
            ),
        )

    if data.get("video"):
        await context.bot.send_video(
            chat_id=ADMIN_CHAT_ID,
            video=data["video"],
            caption="Submission Code: {}\nSubmission video".format(
                safe_text(data.get("submission_code"))
            ),
        )


async def confirm(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    answer = update.message.text.strip().lower()

    if answer not in ["yes", "no"]:
        await update.message.reply_text("Please reply with Yes or No.")
        return CONFIRM

    if answer == "no":
        context.user_data.clear()
        return await show_main_menu(
            update,
            context,
            "Submission cancelled. You’re back at the main menu.",
        )

    user = update.effective_user
    data = dict(context.user_data)

    try:
        await send_submission_to_admin(
            context=context,
            data=data,
            user_id=user.id,
            username=user.username,
        )
        submission_code = safe_text(data.get("submission_code"))
        context.user_data.clear()
        return await show_main_menu(
            update,
            context,
            "Thank you. Your submission has been sent to the WLJ admin team for review.\n\n"
            "Your marketplace submission code is:\n"
            "{}\n\n"
            "Please keep this code safe. You will need it if you want to request removal of your sale post later.\n\n"
            "You’re back at the main menu.".format(submission_code),
        )
    except Exception as e:
        print("ERROR SENDING TO ADMIN CHAT:", e)
        context.user_data.clear()
        return await show_main_menu(
            update,
            context,
            "I collected your answers, but I could not send them to the admin chat.\n\n"
            "Please try again from the menu.",
        )


async def start_remove_sale_post(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data.clear()
    await update.message.reply_text(
        "You chose Remove Sale Post.\n\n"
        "Please send the Telegram post link of the sale post you want removed.",
        reply_markup=ReplyKeyboardRemove(),
    )
    return REMOVE_POST_LINK


async def remove_post_link(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["remove_post_link"] = update.message.text.strip()
    await update.message.reply_text(
        "Please send your marketplace submission code."
    )
    return REMOVE_SUBMISSION_CODE


async def remove_submission_code(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["remove_submission_code"] = update.message.text.strip()
    await update.message.reply_text(
        "Final confirmation:\n"
        "Do you want WLJ admin to remove this sale post?",
        reply_markup=yes_no_markup(),
    )
    return REMOVE_CONFIRM


async def send_remove_request_to_admin(
    context: ContextTypes.DEFAULT_TYPE, data: dict, user_id: int, username
) -> None:
    requested_by = "@{}".format(username) if username else "(no username)"

    details = (
        "WLJ Remove Sale Post Request\n\n"
        "Requested by Telegram user: {}\n"
        "User ID: {}\n\n"
        "Telegram Post Link: {}\n"
        "Marketplace Submission Code: {}"
    ).format(
        requested_by,
        user_id,
        safe_text(data.get("remove_post_link")),
        safe_text(data.get("remove_submission_code")),
    )

    await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=details)


async def remove_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    answer = update.message.text.strip().lower()

    if answer not in ["yes", "no"]:
        await update.message.reply_text("Please reply with Yes or No.")
        return REMOVE_CONFIRM

    if answer == "no":
        context.user_data.clear()
        return await show_main_menu(
            update,
            context,
            "Remove sale post request cancelled. You’re back at the main menu.",
        )

    user = update.effective_user
    data = dict(context.user_data)

    try:
        await send_remove_request_to_admin(
            context=context,
            data=data,
            user_id=user.id,
            username=user.username,
        )
        context.user_data.clear()
        return await show_main_menu(
            update,
            context,
            "Your remove sale post request has been sent to the WLJ admin team.\n\n"
            "You’re back at the main menu.",
        )
    except Exception as e:
        print("ERROR SENDING REMOVE REQUEST TO ADMIN CHAT:", e)
        context.user_data.clear()
        return await show_main_menu(
            update,
            context,
            "I collected your remove request, but I could not send it to the admin chat.\n\n"
            "Please try again from the menu.",
        )


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data.clear()
    return await show_main_menu(
        update,
        context,
        "Action cancelled. You’re back at the main menu.",
    )


async def invalid_photo_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Please send a photo, or send /done when finished."
    )
    return PHOTOS


async def invalid_video_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Please send one video, or send /skip.")
    return VIDEO


def main() -> None:
    app = Application.builder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("start", start),
            CommandHandler("submit", start_submission),
            CommandHandler("remove", start_remove_sale_post),
        ],
        states={
            MENU: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, menu_handler),
            ],
            YOUR_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, your_name)],
            INSTAGRAM: [MessageHandler(filters.TEXT & ~filters.COMMAND, instagram)],
            TELEGRAM_HANDLE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, telegram_handle)
            ],
            ITEM_TITLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, item_title)],
            PIECE_TYPE: [MessageHandler(filters.TEXT & ~filters.COMMAND, piece_type)],
            SIZE: [MessageHandler(filters.TEXT & ~filters.COMMAND, size)],
            PRICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, price)],
            PURCHASE_INFO: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, purchase_info)
            ],
            DESCRIPTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, description)],
            FLAWS: [MessageHandler(filters.TEXT & ~filters.COMMAND, flaws)],
            CERTIFICATIONS: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, certifications)
            ],
            DEALING: [MessageHandler(filters.TEXT & ~filters.COMMAND, dealing)],
            PHOTOS: [
                MessageHandler(filters.PHOTO, handle_photo),
                CommandHandler("done", done_photos),
                MessageHandler(
                    filters.ALL & ~filters.PHOTO & ~filters.COMMAND,
                    invalid_photo_input,
                ),
            ],
            VIDEO: [
                MessageHandler(filters.VIDEO, handle_video),
                CommandHandler("skip", skip_video),
                MessageHandler(
                    filters.ALL & ~filters.VIDEO & ~filters.COMMAND,
                    invalid_video_input,
                ),
            ],
            CONFIRM: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, confirm),
            ],
            REMOVE_POST_LINK: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, remove_post_link),
            ],
            REMOVE_SUBMISSION_CODE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, remove_submission_code),
            ],
            REMOVE_CONFIRM: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, remove_confirm),
            ],
        },
        fallbacks=[
            CommandHandler("cancel", cancel),
            CommandHandler("start", start),
        ],
        allow_reentry=True,
    )

    app.add_handler(conv_handler)

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
