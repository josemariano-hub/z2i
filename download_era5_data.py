"""
Download ERA5 wind data from Copernicus Climate Data Store (CDS)

Before running this script, you need to:
1. Register at https://cds.climate.copernicus.eu
2. Get your API key from your profile page
3. Create ~/.cdsapirc file with:
   url: https://cds.climate.copernicus.eu/api/v2
   key: YOUR_UID:YOUR_API_KEY
"""

import cdsapi
import os
from pathlib import Path
import balloon_feasibility_config as config
from tqdm import tqdm
import calendar

def setup_data_directory():
    """Create data directory if it doesn't exist"""
    Path(config.DATA_DIR).mkdir(parents=True, exist_ok=True)
    print(f"Data directory: {config.DATA_DIR}")

def download_era5_monthly_data(year, month):
    """
    Download ERA5 wind data for a specific month

    Parameters:
    -----------
    year : int
        Year to download
    month : int
        Month to download (1-12)
    """
    c = cdsapi.Client()

    # Get number of days in month
    days_in_month = calendar.monthrange(year, month)[1]
    days = [f"{d:02d}" for d in range(1, days_in_month + 1)]

    # All hours in a day
    hours = [f"{h:02d}:00" for h in range(24)]

    output_file = f"{config.DATA_DIR}/era5_wind_{year}_{month:02d}.nc"

    # Check if file already exists
    if os.path.exists(output_file):
        print(f"File {output_file} already exists. Skipping download.")
        return output_file

    print(f"\nDownloading ERA5 data for {year}-{month:02d}...")
    print(f"Pressure levels: {config.PRESSURE_LEVELS}")
    print(f"Geographic bounds: {config.USA_BOUNDS}")

    try:
        c.retrieve(
            'reanalysis-era5-pressure-levels',
            {
                'product_type': 'reanalysis',
                'variable': [
                    'u_component_of_wind',
                    'v_component_of_wind',
                    'geopotential',  # for altitude calculation
                ],
                'pressure_level': config.PRESSURE_LEVELS,
                'year': str(year),
                'month': f"{month:02d}",
                'day': days,
                'time': hours,
                'area': [  # North, West, South, East
                    config.USA_BOUNDS['lat_max'],
                    config.USA_BOUNDS['lon_min'],
                    config.USA_BOUNDS['lat_min'],
                    config.USA_BOUNDS['lon_max'],
                ],
                'format': 'netcdf',
            },
            output_file
        )
        print(f"Successfully downloaded: {output_file}")
        return output_file
    except Exception as e:
        print(f"Error downloading data: {e}")
        if os.path.exists(output_file):
            os.remove(output_file)
        raise

def download_era5_surface_data(year, month):
    """
    Download ERA5 surface data (10m winds and geopotential) for a specific month
    This is needed to estimate 100m wind speed

    Parameters:
    -----------
    year : int
        Year to download
    month : int
        Month to download (1-12)
    """
    c = cdsapi.Client()

    # Get number of days in month
    days_in_month = calendar.monthrange(year, month)[1]
    days = [f"{d:02d}" for d in range(1, days_in_month + 1)]

    # All hours in a day
    hours = [f"{h:02d}:00" for h in range(24)]

    output_file = f"{config.DATA_DIR}/era5_surface_{year}_{month:02d}.nc"

    # Check if file already exists
    if os.path.exists(output_file):
        print(f"File {output_file} already exists. Skipping download.")
        return output_file

    print(f"\nDownloading ERA5 surface data for {year}-{month:02d}...")

    try:
        c.retrieve(
            'reanalysis-era5-single-levels',
            {
                'product_type': 'reanalysis',
                'variable': [
                    '10m_u_component_of_wind',
                    '10m_v_component_of_wind',
                    'geopotential',
                    'surface_pressure',
                ],
                'year': str(year),
                'month': f"{month:02d}",
                'day': days,
                'time': hours,
                'area': [  # North, West, South, East
                    config.USA_BOUNDS['lat_max'],
                    config.USA_BOUNDS['lon_min'],
                    config.USA_BOUNDS['lat_min'],
                    config.USA_BOUNDS['lon_max'],
                ],
                'format': 'netcdf',
            },
            output_file
        )
        print(f"Successfully downloaded: {output_file}")
        return output_file
    except Exception as e:
        print(f"Error downloading surface data: {e}")
        if os.path.exists(output_file):
            os.remove(output_file)
        raise

def download_all_data():
    """Download all ERA5 data for the configured year"""
    setup_data_directory()

    print(f"\n{'='*60}")
    print(f"ERA5 Data Download for {config.YEAR}")
    print(f"{'='*60}")
    print(f"Months: {config.START_MONTH} to {config.END_MONTH}")
    print(f"Region: Continental USA")
    print(f"Data will be saved to: {config.DATA_DIR}")
    print(f"{'='*60}\n")

    # Check if CDS API is configured
    cdsapirc_path = os.path.expanduser(config.CDS_API_RC)
    if not os.path.exists(cdsapirc_path):
        print(f"\n{'!'*60}")
        print("ERROR: CDS API not configured!")
        print(f"{'!'*60}")
        print("\nTo download ERA5 data, you need to:")
        print("1. Register at https://cds.climate.copernicus.eu")
        print("2. Login and go to your profile page")
        print("3. Copy your UID and API key")
        print(f"4. Create file {cdsapirc_path} with content:")
        print("   url: https://cds.climate.copernicus.eu/api/v2")
        print("   key: YOUR_UID:YOUR_API_KEY")
        print(f"\n{'!'*60}\n")
        return False

    months = range(config.START_MONTH, config.END_MONTH + 1)

    for month in tqdm(months, desc="Downloading months"):
        try:
            # Download pressure level data
            download_era5_monthly_data(config.YEAR, month)

            # Download surface data
            download_era5_surface_data(config.YEAR, month)

        except Exception as e:
            print(f"\nFailed to download data for {config.YEAR}-{month:02d}: {e}")
            print("Continuing with next month...")
            continue

    print(f"\n{'='*60}")
    print("Download complete!")
    print(f"{'='*60}\n")
    return True

if __name__ == "__main__":
    # For initial testing, you might want to download just one month
    # Uncomment the following to download just January 2024:
    # setup_data_directory()
    # download_era5_monthly_data(2024, 1)
    # download_era5_surface_data(2024, 1)

    # Or download all configured months:
    download_all_data()
