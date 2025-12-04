import sys
from typing import Tuple
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def load_and_clean_data(file_path: str) -> pd.DataFrame:
    """
    Reads CSV, parses 'Date' to datetime, sets it as index,
    and linearly interpolates missing numeric values.
    """
    df = pd.read_csv(file_path)

    if 'Date' not in df.columns:
        raise ValueError("CSV must contain a 'Date' column")

    df['Date'] = pd.to_datetime(df['Date'])
    df = df.set_index('Date').sort_index()

    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 0:
        df[numeric_cols] = df[numeric_cols].interpolate(method='linear', limit_direction='both')

    return df


def analyze_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Resamples to monthly ('M') and computes:
    - mean/min/max for Temperature_C
    - total (sum) for Rainfall_mm
    Returns a DataFrame with columns: MonthlyMeanTemp, MonthlyMinTemp, MonthlyMaxTemp, MonthlyTotalRainfall.
    """
    if 'Temperature_C' not in df.columns:
        raise ValueError("DataFrame must contain 'Temperature_C' column")
    if 'Rainfall_mm' not in df.columns:
        raise ValueError("DataFrame must contain 'Rainfall_mm' column")

    monthly_mean_temp = df['Temperature_C'].resample('ME').mean()
    monthly_min_temp = df['Temperature_C'].resample('ME').min()
    monthly_max_temp = df['Temperature_C'].resample('ME').max()
    monthly_total_rain = df['Rainfall_mm'].resample('ME').sum()

    df_monthly = pd.DataFrame({
        'MonthlyMeanTemp': monthly_mean_temp,
        'MonthlyMinTemp': monthly_min_temp,
        'MonthlyMaxTemp': monthly_max_temp,
        'MonthlyTotalRainfall': monthly_total_rain,
    })

    return df_monthly


def create_visualizations(df_monthly: pd.DataFrame) -> Tuple[plt.Figure, plt.Axes]:
    """
    Generates three plots:
    1) Line chart for monthly mean temperature
    2) Bar chart for monthly total rainfall
    3) Combined figure with twin axes (line + bars)
    Returns the combined figure and its primary axis.
    """
    fig1, ax1 = plt.subplots(figsize=(10, 4))
    ax1.plot(df_monthly.index, df_monthly['MonthlyMeanTemp'], color='tab:red', linewidth=2)
    ax1.set_title('Monthly Mean Temperature (°C)')
    ax1.set_xlabel('Month')
    ax1.set_ylabel('Temperature (°C)')
    fig1.tight_layout()

    fig2, ax2 = plt.subplots(figsize=(10, 4))
    ax2.bar(df_monthly.index, df_monthly['MonthlyTotalRainfall'], color='tab:blue', width=20)  # width ~ days
    ax2.set_title('Monthly Total Rainfall (mm)')
    ax2.set_xlabel('Month')
    ax2.set_ylabel('Rainfall (mm)')
    fig2.tight_layout()

    fig3, ax3 = plt.subplots(figsize=(11, 5))
    ax3.plot(df_monthly.index, df_monthly['MonthlyMeanTemp'], color='tab:red', linewidth=2, label='Mean Temp (°C)')
    ax3.set_xlabel('Month')
    ax3.set_ylabel('Temperature (°C)', color='tab:red')
    ax3.tick_params(axis='y', labelcolor='tab:red')

    ax3b = ax3.twinx()
    ax3b.bar(df_monthly.index, df_monthly['MonthlyTotalRainfall'], color='tab:blue', alpha=0.6, width=20, label='Total Rainfall (mm)')
    ax3b.set_ylabel('Rainfall (mm)', color='tab:blue')
    ax3b.tick_params(axis='y', labelcolor='tab:blue')

    fig3.suptitle('Monthly Temperature and Rainfall')
    lines, labels = ax3.get_legend_handles_labels()
    lines2, labels2 = ax3b.get_legend_handles_labels()
    ax3.legend(lines + lines2, labels + labels2, loc='upper left')

    fig3.tight_layout()
    return fig3, ax3


def main(argv=None):
    argv = argv or sys.argv[1:]
    if len(argv) < 1:
        print("Usage: python weather_analysis.py <path_to_csv>")
        print("CSV must include columns: 'Date', 'Temperature_C', 'Rainfall_mm'")
        return 1

    file_path = argv[0]
    df = load_and_clean_data(file_path)
    df_monthly = analyze_data(df)
    fig, _ = create_visualizations(df_monthly)

    output_path = 'output_plot.png'
    fig.savefig(output_path, dpi=150)
    print(f"Saved combined plot to {output_path}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())