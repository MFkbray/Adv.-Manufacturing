import streamlit as st
import time

# Configure the page
st.set_page_config(
    page_title="Advanced Manufacturing Control Panel",
    page_icon="🏭",
    layout="wide"
)

# Mock data for machine status
MACHINE_STATUS = {
    'machines': [
        {'id': 1, 'name': 'CNC Machine 1', 'status': 'Running', 'uptime': '12h 30m'},
        {'id': 2, 'name': 'Assembly Line A', 'status': 'Idle', 'uptime': '8h 45m'},
        {'id': 3, 'name': '3D Printer', 'status': 'Maintenance', 'uptime': '0h'}
    ]
}

# Title and description
st.title("Advanced Manufacturing Control Panel")
st.markdown("Monitor and control manufacturing equipment from anywhere")

# Create columns for the dashboard
col1, col2 = st.columns(2)

with col1:
    st.subheader("Equipment Status")
    # Display each machine's status in a card
    for machine in MACHINE_STATUS['machines']:
        with st.container():
            st.markdown(f"""
            <div style='padding: 10px; border: 1px solid #ddd; border-radius: 5px; margin: 10px 0;'>
                <h3>{machine['name']}</h3>
                <p>Status: <span style='color: {'green' if machine['status'] == 'Running' else 'orange' if machine['status'] == 'Idle' else 'red'};'>
                    {machine['status']}</span></p>
                <p>Uptime: {machine['uptime']}</p>
            </div>
            """, unsafe_allow_html=True)

with col2:
    st.subheader("Machine Controls")
    # Control panel for each machine
    for machine in MACHINE_STATUS['machines']:
        with st.expander(f"Control {machine['name']}"):
            col_start, col_stop, col_maint = st.columns(3)
            with col_start:
                if st.button(f"Start", key=f"start_{machine['id']}"):
                    st.success(f"Start command sent to {machine['name']}")
            with col_stop:
                if st.button(f"Stop", key=f"stop_{machine['id']}"):
                    st.warning(f"Stop command sent to {machine['name']}")
            with col_maint:
                if st.button(f"Maintenance", key=f"maint_{machine['id']}"):
                    st.info(f"Maintenance mode activated for {machine['name']}")

# System metrics
st.subheader("System Metrics")
metrics_col1, metrics_col2, metrics_col3 = st.columns(3)

with metrics_col1:
    st.metric("Total Uptime", "21h 15m")
with metrics_col2:
    st.metric("Active Machines", "1/3")
with metrics_col3:
    st.metric("Efficiency", "85%", "+2%")

# Auto-refresh functionality
if st.button("Refresh Data"):
    st.experimental_rerun()

# Add a footer with timestamp
st.markdown("---")
st.markdown(f"Last updated: {time.strftime('%Y-%m-%d %H:%M:%S')}") 