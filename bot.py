from PIL import Image
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters

import os
TOKEN = os.getenv("BOT_TOKEN")


LOGO_PATH = "logo.png"

def add_logo(photo_path, out_path):
    base = Image.open(photo_path).convert("RGBA")
    logo = Image.open(LOGO_PATH).convert("RGBA")

    bw, bh = base.size
    logo_w = int(bw * 0.35)
    logo_h = int(logo.size[1] * logo_w / logo.size[0])
    logo = logo.resize((logo_w, logo_h))

    x = bw - logo_w - 30
    y = bh - logo_h - 30

    base.alpha_composite(logo, (x, y))
    base.convert("RGB").save(out_path, "JPEG", quality=95)

async def on_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo[-1]
    file = await context.bot.get_file(photo.file_id)

    input_path = "input.jpg"
    output_path = "output.jpg"

    await file.download_to_drive(input_path)
    add_logo(input_path, output_path)

    await update.message.reply_photo(photo=open(output_path, "rb"))

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.PHOTO, on_photo))
    app.run_polling()

if __name__ == "__main__":
    main()
