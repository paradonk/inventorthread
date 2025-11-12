# ISO Metric Thread Calculator for Autodesk Inventor

**Create custom ISO metric threads with ANY size and pitch combination - even those not available in Inventor's built-in thread library!**

## Why Use This Calculator?

Autodesk Inventor's thread library only includes standard thread sizes and pitches defined in the ThreadData.xml file. But what if you need:
- **Non-standard pitches** (e.g., M20×1.75 instead of the standard M20×2.5)
- **Custom thread sizes** not in Inventor's library
- **Special applications** requiring unique thread combinations
- **Prototype designs** with non-standard specifications

This calculator solves that problem by generating accurate ISO-compliant thread dimensions for **any size and pitch combination**, ready to import into Inventor or use for manufacturing.

## Author
**Paradorn Katananon**

## Key Features

- **Unlimited Custom Threads**
  - ANY thread size and pitch combination
  - Not limited to Inventor's pre-defined thread library
  - Create non-standard threads for special applications
  - Perfect for prototypes and custom designs

- **Accurate ISO Standard Calculations**
  - Based on ISO 68-1 (thread profile) and ISO 965-1 (tolerances)
  - Supports external threads (bolts) and internal threads (nuts)
  - Tolerance classes: 6g (external) and 6H (internal)
  - 4-digit precision for manufacturing accuracy

- **Complete Thread Data**
  - Major, pitch, and minor diameters (max/min values)
  - Tap drill diameter for internal threads
  - Thread depth (2× nominal diameter - matches Inventor standard)
  - Thread runout length for machining
  - All dimensions ready for production

- **User-Friendly GUI**
  - Clean, intuitive interface built with tkinter
  - Real-time calculation with input validation
  - Formatted results display with color-coded sections
  - No installation required (just Python)

- **Export Functionality**
  - Export results to CSV format
  - Easy documentation and record-keeping
  - Compatible with Excel/spreadsheet applications
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

## Examples

### Standard Thread
For **M20×2.5** (standard, available in Inventor):
- Thread Depth: 40.0000 mm
- Tap Drill: 17.2948 mm
- External Major (6g): 19.9400 - 19.6786 mm
- Internal Pitch (6H): 17.6255 - 17.7854 mm

### Custom Thread (NOT in Inventor's library)
For **M20×1.75** (non-standard pitch):
- Thread Depth: 40.0000 mm
- Tap Drill: 18.1032 mm
- External Major (6g): 19.9580 - 19.7436 mm
- Internal Pitch (6H): 18.4756 - 18.6164 mm

### Special Application
For **M15×1.25** (uncommon size):
- Thread Depth: 30.0000 mm
- Tap Drill: 13.6468 mm
- External Major (6g): 14.9700 - 14.7858 mm
- Internal Pitch (6H): 13.8255 - 13.9414 mm

## Using with Autodesk Inventor

1. **Calculate** your custom thread dimensions using this tool
2. **Export to CSV** for documentation
3. **Manually edit** Inventor's ThreadData.xml file (in your Design Data folder) to add the custom thread
4. **Or use** the dimensions directly when modeling custom threads in Inventor

**Note:** Always backup your ThreadData.xml before editing!

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
