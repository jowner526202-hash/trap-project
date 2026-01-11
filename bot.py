import os
import base64
import requests
import platform
import psutil
from flask import Flask
from threading import Thread
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

# --- نظام البقاء حياً لاستضافة Render ---
server = Flask('')

@server.route('/')
def home():
    return "The Bot is Running 24/7"

def run():
    server.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- إعدادات المطور أحمد ---
ENCODED_TOKEN = "ODI4MDkzOTI5MTpBQUZfZFR1MThEMGVkSlBPWVB6d3NQaVNfRFFlTW9uSEFRYw=="
DEV_NAME = "Ahmed"

def get_token():
    return base64.b64decode(ENCODED_TOKEN).decode('utf-8')

def get_ip_details():
    try:
        return requests.get('https://ipapi.co/json/').json()
    except: return {}

# --- دوال البوت ---
def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("📸 سحب الكاميرا", callback_data='cam'),
         InlineKeyboardButton("🌐 عنوان IP", callback_data='ip')],
        [InlineKeyboardButton("📱 بيانات الجهاز", callback_data='sys'),
         InlineKeyboardButton("📍 موقع الضحية", callback_data='loc')],
        [InlineKeyboardButton("🔗 رابط الاختراق", callback_data='link')],
        [InlineKeyboardButton("🎤 تسجيل الصوت", callback_data='audio'),
         InlineKeyboardButton("🖼️ سحب الاستوديو", callback_data='gallery')],
        [InlineKeyboardButton("📞 جهات الاتصال", callback_data='contacts'),
         InlineKeyboardButton("⌨️ Keylogger", callback_data='key')],
        [InlineKeyboardButton("💥 هجوم DDoS", callback_data='ddos'),
         InlineKeyboardButton("🔐 Ransomware", callback_data='ransom')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        f"💀 **لوحة التحكم المركزية - المطور {DEV_NAME}**\n"
        f"الحالة: متصل وسري للغاية 🛡️",
        reply_markup=reply_markup, parse_mode='Markdown'
    )

def handle_actions(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    data = get_ip_details()
    
    responses = {
        'ip': f"🌐 IP: `{data.get('ip')}`\nمزود الخدمة: {data.get('org')}",
        'sys': f"💻 OS: {platform.system()}\n🔋 Bat: {psutil.sensors_battery().percent if psutil.sensors_battery() else 'N/A'}%",
        'loc': f"📍 الموقع: {data.get('city')}, {data.get('country')}\n🔗 Maps: https://www.google.com/maps?q={data.get('latitude')},{data.get('longitude')}",
        'link': f"⚠️ أرسل هذا الرابط للضحية سيدي {DEV_NAME}:\n`https://secure-login-v4.net/auth`",
        'cam': "🚀 جاري تشغيل سيرفر استقبال الصور...",
        'audio': "🎧 ميكروفون الضحية قيد التنصت...",
        'gallery': "🖼️ يتم الآن ضغط ملفات الاستوديو وسحبها...",
        'contacts': "📞 تم البدء بسحب قائمة الأسماء...",
        'key': "⌨️ الـ Keylogger يعمل.. سيتم إرسال كل حرف يتم كتابته.",
        'ddos': "💥 حدد الهدف سيدي للبدء بالإغراق..",
        'ransom': "🔐 تحذير: سيتم تشفير كافة الملفات بلاحقة .Crypted"
    }
    
    res_text = responses.get(query.data, "خطأ في الأمر")
    query.edit_message_text(f"{res_text}\n\nبواسطة: {DEV_NAME}", parse_mode='Markdown')

def main():
    keep_alive() # تشغيل السيرفر الوهمي
    updater = Updater(get_token())
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(handle_actions))
    
    print(f"Master {DEV_NAME}, I am online.")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
