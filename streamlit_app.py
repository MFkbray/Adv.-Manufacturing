import streamlit as st
import time
import os
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

# Configure the page
st.set_page_config(
    page_title="Advanced Manufacturing Control Panel",
    page_icon="🏭",
    layout="wide"
)

# Initialize session state for file management
if 'selected_files' not in st.session_state:
    st.session_state.selected_files = []
if 'current_directory' not in st.session_state:
    st.session_state.current_directory = os.path.expanduser("~")

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

# Function to save Excel rows as CSV files
def save_rows_as_csv(df, output_folder, start_row, end_row):
    try:
        # Adjust for zero-indexing
        start_row -= 1
        end_row -= 1

        # Ensure the row range is valid
        if start_row < 0 or end_row >= len(df) or start_row > end_row:
            st.error("Please enter a valid row range.")
            return []

        saved_files = []
        # Iterate over the specified rows in the DataFrame
        for index in range(start_row, end_row + 1):
            row = df.iloc[index]

            # Check if the row is completely blank
            if row.isnull().all():
                continue  # Skip this row if it's blank

            # Get the name from the first column
            file_name = str(row[0])  # Assuming the name is in the first column
            
            # Create a new DataFrame with the header and the current row
            row_df = pd.DataFrame([row.values], columns=df.columns)

            # Save the row as a CSV file, ensuring the file name is valid
            if pd.notna(file_name) and file_name:  # Ensure the file name is not NaN or empty
                file_path = os.path.join(output_folder, f"{file_name}.csv")
                row_df.to_csv(file_path, index=False)
                saved_files.append(file_name)
            else:
                st.warning(f"Row {index + 1} has an invalid name; skipping.")

        return saved_files

    except Exception as e:
        st.error(f"Error: {str(e)}")
        return []

def list_directory_contents(path):
    try:
        # Get directories and files
        items = list(Path(path).glob('*'))
        directories = [item for item in items if item.is_dir()]
        files = [item for item in items if item.is_file()]
        
        # Sort alphabetically
        directories.sort(key=lambda x: x.name.lower())
        files.sort(key=lambda x: x.name.lower())
        
        return directories, files
    except Exception as e:
        st.error(f"Error accessing directory: {str(e)}")
        return [], []

def get_file_info(file_path):
    try:
        stats = os.stat(file_path)
        size = stats.st_size
        modified = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(stats.st_mtime))
        
        # Convert size to readable format
        if size < 1024:
            size_str = f"{size} B"
        elif size < 1024 * 1024:
            size_str = f"{size/1024:.1f} KB"
        else:
            size_str = f"{size/(1024*1024):.1f} MB"
            
        return size_str, modified
    except:
        return "N/A", "N/A"

# Function to create folders based on Sample ID and save CSV
def create_folders_for_csv(csv_file, file_name, row_df, save_location, fabrication_checked, inspection_checked):
    created_folders = []
    try:
        # Folder paths based on the Sample ID
        run_folder = os.path.join(save_location, f"Run={file_name}")
        stage_folder = os.path.join(run_folder, "Stage=source_data")
        
        # Create the "Stage=source_data" folder
        os.makedirs(stage_folder, exist_ok=True)
        created_folders.append(stage_folder)

        # Create folders based on options
        if fabrication_checked:
            fabrication_folder = os.path.join(run_folder, "Stage=source_data", "Modality=record_manufacture")
            os.makedirs(fabrication_folder, exist_ok=True)
            created_folders.append(fabrication_folder)
            # Save CSV in the "record_manufacture" folder
            if not row_df.empty:
                csv_file_path = os.path.join(fabrication_folder, csv_file)
                row_df.to_csv(csv_file_path, index=False)

        if inspection_checked:
            # Create all modality folders except "Modality=record_manufacture"
            modalities = [
                "Modality=optical_image",
                "Modality=sem_c_0deg",
                "Modality=sem_c_high_angle",
                "Modality=sem_c_medium_angle",
                "Modality=sem_p_0deg",
                "Modality=sem_p_high_angle",
                "Modality=sem_p_medium_angle"
            ]
            
            for modality in modalities:
                modality_folder = os.path.join(stage_folder, modality)
                os.makedirs(modality_folder, exist_ok=True)
                created_folders.append(modality_folder)
                # Save the CSV in the stage folder
                if not row_df.empty:
                    csv_file_path = os.path.join(stage_folder, csv_file)
                    row_df.to_csv(csv_file_path, index=False)
        
        return True, created_folders
    except Exception as e:
        return False, str(e)

# Title and description
st.title("Advanced Manufacturing Control Panel")
st.markdown("Monitor and control manufacturing equipment from anywhere")

# Create tabs for different functionalities
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Equipment Dashboard", 
    "File Management", 
    "Excel Row Exporter", 
    "Data Structure Creator",
    "Line Scaling"
])

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
    
    # Directory navigation
    col1, col2 = st.columns([2, 1])
    with col1:
        st.text("Current Directory:")
        st.code(st.session_state.current_directory)
    with col2:
        if st.button("⬆️ Up One Level"):
            parent = str(Path(st.session_state.current_directory).parent)
            if os.path.exists(parent):
                st.session_state.current_directory = parent
                st.rerun()
    
    # List directories and files
    directories, files = list_directory_contents(st.session_state.current_directory)
    
    # Show directories
    if directories:
        st.subheader("📁 Directories")
        for dir in directories:
            if st.button(f"📁 {dir.name}", key=f"dir_{dir}"):
                st.session_state.current_directory = str(dir)
                st.rerun()
    
    # Show files with selection
    if files:
        st.subheader("📄 Files")
        
        # File filter
        file_filter = st.text_input("🔍 Filter files (leave empty to show all):", "")
        
        # Create a table-like display for files
        col1, col2, col3, col4 = st.columns([0.5, 2, 1, 1])
        with col1:
            st.write("Select")
        with col2:
            st.write("File Name")
        with col3:
            st.write("Size")
        with col4:
            st.write("Modified")
        
        for file in files:
            if file_filter.lower() in file.name.lower() or not file_filter:
                size, modified = get_file_info(file)
                col1, col2, col3, col4 = st.columns([0.5, 2, 1, 1])
                with col1:
                    if st.checkbox("", key=f"select_{file}", value=str(file) in st.session_state.selected_files):
                        if str(file) not in st.session_state.selected_files:
                            st.session_state.selected_files.append(str(file))
                    else:
                        if str(file) in st.session_state.selected_files:
                            st.session_state.selected_files.remove(str(file))
                with col2:
                    st.write(file.name)
                with col3:
                    st.write(size)
                with col4:
                    st.write(modified)
    
    # File renaming options
    if st.session_state.selected_files:
        st.subheader("Rename Selected Files")
        st.write(f"Selected {len(st.session_state.selected_files)} files")
        
        col1, col2 = st.columns(2)
        with col1:
            old_string = st.text_input("Text to Replace", placeholder="Leave blank to skip")
            new_string = st.text_input("Replace With", placeholder="New text")
        with col2:
            prefix_string = st.text_input("Add Prefix", placeholder="Leave blank to skip")
            
        if st.button("Preview Changes"):
            st.write("Preview of changes:")
            for file_path in st.session_state.selected_files:
                file = Path(file_path)
                new_filename = file.name
                if old_string:
                    new_filename = new_filename.replace(old_string, new_string)
                if prefix_string:
                    new_filename = f"{prefix_string}{new_filename}"
                new_filename = new_filename.replace(' ', '_').replace('_-_', '_')
                
                if new_filename != file.name:
                    st.text(f"'{file.name}' → '{new_filename}'")
                
        if st.button("Rename Selected Files"):
            renamed_count = 0
            for file_path in st.session_state.selected_files:
                file = Path(file_path)
                new_filename = file.name
                if old_string:
                    new_filename = new_filename.replace(old_string, new_string)
                if prefix_string:
                    new_filename = f"{prefix_string}{new_filename}"
                new_filename = new_filename.replace(' ', '_').replace('_-_', '_')
                
                if new_filename != file.name:
                    try:
                        new_path = file.parent / new_filename
                        os.rename(file, new_path)
                        renamed_count += 1
                    except Exception as e:
                        st.error(f"Error renaming {file.name}: {str(e)}")
            
            if renamed_count > 0:
                st.success(f"Successfully renamed {renamed_count} files!")
                st.session_state.selected_files = []
                st.rerun()
            else:
                st.info("No files were renamed.")

# Tab 3: Excel Row Exporter
with tab3:
    st.subheader("Excel Row Exporter")
    
    uploaded_file = st.file_uploader("Choose an Excel file", type=['xlsx', 'xls'])
    
    if uploaded_file is not None:
        try:
            # Read Excel file
            excel_file = pd.ExcelFile(uploaded_file)
            sheet_name = st.selectbox("Select Sheet", excel_file.sheet_names)
            
            # Read the selected sheet
            df = pd.read_excel(uploaded_file, sheet_name=sheet_name)
            
            # Show DataFrame preview
            st.write("Preview of the Excel file:")
            st.dataframe(df.head())
            
            # Input for row range
            col1, col2 = st.columns(2)
            with col1:
                start_row = st.number_input("Start Row", min_value=1, max_value=len(df), value=1)
            with col2:
                end_row = st.number_input("End Row", min_value=1, max_value=len(df), value=min(5, len(df)))
            
            # Output folder
            output_folder = st.text_input("Output Folder Path", placeholder="Enter the folder path for CSV files", key="excel_folder")
            
            if st.button("Export Rows"):
                if not output_folder:
                    st.warning("Please enter an output folder path.")
                elif not os.path.exists(output_folder):
                    st.error("Output folder does not exist.")
                else:
                    saved_files = save_rows_as_csv(df, output_folder, start_row, end_row)
                    if saved_files:
                        st.success(f"Successfully exported {len(saved_files)} files!")
                        st.write("Exported files:")
                        for file_name in saved_files:
                            st.text(f"- {file_name}.csv")
                    else:
                        st.warning("No files were exported. Please check your row range and data.")
                        
        except Exception as e:
            st.error(f"Error reading Excel file: {str(e)}")

# Tab 4: Data Structure Creator
with tab4:
    st.subheader("Data Structure Creator")
    
    # Two methods: Excel file or manual Sample ID
    method = st.radio("Choose Method", ["Upload Excel File", "Enter Sample ID Manually"])
    
    col1, col2 = st.columns(2)
    with col1:
        fabrication = st.checkbox("Include Fabrication Folder")
    with col2:
        inspection = st.checkbox("Include Inspection Folders")
    
    if method == "Upload Excel File":
        excel_file = st.file_uploader("Choose Excel File", type=['xlsx', 'xls'], key="structure_excel")
        
        if excel_file is not None:
            # Read Excel file
            excel_data = pd.ExcelFile(excel_file)
            sheet_name = st.selectbox("Select Sheet", excel_data.sheet_names, key="structure_sheet")
            
            # Read the selected sheet
            df = pd.read_excel(excel_file, sheet_name=sheet_name)
            
            # Show DataFrame preview
            st.write("Preview of the Excel file:")
            st.dataframe(df.head())
            
            # Row range selection
            col1, col2 = st.columns(2)
            with col1:
                start_row = st.number_input("Start Row", min_value=1, max_value=len(df), value=1, key="structure_start")
            with col2:
                end_row = st.number_input("End Row", min_value=1, max_value=len(df), value=min(5, len(df)), key="structure_end")
    else:
        sample_id = st.text_input("Enter Sample ID")
    
    # Output location
    save_location = st.text_input("Output Location", placeholder="Enter the path where folders should be created")
    
    if st.button("Create Folder Structure"):
        if not save_location:
            st.error("Please specify an output location")
        elif not os.path.exists(save_location):
            st.error("Output location does not exist")
        else:
            if method == "Upload Excel File" and excel_file is not None:
                success_count = 0
                error_messages = []
                
                # Process Excel rows
                for index in range(start_row-1, end_row):
                    row = df.iloc[index]
                    if not row.isnull().all():
                        sample_id = str(row[0])
                        if pd.notna(sample_id) and sample_id:
                            success, result = create_folders_for_csv(
                                f"{sample_id}.csv",
                                sample_id,
                                pd.DataFrame([row.values], columns=df.columns),
                                save_location,
                                fabrication,
                                inspection
                            )
                            if success:
                                success_count += 1
                            else:
                                error_messages.append(f"Error with {sample_id}: {result}")
                
                if success_count > 0:
                    st.success(f"Successfully created folder structures for {success_count} samples!")
                if error_messages:
                    for msg in error_messages:
                        st.error(msg)
                        
            else:  # Manual Sample ID
                if not sample_id:
                    st.error("Please enter a Sample ID")
                else:
                    success, result = create_folders_for_csv(
                        f"{sample_id}.csv",
                        sample_id,
                        pd.DataFrame(),
                        save_location,
                        fabrication,
                        inspection
                    )
                    if success:
                        st.success(f"Successfully created folder structure for {sample_id}!")
                        st.write("Created folders:")
                        for folder in result:
                            st.text(f"📁 {os.path.basename(folder)}")
                    else:
                        st.error(f"Error creating folders: {result}")

# Tab 5: Line Scaling
with tab5:
    st.subheader("Line Scaling Tool")
    st.write("Scale and visualize lines based on different working areas")

    # Input for working areas
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Original Working Area")
        old_width = st.number_input("Original Width", value=1300, step=50)
        old_height = st.number_input("Original Height", value=1100, step=50)
    
    with col2:
        st.subheader("New Working Area")
        new_width = st.number_input("New Width", value=650, step=50)
        new_height = st.number_input("New Height", value=550, step=50)

    # Define default lines and parameters
    default_lines = [
        ((430, 120), (430, 1000)),  
        ((250, 1000), (250, 120)),  
        ((787, 120), (787, 1000)),  
        ((650, 1000), (650, 120)),  
        ((1100, 120), (1100, 1000)),
        ((1250, 1010), (790, 1010)),
        ((1250, 90), (790, 90)),  
        ((1250, 55), (1250, 1050))
    ]

    default_speed = [58.1, 282.7, 66.9, 138.9, 53.5, 229.7, 229.7, 111.5]
    default_t_cycle = [5, 20, 5, 5, 5, 20, 20, 5]
    default_t_pulse = [2, 2, 2, 2, 2, 2, 2, 2]

    # Create input for lines and parameters
    st.subheader("Line Parameters")
    
    # Initialize session state for lines if not exists
    if 'lines' not in st.session_state:
        st.session_state.lines = default_lines
        st.session_state.speed = default_speed
        st.session_state.t_cycle = default_t_cycle
        st.session_state.t_pulse = default_t_pulse

    # Display current lines and parameters in a table
    df_lines = pd.DataFrame([
        {
            "Line": f"Line {i+1}",
            "Speed (mm/s)": st.session_state.speed[i],
            "X start (mm)": round(line[0][0], 2),
            "Y start (mm)": round(line[0][1], 2),
            "X end (mm)": round(line[1][0], 2),
            "Y end (mm)": round(line[1][1], 2),
            "T cycle (ms)": st.session_state.t_cycle[i],
            "T pulse (ms)": st.session_state.t_pulse[i]
        }
        for i, line in enumerate(st.session_state.lines)
    ])

    st.dataframe(df_lines)

    if st.button("Scale Lines"):
        # Scale the lines
        old_area = (old_width, old_height)
        new_area = (new_width, new_height)
        scaled_lines = scale_lines(st.session_state.lines, old_area, new_area)

        # Create visualization
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Original Lines")
            fig_original = draw_lines(st.session_state.lines, old_area, title="Original Lines")
            st.pyplot(fig_original)
            
        with col2:
            st.subheader("Scaled Lines")
            fig_scaled = draw_lines(scaled_lines, new_area, title="Scaled Lines")
            st.pyplot(fig_scaled)

        # Display scaled results
        st.subheader("Scaled Line Parameters")
        df_scaled = pd.DataFrame([
            {
                "Line": f"Line {i+1}",
                "Speed (mm/s)": st.session_state.speed[i],
                "Original X start": round(line[0][0], 2),
                "Original Y start": round(line[0][1], 2),
                "Original X end": round(line[1][0], 2),
                "Original Y end": round(line[1][1], 2),
                "Scaled X start": round(scaled_line[0][0], 2),
                "Scaled Y start": round(scaled_line[0][1], 2),
                "Scaled X end": round(scaled_line[1][0], 2),
                "Scaled Y end": round(scaled_line[1][1], 2),
                "T cycle (ms)": st.session_state.t_cycle[i],
                "T pulse (ms)": st.session_state.t_pulse[i]
            }
            for i, (line, scaled_line) in enumerate(zip(st.session_state.lines, scaled_lines))
        ])
        
        st.dataframe(df_scaled)

# Add a footer with timestamp
st.markdown("---")
st.markdown(f"Last updated: {time.strftime('%Y-%m-%d %H:%M:%S')}")

# Auto-refresh functionality
if st.button("Refresh Data"):
    st.experimental_rerun()

# Add the line scaling functions
def scale_lines(lines, old_area, new_area):
    """
    Scales lines based on the resizing of the working area.
    """
    old_width, old_height = old_area
    new_width, new_height = new_area

    scale_x = new_width / old_width
    scale_y = new_height / old_height

    scaled_lines = [
        ((x1 * scale_x, y1 * scale_y), (x2 * scale_x, y2 * scale_y))
        for ((x1, y1), (x2, y2)) in lines
    ]

    return scaled_lines

def draw_lines(lines, area, title="Lines"):
    """
    Draws lines on a plot.
    """
    width, height = area
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(0, width * 1.08)
    ax.set_ylim(0, height * 1.08)
    ax.set_aspect('equal', adjustable='box')
    
    # Draw the working area edges
    ax.plot([0, width, width, 0, 0], [0, 0, height, height, 0], color='black', linestyle='-', linewidth=3)

    for ((x1, y1), (x2, y2)) in lines:
        ax.plot([x1, x2], [y1, y2], marker="o")

    # Annotate the width and height of the working area
    ax.annotate(f"Width: {width}", xy=(width / 2, height * 1.02), ha='center', fontsize=10, color='blue')
    ax.annotate(f"Height: {height}", xy=(width * 1.02, height / 2), va='center', rotation=-90, fontsize=10, color='blue')

    ax.set_title(title)
    ax.set_xlabel("Width")
    ax.set_ylabel("Height")
    ax.grid(True)
    
    return fig

def format_coordinates_to_decimal_places(line, decimals=2):
    """
    Formats the coordinates of a line to the specified number of decimal places.
    """
    start, end = line
    formatted_start = tuple(round(coord, decimals) for coord in start)
    formatted_end = tuple(round(coord, decimals) for coord in end)
    return formatted_start, formatted_end 