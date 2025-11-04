# Balloon Launch Feasibility Analysis

This system analyzes global locations to find the best places for safe balloon launches and landings based on wind conditions.

## Overview

The system:
1. Downloads ERA5 meteorological data from Copernicus Climate Data Store
2. Creates a geographic grid over the analysis region (currently continental USA)
3. For each grid point and each day:
   - Identifies hours with low wind speeds (<2 m/s at 100m altitude)
   - Simulates balloon trajectories following wind patterns
   - Checks if landing locations also have safe wind conditions
4. Calculates feasibility probability for each location
5. Generates a colored map showing the best launch locations

## Key Features

- **Adjustable Parameters**: Ascent speed, descent speed, cruise time, and wind thresholds
- **3-Phase Flight Simulation**: Ascent, cruise at altitude, descent
- **Wind Profile Interpolation**: Accurate wind calculation at any altitude
- **Statistical Analysis**: Identifies locations with highest success probability
- **Beautiful Visualizations**: High-resolution maps with geographic features

## Installation

### 1. Install Required Packages

```bash
pip install -r requirements.txt
```

### 2. Set Up Copernicus CDS API

To download ERA5 data, you need a free account:

1. Register at https://cds.climate.copernicus.eu
2. Log in and go to your profile page
3. Copy your UID and API key
4. Create file `~/.cdsapirc` with:

```
url: https://cds.climate.copernicus.eu/api/v2
key: YOUR_UID:YOUR_API_KEY
```

## Usage

### Step 1: Configure Parameters

Edit `balloon_feasibility_config.py` to adjust:

```python
# Balloon parameters
ASCENT_SPEED = 2.5  # m/s
DESCENT_SPEED = 3.0  # m/s
CRUISE_TIME = 2.0  # hours

# Wind criteria
WIND_THRESHOLD = 2.0  # m/s at 100m altitude

# Geographic bounds (currently set for continental USA)
USA_BOUNDS = {
    'lat_min': 25.0,
    'lat_max': 49.0,
    'lon_min': -125.0,
    'lon_max': -66.0
}

# Grid resolution
GRID_RESOLUTION = 0.5  # degrees (~50km)

# Year to analyze
YEAR = 2024
```

### Step 2: Download ERA5 Data

```bash
python download_era5_data.py
```

This will download:
- Wind data at multiple pressure levels (surface to 5000m)
- Surface wind data for 100m wind estimation
- Hourly data for the entire year

**Note**: Downloading a full year takes several hours. The script downloads one month at a time and can be interrupted/resumed.

For testing, you can modify the script to download just one month:

```python
# In download_era5_data.py, at the bottom:
setup_data_directory()
download_era5_monthly_data(2024, 1)  # Just January
download_era5_surface_data(2024, 1)
```

### Step 3: Run Feasibility Analysis

```bash
python analyze_feasibility.py
```

This will:
- Create geographic grid (~5,760 points for USA at 0.5° resolution)
- Analyze each grid point for each day
- Simulate thousands of balloon trajectories
- Calculate feasibility probabilities
- Generate statistics and visualization

**Note**: Full year analysis is computationally intensive and may take several hours to days depending on grid resolution.

### Step 4: View Results

The analysis generates:

1. **feasibility_map.png**: Colored map showing probability of successful launch/landing
   - Green areas: High feasibility
   - Yellow areas: Medium feasibility
   - Red areas: Low feasibility

2. **feasibility_results.pkl**: Pickled results for further analysis

3. **Console output**: Top 10 locations with statistics

## Output Interpretation

The feasibility probability for each location represents:
- **Numerator**: Number of successful launch attempts (safe takeoff wind AND safe landing wind)
- **Denominator**: Total number of potential launch attempts (hours with safe takeoff wind)

Example: 45% feasibility means that on days when morning winds are calm enough for takeoff, there's a 45% chance the landing site will also have calm winds.

## File Structure

```
.
├── balloon_feasibility_config.py   # Configuration parameters
├── download_era5_data.py           # Data download script
├── balloon_trajectory.py           # Trajectory simulation module
├── analyze_feasibility.py          # Main analysis script
├── requirements.txt                # Python dependencies
├── balloon_data/                   # Data directory (created automatically)
│   ├── era5_wind_2024_*.nc        # Monthly pressure level data
│   ├── era5_surface_2024_*.nc     # Monthly surface data
│   ├── feasibility_results.pkl    # Analysis results
│   └── feasibility_map.png        # Output map
└── README_BALLOON_FEASIBILITY.md   # This file
```

## How It Works

### Wind Speed Calculation at 100m

The system uses two methods:
1. **From surface data**: Logarithmic wind profile extrapolation from 10m winds
2. **From pressure levels**: Interpolation between pressure levels

Formula: `WS(100m) = WS(10m) × ln(100/z₀) / ln(10/z₀)` where z₀ = 0.03m (roughness length)

### Trajectory Simulation

The balloon trajectory follows three phases:

1. **Ascent Phase**:
   - Rises at constant vertical speed (default 2.5 m/s)
   - Drifts horizontally with wind at each altitude
   - Wind interpolated from pressure level data

2. **Cruise Phase**:
   - Maintains altitude for specified duration (default 2 hours)
   - Drifts with wind at cruise altitude
   - Altitude = ascent_speed × cruise_time

3. **Descent Phase**:
   - Descends at constant vertical speed (default 3.0 m/s)
   - Continues drifting with wind

### Feasibility Criteria

A launch is considered feasible if:
1. **Takeoff**: Wind speed < 2 m/s at 100m altitude
2. **Landing**: Wind speed < 2 m/s at 100m altitude at landing location and time
3. **Trajectory**: Balloon remains within data boundaries

## Extending to Global Analysis

To analyze the entire planet (~20,000 grid points):

1. Modify `balloon_feasibility_config.py`:

```python
# Global bounds
GLOBAL_BOUNDS = {
    'lat_min': -90.0,
    'lat_max': 90.0,
    'lon_min': -180.0,
    'lon_max': 180.0
}

# For ~20,000 points: 200 lat × 100 lon = 20,000
GRID_RESOLUTION = 0.9  # degrees
```

2. Update data download script to use global bounds

**Warning**: Global analysis requires:
- Much larger data downloads (~100GB per year)
- Significantly longer computation time
- More storage space

## Performance Optimization Tips

1. **Start small**: Test with one month and coarse resolution first
2. **Parallel processing**: Modify script to use multiprocessing
3. **Partial analysis**: Analyze specific regions or seasons
4. **Results caching**: Save intermediate results

## Troubleshooting

### "CDS API not configured"
- Make sure `~/.cdsapirc` exists with correct credentials
- Verify you've accepted the ERA5 license agreement on the CDS website

### "Data file not found"
- Run `download_era5_data.py` first
- Check that downloads completed successfully

### Slow analysis
- Reduce grid resolution for testing
- Analyze fewer months
- Consider running on a more powerful machine

### Out of memory
- Reduce grid resolution
- Process fewer days at once
- Close other applications

## Citation

If you use this system in research, please cite:
- ERA5 data: Hersbach et al. (2020), DOI: 10.1002/qj.3803
- Copernicus Climate Change Service

## Future Enhancements

- [ ] Multi-year statistical analysis
- [ ] Seasonal variation analysis
- [ ] Parallel processing support
- [ ] Interactive web visualization
- [ ] Cloud/precipitation filtering
- [ ] Terrain avoidance
- [ ] Configurable safety margins
- [ ] Export to GeoJSON/KML

## License

This code is provided as-is for research and educational purposes.

## Contact

For questions or issues, please open an issue on the repository.
