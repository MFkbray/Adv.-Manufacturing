# Advanced Manufacturing Web App

A comprehensive web application built with Streamlit for manufacturing control, data management, and line scaling operations.

## Features

### 1. Equipment Dashboard
- Real-time monitoring of manufacturing equipment status
- Interactive control panel for each machine
- System metrics display including:
  - Total uptime
  - Active machines count
  - System efficiency

### 2. File Management
- Browse and navigate directories
- Batch file selection and renaming
- File filtering and sorting capabilities
- Detailed file information display (size, modification date)
- Support for adding prefixes and text replacement

### 3. Excel Row Exporter
- Upload and process Excel files
- Select specific sheets and row ranges
- Export selected rows to individual CSV files
- Customizable output directory

### 4. Data Structure Creator
Two methods available:
1. Excel File Upload
   - Process multiple Sample IDs from Excel
   - Batch folder creation
2. Manual Sample ID Entry
   - Single folder structure creation
   - Custom naming

Folder Structure Options:
- Fabrication folders
- Inspection folders
- Standardized hierarchy:
  ```
  Run={Sample_ID}/
  ├── Stage=source_data/
  │   ├── Modality=record_manufacture/
  │   ├── Modality=optical_image/
  │   ├── Modality=sem_c_0deg/
  │   ├── Modality=sem_c_high_angle/
  │   ├── Modality=sem_c_medium_angle/
  │   ├── Modality=sem_p_0deg/
  │   ├── Modality=sem_p_high_angle/
  │   └── Modality=sem_p_medium_angle/
  ```

### 5. Line Scaling Tool
- Scale and visualize manufacturing lines between different working areas
- Features include:
  - Interactive dimension input
  - Visual representation of original and scaled lines
  - Detailed parameter tables
  - Speed and timing preservation
  - Real-time visualization updates

## Installation

1. Ensure Python 3.7+ is installed on your system
2. Install required packages:
```bash
pip install streamlit pandas matplotlib numpy
```

## Usage

1. Navigate to the application directory:
```bash
cd "Advanced Manufacturing Web App"
```

2. Run the Streamlit application:
```bash
streamlit run streamlit_app.py
```

3. Access the web interface at `http://localhost:8501` in your browser

## Dependencies
- Python 3.7+
- Streamlit
- Pandas
- Matplotlib
- NumPy

## Data Management
The application handles various data types:
- Excel files (.xlsx, .xls)
- CSV files
- Directory structures
- Manufacturing line coordinates
- Equipment status data

## Contributing
Feel free to submit issues and enhancement requests.

## License
This project is licensed under the MIT License - see the LICENSE file for details. 