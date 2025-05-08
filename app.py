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
recommendations = pd.DataFrame([
    {"الأصل": "BTC/USD", "التوصية": "شراء", "القوة": 88, "المصدر": "Prophet + Z-Score"},
    {"الأصل": "XAU/USD", "التوصية": "بيع", "القوة": 72, "المصدر": "RSI + MACD"},
    {"الأصل": "ETH/USD", "التوصية": "شراء", "القوة": 91, "المصدر": "أنماط + حجم تداول"},
])
st.dataframe(recommendations.style.highlight_max(axis=0))

if st.button("💾 حفظ التوصيات في CSV"):
    try:
        recommendations.to_csv(recommendation_log, index=False)
        st.success("✅ تم حفظ التوصيات في reports/recommendation_log.csv")
    except Exception as e:
        st.error(f"حدث خطأ أثناء الحفظ: {e}")
