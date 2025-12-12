# AccuWeather Automation Testing Framework

A comprehensive Robot Framework automation solution for extracting and analyzing weather data from AccuWeather.com. This framework retrieves daily weather information for 30-45 days, validates temperature data, and generates detailed reports.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Running Tests](#running-tests)
- [Generated Reports](#generated-reports)

## Prerequisites

### Required Software
- **Python 3.8+** - [Download Python](https://www.python.org/downloads/)
- **Google Chrome** - [Download Chrome](https://googlechromelabs.github.io/chrome-for-testing/#stable)
- **Git** (optional) - [Download Git](https://git-scm.com/downloads/)

### Check Your Installation
```bash
# Check Python version
python --version
# Should show: Python 3.8.x or higher

# Check pip (Python package manager)
pip --version
```

## Installation

### Step 1: Download or Clone the Project

**Clone with Git**
```bash
git clone https://github.com/your-username/weather-automation.git
cd weather-automation
```

### Step 2: Install Python Dependencies

Open a terminal/command prompt in the project folder and run:

```bash
# Install required packages
pip install -r requirements.txt
```

### Step 3: Verify Installation

```bash
# Check if Robot Framework is installed
robot --version

```

## Project Structure

```
weather-automation/
├── Testcase/                          # Test files
│   └── weather_test.robot          # Main test file
├── Resources/                      # Reusable components  
│   ├── accuweather.json            # Data file prepare for test case
├── Libs/                           # Custom library  
│   ├── Share                       
│      ├── Keywords                 
│         ├── init.py               # export custom keywords
│         ├── common.py             # Custom keywords
│      ├── init.py                  # Declare and export custom libraries
├── Setup/                          # Reusable components  
│   ├── keywords.robot              # Contains suites setup/teawdown
├── Pages/                          # Test execution results
│   ├── locators.robot              # Contains locators
│   ├── actions.robot               # Contains actions
│   └── keywords.robot              # Contains keywords
├── Report/                         # Test execution results
│   ├── output.xml                  # Robot Framework output
│   ├── log.html                    # Detailed execution log
│   └── report.html                 # Test execution report
├── generated_reports/              # Auto-generated weather reports
│   ├── weather_report_YYYYMMDD_HHMMSS.txt
├── Drivers                        # Drivers
├── requirements.txt               # Python dependencies
├── run_tests.py                  # Python test runner
├── README.md                     # This file
└── .gitignore                    # Git ignore file
```

## Configuration

### Basic Configuration

Edit the variables in `.env`:

```
BASE_URL = https://www.accuweather.com
BROWSER = Chrome            # Chrome, Firefox, Edge
HEADLESS = false
TIMEOUT = 30
```

## Running Tests

### 1. Basic Test Run

```bash
# Run the weather automation test
robot -P ./Libs -d Report Testcase
```

### 1. Run individual test case 

```bash
# Run the weather automation test
robot -P ./Libs -d Report - i <tagname> Testcase

E.g:
robot -P ./Libs -d Report - i wearther_daily Testcase
```

### Expected Output
```
==============================================================================
Tests.Weather Test                                                            
==============================================================================
Weather Information Retrieval Test                                   | PASS |
------------------------------------------------------------------------------
Tests.Weather Test                                                    | PASS |
1 critical test, 1 passed, 0 failed
==============================================================================

Reports generated:
Output:  path\weather-automation\Report\output.xml
Log:     path\weather-automation\Report\log.html
Report:  path\weather-automation\Report\report.html

```

## Generated Reports

After running tests, you'll get several types of reports:

### 1. Weather Report (`weather_report_TIMESTAMP.txt`)
```
====================================================================================================
ACCUWEATHER AUTOMATION TEST REPORT
====================================================================================================
Generated: 2024-12-27 14:30:15
Total Days Analyzed: 45

EXECUTIVE SUMMARY
--------------------------------------------------
Successfully processed: 43/45 days (95.6%)
Average temperature: 78.5°F (25.8°C)
Most common weather: Partly Cloudy (12 days)

DAILY WEATHER DETAILS
--------------------------------------------------
DAY 1: Thursday, November 8
   Temperature: 88°F (31.1°C)  
   Condition: Mostly sunny
   RealFeel: 103°F
   Humidity: 76%
```

### 2. Summary Report (`weather_summary_TIMESTAMP.txt`)
Quick overview with key metrics and statistics.

### 3. CSV Export (`weather_data_TIMESTAMP.csv`)
Excel-compatible data file for further analysis.

### 4. Robot Framework Reports
- `log.html` - Detailed test execution log
- `report.html` - Test execution summary
- `output.xml` - Raw test data
