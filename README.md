# Aditya Singh Sales Analytics Assignment

## Overview
This system processes sales data, generates analytics, fetches product details from an external API, and produces a comprehensive report.

## Setup Instructions

1.  **Helper Library Installation**:
    Ensure you have Python installed. Install the required libraries:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Data Placement**:
    Ensure `sales_data.txt` is located in the `data/` folder.

## How to Run

Run the main script to process data and generate reports:
```bash
python main.py
```

## Outputs

*   **`output/sales_report.txt`**: The final analytics report.
*   **`output/enriched_sales_data.txt`**: A CSV-like file containing transactions enriched with API data.

## Project Structure
*   `data/`: Input data.
*   `utils/`: Helper modules for file handling, processing, API, and reporting.
*   `output/`: Generated results.
*   `main.py`: Main execution script.
*   `test_assignment.py`: Verification tests.
