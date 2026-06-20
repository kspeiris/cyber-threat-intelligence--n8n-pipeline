import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json

# Page configuration
st.set_page_config(
    page_title="Cyber Threat Intelligence Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API base URL
API_URL = "http://localhost:8000/api"

# Custom Advanced UI CSS
st.markdown("""
    <style>
    /* Premium Glassmorphism Metrics */
    div[data-testid="stMetric"] {
        background-color: rgba(30, 34, 45, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 1.2rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        backdrop-filter: blur(10px);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(123, 97, 255, 0.2);
        border: 1px solid rgba(123, 97, 255, 0.4);
    }
    
    /* Headers & Text */
    h1, h2, h3 {
        color: #e2e8f0;
        font-weight: 600 !important;
        letter-spacing: -0.02em;
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #7b61ff 0%, #5a3ce8 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        box-shadow: 0 4px 10px rgba(123, 97, 255, 0.3);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #8d76ff 0%, #6e52eb 100%);
        box-shadow: 0 6px 15px rgba(123, 97, 255, 0.5);
        transform: translateY(-1px);
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: rgba(30, 34, 45, 0.8) !important;
        border-radius: 8px;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    /* Table styling */
    .stDataFrame {
        border-radius: 10px;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    .severity-critical { color: #ff4b4b; font-weight: bold; }
    .severity-high { color: #ff8c00; font-weight: bold; }
    .severity-medium { color: #ffd166; font-weight: bold; }
    .severity-low { color: #06d6a0; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("🛡️ Threat Intelligence")
st.sidebar.markdown("---")

# Navigation
page = st.sidebar.selectbox(
    "Navigation",
    ["Dashboard", "Threats", "Indicators", "Alerts", "Reports", "AI Analysis"]
)

# Refresh button
if st.sidebar.button("🔄 Refresh Data"):
    st.rerun()

# Function to fetch data from API
def fetch_data(endpoint):
    try:
        response = requests.get(f"{API_URL}/{endpoint}", timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error fetching data: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Connection error: {str(e)}")
        return None

# Main content
if page == "Dashboard":
    st.title("📊 Threat Intelligence Dashboard")
    st.markdown(f"*Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
    
    # Fetch statistics
    stats = fetch_data("threats/statistics")
    indicators_stats = fetch_data("indicators/statistics")
    trends = fetch_data("threats/trends?days=30")
    
    if stats:
        # Metrics row
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Threats", stats["total_threats"])
        
        with col2:
            st.metric("Critical Threats", stats["critical"], delta_color="inverse")
        
        with col3:
            st.metric("New Today", stats["new_today"])
        
        with col4:
            st.metric("Active Alerts", "5", delta="2")
    
    # Charts row
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Threat Severity Distribution")
        if stats:
            total_severity = stats.get("critical", 0) + stats.get("high", 0) + stats.get("medium", 0) + stats.get("low", 0)
            if total_severity > 0:
                severity_data = {
                    "Severity": ["Critical", "High", "Medium", "Low"],
                    "Count": [stats["critical"], stats["high"], stats["medium"], stats["low"]]
                }
                df = pd.DataFrame(severity_data)
                
                colors = ["#ff4b4b", "#ff8c00", "#ffd166", "#06d6a0"]
                fig = px.pie(
                    df,
                    values="Count",
                    names="Severity",
                    color="Severity",
                    color_discrete_sequence=colors,
                    template="plotly_dark",
                    hole=0.4
                )
                fig.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    margin=dict(t=30, b=10, l=10, r=10)
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No threat severity data available. Collect threats to view distribution.")
    
    with col2:
        st.subheader("Threat Trends (30 Days)")
        if trends and trends.get("labels"):
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=trends["labels"],
                y=trends["values"],
                mode="lines+markers",
                name="Threats",
                line=dict(color="#7b61ff", width=3),
                marker=dict(size=8, color="#5a3ce8"),
                fill='tozeroy',
                fillcolor='rgba(123, 97, 255, 0.1)'
            ))
            fig.update_layout(
                xaxis_title="Date",
                yaxis_title="Number of Threats",
                hovermode='x',
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(t=30, b=10, l=10, r=10)
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No trend data available. Click 'Collect New Threats' on the Threats page.")
    
    # Recent threats table
    st.subheader("Recent Threats")
    threats = fetch_data("threats?limit=10")
    if threats:
        df = pd.DataFrame(threats)
        df = df[["cve_id", "title", "severity", "cvss_score", "published_date"]]
        df.columns = ["CVE ID", "Title", "Severity", "CVSS Score", "Published"]
        
        # Color code severity
        def color_severity(val):
            colors = {
                "critical": "red",
                "high": "orange",
                "medium": "yellow",
                "low": "green"
            }
            return f"color: {colors.get(val, 'black')}"
        
        st.dataframe(
            df.style.applymap(color_severity, subset=["Severity"]),
            use_container_width=True
        )
    else:
        st.info("No recent threats found. Try collecting new threats.")

elif page == "Threats":
    st.title("🔍 Threat Management")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        severity_filter = st.selectbox(
            "Filter by Severity",
            ["All", "critical", "high", "medium", "low"]
        )
    
    with col2:
        limit = st.number_input("Results per page", min_value=10, max_value=100, value=50)
    
    with col3:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 Collect New Threats"):
            with st.spinner("Collecting threats..."):
                response = requests.post(f"{API_URL}/threats/collect")
                if response.status_code == 200:
                    st.success("Threat collection started!")
                else:
                    st.error("Failed to start collection")
    
    # Fetch and display threats
    url = f"threats?limit={limit}"
    if severity_filter != "All":
        url += f"&severity={severity_filter}"
    
    threats = fetch_data(url)
    if threats:
        df = pd.DataFrame(threats)
        st.dataframe(df, use_container_width=True)
        
        # Export button
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name=f"threats_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    else:
        st.info("No threats found in the database. Click 'Collect New Threats' to start.")

elif page == "Indicators":
    st.title("🎯 Indicators of Compromise")
    
    col1, col2 = st.columns(2)
    with col1:
        indicator_type = st.selectbox(
            "Filter by Type",
            ["All", "ip", "domain", "url", "hash"]
        )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 Collect Indicators"):
            with st.spinner("Collecting indicators..."):
                response = requests.post(f"{API_URL}/indicators/collect")
                if response.status_code == 200:
                    st.success("Indicator collection started!")
                else:
                    st.error("Failed to start collection")
    
    url = "indicators?limit=100"
    if indicator_type != "All":
        url += f"&indicator_type={indicator_type}"
    
    indicators = fetch_data(url)
    if indicators:
        df = pd.DataFrame(indicators)
        
        # Risk score gauge
        fig = go.Figure()
        for idx, row in df.iterrows():
            fig.add_trace(go.Indicator(
                mode="gauge+number+delta",
                value=row["risk_score"],
                title={"text": row["indicator_value"][:20]},
                delta={"reference": 5},
                gauge={"axis": {"range": [0, 10]},
                       "steps": [
                           {"range": [0, 4], "color": "green"},
                           {"range": [4, 7], "color": "yellow"},
                           {"range": [7, 10], "color": "red"}
                       ]}
            ))
        
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No indicators found. Click 'Collect Indicators' to fetch data.")

elif page == "Alerts":
    st.title("🔔 Security Alerts")
    
    col1, col2 = st.columns(2)
    with col1:
        resolved_filter = st.selectbox(
            "Filter by Status",
            ["All", "Active", "Resolved"]
        )
    
    with col2:
        if st.button("🔄 Refresh Alerts"):
            st.rerun()
    
    url = "alerts?limit=100"
    if resolved_filter == "Active":
        url += "&resolved=false"
    elif resolved_filter == "Resolved":
        url += "&resolved=true"
    
    alerts = fetch_data(url)
    if alerts:
        for alert in alerts:
            with st.container():
                severity_color = {
                    "critical": "🔴",
                    "high": "🟠",
                    "medium": "🟡",
                    "low": "🟢"
                }.get(alert["severity"], "⚪")
                
                col1, col2, col3 = st.columns([1, 6, 1])
                with col1:
                    st.markdown(f"<h1>{severity_color}</h1>", unsafe_allow_html=True)
                with col2:
                    st.markdown(f"**{alert['alert_type'].replace('_', ' ').title()}**")
                    st.caption(alert["message"][:200] + "...")
                    st.caption(f"*{alert['created_at']}*")
                with col3:
                    if not alert["is_resolved"]:
                        if st.button("✅ Resolve", key=f"resolve_{alert['id']}"):
                            response = requests.post(f"{API_URL}/alerts/{alert['id']}/resolve")
                            if response.status_code == 200:
                                st.success("Alert resolved!")
                                st.rerun()
                st.divider()
    else:
        st.info("No active alerts found.")

elif page == "Reports":
    st.title("📋 Reports")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📊 Generate Daily Report"):
            with st.spinner("Generating daily report..."):
                response = requests.get(f"{API_URL}/reports/daily")
                if response.status_code == 200:
                    st.success("Daily report generated!")
                    report = response.json()
                    st.json(report)
                else:
                    st.error("Failed to generate report")
    
    with col2:
        if st.button("📈 Generate Weekly Report"):
            with st.spinner("Generating weekly report..."):
                response = requests.get(f"{API_URL}/reports/weekly")
                if response.status_code == 200:
                    st.success("Weekly report generated!")
                    report = response.json()
                    st.json(report)
                else:
                    st.error("Failed to generate report")

elif page == "AI Analysis":
    st.title("🤖 AI Threat Analysis")
    
    # Select threat to analyze
    threats = fetch_data("threats?limit=50")
    if threats:
        threat_options = {f"{t['cve_id']} - {t['title'][:50]}": t["id"] for t in threats}
        selected = st.selectbox("Select Threat to Analyze", list(threat_options.keys()))
        threat_id = threat_options[selected]
        
        if st.button("🔍 Analyze Threat"):
            with st.spinner("Analyzing threat with AI..."):
                response = requests.post(f"{API_URL}/threats/{threat_id}/analyze")
                if response.status_code == 200:
                    analysis = response.json()
                    
                    st.subheader("📊 Threat Analysis")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Overall Risk", analysis.get("risk_assessment", {}).get("overall_risk", "Unknown").upper())
                        st.metric("Exploitability", analysis.get("risk_assessment", {}).get("exploitability", "Unknown"))
                        st.metric("Impact", analysis.get("risk_assessment", {}).get("impact", "Unknown"))
                    
                    with col2:
                        insights = analysis.get("additional_insights", {})
                        st.metric("Affected Systems", insights.get("affected_systems", "Unknown"))
                        st.metric("Attack Vector", insights.get("attack_vector", "Unknown"))
                        st.metric("Known Exploits", insights.get("known_exploits", "Unknown"))
                    
                    st.subheader("📝 Summary")
                    st.write(analysis.get("summary", "No summary available"))
                    
                    st.subheader("💡 Recommendations")
                    recommendations = analysis.get("recommendations", "No recommendations available")
                    for rec in recommendations.split("\n"):
                        if rec.strip():
                            st.markdown(f"- {rec}")
                else:
                    st.error("Failed to analyze threat")
    else:
        st.info("No threats available for AI analysis. Please collect threats first.")