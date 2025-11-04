"""
Main balloon launch feasibility analysis script

This script analyzes balloon launch feasibility across a geographic grid
by checking wind conditions and simulating trajectories.
"""

import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from pathlib import Path
from tqdm import tqdm
import pickle
from datetime import datetime, timedelta
import pandas as pd

import balloon_feasibility_config as config
from balloon_trajectory import BalloonTrajectory


class FeasibilityAnalyzer:
    """Analyze balloon launch feasibility for geographic regions"""

    def __init__(self):
        self.config = config
        self.trajectory_sim = BalloonTrajectory(
            ascent_speed=config.ASCENT_SPEED,
            descent_speed=config.DESCENT_SPEED,
            cruise_time=config.CRUISE_TIME
        )
        self.grid_lats = None
        self.grid_lons = None
        self.feasibility_matrix = None

    def create_grid(self):
        """Create geographic grid for analysis"""
        print("Creating geographic grid...")

        lat_min = self.config.IBERIA_BOUNDS['lat_min']
        lat_max = self.config.IBERIA_BOUNDS['lat_max']
        lon_min = self.config.IBERIA_BOUNDS['lon_min']
        lon_max = self.config.IBERIA_BOUNDS['lon_max']
        resolution = self.config.GRID_RESOLUTION

        self.grid_lats = np.arange(lat_min, lat_max + resolution, resolution)
        self.grid_lons = np.arange(lon_min, lon_max + resolution, resolution)

        print(f"Grid created: {len(self.grid_lats)} x {len(self.grid_lons)} = "
              f"{len(self.grid_lats) * len(self.grid_lons)} points")

        # Initialize feasibility counters
        self.feasibility_counts = np.zeros((len(self.grid_lats), len(self.grid_lons)))
        self.total_attempts = np.zeros((len(self.grid_lats), len(self.grid_lons)))

        return self.grid_lats, self.grid_lons

    def calculate_wind_speed_100m(self, ds_surface, lat, lon, time_idx):
        """
        Calculate wind speed at 100m altitude using surface data and wind profile

        Uses logarithmic wind profile to estimate 100m wind from 10m measurements

        Parameters:
        -----------
        ds_surface : xarray.Dataset
            Surface wind data
        lat : float
            Latitude
        lon : float
            Longitude
        time_idx : int
            Time index

        Returns:
        --------
        wind_speed : float
            Wind speed at 100m in m/s
        """
        try:
            # Get 10m winds
            ds_point = ds_surface.sel(
                latitude=lat,
                longitude=lon,
                time=time_idx,
                method='nearest'
            )

            u10 = float(ds_point['u10'].values)
            v10 = float(ds_point['v10'].values)

            # Wind speed at 10m
            ws10 = np.sqrt(u10**2 + v10**2)

            # Logarithmic wind profile approximation
            # WS(z) = WS(z_ref) * ln(z/z0) / ln(z_ref/z0)
            # Typical z0 (roughness length) for open terrain: 0.03m
            # z_ref = 10m, z = 100m
            z0 = 0.03
            z_ref = 10.0
            z = 100.0

            ws100 = ws10 * np.log(z / z0) / np.log(z_ref / z0)

            return ws100

        except Exception as e:
            return np.nan

    def calculate_wind_speed_100m_from_pressure(self, ds_pressure, lat, lon, time_idx):
        """
        Calculate wind speed at 100m using pressure level data

        Parameters:
        -----------
        ds_pressure : xarray.Dataset
            Pressure level wind data
        lat : float
            Latitude
        lon : float
            Longitude
        time_idx : int
            Time index

        Returns:
        --------
        wind_speed : float
            Wind speed at 100m in m/s
        """
        try:
            # 100m is approximately at 1000 hPa (near surface)
            # We'll interpolate between pressure levels
            u, v = self.trajectory_sim.get_wind_at_point(
                ds_pressure, lat, lon, time_idx, 100.0
            )

            wind_speed = np.sqrt(u**2 + v**2)
            return wind_speed

        except Exception as e:
            return np.nan

    def check_launch_window(self, ds_pressure, ds_surface, lat, lon, date_idx):
        """
        Check if there's a suitable launch window (wind < threshold for at least 1 hour)

        Parameters:
        -----------
        ds_pressure : xarray.Dataset
            Pressure level data
        ds_surface : xarray.Dataset
            Surface data
        lat : float
            Latitude
        lon : float
            Longitude
        date_idx : int
            Day index (0 = first day of dataset)

        Returns:
        --------
        launch_hours : list
            List of hours (0-23) with suitable wind conditions
        """
        suitable_hours = []

        # Check each hour of the day
        for hour in range(24):
            time_idx = date_idx * 24 + hour

            # Calculate wind at 100m
            ws100 = self.calculate_wind_speed_100m_from_pressure(
                ds_pressure, lat, lon, time_idx
            )

            # Check if wind is below threshold
            if not np.isnan(ws100) and ws100 < self.config.WIND_THRESHOLD:
                suitable_hours.append(hour)

        return suitable_hours

    def check_landing_conditions(self, ds_pressure, end_lat, end_lon, end_time_idx):
        """
        Check if landing location has suitable wind conditions

        Parameters:
        -----------
        ds_pressure : xarray.Dataset
            Pressure level data
        end_lat : float
            Landing latitude
        end_lon : float
            Landing longitude
        end_time_idx : int
            Landing time index

        Returns:
        --------
        is_suitable : bool
            True if wind speed < threshold
        wind_speed : float
            Wind speed at landing
        """
        # Check if landing point is within data bounds
        if (end_lat < ds_pressure.latitude.min() or
            end_lat > ds_pressure.latitude.max() or
            end_lon < ds_pressure.longitude.min() or
            end_lon > ds_pressure.longitude.max()):
            return False, np.nan

        # Check if time is within data bounds
        if end_time_idx >= len(ds_pressure.time):
            return False, np.nan

        # Calculate wind at 100m at landing site
        ws100 = self.calculate_wind_speed_100m_from_pressure(
            ds_pressure, end_lat, end_lon, end_time_idx
        )

        if np.isnan(ws100):
            return False, ws100

        is_suitable = ws100 < self.config.WIND_THRESHOLD

        return is_suitable, ws100

    def analyze_month(self, year, month):
        """
        Analyze feasibility for a specific month

        Parameters:
        -----------
        year : int
            Year
        month : int
            Month (1-12)
        """
        print(f"\n{'='*60}")
        print(f"Analyzing {year}-{month:02d}")
        print(f"{'='*60}")

        # Load data
        pressure_file = f"{self.config.DATA_DIR}/era5_wind_{year}_{month:02d}.nc"
        surface_file = f"{self.config.DATA_DIR}/era5_surface_{year}_{month:02d}.nc"

        if not Path(pressure_file).exists():
            print(f"Data file not found: {pressure_file}")
            print("Please run download_era5_data.py first")
            return

        if not Path(surface_file).exists():
            print(f"Data file not found: {surface_file}")
            print("Please run download_era5_data.py first")
            return

        print(f"Loading pressure data: {pressure_file}")
        ds_pressure = xr.open_dataset(pressure_file)

        print(f"Loading surface data: {surface_file}")
        ds_surface = xr.open_dataset(surface_file)

        # Get number of days in month
        num_days = len(ds_pressure.time) // 24

        print(f"Data loaded: {num_days} days, {len(ds_pressure.time)} hours")

        # Calculate cruise altitude
        cruise_altitude = self.config.ASCENT_SPEED * self.config.CRUISE_TIME * 3600

        # Analyze each grid point
        total_points = len(self.grid_lats) * len(self.grid_lons)
        progress_bar = tqdm(total=total_points * num_days,
                           desc=f"Analyzing {year}-{month:02d}")

        for i, lat in enumerate(self.grid_lats):
            for j, lon in enumerate(self.grid_lons):
                # Check each day
                for day in range(num_days):
                    # Find suitable launch windows
                    launch_hours = self.check_launch_window(
                        ds_pressure, ds_surface, lat, lon, day
                    )

                    # Try launching in each suitable hour
                    for hour in launch_hours:
                        time_idx = day * 24 + hour

                        # Simulate trajectory
                        try:
                            trajectory = self.trajectory_sim.simulate_trajectory(
                                ds_pressure, lat, lon, time_idx, cruise_altitude
                            )

                            # Check landing conditions
                            is_suitable, landing_ws = self.check_landing_conditions(
                                ds_pressure,
                                trajectory['end_lat'],
                                trajectory['end_lon'],
                                trajectory['end_time_idx']
                            )

                            # Update counters
                            self.total_attempts[i, j] += 1
                            if is_suitable:
                                self.feasibility_counts[i, j] += 1

                        except Exception as e:
                            # Trajectory simulation failed
                            self.total_attempts[i, j] += 1
                            pass

                    progress_bar.update(1)

        progress_bar.close()

        # Close datasets
        ds_pressure.close()
        ds_surface.close()

        print(f"Month {year}-{month:02d} analysis complete")

    def analyze_year(self, year):
        """Analyze entire year"""
        for month in range(self.config.START_MONTH, self.config.END_MONTH + 1):
            self.analyze_month(year, month)

    def calculate_feasibility_probability(self):
        """Calculate feasibility probability for each grid point"""
        # Avoid division by zero
        with np.errstate(divide='ignore', invalid='ignore'):
            self.feasibility_matrix = np.where(
                self.total_attempts > 0,
                self.feasibility_counts / self.total_attempts,
                0
            )

        return self.feasibility_matrix

    def save_results(self, filename='feasibility_results.pkl'):
        """Save analysis results"""
        results = {
            'grid_lats': self.grid_lats,
            'grid_lons': self.grid_lons,
            'feasibility_counts': self.feasibility_counts,
            'total_attempts': self.total_attempts,
            'feasibility_matrix': self.feasibility_matrix,
            'config': {
                'ascent_speed': self.config.ASCENT_SPEED,
                'descent_speed': self.config.DESCENT_SPEED,
                'cruise_time': self.config.CRUISE_TIME,
                'wind_threshold': self.config.WIND_THRESHOLD,
                'year': self.config.YEAR,
            }
        }

        filepath = Path(self.config.DATA_DIR) / filename
        with open(filepath, 'wb') as f:
            pickle.dump(results, f)

        print(f"\nResults saved to: {filepath}")

    def load_results(self, filename='feasibility_results.pkl'):
        """Load previous analysis results"""
        filepath = Path(self.config.DATA_DIR) / filename

        if not filepath.exists():
            print(f"Results file not found: {filepath}")
            return False

        with open(filepath, 'rb') as f:
            results = pickle.load(f)

        self.grid_lats = results['grid_lats']
        self.grid_lons = results['grid_lons']
        self.feasibility_counts = results['feasibility_counts']
        self.total_attempts = results['total_attempts']
        self.feasibility_matrix = results['feasibility_matrix']

        print(f"Results loaded from: {filepath}")
        return True

    def plot_feasibility_map(self, output_file='feasibility_map.png'):
        """
        Create colored map showing feasibility probability

        Parameters:
        -----------
        output_file : str
            Output filename for the map
        """
        if self.feasibility_matrix is None:
            self.calculate_feasibility_probability()

        print("\nGenerating feasibility map...")

        # Create figure
        fig = plt.figure(figsize=(16, 10))
        ax = plt.axes(projection=ccrs.PlateCarree())

        # Set map extent
        ax.set_extent([
            self.config.IBERIA_BOUNDS['lon_min'],
            self.config.IBERIA_BOUNDS['lon_max'],
            self.config.IBERIA_BOUNDS['lat_min'],
            self.config.IBERIA_BOUNDS['lat_max']
        ], crs=ccrs.PlateCarree())

        # Add map features
        ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
        ax.add_feature(cfeature.BORDERS, linewidth=0.5)
        ax.add_feature(cfeature.STATES, linewidth=0.3, edgecolor='gray')
        ax.add_feature(cfeature.LAND, facecolor='lightgray', alpha=0.3)

        # Create mesh grid for plotting
        lon_mesh, lat_mesh = np.meshgrid(self.grid_lons, self.grid_lats)

        # Plot feasibility
        im = ax.pcolormesh(
            lon_mesh, lat_mesh, self.feasibility_matrix * 100,
            transform=ccrs.PlateCarree(),
            cmap='RdYlGn',
            vmin=0, vmax=100,
            alpha=0.7
        )

        # Add colorbar
        cbar = plt.colorbar(im, ax=ax, orientation='vertical', pad=0.05, shrink=0.8)
        cbar.set_label('Feasibility Probability (%)', fontsize=12)

        # Add gridlines
        gl = ax.gridlines(draw_labels=True, linewidth=0.5, alpha=0.5, linestyle='--')
        gl.top_labels = False
        gl.right_labels = False

        # Title
        plt.title(
            f'Balloon Launch Feasibility - Iberian Peninsula {self.config.YEAR}\n'
            f'Ascent: {self.config.ASCENT_SPEED}m/s, Descent: {self.config.DESCENT_SPEED}m/s, '
            f'Cruise: {self.config.CRUISE_TIME}h, Wind threshold: {self.config.WIND_THRESHOLD}m/s',
            fontsize=14, pad=20
        )

        # Save figure
        output_path = Path(self.config.DATA_DIR) / output_file
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"Map saved to: {output_path}")

        plt.close()

    def print_statistics(self):
        """Print summary statistics"""
        print(f"\n{'='*60}")
        print("FEASIBILITY ANALYSIS SUMMARY")
        print(f"{'='*60}")

        if self.feasibility_matrix is None:
            self.calculate_feasibility_probability()

        # Find locations with highest feasibility
        valid_mask = self.total_attempts > 0
        valid_probs = self.feasibility_matrix[valid_mask]

        if len(valid_probs) > 0:
            print(f"\nOverall Statistics:")
            print(f"  Total grid points analyzed: {np.sum(valid_mask)}")
            print(f"  Mean feasibility: {np.mean(valid_probs)*100:.2f}%")
            print(f"  Max feasibility: {np.max(valid_probs)*100:.2f}%")
            print(f"  Min feasibility: {np.min(valid_probs)*100:.2f}%")

            # Find top 10 locations
            print(f"\nTop 10 Most Feasible Locations:")
            print(f"  {'Rank':<6} {'Latitude':<10} {'Longitude':<12} {'Probability':<12} {'Attempts'}")
            print(f"  {'-'*60}")

            # Flatten and sort
            probs_flat = self.feasibility_matrix.flatten()
            attempts_flat = self.total_attempts.flatten()
            indices = np.argsort(probs_flat)[::-1]

            count = 0
            for idx in indices:
                if count >= 10:
                    break
                if attempts_flat[idx] > 0:
                    i = idx // len(self.grid_lons)
                    j = idx % len(self.grid_lons)
                    lat = self.grid_lats[i]
                    lon = self.grid_lons[j]
                    prob = probs_flat[idx]
                    attempts = attempts_flat[idx]

                    count += 1
                    print(f"  {count:<6} {lat:<10.2f} {lon:<12.2f} {prob*100:<12.2f} {int(attempts)}")

        print(f"\n{'='*60}\n")


def main():
    """Main execution function"""
    print("\n" + "="*60)
    print("BALLOON LAUNCH FEASIBILITY ANALYSIS")
    print("="*60)

    # Initialize analyzer
    analyzer = FeasibilityAnalyzer()

    # Create grid
    analyzer.create_grid()

    # Analyze full year
    analyzer.analyze_year(config.YEAR)

    # Calculate probabilities
    analyzer.calculate_feasibility_probability()

    # Save results
    analyzer.save_results()

    # Print statistics
    analyzer.print_statistics()

    # Generate map
    analyzer.plot_feasibility_map()

    print("\nAnalysis complete!")


if __name__ == "__main__":
    main()
