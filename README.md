# ISO Metric Thread Calculator for Autodesk Inventor

A professional GUI-based calculator for ISO metric thread dimensions, designed to generate accurate thread parameters for Autodesk Inventor and general manufacturing applications.

## Author
**Paradorn Katananon**

## Features

- **Accurate ISO Standard Calculations**
  - Based on ISO 68-1 (thread profile) and ISO 965-1 (tolerances)
  - Supports external threads (bolts) and internal threads (nuts)
  - Tolerance classes: 6g (external) and 6H (internal)

- **Comprehensive Results**
  - Major, pitch, and minor diameters (max/min values)
  - Tap drill diameter for internal threads
  - Thread depth (2× nominal diameter - matches Inventor)
  - Thread runout length

- **User-Friendly GUI**
  - Clean, intuitive interface built with tkinter
  - Real-time calculation with input validation
  - Formatted results display with color-coded sections
  - 4-digit precision for all measurements

- **Export Functionality**
  - Export results to CSV format
  - Compatible with spreadsheet applications
  - Includes complete dimensional data

## Requirements

- Python 3.x
- tkinter (included with standard Python installation)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/paradonk/inventorthread.git
cd inventorthread
```

2. Run the application:
```bash
python inv_thread.py
```

## Usage

1. **Enter Thread Parameters:**
   - Thread Size (mm): e.g., 20 for M20
   - Pitch (mm): e.g., 2.0 for 2mm pitch
   - Select tolerance classes (default: 6g/6H)

2. **Calculate:**
   - Click "Calculate" to compute all thread dimensions

3. **Export:**
   - Click "Export to CSV" to save results to a file

4. **Clear:**
   - Click "Clear" to reset the results display

## Thread Depth Calculation

This calculator uses **2× nominal diameter** for thread depth, matching Autodesk Inventor's approach:

```
Thread Depth = 2.0 × Nominal Diameter
```

This practical formula accounts for:
- Thread runout zones
- Tap geometry clearance
- Chip clearance
- Incomplete threads at the bottom

## Example

For **M20×2.0** thread:
- Thread Depth: 40.0000 mm
- Tap Drill: 17.2948 mm
- External Major (6g): 19.9520 - 19.6906 mm
- Internal Pitch (6H): 18.3505 - 18.5104 mm

## Technical Background

The calculator implements:
- **H value**: 0.866025 × pitch (fundamental triangle height)
- **Basic diameters**: Per ISO 68-1 formulas
- **Tolerance zones**: Dynamic calculation based on ISO 965-1
- **Precision**: 4 decimal places for manufacturing accuracy

## License

MIT License - Feel free to use and modify for your projects.

## Contributing

Contributions, issues, and feature requests are welcome!

## Acknowledgments

Based on ISO 68-1 and ISO 965-1 international standards for metric screw threads.
