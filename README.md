# Dashboard PyQT
This repository contains a PyQT-based dashboard for structural deformation analysis and damage detection. The dashboard provides an intuitive interface to visualize and analyze structural health data collected from various sensors.

# Project Documentation

## Overview
This repository contains a **PyQT-based dashboard** for **structural deformation analysis and damage detection**. The dashboard provides an intuitive interface to visualize and analyze structural health data collected from various sensors.

## Project Structure
```
├── acc_data.csv                         # Accelerometer data
├── damage_detection.py                   # Damage detection module
├── dashboard.py                           # Main entry point - PyQT Dashboard
├── deformation_analysis.py                # Deformation analysis module
├── heatmap.csv                            # Heatmap data for visualization
├── heatmap_extrapolated_corrected.csv     # Processed heatmap data
├── images/                                # Directory for UI and analysis-related images
│   ├── Camera.jpg
│   ├── Cost.jpg
│   ├── Crack_Det.jpg
│   ├── Damage.jpg
│   ├── Deformation.jpg
│   ├── Load.jpg
│   ├── Maintenance.jpg
│   ├── Musaffah_Bridge.jpg
│   ├── Real_Life_Response.jpg
│   ├── SHI.jpg
│   ├── Strain.jpg
│   ├── Suggestions.jpg
│   ├── Traffic.jpg
│   ├── Uncertainty.jpg
│   ├── accelerometer.jpg
│   ├── accelerometer_img.jpg
│   ├── bridge_image.png
│   ├── displacement_sensor_img.jpg
│   ├── sensor.jpg
│   └── strain_gauge_img.jpeg
├── model_main.py                          # Main computational model for analysis
├── nodes.csv                              # Node coordinates for visualization
├── nodes_animated.csv                     # Animated nodes for simulation
├── sensor_data_acc.csv                    # Sensor acceleration data
├── strain_data.csv                        # Strain gauge data
```

## Features
- **PyQT-based Dashboard (`dashboard.py`)**:
  - Interactive UI for loading and analyzing structural data.
  - Displays damage detection results and deformation analysis.
  - Provides heatmaps and sensor data visualization.
  
- **Deformation Analysis (`deformation_analysis.py`)**:
  - Processes node data to visualize structural deformations.
  - Uses heatmaps to represent strain and displacement.
  
- **Damage Detection (`damage_detection.py`)**:
  - Implements damage detection algorithms.
  - Processes input from strain and accelerometer sensors.
  
- **Sensor Data Processing (`model_main.py`)**:
  - Handles input data from accelerometers and strain gauges.
  - Computes relevant structural health metrics.
  
## Installation & Setup
### Prerequisites
Ensure you have **Python 3.x** installed along with the following dependencies:
```
pip install PyQt5 pandas numpy matplotlib
```

### Running the Dashboard
To launch the PyQT Dashboard, run:
```
python dashboard.py
```

## Data Files Description
- **`acc_data.csv`**: Accelerometer readings.
- **`sensor_data_acc.csv`**: Additional accelerometer data.
- **`strain_data.csv`**: Strain gauge readings for structural analysis.
- **`nodes.csv`**: Node positions for structural visualization.
- **`heatmap.csv`**: Initial heatmap data for deformation analysis.
- **`heatmap_extrapolated_corrected.csv`**: Processed heatmap data for improved visualization.

## Usage
1. **Launch the Dashboard (`dashboard.py`)**.
2. **Navigate through the UI** to select deformation analysis or damage detection.
3. **Load relevant datasets** and view visualizations.
4. **Analyze damage locations and deformation trends**.
5. **Use insights for structural health monitoring and maintenance planning**.

## Future Improvements
- Implement AI-based anomaly detection for better damage identification.
- Enhance real-time sensor data streaming capabilities.
- Integrate 3D visualization for better insights into structural health.


# CN_project1
