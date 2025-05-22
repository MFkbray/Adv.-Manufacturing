import streamlit as st
import time
import os

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

# Function to rename files
def rename_files_in_folder(folder_path, old_string, new_string, prefix_string):
    if not os.path.exists(folder_path):
        st.error(f"The folder {folder_path} does not exist.")
        return []
    
    renamed_files = []
    for filename in os.listdir(folder_path):
        old_file_path = os.path.join(folder_path, filename)
        if os.path.isfile(old_file_path):
            new_filename = filename
            
            # Apply old_string to new_string replacement if old_string is provided
            if old_string:
                new_filename = new_filename.replace(old_string, new_string)

            # Prepend the prefix_string if provided
            if prefix_string:
                new_filename = f"{prefix_string}{new_filename}".replace(' ', '_').replace('_-_', '_')
            else:
                new_filename = new_filename.replace(' ', '_').replace('_-_', '_')

            new_file_path = os.path.join(folder_path, new_filename)

            if old_file_path != new_file_path:
                try:
                    os.rename(old_file_path, new_file_path)
                    renamed_files.append((filename, new_filename))
                except Exception as e:
                    st.error(f"Error renaming {filename}: {str(e)}")
    
    return renamed_files

# Title and description
st.title("Advanced Manufacturing Control Panel")
st.markdown("Monitor and control manufacturing equipment from anywhere")

# Create tabs for different functionalities
tab1, tab2 = st.tabs(["Equipment Dashboard", "File Management"])

# Tab 1: Equipment Dashboard
with tab1:
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

# Tab 2: File Management
with tab2:
    st.subheader("File Renaming Tool")
    
    # File management interface
    folder_path = st.text_input("Folder Path", placeholder="Enter the full path to your folder")
    
    col1, col2 = st.columns(2)
    with col1:
        old_string = st.text_input("Old String (leave blank to skip)", placeholder="Text to replace")
        new_string = st.text_input("New String", placeholder="Replacement text")
    
    with col2:
        prefix_string = st.text_input("Prefix (leave blank to skip)", placeholder="Add prefix to filenames")
        
    if st.button("Preview Changes"):
        if not folder_path:
            st.warning("Please enter a folder path.")
        else:
            st.write("Files that will be renamed:")
            preview_files = []
            for filename in os.listdir(folder_path):
                if os.path.isfile(os.path.join(folder_path, filename)):
                    new_filename = filename
                    if old_string:
                        new_filename = new_filename.replace(old_string, new_string)
                    if prefix_string:
                        new_filename = f"{prefix_string}{new_filename}".replace(' ', '_').replace('_-_', '_')
                    else:
                        new_filename = new_filename.replace(' ', '_').replace('_-_', '_')
                    if new_filename != filename:
                        preview_files.append((filename, new_filename))
            
            if preview_files:
                for old, new in preview_files:
                    st.text(f"'{old}' → '{new}'")
            else:
                st.info("No files will be changed with these settings.")

    if st.button("Rename Files"):
        if not folder_path:
            st.warning("Please enter a folder path.")
        else:
            renamed_files = rename_files_in_folder(folder_path, old_string, new_string, prefix_string)
            if renamed_files:
                st.success("Files renamed successfully!")
                st.write("Renamed files:")
                for old, new in renamed_files:
                    st.text(f"'{old}' → '{new}'")
            else:
                st.info("No files were renamed.")

# Add a footer with timestamp
st.markdown("---")
st.markdown(f"Last updated: {time.strftime('%Y-%m-%d %H:%M:%S')}")

# Auto-refresh functionality
if st.button("Refresh Data"):
    st.experimental_rerun() 