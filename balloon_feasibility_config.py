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

# Geographic bounds for Iberian Peninsula (Spain + Portugal)
IBERIA_BOUNDS = {
    'lat_min': 36.0,   # Southern Spain (Tarifa area)
    'lat_max': 44.0,   # Northern Spain (Galicia/Basque Country)
    'lon_min': -10.0,  # Western Portugal (Atlantic coast)
    'lon_max': 3.5     # Eastern Spain (Mediterranean coast)
}

# Grid resolution (degrees)
# For Iberian Peninsula: 0.5 degree resolution creates ~16x27 = 432 grid points
# This is much smaller than USA, so analysis will be faster
GRID_RESOLUTION = 0.5  # degrees (~50km)

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
# Start with one month for testing, then expand to full year
START_MONTH = 1
END_MONTH = 1  # Set to 12 for full year analysis

# Data directory
DATA_DIR = './balloon_data'

# ERA5 CDS API configuration file path
# Users need to create ~/.cdsapirc with their credentials
CDS_API_RC = '~/.cdsapirc'
