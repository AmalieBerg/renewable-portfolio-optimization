"""
Visualization Module

Utility functions for creating consistent, publication-quality plots.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from typing import Optional, List, Tuple
from pathlib import Path

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
FIGURES_DIR = PROJECT_ROOT / "results" / "figures"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)


def plot_price_timeseries(
    df: pd.DataFrame,
    price_col: str = 'dam_price',
    datetime_col: str = 'datetime',
    title: str = 'ERCOT Day-Ahead Market Prices',
    save_path: Optional[str] = None
) -> plt.Figure:
    """
    Plot electricity price time series.
    
    Args:
        df: DataFrame with price data
        price_col: Name of price column
        datetime_col: Name of datetime column
        title: Plot title
        save_path: Optional path to save figure
        
    Returns:
        matplotlib Figure object
    """
    fig, ax = plt.subplots(figsize=(14, 6))
    
    ax.plot(df[datetime_col], df[price_col], linewidth=0.5, alpha=0.7)
    ax.set_xlabel('Date')
    ax.set_ylabel('Price ($/MWh)')
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    # Add summary statistics
    mean_price = df[price_col].mean()
    ax.axhline(mean_price, color='r', linestyle='--', linewidth=1, 
               label=f'Mean: ${mean_price:.2f}/MWh')
    ax.legend()
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(FIGURES_DIR / save_path, dpi=300, bbox_inches='tight')
        print(f"Saved to {FIGURES_DIR / save_path}")
    
    return fig


def plot_price_distribution(
    df: pd.DataFrame,
    price_col: str = 'dam_price',
    title: str = 'Price Distribution',
    save_path: Optional[str] = None
) -> plt.Figure:
    """
    Plot price distribution with statistics.
    
    Args:
        df: DataFrame with price data
        price_col: Name of price column
        title: Plot title
        save_path: Optional path to save figure
        
    Returns:
        matplotlib Figure object
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Histogram
    ax1.hist(df[price_col], bins=50, alpha=0.7, edgecolor='black')
    ax1.axvline(df[price_col].mean(), color='r', linestyle='--', 
                linewidth=2, label=f"Mean: ${df[price_col].mean():.2f}")
    ax1.axvline(df[price_col].median(), color='g', linestyle='--', 
                linewidth=2, label=f"Median: ${df[price_col].median():.2f}")
    ax1.set_xlabel('Price ($/MWh)')
    ax1.set_ylabel('Frequency')
    ax1.set_title('Price Histogram')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Box plot
    ax2.boxplot(df[price_col], vert=True)
    ax2.set_ylabel('Price ($/MWh)')
    ax2.set_title('Price Box Plot')
    ax2.grid(True, alpha=0.3)
    
    fig.suptitle(title, fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    if save_path:
        plt.savefig(FIGURES_DIR / save_path, dpi=300, bbox_inches='tight')
        print(f"Saved to {FIGURES_DIR / save_path}")
    
    return fig


def plot_hourly_patterns(
    df: pd.DataFrame,
    value_col: str = 'dam_price',
    datetime_col: str = 'datetime',
    title: str = 'Hourly Price Patterns',
    save_path: Optional[str] = None
) -> plt.Figure:
    """
    Plot average patterns by hour of day.
    
    Args:
        df: DataFrame with data
        value_col: Name of value column to plot
        datetime_col: Name of datetime column
        title: Plot title
        save_path: Optional path to save figure
        
    Returns:
        matplotlib Figure object
    """
    # Calculate hourly statistics
    df = df.copy()
    df['hour'] = pd.to_datetime(df[datetime_col]).dt.hour
    hourly_stats = df.groupby('hour')[value_col].agg(['mean', 'std', 'min', 'max'])
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    hours = hourly_stats.index
    ax.plot(hours, hourly_stats['mean'], 'b-', linewidth=2, marker='o', label='Mean')
    ax.fill_between(hours, 
                     hourly_stats['mean'] - hourly_stats['std'],
                     hourly_stats['mean'] + hourly_stats['std'],
                     alpha=0.3, label='±1 Std Dev')
    
    ax.set_xlabel('Hour of Day')
    ax.set_ylabel(f'{value_col}')
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_xticks(range(0, 24))
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(FIGURES_DIR / save_path, dpi=300, bbox_inches='tight')
        print(f"Saved to {FIGURES_DIR / save_path}")
    
    return fig


def plot_seasonal_patterns(
    df: pd.DataFrame,
    value_col: str = 'dam_price',
    datetime_col: str = 'datetime',
    title: str = 'Seasonal Patterns',
    save_path: Optional[str] = None
) -> plt.Figure:
    """
    Plot seasonal patterns by month.
    
    Args:
        df: DataFrame with data
        value_col: Name of value column to plot
        datetime_col: Name of datetime column
        title: Plot title
        save_path: Optional path to save figure
        
    Returns:
        matplotlib Figure object
    """
    df = df.copy()
    df['month'] = pd.to_datetime(df[datetime_col]).dt.month
    monthly_stats = df.groupby('month')[value_col].agg(['mean', 'std'])
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    months = monthly_stats.index
    ax.bar(months, monthly_stats['mean'], yerr=monthly_stats['std'], 
           capsize=5, alpha=0.7, edgecolor='black')
    
    ax.set_xlabel('Month')
    ax.set_ylabel(f'Average {value_col}')
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_xticks(range(1, 13))
    ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(FIGURES_DIR / save_path, dpi=300, bbox_inches='tight')
        print(f"Saved to {FIGURES_DIR / save_path}")
    
    return fig


def plot_correlation_heatmap(
    df: pd.DataFrame,
    columns: Optional[List[str]] = None,
    title: str = 'Feature Correlations',
    save_path: Optional[str] = None
) -> plt.Figure:
    """
    Plot correlation heatmap.
    
    Args:
        df: DataFrame with data
        columns: List of columns to include (None for all numeric)
        title: Plot title
        save_path: Optional path to save figure
        
    Returns:
        matplotlib Figure object
    """
    if columns:
        corr = df[columns].corr()
    else:
        corr = df.select_dtypes(include=[np.number]).corr()
    
    fig, ax = plt.subplots(figsize=(12, 10))
    
    sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm', 
                center=0, square=True, ax=ax, cbar_kws={'shrink': 0.8})
    
    ax.set_title(title, fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    if save_path:
        plt.savefig(FIGURES_DIR / save_path, dpi=300, bbox_inches='tight')
        print(f"Saved to {FIGURES_DIR / save_path}")
    
    return fig


def plot_scatter_with_regression(
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    title: str = 'Scatter Plot',
    save_path: Optional[str] = None
) -> plt.Figure:
    """
    Plot scatter plot with regression line.
    
    Args:
        df: DataFrame with data
        x_col: Name of x-axis column
        y_col: Name of y-axis column
        title: Plot title
        save_path: Optional path to save figure
        
    Returns:
        matplotlib Figure object
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Scatter plot
    ax.scatter(df[x_col], df[y_col], alpha=0.5, s=10)
    
    # Regression line
    z = np.polyfit(df[x_col].dropna(), df[y_col].dropna(), 1)
    p = np.poly1d(z)
    ax.plot(df[x_col], p(df[x_col]), "r--", linewidth=2, 
            label=f'y = {z[0]:.2f}x + {z[1]:.2f}')
    
    # Calculate R²
    from scipy import stats
    slope, intercept, r_value, p_value, std_err = stats.linregress(
        df[x_col].dropna(), df[y_col].dropna()
    )
    ax.text(0.05, 0.95, f'R² = {r_value**2:.3f}', 
            transform=ax.transAxes, fontsize=12,
            verticalalignment='top', bbox=dict(boxstyle='round', 
            facecolor='wheat', alpha=0.5))
    
    ax.set_xlabel(x_col)
    ax.set_ylabel(y_col)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(FIGURES_DIR / save_path, dpi=300, bbox_inches='tight')
        print(f"Saved to {FIGURES_DIR / save_path}")
    
    return fig


def create_summary_dashboard(
    df: pd.DataFrame,
    save_path: str = 'summary_dashboard.png'
) -> plt.Figure:
    """
    Create a comprehensive summary dashboard.
    
    Args:
        df: DataFrame with all data
        save_path: Path to save figure
        
    Returns:
        matplotlib Figure object
    """
    fig = plt.figure(figsize=(16, 12))
    gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
    
    # Price time series
    ax1 = fig.add_subplot(gs[0, :])
    ax1.plot(df['datetime'], df['dam_price'], linewidth=0.5, alpha=0.7)
    ax1.set_title('Price Time Series', fontweight='bold')
    ax1.set_ylabel('Price ($/MWh)')
    ax1.grid(True, alpha=0.3)
    
    # Price distribution
    ax2 = fig.add_subplot(gs[1, 0])
    ax2.hist(df['dam_price'], bins=50, alpha=0.7, edgecolor='black')
    ax2.set_title('Price Distribution', fontweight='bold')
    ax2.set_xlabel('Price ($/MWh)')
    ax2.set_ylabel('Frequency')
    ax2.grid(True, alpha=0.3)
    
    # Hourly pattern
    ax3 = fig.add_subplot(gs[1, 1])
    hourly = df.groupby(df['datetime'].dt.hour)['dam_price'].mean()
    ax3.plot(hourly.index, hourly.values, marker='o')
    ax3.set_title('Average Hourly Pattern', fontweight='bold')
    ax3.set_xlabel('Hour')
    ax3.set_ylabel('Avg Price')
    ax3.grid(True, alpha=0.3)
    
    # Monthly pattern
    ax4 = fig.add_subplot(gs[1, 2])
    monthly = df.groupby(df['datetime'].dt.month)['dam_price'].mean()
    ax4.bar(monthly.index, monthly.values, alpha=0.7, edgecolor='black')
    ax4.set_title('Average Monthly Pattern', fontweight='bold')
    ax4.set_xlabel('Month')
    ax4.set_ylabel('Avg Price')
    ax4.grid(True, alpha=0.3, axis='y')
    
    # Renewable generation
    ax5 = fig.add_subplot(gs[2, 0])
    ax5.plot(df['datetime'], df['wind_generation_mw'], 
             linewidth=0.5, alpha=0.7, label='Wind')
    ax5.plot(df['datetime'], df['solar_generation_mw'], 
             linewidth=0.5, alpha=0.7, label='Solar')
    ax5.set_title('Renewable Generation', fontweight='bold')
    ax5.set_ylabel('Generation (MW)')
    ax5.legend()
    ax5.grid(True, alpha=0.3)
    
    # Load vs Renewables
    ax6 = fig.add_subplot(gs[2, 1])
    daily_df = df.set_index('datetime').resample('D').mean()
    ax6.scatter(daily_df['system_load_mw'], daily_df['total_renewable_mw'], 
                alpha=0.5)
    ax6.set_title('Load vs Renewable Generation', fontweight='bold')
    ax6.set_xlabel('System Load (MW)')
    ax6.set_ylabel('Renewable Gen (MW)')
    ax6.grid(True, alpha=0.3)
    
    # Price vs Temperature
    ax7 = fig.add_subplot(gs[2, 2])
    ax7.scatter(df['temperature_f'], df['dam_price'], alpha=0.3, s=5)
    ax7.set_title('Price vs Temperature', fontweight='bold')
    ax7.set_xlabel('Temperature (°F)')
    ax7.set_ylabel('Price ($/MWh)')
    ax7.grid(True, alpha=0.3)
    
    fig.suptitle('ERCOT Market Data Summary Dashboard', 
                 fontsize=16, fontweight='bold')
    
    plt.savefig(FIGURES_DIR / save_path, dpi=300, bbox_inches='tight')
    print(f"Dashboard saved to {FIGURES_DIR / save_path}")
    
    return fig
