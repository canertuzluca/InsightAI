import streamlit as st
import pandas as pd

from app.graph.workflow import graph


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="InsightAI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 0;
    }

    .subtitle {
        font-size: 17px;
        color: #888;
        margin-top: 0;
        margin-bottom: 25px;
    }

    .kpi-card {
        padding: 18px;
        border-radius: 12px;
        border: 1px solid rgba(128,128,128,0.25);
        background-color: rgba(128,128,128,0.05);
        text-align: center;
        min-height: 120px;
    }

    .kpi-title {
        font-size: 14px;
        color: #888;
        margin-bottom: 8px;
    }

    .kpi-value {
        font-size: 26px;
        font-weight: 700;
    }

    .tool-card {
        padding: 10px 14px;
        border-radius: 8px;
        margin-bottom: 8px;
        border: 1px solid rgba(128,128,128,0.2);
    }

    .architecture-box {
        padding: 15px;
        border-radius: 10px;
        border: 1px solid rgba(128,128,128,0.2);
        background-color: rgba(128,128,128,0.04);
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "last_result" not in st.session_state:
    st.session_state.last_result = None


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## 🤖 InsightAI")

    st.caption("Enterprise Multi-Agent AI Assistant")

    st.divider()

    st.markdown("### 🧠 Capabilities")

    st.markdown(
        """
        - 🔎 **RAG Document Search**
        - 🗄️ **SQL Database Querying**
        - 📊 **Business Analytics**
        - 🔄 **Agent Orchestration**
        - 🛡️ **Self Validation**
        """
    )

    st.divider()

    st.markdown("### 🏗️ Architecture")

    st.markdown(
        """
        <div class="architecture-box">

        <b>Router Agent</b>

        ↓

        <b>SQL / RAG</b>

        ↓

        <b>Orchestrator</b>

        ↓

        <b>Analytics</b>

        ↓

        <b>Response Generator</b>

        ↓

        <b>Validation</b>

        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    st.markdown("### 📌 Example Questions")

    st.markdown(
        """
        **RAG**

        Çalışanların yıllık ücretli izin hakkı kaç gün?

        **SQL**

        Caner Tuzluca hangi departmanda çalışıyor?

        **Analytics**

        IT departmanının satış performansı nedir?

        **Multi-Agent**

        Caner Tuzluca hangi departmanda çalışıyor ve
        bu departmanın satış performansı nedir?
        """
    )

    st.divider()

    if st.button("🗑️ Sohbeti Temizle", use_container_width=True):

        st.session_state.messages = []
        st.session_state.last_result = None

        st.rerun()


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🤖 InsightAI</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">'
    'Enterprise Multi-Agent AI Assistant'
    '</div>',
    unsafe_allow_html=True,
)


# ============================================================
# WELCOME
# ============================================================

if not st.session_state.messages:

    st.info(
        "👋 Merhaba! Şirket verileri, çalışanlar, "
        "dokümanlar ve satış performansı hakkında "
        "sorularınızı sorabilirsiniz."
    )


# ============================================================
# PREVIOUS MESSAGES
# ============================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# ============================================================
# ANALYTICS DASHBOARD
# ============================================================

def render_analytics_dashboard(result):

    if not result:
        return

    history = result.get("tool_history", [])

    analytics_result = None

    for item in history:

        if (
            getattr(item, "tool", None) == "ANALYTICS"
            and getattr(item, "success", False)
            and isinstance(getattr(item, "result", None), dict)
        ):

            analytics_result = item.result

    if not analytics_result:
        return

    department = analytics_result.get(
        "department",
        "Bilinmiyor"
    )

    total_sales = analytics_result.get(
        "total_sales"
    )

    total_revenue = analytics_result.get(
        "total_revenue"
    )

    total_quantity = analytics_result.get(
        "total_quantity"
    )

    average_sale = analytics_result.get(
        "average_sale"
    )

    growth = analytics_result.get(
        "growth_percentage"
    )

    highest_month = analytics_result.get(
        "highest_month"
    )

    highest_month_revenue = analytics_result.get(
        "highest_month_revenue"
    )

    monthly_sales = analytics_result.get(
        "monthly_sales"
    )

    st.divider()

    st.markdown(
        f"### 📊 {department} Departmanı — Analytics Dashboard"
    )

    # --------------------------------------------------------
    # KPI CARDS
    # --------------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">Toplam Gelir</div>
                <div class="kpi-value">
                    {total_revenue:,.2f} TL
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:

        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">Toplam Satış</div>
                <div class="kpi-value">
                    {total_sales:,}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:

        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">Ortalama Satış</div>
                <div class="kpi-value">
                    {average_sale:,.2f} TL
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col4:

        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">Büyüme</div>
                <div class="kpi-value">
                    {growth:.2f}%
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("")

    # --------------------------------------------------------
    # SECONDARY INFORMATION
    # --------------------------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Toplam Ürün Miktarı",
            f"{total_quantity:,}"
        )

    with col2:

        if highest_month:

            st.metric(
                "En Yüksek Gelir",
                f"{highest_month_revenue:,.2f} TL"
            )

            st.caption(
                f"Ay: {highest_month}"
            )

    with col3:

        st.metric(
            "Departman",
            department
        )

    # --------------------------------------------------------
    # MONTHLY SALES CHART
    # --------------------------------------------------------

    if monthly_sales:

        st.markdown("#### 📈 Aylık Gelir Trendi")

        chart_data = pd.DataFrame(
            {
                "Tarih": list(monthly_sales.keys()),
                "Gelir": list(monthly_sales.values()),
            }
        )

        chart_data["Tarih"] = pd.to_datetime(
            chart_data["Tarih"]
        )

        chart_data = chart_data.set_index("Tarih")

        st.line_chart(
            chart_data,
            use_container_width=True,
        )


# ============================================================
# AGENT EXECUTION PANEL
# ============================================================

def render_agent_execution(result):

    if not result:
        return

    history = result.get(
        "tool_history",
        []
    )

    if not history:
        return

    with st.expander(
        "🔍 Agent Execution & Validation",
        expanded=False,
    ):

        st.markdown("### 🔄 Tool Execution")

        for index, item in enumerate(history, start=1):

            tool = getattr(
                item,
                "tool",
                "UNKNOWN"
            )

            success = getattr(
                item,
                "success",
                False
            )

            if success:

                icon = "✅"

                status = "Başarılı"

            else:

                icon = "❌"

                status = "Başarısız"

            st.markdown(
                f"""
                <div class="tool-card">
                    <b>{index}. {icon} {tool}</b>
                    <br>
                    <small>{status}</small>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("### 🛡️ Validation")

        validation_status = result.get(
            "validation_status"
        )

        if validation_status == "PASSED":

            st.success(
                "Validation: PASS — "
                "Üretilen cevap tool sonuçlarıyla doğrulandı."
            )

        elif validation_status == "FAILED":

            st.error(
                "Validation: FAILED"
            )

        else:

            st.info(
                "Validation sonucu bulunamadı."
            )


# ============================================================
# CHAT INPUT
# ============================================================

question = st.chat_input(
    "InsightAI'ye bir soru sorun..."
)


# ============================================================
# PROCESS QUESTION
# ============================================================

if question:

    # --------------------------------------------------------
    # USER MESSAGE
    # --------------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    with st.chat_message("user"):

        st.markdown(question)

    # --------------------------------------------------------
    # AGENT
    # --------------------------------------------------------

    with st.chat_message("assistant"):

        with st.spinner(
            "InsightAI düşünüyor..."
        ):

            try:

                result = graph.invoke(
                    {
                        "question": question,
                        "tool_history": [],
                        "iteration": 0,
                    }
                )

                st.session_state.last_result = result

                answer = result.get(
                    "final_answer",
                    "Üzgünüm, bir cevap oluşturulamadı.",
                )

                st.markdown(answer)

                # Agent execution
                render_agent_execution(
                    result
                )

                # Analytics dashboard
                render_analytics_dashboard(
                    result
                )

            except Exception as e:

                answer = (
                    "Bir hata oluştu: "
                    f"{str(e)}"
                )

                st.error(answer)

                result = None

                st.session_state.last_result = None

    # --------------------------------------------------------
    # SAVE ASSISTANT MESSAGE
    # --------------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
        }
    )
