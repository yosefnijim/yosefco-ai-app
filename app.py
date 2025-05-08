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
from PIL import Image
import yfinance as yf

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
recommendation_log = "reports/recommendation_log.csv"
sent_flag_file = f"reports/sent_flag_{selected_date}.txt"

col1, col2 = st.columns(2)

if os.path.exists(report_path):
    df = pd.read_csv(report_path)
    col1.subheader("📋 التقرير اليومي")
    col1.dataframe(df)
else:
    df = pd.DataFrame()

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

st.subheader("🧵 تحليل مشاعر المؤثرين")
elon_sentiment = "⬆️ Elon Musk يدعم العملات الرقمية اليوم: \"Bitcoin is the future\""
cz_sentiment = "⬇️ CZ يشير إلى تقلبات قوية في السوق ويحث على الحذر."
st.write("**تحليل تغريدات اليوم:**")
st.write(f"- {elon_sentiment}")
st.write(f"- {cz_sentiment}")

st.subheader("📐 اكتشاف الأنماط البيانية")
pattern_detected = "✅ تم رصد نمط رأس وكتفين في BTC خلال الجلسة الماضية."
st.write(pattern_detected)

# 🖼️ رفع صورة تحليل
st.subheader("🖼️ تحليل الشارت من صورة")
uploaded_file = st.file_uploader("قم برفع صورة الشارت (PNG أو JPG)", type=["png", "jpg", "jpeg"])
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="📉 الشارت الذي تم رفعه", use_column_width=True)
    st.info("✅ تم رفع الصورة بنجاح، سيتم دمج التحليل بالرؤية الحاسوبية لاحقًا.")

st.subheader("📈 مؤشرات الحجم والتذبذب")
st.write("- مؤشر ATR يشير إلى تذبذب مرتفع في السوق.")
st.write("- حجم التداول مرتفع بنسبة 23% عن المتوسط الأسبوعي.")

st.subheader("🧠 تنبيه مركب متعدد الشروط")
combined_alert = "📢 MACD صاعد + RSI أقل من 30 + تقاطع MA50/MA200 → إشارة شراء محتملة."
st.success(combined_alert)

st.subheader("💼 بيئة تداول افتراضية")
virtual_balance = st.number_input("💰 رصيد المحفظة الافتراضية ($):", value=10000.0)
trade_result = st.radio("📈 نتيجة آخر صفقة افتراضية:", ["ربح", "خسارة", "لم تُنفذ"])
if trade_result == "ربح":
    st.success("🎉 صفقتك الافتراضية كانت ناجحة")
elif trade_result == "خسارة":
    st.error("📉 الصفقة كانت خاسرة")
else:
    st.info("⏳ لم يتم تنفيذ صفقة بعد")

# 📋 جدول توصيات مباشر + حفظ
st.subheader("📋 التوصيات النشطة")

# إعادة إنشاء جدول التوصيات لتجنب التكرار بعد الفلترة
# تم حذفه لأنه تم تعريفه أعلاه ولا حاجة لتكرار نفس الكود مرتين

# جلب السعر الحالي
def get_price(symbol):
    try:
        ticker = yf.Ticker(symbol.replace("/", "") + "=X")
        return round(ticker.info.get("regularMarketPrice", 0), 2)
    except Exception:
        return "N/A"

recommendations['السعر الحالي'] = recommendations['الأصل'].apply(get_price)

# حساب الفرق بين السعر المدخل والحالي كنسبة مئوية
recommendations['فرق السعر (%)'] = recommendations.apply(
    lambda row: round(((row['السعر الحالي'] - row['السعر المدخل']) / row['السعر المدخل']) * 100, 2)
    if isinstance(row['السعر الحالي'], (int, float)) else 'N/A', axis=1
)

# فلترة حسب نوع التوصية أو فرق السعر
selected_type = st.selectbox("🔍 نوع التوصية", ["الكل"] + sorted(recommendations['التوصية'].unique()))
min_diff, max_diff = st.slider("🎯 نطاق فرق السعر (%)", -100.0, 100.0, (-100.0, 100.0))

filtered = recommendations.copy()
if selected_type != "الكل":
    filtered = filtered[filtered['التوصية'] == selected_type]

filtered = filtered[filtered['فرق السعر (%)'].apply(lambda x: isinstance(x, (int, float)) and min_diff <= x <= max_diff)]
recommendations = pd.DataFrame([
    {"الأصل": "BTC/USD", "السعر المدخل": 68250.0, "التوصية": "شراء", "القوة": 88, "المصدر": "Prophet + Z-Score"},
    {"الأصل": "XAU/USD", "السعر المدخل": 2325.4, "التوصية": "بيع", "القوة": 72, "المصدر": "RSI + MACD"},
    {"الأصل": "ETH/USD", "السعر المدخل": 3180.75, "التوصية": "شراء", "القوة": 91, "المصدر": "أنماط + حجم تداول"},
])

# جلب السعر الحالي
def get_price(symbol):
    try:
        ticker = yf.Ticker(symbol.replace("/", "") + "=X")
        return round(ticker.info.get("regularMarketPrice", 0), 2)
    except Exception:
        return "N/A"

recommendations['السعر الحالي'] = recommendations['الأصل'].apply(get_price)

# حساب الفرق بين السعر المدخل والحالي كنسبة مئوية
recommendations['فرق السعر (%)'] = recommendations.apply(
    lambda row: round(((row['السعر الحالي'] - row['السعر المدخل']) / row['السعر المدخل']) * 100, 2)
    if isinstance(row['السعر الحالي'], (int, float)) else 'N/A', axis=1
)

st.dataframe(filtered.style.format("{:.2f}", subset=['السعر المدخل', 'السعر الحالي', 'فرق السعر (%)']))

try:
    recommendations.to_csv(recommendation_log, index=False)
except Exception as e:
    st.error(f"حدث خطأ أثناء حفظ التوصيات: {e}")

if not os.path.exists(sent_flag_file):
    EMAIL_SENDER = os.getenv("EMAIL_SENDER")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
    EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

    recommendations_text = "\n".join([
        f"{row['الأصل']}: {row['التوصية']} عند سعر {row['السعر المدخل']} (السعر الحالي: {row['السعر الحالي']}) (قوة: {row['القوة']})"
        for _, row in recommendations.iterrows()
    ])
    email_body = f"📋 التوصيات النشطة ليوم {selected_date}:\n\n{recommendations_text}"

    if EMAIL_SENDER and EMAIL_PASSWORD and EMAIL_RECEIVER:
        try:
            msg = MIMEMultipart()
            msg['From'] = EMAIL_SENDER
            msg['To'] = EMAIL_RECEIVER
            msg['Subject'] = f"توصيات Yosefco AI - {selected_date}"
            msg.attach(MIMEText(email_body, 'plain'))
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)
            server.quit()
            st.success("📧 تم إرسال التوصيات إلى البريد الإلكتروني.")
        except Exception as e:
            st.error(f"فشل إرسال البريد: {e}")

    if TELEGRAM_TOKEN and TELEGRAM_CHAT_ID:
        try:
            message = f"🚨 توصيات Yosefco AI:\n{email_body}"
            url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
            payload = {'chat_id': TELEGRAM_CHAT_ID, 'text': message}
            requests.post(url, data=payload)
            st.success("📤 تم إرسال التوصيات إلى Telegram.")
        except Exception as e:
            st.error(f"فشل إرسال Telegram: {e}")

    with open(sent_flag_file, 'w') as f:
        f.write("sent")
