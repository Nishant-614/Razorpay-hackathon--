import streamlit as st
import pandas as pd
import numpy as np
import datetime
import os
import plotly.express as px
import plotly.graph_objects as go
from finance_controller_agent_v3 import FinanceControllerAgent

# Set page layout to wide and add title
st.set_page_config(page_title="FinOps Copilot - AI Finance Controller", layout="wide", page_icon="🤖")

# ── Dynamic Mascot Image Path & Fallback URL Resolver ──

MASCOT_URLS = {
    "mascot_happy.png": "https://lh3.googleusercontent.com/notebooklm/AKYWMX85DL1gbP7C9h2CZKOTRcVLKiTe-Ca8yf6Ao5qATQ5gpKe4njIAgpd8b0UAIRghNASlIhf5P1d8lHiUbP8-ssR0aGs_6vqJE4lCb97kc-vkD6Y0IMxNOgI0p-hkW83gIMiSvnGjR6WZBslwe6xnUo2cidUeVw",
    "mascot_neutral.png": "https://lh3.googleusercontent.com/notebooklm/AKYWMX-pOoEGtX1JWXNoRzswj6sdRrS7fGq2I3SaVktg1ZbUDXTDwRckJyjScH7lzajcNw4UktilyKszvPm_L27Kh25YlWXeAAyaUrYRs-o701d03KAFerB91LjcJxLiXzaIOnRbFikMcaXV-7AfEvrRHFJ0mkw6F-c",
    "mascot_panic.png": "https://lh3.googleusercontent.com/notebooklm/AKYWMX-VRV_eUCK4esxHL2jkLLRjOYnrU63mxqj4c_s3YOPErWMintfih7ZhZr1jmUg2dpfVOcl7ICMQsbPlVTOmjK-OkbwPMvvXtwxyOvPcdYSyEu5w1PSqyQbTt_3JHFw_GcZoV-n5nMI1qbsKXXuNaMoqx39_sA8"
}

def get_mascot_image(filename):
    """Robust image locator: 1. Local folder, 2. Workspace directory, 3. Cloud serving URL fallback"""
    if os.path.exists(filename):
        return filename
    workspace_path = os.path.join("/workspace/artifacts", filename)
    if os.path.exists(workspace_path):
        return workspace_path
    return MASCOT_URLS.get(filename, None)

# --- CSS Styling Injection ---
st.markdown("""
<style>
    /* Premium slate background and glowing accents */
    .stApp {
        background-color: #0F172A;
        color: #F8FAFC;
    }
    
    /* Clean custom CSS tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background-color: #1E293B;
        padding: 8px;
        border-radius: 12px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 45px;
        white-space: pre-wrap;
        background-color: #1E293B;
        border-radius: 8px;
        color: #94A3B8;
        font-weight: 600;
        border: none;
        padding: 0px 20px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #3B82F6 !important;
        color: #FFFFFF !important;
    }
    
    /* Elegant metric card styling */
    .metric-card {
        background-color: #1E293B;
        border-radius: 16px;
        padding: 24px;
        border-left: 5px solid #64748B;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
        transition: transform 0.2s;
    }
    .metric-card:hover {
        transform: translateY(-2px);
    }
    .metric-title {
        font-size: 14px;
        color: #94A3B8;
        font-weight: 600;
        text-transform: uppercase;
        margin-bottom: 8px;
    }
    .metric-value {
        font-size: 28px;
        font-weight: 700;
        color: #F1F5F9;
    }
    
    /* Conversational Mascot Speech Bubble */
    .speech-bubble {
        background-color: #1E293B;
        border: 2px solid #3B82F6;
        border-radius: 16px;
        padding: 16px;
        position: relative;
        margin-bottom: 25px;
        color: #F1F5F9;
        font-weight: 500;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.15);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .speech-bubble::after {
        content: '';
        position: absolute;
        bottom: -10px;
        left: 45px;
        border-width: 10px 10px 0;
        border-style: solid;
        border-color: #1E293B transparent;
        display: block;
        width: 0;
    }
    .speech-bubble::before {
        content: '';
        position: absolute;
        bottom: -13px;
        left: 44px;
        border-width: 11px 11px 0;
        border-style: solid;
        border-color: #3B82F6 transparent;
        display: block;
        width: 0;
    }
    
    /* Custom Chat Tab Container */
    .chat-header {
        background-color: #1E293B;
        padding: 18px;
        border-radius: 16px;
        border-bottom: 4px solid #3B82F6;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Main Title Header with gorgeous blue-green linear gradient
st.markdown("""
<h1 style='text-align: left; font-size: 38px; font-weight: 800; background: linear-gradient(90deg, #3B82F6 0%, #10B981 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 5px;'>
    💼 FinOps Copilot: Autonomous Finance Controller Agent
</h1>
<p style='color: #94A3B8; font-size: 16px; margin-bottom: 25px;'>
    Enterprise-ready verification-first ledger reconciliation, dynamic GST compliance auditing, and interactive predictive liquidity forecasting.
</p>
""", unsafe_allow_html=True)

# --- Sidebar: Batch Ingestion Hub ---
st.sidebar.markdown("""
<div style='background-color: #1E293B; padding: 15px; border-radius: 12px; margin-bottom: 20px;'>
    <h3 style='margin: 0; color: #3B82F6; font-size: 18px;'>📁 Batch Ingestion Hub</h3>
    <p style='margin: 5px 0 0 0; color: #94A3B8; font-size: 13px;'>Upload your simulated financial CSV documents here to load the matching loop.</p>
</div>
""", unsafe_allow_html=True)

uploaded_invoices = st.sidebar.file_uploader("Upload Invoices CSV", type=["csv"])
uploaded_payments = st.sidebar.file_uploader("Upload Payments CSV", type=["csv"])
uploaded_txns = st.sidebar.file_uploader("Upload Bank Transactions CSV", type=["csv"])

# Define paths (fallback to pre-generated synthetic files)
DEFAULT_INVOICES = "/workspace/artifacts/invoices.csv" if os.path.exists("/workspace/artifacts/invoices.csv") else "invoices.csv"
DEFAULT_PAYMENTS = "/workspace/artifacts/payments.csv" if os.path.exists("/workspace/artifacts/payments.csv") else "payments.csv"
DEFAULT_TXNS = "/workspace/artifacts/bank_transactions.csv" if os.path.exists("/workspace/artifacts/bank_transactions.csv") else "bank_transactions.csv"

# Resolve paths
inv_path = DEFAULT_INVOICES
pay_path = DEFAULT_PAYMENTS
txn_path = DEFAULT_TXNS

if uploaded_invoices and uploaded_payments and uploaded_txns:
    with open("temp_invoices.csv", "wb") as f:
        f.write(uploaded_invoices.getbuffer())
    with open("temp_payments.csv", "wb") as f:
        f.write(uploaded_payments.getbuffer())
    with open("temp_transactions.csv", "wb") as f:
        f.write(uploaded_txns.getbuffer())
    inv_path = "temp_invoices.csv"
    pay_path = "temp_payments.csv"
    txn_path = "temp_transactions.csv"
    st.sidebar.success("✅ Custom files configured successfully!")
else:
    st.sidebar.info("ℹ️ Running on pre-loaded synthetic datasets (100+ records) for demonstration.")

# Add manual trigger button in the sidebar to run reconciliation
st.sidebar.markdown("---")
st.sidebar.markdown("**Verification Execution Panel**")
run_reconciliation_clicked = st.sidebar.button("🚀 Run Reconciliation", use_container_width=True)

# Initialize session states
if "reconciled" not in st.session_state:
    st.session_state.reconciled = False

if run_reconciliation_clicked:
    st.cache_data.clear() # Clear cached calculations to force re-reading new file contents!
    st.session_state.reconciled = True

# --- Standby Screen ---
if not st.session_state.reconciled:
    st.info("👋 **Welcome to your Autonomous Finance Controller Agent!** Configure your uploader files in the left sidebar and click the **'Run Reconciliation'** button to kick off the ledger verification loop.")
    
    # Standby visual layout showing mascot
    col_standby_left, col_standby_right = st.columns([1, 2])
    with col_standby_left:
        neutral_img = get_mascot_image("mascot_neutral.png")
        if neutral_img:
            st.image(neutral_img, width=280)
    with col_standby_right:
        st.markdown("""
        ### Ready to Audit Your Financial Batches?
        Click **Run Reconciliation** in the sidebar to start the 5-step controller agent workflow:
        1. **Data Normalization:** Structural column header, currency, and datetime standardization.
        2. **Deterministic Matching:** High-speed reference linkage between invoices, gateways, and bank entries.
        3. **AI Fuzzy Matching:** Dynamic string similarity lookup for unstructured bank descriptions.
        4. **Tax-Line Integrity Audits:** Accurate GST tier validation (18% vs 12%).
        5. **Honest Exception Classification:** Segregation of anomalies for easy human review.
        """)
    st.stop()

# --- Initialize and Run Reconciliation Agent ---
@st.cache_data(show_spinner=False)
def run_agent_reconciliation(inv, pay, txn):
    agent = FinanceControllerAgent(inv, pay, txn)
    results, exceptions, match_rate = agent.run_reconciliation()
    forecast = agent.forward_cash_forecast()
    return agent, results, exceptions, match_rate, forecast

with st.spinner("Executing Intelligent 3-Way Reconciliation and Tax-Line Audits..."):
    agent, results_df, exceptions_df, match_rate, forecast_df = run_agent_reconciliation(inv_path, pay_path, txn_path)

# ── Dynamic Mascot Expression Evaluation ──
mascot_file = "mascot_neutral.png"
speech_text = ""
accent_border = "#64748B"

if match_rate >= 90.0:
    mascot_file = "mascot_happy.png"
    accent_border = "#10B981" # Emerald Green
    speech_text = f"✨ **Yahoo! Excellent matching health at {match_rate:.2f}%!** The ledger aligns beautifully! Let's sign off on these books."
elif match_rate >= 75.0:
    mascot_file = "mascot_neutral.png"
    accent_border = "#3B82F6" # Royal Blue
    speech_text = f"📚 **Audit complete! We hit a {match_rate:.2f}% match rate.** I isolated {len(exceptions_df)} exceptions. Let's triage them in the Chat Copilot below!"
else:
    mascot_file = "mascot_panic.png"
    accent_border = "#EF4444" # Danger Red
    speech_text = f"😱 **Oh no! Our match rate fell to {match_rate:.2f}%!** Heavy variances or tax compliance integrity failures detected. Triage needed!"

# Resolve current mascot image path/url
mascot_image_src = get_mascot_image(mascot_file)

# --- Metrics Row: Custom CSS KPI Cards ---
st.header("📊 Performance & Verification KPI Metrics")

kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)

with kpi_col1:
    total_records = len(agent.invoices) + len(agent.payments) + len(agent.bank_transactions)
    st.markdown(f"""
    <div class='metric-card' style='border-left: 5px solid #3B82F6;'>
        <div class='metric-title'>📈 Total Throughput</div>
        <div class='metric-value'>{total_records} rows</div>
        <div style='color: #94A3B8; font-size: 11px; margin-top: 5px;'>Combined records audited</div>
    </div>
    """, unsafe_allow_html=True)

with kpi_col2:
    st.markdown(f"""
    <div class='metric-card' style='border-left: 5px solid #10B981;'>
        <div class='metric-title'>✅ Match Rate</div>
        <div class='metric-value'>{match_rate:.2f}%</div>
        <div style='color: #10B981; font-size: 11px; margin-top: 5px;'>Target: &gt;90% threshold</div>
    </div>
    """, unsafe_allow_html=True)

with kpi_col3:
    st.markdown(f"""
    <div class='metric-card' style='border-left: 5px solid #EF4444;'>
        <div class='metric-title'>⚠️ Exceptions</div>
        <div class='metric-value'>{len(exceptions_df)} cases</div>
        <div style='color: #EF4444; font-size: 11px; margin-top: 5px;'>Isolated for human-in-the-loop</div>
    </div>
    """, unsafe_allow_html=True)

with kpi_col4:
    current_cash = agent.bank_transactions.sort_values('booking_date').iloc[-1]['balance']
    st.markdown(f"""
    <div class='metric-card' style='border-left: 5px solid #F59E0B;'>
        <div class='metric-title'>💰 Cash Balance</div>
        <div class='metric-value'>₹{current_cash:,.2f}</div>
        <div style='color: #F59E0B; font-size: 11px; margin-top: 5px;'>Reconciled cash-at-bank</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- Layout: Main Dashboard (Tabs) ---
tab_recon, tab_forecast, tab_chat = st.tabs(["🔍 Reconciliation & Triage", "📈 30-Day Liquidity Forecast", "💬 Conversational Copilot Chat"])

with tab_recon:
    st.subheader("📊 Reconciliation Metrics & Matching Health")
    
    # Render two columns for charts
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        if not exceptions_df.empty:
            exc_counts = exceptions_df['type'].value_counts().reset_index()
            exc_counts.columns = ['Exception Type', 'Count']
            fig_exc = px.bar(
                exc_counts, 
                x='Count', 
                y='Exception Type',
                orientation='h',
                title="Isolated Exceptions by Failure Profile",
                color='Exception Type',
                color_discrete_sequence=px.colors.sequential.YlOrRd_r
            )
            fig_exc.update_layout(
                showlegend=False, 
                height=350, 
                margin=dict(l=20, r=20, t=40, b=20),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color="#F8FAFC")
            )
            st.plotly_chart(fig_exc, use_container_width=True)
        else:
            st.success("🎉 Zero exceptions found! Clean sheet reconciliation completed.")

    with chart_col2:
        # Ledger Health Donut Chart showing Matched vs Unresolved
        status_counts = results_df['reconciliation_status'].value_counts().reset_index()
        status_counts.columns = ['Audit Status', 'Record Count']
        fig_donut = px.pie(
            status_counts,
            values='Record Count',
            names='Audit Status',
            hole=0.45,
            title="Overall Matching Health (Matched vs. Exceptions)",
            color='Audit Status',
            color_discrete_map={
                'Matched': '#10B981',               # Emerald Green
                'Unresolved': '#EF4444',            # Coral Red
                'Matched with Exception': '#F59E0B' # Amber Orange
            }
        )
        fig_donut.update_layout(
            height=350, 
            margin=dict(l=20, r=20, t=40, b=20),
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color="#F8FAFC")
        )
        st.plotly_chart(fig_donut, use_container_width=True)

    st.subheader("📋 Exception Triage Table (Human Review Queue)")
    st.markdown("These isolated anomalies require direct manual oversight or corrective billing action:")
    
    # Filter multi-select for Exception Profiles
    all_exception_types = exceptions_df['type'].unique().tolist() if not exceptions_df.empty else []
    selected_profiles = st.multiselect("Filter by Exception Profile", options=all_exception_types, default=all_exception_types)
    
    if not exceptions_df.empty:
        filtered_exc = exceptions_df[exceptions_df['type'].isin(selected_profiles)]
        st.dataframe(
            filtered_exc[['source_id', 'type', 'customer_name', 'amount_expected', 'amount_received', 'variance', 'description']],
            column_config={
                "source_id": "Invoice ID / Ref",
                "type": "Exception Type",
                "customer_name": "Customer Name",
                "amount_expected": st.column_config.NumberColumn("Expected Total (₹)", format="₹%,.2f"),
                "amount_received": st.column_config.NumberColumn("Received Total (₹)", format="₹%,.2f"),
                "variance": st.column_config.NumberColumn("Variance (₹)", format="₹%,.2f"),
                "description": "System Diagnostic Message"
            },
            hide_index=True,
            use_container_width=True
        )
        
        # Download button for exceptions ledger
        csv_data = exceptions_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Export Exceptions for Audit Ledger (CSV)",
            data=csv_data,
            file_name="reconciliation_exceptions.csv",
            mime="text/csv"
        )
    else:
        st.info("No exceptions matches current filters.")

with tab_forecast:
    st.subheader("🔮 Predictive 30-Day Forward Liquidity Forecast")
    st.markdown("""
    This forecast maps out rolling liquidity by factoring in expected cash flows from reconciled accounts
    and scheduled corporate expenses (SaaS subscriptions, Payroll, and Rent).
    """)
    
    # Plotly Line Chart for forward projections
    fig_cash = go.Figure()
    fig_cash.add_trace(go.Scatter(
        x=forecast_df['date'], 
        y=forecast_df['closing_balance'], 
        mode='lines+markers',
        name='Projected Cash Balance',
        line=dict(color='#3B82F6', width=3.5),
        marker=dict(size=7, color='#10B981')
    ))
    # Threshold alert line at 3.3 Million
    fig_cash.add_hline(y=3300000.0, line_dash="dash", line_color="#EF4444", annotation_text="Liquidity Guardrail Threshold (₹3.3M)", annotation_position="top left")
    
    fig_cash.update_layout(
        title="Projected Rolling Cash Balance (30 Days Out)",
        xaxis_title="Timeline",
        yaxis_title="Cash Balance (₹)",
        height=400,
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color="#F8FAFC"),
        xaxis=dict(showgrid=True, gridcolor="#334155"),
        yaxis=dict(showgrid=True, gridcolor="#334155")
    )
    st.plotly_chart(fig_cash, use_container_width=True)
    
    # Display Cash Projection Table
    st.markdown("**30-Day Liquidity Projection Table:**")
    st.dataframe(
        forecast_df[['date', 'opening_balance', 'inflow', 'outflow', 'closing_balance', 'events']],
        column_config={
            "date": st.column_config.DateColumn("Date", format="YYYY-MM-DD"),
            "opening_balance": st.column_config.NumberColumn("Opening Balance (₹)", format="₹%,.2f"),
            "inflow": st.column_config.NumberColumn("Scheduled Inflow (₹)", format="₹%,.2f"),
            "outflow": st.column_config.NumberColumn("Expected Outflow (₹)", format="₹%,.2f"),
            "closing_balance": st.column_config.NumberColumn("Closing Balance (₹)", format="₹%,.2f"),
            "events": "Scheduled Event Description"
        },
        hide_index=True,
        use_container_width=True
    )

with tab_chat:
    # ── Interactive 2-Column Chat Layout ──

    chat_col_left, chat_col_right = st.columns([1.8, 1])
    
    with chat_col_left:
        # Styled Chat Header
        st.markdown("""
        <div class="chat-header">
            <h4 style="margin: 0; color: #3B82F6; font-size: 18px; font-weight: 700;">🤖 Interactive FinOps Copilot</h4>
            <p style="margin: 4px 0 0 0; color: #94A3B8; font-size: 13px;">
                Direct conversational interface. Ask about INV-083, exception profiles, or liquidity forecasting.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Initialize chatbot session state
        if "messages" not in st.session_state:
            st.session_state.messages = [
                {"role": "assistant", "content": "Hello! I am your FinOps Copilot. You can ask me questions like 'Why is INV-083 still open?' or 'What is the summary of outstanding exceptions?'"}
            ]
            
        # Display chat logs
        for msg in st.session_state.messages:
            # We dynamically set the avatar image for the assistant's replies!
            avatar_path = mascot_image_src if msg["role"] == "assistant" else None
            with st.chat_message(msg["role"], avatar=avatar_path):
                st.markdown(msg["content"])
                
        if user_query := st.chat_input("Ask a question regarding the audit ledger..."):
            st.session_state.messages.append({"role": "user", "content": user_query})
            with st.chat_message("user"):
                st.markdown(user_query)
                
            with st.chat_message("assistant", avatar=mascot_image_src):
                with st.spinner("Analyzing ledger data..."):
                    response = agent.conversational_query(user_query)
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    
    with chat_col_right:
        # Mascot Card Container
        st.markdown(f"""
        <div class="speech-bubble" style="border-color: {accent_border};">
            {speech_text}
        </div>
        """, unsafe_allow_html=True)
        
        if mascot_image_src:
            st.image(mascot_image_src, use_container_width=True)
            # Removed status text as requested

# Footer Layout
st.markdown("---")
st.markdown("Generated with ❤️ by Phoenix - **Autonomous Finance Controller Agent**")
