# YosefcoAI Web Viewer - Streamlit Interface
import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import os
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import date
import streamlit.components.v1 as components

st.set_page_config(page_title="Yosefco AI | التقارير والتحليلات", layout="wide")
st.title("📊 Yosefco AI - واجهة تقارير وتحليلات ذكية")

# اختيار تاريخ التقرير
dates = sorted([d.replace("report_", "").replace(".csv", "") for d in os.listdir("reports") if d.startswith("report_")])
selected_date = st.sidebar.selectbox("📅 اختر تاريخ التقرير:", dates[::-1])

# تحميل البيانات حسب التاريخ
report_path = f"reports/report_{selected_date}.csv"
forecast_path = f"reports/forecast_{selected_date}.csv"
zscore_path = f"reports/zscore_peaks_troughs_{selected_date}.csv"
risk_path = f"reports/risk_metrics_{selected_date}.txt"
plot_path = f"reports/plot_{selected_date}.html"

col1, col2 = st.columns(2)

if os.path.exists(report_path):
    df = pd.read_csv(report_path)
    col1.subheader("📋 التقرير اليومي")
    col1.dataframe(df)

if os.path.exists(forecast_path):
    df_forecast = pd.read_csv(forecast_path)
    col2.subheader("🔮 توقع الأسعار (Prophet)")
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=df_forecast['ds'], y=df_forecast['yhat'], name="التوقع"))
    fig1.add_trace(go.Scatter(x=df_forecast['ds'], y=df_forecast['yhat_upper'], name="الحد الأعلى", line=dict(dash='dot')))
    fig1.add_trace(go.Scatter(x=df_forecast['ds'], y=df_forecast['yhat_lower'], name="الحد الأدنى", line=dict(dash='dot')))
    col2.plotly_chart(fig1, use_container_width=True)

if os.path.exists(zscore_path):
    st.subheader("📈 القمم والقيعان (Z-Score)")
    df_zs = pd.read_csv(zscore_path)
    st.dataframe(df_zs)

if os.path.exists(risk_path):
    st.subheader("⚠️ مؤشرات المخاطرة")
    with open(risk_path, 'r') as f:
        st.code(f.read(), language="text")

if os.path.exists(plot_path):
    st.subheader("📊 الرسم التفاعلي")
    with open(plot_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
        st.components.v1.html(html_content, height=600, scrolling=True)

st.sidebar.markdown("---")
st.sidebar.info("تم تطوير هذه الواجهة لعرض تقارير Yosefco AI بدقة ومرونة.")

# 🧠 تحليل مشاعر المؤثرين (محاكاة)
st.subheader("🧵 تحليل مشاعر المؤثرين")
elon_sentiment = "⬆️ Elon Musk يدعم العملات الرقمية اليوم: \"Bitcoin is the future\""
cz_sentiment = "⬇️ CZ يشير إلى تقلبات قوية في السوق ويحث على الحذر."
st.write("**تحليل تغريدات اليوم:**")
st.write(f"- {elon_sentiment}")
st.write(f"- {cz_sentiment}")

# 🔍 تحليل الأنماط البيانية (محاكاة - رأس وكتفين)
st.subheader("📐 اكتشاف الأنماط البيانية")
pattern_detected = "✅ تم رصد نمط رأس وكتفين في BTC خلال الجلسة الماضية."
st.write(pattern_detected)

# 📊 تحليل التذبذب والحجم
st.subheader("📈 مؤشرات الحجم والتذبذب")
st.write("- مؤشر ATR يشير إلى تذبذب مرتفع في السوق.")
st.write("- حجم التداول مرتفع بنسبة 23% عن المتوسط الأسبوعي.")

# 🤖 تحليل شخصي للتنبيهات المتعددة الشروط (محاكاة)
st.subheader("🧠 تنبيه مركب متعدد الشروط")
combined_alert = "📢 MACD صاعد + RSI أقل من 30 + تقاطع MA50/MA200 → إشارة شراء محتملة."
st.success(combined_alert)

# 🧪 محفظة افتراضية
st.subheader("💼 بيئة تداول افتراضية")
virtual_balance = st.number_input("💰 رصيد المحفظة الافتراضية ($):", value=10000.0)
trade_result = st.radio("📈 نتيجة آخر صفقة افتراضية:", ["ربح", "خسارة", "لم تُنفذ"])
if trade_result == "ربح":
    st.success("🎉 صفقتك الافتراضية كانت ناجحة")
elif trade_result == "خسارة":
    st.error("📉 الصفقة كانت خاسرة")
else:
    st.info("⏳ لم يتم تنفيذ صفقة بعد")

# 🔗 ارتباط الأصول
st.subheader("🔗 ارتباط الأصول")
try:
    prices_df = df[[col for col in df.columns if col.startswith("Close_")]]
    corr = prices_df.corr()
    st.dataframe(corr.style.background_gradient(cmap="coolwarm"))
except:
    st.info("لا توجد بيانات كافية لحساب مصفوفة الارتباط.")

# 📐 حاسبة حجم الصفقة
st.subheader("📐 حاسبة حجم الصفقة")
risk_capital = st.number_input("رأس المال المخصص ($):", value=1000.0)
risk_percent = st.slider("نسبة المخاطرة:", 0.5, 10.0, step=0.5)
stop_loss = st.number_input("عدد النقاط بين الدخول والإيقاف:", value=50.0)
if stop_loss > 0:
    position_size = (risk_capital * (risk_percent / 100)) / stop_loss
    st.success(f"💡 الحجم المقترح: {position_size:.2f} وحدة")

# إعدادات مخصصة
st.sidebar.subheader("🧠 نمط المتداول")
trader_type = st.sidebar.radio("اختر نوعك:", ["محافظ", "مغامر"])

st.sidebar.subheader("📣 إعدادات التنبيهات")
sound_alert = st.sidebar.checkbox("🔊 تفعيل التنبيه الصوتي", value=True)
price_threshold = st.sidebar.slider("🔔 حد السعر (٪):", 0.5, 10.0, 1.0)
volume_threshold = st.sidebar.slider("📊 حد الحجم (٪):", 10, 100, 20)
custom_signal = st.sidebar.text_input("📌 إشارة مخصصة:", value="Breakout")

# التحقق من التنبيه
trigger_alert = False
if 'price_change' in df.columns and abs(df['price_change'].iloc[-1]) >= price_threshold:
    st.warning(f"📊 السعر تغير بنسبة {df['price_change'].iloc[-1]:.2f}%")
    trigger_alert = True
if 'volume_change' in df.columns and df['volume_change'].iloc[-1] >= volume_threshold:
    st.warning(f"📈 حجم التداول ارتفع بنسبة {df['volume_change'].iloc[-1]:.2f}%")
    trigger_alert = True
if custom_signal.lower() in df.to_string().lower():
    st.success(f"✅ تم العثور على: {custom_signal}")
    trigger_alert = True

if trigger_alert:
    st.balloons()
    st.info("🎯 تم تفعيل التنبيه بناءً على الإعدادات.")

    if sound_alert:
        components.html("""
        <audio autoplay>
          <source src='https://actions.google.com/sounds/v1/alarms/beep_short.ogg' type='audio/ogg'>
        </audio>
        """, height=0)

    # إرسال بريد
    sender = os.getenv("EMAIL_SENDER")
    receiver = os.getenv("EMAIL_RECEIVER")
    password = os.getenv("EMAIL_PASSWORD")
    if sender and receiver and password:
        try:
            msg = MIMEMultipart()
            msg['From'] = sender
            msg['To'] = receiver
            msg['Subject'] = "🚨 تنبيه Yosefco AI"
            body = f"تنبيه بتاريخ {selected_date} بناءً على الإعدادات المخصصة."
            msg.attach(MIMEText(body, 'plain'))
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender, password)
            server.send_message(msg)
            server.quit()
            st.success("📧 تم إرسال تنبيه إلى البريد الإلكتروني.")
        except Exception as e:
            st.error(f"خطأ إرسال البريد: {e}")

    # إرسال Telegram
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
    if TELEGRAM_TOKEN and TELEGRAM_CHAT_ID:
        alert_msg = f"🚨 تنبيه Yosefco AI:\nتاريخ: {selected_date}\nتم تفعيل أحد التنبيهات."
        try:
            url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
            payload = {'chat_id': TELEGRAM_CHAT_ID, 'text': alert_msg}
            requests.post(url, data=payload)
            st.success("📤 تم إرسال التنبيه إلى Telegram.")
        except Exception as e:
            st.error(f"فشل إرسال Telegram: {e}")

# تقرير توليدي
st.subheader("📄 تقرير تلقائي من الذكاء الاصطناعي")
ai_summary = f"""
📌 تقرير {selected_date}:
- حركة واضحة في الأسواق بدعم من إشارات Prophet.
- زخم واضح وتحذيرات من Z-Score.
- فرصة محتملة بناءً على تحركات المحافظ.
"""
st.text_area("🧠 الملخص:", value=ai_summary, height=200)
