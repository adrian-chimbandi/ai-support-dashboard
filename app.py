import streamlit as st
from analysis.ticket_analysis import load_tickets, enrich_tickets, find_automation_candidates
from visuals.charts import category_pie, sentiment_bar, volume_over_time, automation_bar

st.set_page_config(page_title="Support Intelligence", layout="wide", page_icon="🎫")
st.title("🎫 AI Support Ticket Intelligence")

page = st.sidebar.radio("Navigate", [
    "📊 Overview",
    "💬 Sentiment Analysis",
    "⚡ Automation Opportunities"
])

@st.cache_data
def get_data():
    df = load_tickets('data/support_tickets.csv')
    return enrich_tickets(df)

df = get_data()

if page == "📊 Overview":
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Tickets", len(df))
    c2.metric("Frustrated", (df['sentiment'] == 'frustrated').sum())
    c3.metric("Urgent", df['is_urgent'].sum())
    c4.metric("Top Issue", df['category'].mode()[0])
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(category_pie(df), use_container_width=True)
    with col2:
        st.plotly_chart(sentiment_bar(df), use_container_width=True)
    st.plotly_chart(volume_over_time(df), use_container_width=True)
    st.subheader("All tickets")
    st.dataframe(df, use_container_width=True)

elif page == "💬 Sentiment Analysis":
    st.header("Sentiment analysis")
    frustrated = df[df['sentiment'] == 'frustrated']
    pct = round(len(frustrated) / len(df) * 100, 1)
    if pct > 30:
        st.error(f"⚠️ {pct}% of customers are frustrated — above threshold")
    else:
        st.success(f"✅ {pct}% frustrated — within normal range")
    st.subheader("🔴 Frustrated customers — prioritise these")
    st.dataframe(frustrated[['ticket_id', 'customer_name', 'message', 'date']], use_container_width=True)
    st.subheader("All tickets by sentiment")
    st.plotly_chart(sentiment_bar(df), use_container_width=True)

elif page == "⚡ Automation Opportunities":
    st.header("Automation opportunity analysis")
    candidates = find_automation_candidates(df)
    top = candidates.iloc[0]
    st.info(
        f"💡 Top automation candidate: **{top['category']}**\n\n"
        f"{top['count']} tickets ({top['percentage']}% of volume). "
        f"Automating with a chatbot FAQ could significantly reduce agent workload."
    )
    st.plotly_chart(automation_bar(candidates), use_container_width=True)
    st.dataframe(candidates, use_container_width=True)