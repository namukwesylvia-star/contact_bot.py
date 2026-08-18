# بوت التواصل - عبس

بوت تيليجرام يستقبل طلبات التواصل من المستخدمين ويرسلها مباشرة إليك.

## الملفات

| الملف | الوظيفة |
|---|---|
| `contact_bot.py` | كود البوت الرئيسي |
| `requirements.txt` | المكتبات المطلوبة |
| `Procfile` | يخبر السيرفر كيف يشغّل البوت |

---

## الخطوة 1: احصل على التوكن (BOT_TOKEN)

1. افتح تيليجرام وابحث عن `@BotFather`
2. أرسل `/newbot` واتبع التعليمات (اسم البوت + يوزر ينتهي بـ `bot`)
3. راح يعطيك توكن شكله مثل:
   `123456789:AAExxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
4. احتفظ فيه — هذا سرّي، ما تشاركه مع أحد

## الخطوة 2: احصل على ADMIN_CHAT_ID (رقمك الشخصي)

1. ابحث عن `@userinfobot` بتيليجرام
2. اضغط `/start`
3. راح يعطيك رقم `Id:` — هذا رقمك، احتفظ فيه

---

## الخطوة 3: النشر على Railway (مجاني - الأسهل)

1. أنشئ حساب على [railway.app](https://railway.app) (تقدر تسجل بحساب GitHub)
2. أنشئ مستودع (Repository) جديد على GitHub وارفع فيه 3 ملفات:
   - `contact_bot.py`
   - `requirements.txt`
   - `Procfile`
3. بـ Railway: اضغط **New Project** → **Deploy from GitHub repo** → اختر المستودع
4. من تبويب **Variables** بالمشروع، أضف:
   - `BOT_TOKEN` = التوكن اللي أخذته من BotFather
   - `ADMIN_CHAT_ID` = رقمك اللي أخذته من userinfobot
   - `OWNER_NAME` = عبس
5. Railway راح يبني وينشر المشروع تلقائياً خلال دقائق
6. من تبويب **Deployments** تقدر تتابع اللوق (logs) وتتأكد إنه ظاهر:
   `✅ البوت يعمل الآن...`

بعدها البوت يشتغل 24/7 حتى لو جهازك مطفي.

---

## بديل: التشغيل محلياً (للتجربة فقط)

```bash
pip install -r requirements.txt --break-system-packages

# على Windows (Command Prompt):
set BOT_TOKEN=التوكن_هنا
set ADMIN_CHAT_ID=رقمك_هنا
python contact_bot.py

# على macOS/Linux:
export BOT_TOKEN=التوكن_هنا
export ADMIN_CHAT_ID=رقمك_هنا
python3 contact_bot.py
```

⚠️ لازم الجهاز يضل مفتوح ومتصل بالنت طول فترة التشغيل.

---

## ملاحظات أمان مهمة

- **لا ترفع التوكن مباشرة بالكود** لو المستودع (repo) عام (Public) — استخدم متغيرات البيئة دائماً كما هو موضح فوق
- إذا سرّب التوكن بالغلط، روح لـ BotFather وأرسل `/revoke` لإلغائه وأخذ توكن جديد فوراً
- تقدر تخلي المستودع **Private** بـ GitHub لحماية إضافية
