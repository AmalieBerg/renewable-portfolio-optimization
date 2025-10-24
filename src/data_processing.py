"""
Data Processing Module

Handles downloading, cleaning, and processing data from ERCOT and other sources.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, Tuple
import requests
from tqdm import tqdm
import warnings

warnings.filterwarnings('ignore')

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_RAW = PROJECT_ROOT / "data" / "raw"
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"

# Ensure directories exist
DATA_RAW.mkdir(parents=True, exist_ok=True)
DATA_PROCESSED.mkdir(parents=True, exist_ok=True)


class ERCOTDataLoader:
    """
    Download and process ERCOT market data.
    
    ERCOT provides several types of data:
    - Day-Ahead Market (DAM) prices
    - Real-Time Market (RTM) prices
    - Load (demand) data
    - Wind and Solar generation data
    """
    
    def __init__(self):
        self.base_url = "http://www.ercot.com/misapp/servlets/"
        self.data_raw = DATA_RAW
        self.data_processed = DATA_PROCESSED
        
    def download_dam_prices(
        self, 
        start_date: str = "2023-01-01", 
        end_date: str = "2024-12-31"
    ) -> pd.DataFrame:
        """
        Download Day-Ahead Market settlement point prices.
        
        Args:
            start_date: Start date in 'YYYY-MM-DD' format
            end_date: End date in 'YYYY-MM-DD' format
            
        Returns:
            DataFrame with DAM prices
            
        Note:
            For this initial version, we'll create synthetic data that mimics
            real ERCOT price patterns. In production, you would use the actual
            ERCOT API or download historical data files.
        """
        print(f"Generating synthetic ERCOT DAM price data from {start_date} to {end_date}")
        print("Note: Replace with actual ERCOT API calls for production use")
        
        # Create date range
        dates = pd.date_range(start=start_date, end=end_date, freq='H')
        
        # Generate synthetic prices that mimic ERCOT patterns
        np.random.seed(42)
        n = len(dates)
        
        # Base price with seasonal pattern
        day_of_year = dates.dayofyear
        seasonal_pattern = 30 + 10 * np.sin(2 * np.pi * day_of_year / 365)
        
        # Hourly pattern (higher during day, lower at night)
        hourly_pattern = 15 * np.sin(2 * np.pi * (dates.hour - 6) / 24)
        
        # Add weekly pattern (lower on weekends)
        weekly_pattern = -5 * (dates.dayofweek >= 5).astype(int)
        
        # Add random component with occasional spikes
        random_component = np.random.normal(0, 5, n)
        spikes = np.random.choice([0, 50], size=n, p=[0.98, 0.02])  # 2% spike probability
        
        # Combine components
        prices = seasonal_pattern + hourly_pattern + weekly_pattern + random_component + spikes
        prices = np.maximum(prices, 0)  # Prices can't be negative
        
        # Create DataFrame
        df = pd.DataFrame({
            'datetime': dates,
            'settlement_point': 'HB_HOUSTON',
            'dam_price': prices
        })
        
        # Save to file
        output_file = self.data_raw / "ercot_dam_prices.csv"
        df.to_csv(output_file, index=False)
        print(f"Saved to {output_file}")
        
        return df
    
    def download_load_data(
        self,
        start_date: str = "2023-01-01",
        end_date: str = "2024-12-31"
    ) -> pd.DataFrame:
        """
        Download ERCOT system-wide load (demand) data.
        
        Args:
            start_date: Start date in 'YYYY-MM-DD' format
            end_date: End date in 'YYYY-MM-DD' format
            
        Returns:
            DataFrame with hourly load data
        """
        print(f"Generating synthetic ERCOT load data from {start_date} to {end_date}")
        
        dates = pd.date_range(start=start_date, end=end_date, freq='H')
        np.random.seed(43)
        
        # Base load with seasonal pattern
        day_of_year = dates.dayofyear
        # Higher in summer (cooling) and winter (heating)
        seasonal = 50000 + 15000 * np.abs(np.sin(2 * np.pi * day_of_year / 365))
        
        # Hourly pattern
        hourly = 10000 * np.sin(2 * np.pi * (dates.hour - 6) / 24)
        
        # Weekend reduction
        weekend_factor = 0.9 ** (dates.dayofweek >= 5).astype(int)
        
        # Random variation
        noise = np.random.normal(0, 2000, len(dates))
        
        load = (seasonal + hourly) * weekend_factor + noise
        load = np.maximum(load, 0)
        
        df = pd.DataFrame({
            'datetime': dates,
            'system_load_mw': load
        })
        
        output_file = self.data_raw / "ercot_load.csv"
        df.to_csv(output_file, index=False)
        print(f"Saved to {output_file}")
        
        return df
    
    def download_renewable_generation(
        self,
        start_date: str = "2023-01-01",
        end_date: str = "2024-12-31"
    ) -> pd.DataFrame:
        """
        Download renewable generation data (wind and solar).
        
        Args:
            start_date: Start date in 'YYYY-MM-DD' format
            end_date: End date in 'YYYY-MM-DD' format
            
        Returns:
            DataFrame with renewable generation by type
        """
        print(f"Generating synthetic renewable generation data from {start_date} to {end_date}")
        
        dates = pd.date_range(start=start_date, end=end_date, freq='H')
        np.random.seed(44)
        
        # Wind generation (24/7 but variable)
        wind_capacity = 30000  # MW
        # Higher in winter/spring
        day_of_year = dates.dayofyear
        wind_seasonal = 0.4 + 0.3 * np.sin(2 * np.pi * (day_of_year - 90) / 365)
        wind_hourly = 0.8 + 0.2 * np.random.random(len(dates))
        wind_gen = wind_capacity * wind_seasonal * wind_hourly
        
        # Solar generation (daytime only)
        solar_capacity = 15000  # MW
        # Peak around 3 PM, zero at night
        solar_hourly = np.maximum(0, np.sin(np.pi * (dates.hour - 6) / 12))
        # Higher in summer
        solar_seasonal = 0.5 + 0.3 * np.sin(2 * np.pi * (day_of_year - 172) / 365)
        # Cloud variation
        solar_clouds = 0.7 + 0.3 * np.random.random(len(dates))
        solar_gen = solar_capacity * solar_hourly * solar_seasonal * solar_clouds
        
        df = pd.DataFrame({
            'datetime': dates,
            'wind_generation_mw': wind_gen,
            'solar_generation_mw': solar_gen,
            'total_renewable_mw': wind_gen + solar_gen
        })
        
        output_file = self.data_raw / "ercot_renewable_generation.csv"
        df.to_csv(output_file, index=False)
        print(f"Saved to {output_file}")
        
        return df


class WeatherDataLoader:
    """Download and process weather data."""
    
    def __init__(self):
        self.data_raw = DATA_RAW
        
    def download_weather_data(
        self,
        location: str = "Houston, TX",
        start_date: str = "2023-01-01",
        end_date: str = "2024-12-31"
    ) -> pd.DataFrame:
        """
        Download weather data.
        
        In production, this would use APIs like:
        - NREL NSRDB for solar irradiance
        - NOAA for temperature and wind
        - Commercial weather providers
        
        For now, we generate synthetic data.
        """
        print(f"Generating synthetic weather data for {location}")
        
        dates = pd.date_range(start=start_date, end=end_date, freq='H')
        np.random.seed(45)
        
        # Temperature (higher in summer)
        day_of_year = dates.dayofyear
        temp_seasonal = 60 + 30 * np.sin(2 * np.pi * (day_of_year - 90) / 365)
        temp_daily = 10 * np.sin(2 * np.pi * (dates.hour - 12) / 24)
        temperature = temp_seasonal + temp_daily + np.random.normal(0, 3, len(dates))
        
        # Solar irradiance (W/m²)
        solar_hourly = np.maximum(0, 1000 * np.sin(np.pi * (dates.hour - 6) / 12))
        solar_seasonal = 0.5 + 0.5 * np.sin(2 * np.pi * (day_of_year - 172) / 365)
        irradiance = solar_hourly * solar_seasonal * (0.8 + 0.2 * np.random.random(len(dates)))
        
        # Wind speed (m/s)
        wind_base = 5 + 3 * np.sin(2 * np.pi * day_of_year / 365)
        wind_speed = wind_base + np.random.exponential(2, len(dates))
        wind_speed = np.minimum(wind_speed, 25)  # Cap at 25 m/s
        
        df = pd.DataFrame({
            'datetime': dates,
            'temperature_f': temperature,
            'solar_irradiance_w_m2': irradiance,
            'wind_speed_ms': wind_speed
        })
        
        output_file = self.data_raw / "weather_data.csv"
        df.to_csv(output_file, index=False)
        print(f"Saved to {output_file}")
        
        return df


def merge_datasets() -> pd.DataFrame:
    """
    Merge all datasets into a single DataFrame for analysis.
    
    Returns:
        Merged DataFrame with all features
    """
    print("Merging datasets...")
    
    # Load all data
    prices = pd.read_csv(DATA_RAW / "ercot_dam_prices.csv", parse_dates=['datetime'])
    load = pd.read_csv(DATA_RAW / "ercot_load.csv", parse_dates=['datetime'])
    renewable = pd.read_csv(DATA_RAW / "ercot_renewable_generation.csv", parse_dates=['datetime'])
    weather = pd.read_csv(DATA_RAW / "weather_data.csv", parse_dates=['datetime'])
    
    # Merge on datetime
    df = prices.merge(load, on='datetime', how='left')
    df = df.merge(renewable, on='datetime', how='left')
    df = df.merge(weather, on='datetime', how='left')
    
    # Add time-based features
    df['hour'] = df['datetime'].dt.hour
    df['day_of_week'] = df['datetime'].dt.dayofweek
    df['month'] = df['datetime'].dt.month
    df['is_weekend'] = (df['day_of_week'] >= 5).astype(int)
    
    # Add lagged price features
    df['price_lag_1h'] = df['dam_price'].shift(1)
    df['price_lag_24h'] = df['dam_price'].shift(24)
    df['price_lag_168h'] = df['dam_price'].shift(168)  # 1 week
    
    # Add rolling statistics
    df['price_ma_24h'] = df['dam_price'].rolling(24).mean()
    df['price_std_24h'] = df['dam_price'].rolling(24).std()
    
    # Renewable penetration
    df['renewable_penetration'] = df['total_renewable_mw'] / df['system_load_mw']
    
    # Save processed data
    output_file = DATA_PROCESSED / "merged_data.csv"
    df.to_csv(output_file, index=False)
    print(f"Merged dataset saved to {output_file}")
    print(f"Shape: {df.shape}")
    print(f"Date range: {df['datetime'].min()} to {df['datetime'].max()}")
    
    return df


def main():
    """Main function to download all data."""
    print("=" * 60)
    print("ERCOT Data Collection Pipeline")
    print("=" * 60)
    print()
    
    # Initialize loaders
    ercot = ERCOTDataLoader()
    weather = WeatherDataLoader()
    
    # Download all datasets
    print("Step 1: Downloading ERCOT price data...")
    ercot.download_dam_prices()
    print()
    
    print("Step 2: Downloading ERCOT load data...")
    ercot.download_load_data()
    print()
    
    print("Step 3: Downloading renewable generation data...")
    ercot.download_renewable_generation()
    print()
    
    print("Step 4: Downloading weather data...")
    weather.download_weather_data()
    print()
    
    print("Step 5: Merging datasets...")
    df = merge_datasets()
    print()
    
    print("=" * 60)
    print("Data collection complete!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Open notebooks/01_data_exploration.ipynb")
    print("2. Run exploratory data analysis")
    print("3. Build forecasting models")
    
    return df


if __name__ == "__main__":
    main()
