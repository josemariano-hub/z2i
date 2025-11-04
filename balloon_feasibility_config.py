"""
Configuration file for balloon launch feasibility analysis
"""

# Balloon flight parameters (adjustable)
ASCENT_SPEED = 2.5  # m/s (default)
DESCENT_SPEED = 3.0  # m/s (default)
CRUISE_TIME = 2.0  # hours (default)
CRUISE_ALTITUDE = 3000  # meters (default, will be calculated from cruise time and ascent speed)

# Wind criteria
WIND_THRESHOLD = 2.0  # m/s at 100m altitude
WIND_REFERENCE_HEIGHT = 100  # meters

# Geographic bounds for continental USA
USA_BOUNDS = {
    'lat_min': 25.0,
    'lat_max': 49.0,
    'lon_min': -125.0,
    'lon_max': -66.0
}

# Grid resolution (degrees)
# This will create approximately 2400 grid points for USA (60x40)
# For 20,000 points globally, use ~0.9 degree resolution
# For USA with similar density, we'll use 0.5 degree resolution (~120x48 = 5760 points)
GRID_RESOLUTION = 0.5  # degrees

# Pressure levels to download (hPa/mb)
# We need multiple levels to capture wind profile from surface to cruise altitude
PRESSURE_LEVELS = [
    1000,  # ~110m
    975,   # ~320m
    950,   # ~540m
    925,   # ~760m
    900,   # ~990m
    850,   # ~1460m
    800,   # ~1950m
    750,   # ~2470m
    700,   # ~3010m
    650,   # ~3570m
    600,   # ~4210m
    550,   # ~4880m
    500    # ~5570m
]

# Time parameters
YEAR = 2024
# We'll start with a subset of days for testing, then expand
START_MONTH = 1
END_MONTH = 12

# Data directory
DATA_DIR = './balloon_data'

# ERA5 CDS API configuration file path
# Users need to create ~/.cdsapirc with their credentials
CDS_API_RC = '~/.cdsapirc'
