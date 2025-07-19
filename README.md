
# 📊 Interactive Data Visualizer

A modern Python desktop application for visualizing CSV data interactively. Built with Tkinter, Pandas, and Matplotlib, it features a clean UI, chart customization, and robust error handling.

## Features
- **Upload CSV**: Easily load any CSV file.
- **Dynamic Column Selection**: Listbox updates based on chart type.
- **Chart Types**: Bar Chart, Line Plot, Pie Chart, Scatter Plot, Histogram.
- **Custom Marker Style & Color**: Choose marker style and color for Line and Scatter plots.
- **Status Messages**: Clear feedback for user actions and errors.
- **Modern UI**: Styled with colors, icons, and fonts for a professional look.

## Requirements
- Python 3.7+
- pandas
- matplotlib

Install dependencies:
```bash
pip install pandas matplotlib
```

## Usage
1. Run the application:
    ```bash
    python main.py
    ```
2. Click "📂 Upload CSV File" to select your data file.
3. Choose chart type, columns, marker style, and color as needed.
4. Click "📊 Generate Chart" to view your visualization.

## Chart Types
- **Bar Chart**: Sum of selected columns, values shown on bars.
- **Line Plot**: Line(s) for selected columns, customizable marker and color.
- **Pie Chart**: Distribution of values in a selected column (top 10 + others).
- **Scatter Plot**: Relationship between two numeric columns, customizable marker and color.
- **Histogram**: Distribution of values in selected columns, with 30 bins.

## Error Handling
- Status label and popups for missing files, invalid selections, or chart errors.

## Customization
- Marker style and color for Line and Scatter plots.
- Pie chart shows top 10 categories, grouping others for clarity.

## License
MIT License
