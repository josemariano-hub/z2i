"""
Balloon trajectory simulation module

This module simulates balloon trajectories following wind patterns
at different altitudes.
"""

import numpy as np
from scipy.interpolate import interp1d
import xarray as xr

class BalloonTrajectory:
    """
    Simulate balloon trajectory through atmospheric wind field
    """

    def __init__(self, ascent_speed=2.5, descent_speed=3.0, cruise_time=2.0):
        """
        Initialize balloon trajectory simulator

        Parameters:
        -----------
        ascent_speed : float
            Vertical ascent speed in m/s
        descent_speed : float
            Vertical descent speed in m/s
        cruise_time : float
            Time spent at cruise altitude in hours
        """
        self.ascent_speed = ascent_speed
        self.descent_speed = descent_speed
        self.cruise_time_hours = cruise_time
        self.cruise_time_seconds = cruise_time * 3600

    def pressure_to_altitude(self, pressure_hpa):
        """
        Convert pressure to approximate altitude using barometric formula

        Parameters:
        -----------
        pressure_hpa : float or array
            Pressure in hPa

        Returns:
        --------
        altitude : float or array
            Altitude in meters
        """
        # Standard atmosphere approximation
        # h = 44330 * (1 - (P/P0)^0.1903)
        P0 = 1013.25  # Sea level standard pressure (hPa)
        altitude = 44330 * (1 - (pressure_hpa / P0) ** 0.1903)
        return altitude

    def altitude_to_pressure(self, altitude_m):
        """
        Convert altitude to approximate pressure

        Parameters:
        -----------
        altitude_m : float or array
            Altitude in meters

        Returns:
        --------
        pressure : float or array
            Pressure in hPa
        """
        P0 = 1013.25  # Sea level standard pressure (hPa)
        pressure = P0 * (1 - altitude_m / 44330) ** (1 / 0.1903)
        return pressure

    def get_wind_at_point(self, ds, lat, lon, time_idx, altitude_m):
        """
        Interpolate wind components at a specific location and altitude

        Parameters:
        -----------
        ds : xarray.Dataset
            Dataset containing wind data (u, v components)
        lat : float
            Latitude
        lon : float
            Longitude
        time_idx : int
            Time index in dataset
        altitude_m : float
            Altitude in meters

        Returns:
        --------
        u, v : tuple of floats
            Wind components in m/s (u=eastward, v=northward)
        """
        # Convert altitude to pressure
        target_pressure = self.altitude_to_pressure(altitude_m)

        # Get wind profiles at this location
        try:
            # Select nearest lat/lon
            ds_point = ds.sel(latitude=lat, longitude=lon, time=time_idx, method='nearest')

            # Interpolate to target pressure level
            u_interp = interp1d(
                ds_point['level'].values,
                ds_point['u'].values,
                kind='linear',
                bounds_error=False,
                fill_value='extrapolate'
            )
            v_interp = interp1d(
                ds_point['level'].values,
                ds_point['v'].values,
                kind='linear',
                bounds_error=False,
                fill_value='extrapolate'
            )

            u = float(u_interp(target_pressure))
            v = float(v_interp(target_pressure))

            return u, v

        except Exception as e:
            # Return zero wind if interpolation fails
            return 0.0, 0.0

    def simulate_trajectory(self, ds, start_lat, start_lon, start_time_idx, cruise_altitude_m):
        """
        Simulate complete balloon trajectory (ascent, cruise, descent)

        Parameters:
        -----------
        ds : xarray.Dataset
            Dataset containing wind data
        start_lat : float
            Launch latitude
        start_lon : float
            Launch longitude
        start_time_idx : int
            Launch time index
        cruise_altitude_m : float
            Cruise altitude in meters

        Returns:
        --------
        trajectory : dict
            Dictionary containing:
            - end_lat: Landing latitude
            - end_lon: Landing longitude
            - end_time_idx: Landing time index
            - total_time_seconds: Total flight time
            - path: List of (lat, lon, altitude, time) tuples
        """
        # Time step for simulation (seconds)
        dt = 60  # 1 minute time steps

        # Initialize trajectory
        current_lat = start_lat
        current_lon = start_lon
        current_alt = 0.0
        current_time = start_time_idx
        current_time_seconds = 0

        trajectory_path = [(current_lat, current_lon, current_alt, current_time_seconds)]

        # Phase 1: Ascent
        while current_alt < cruise_altitude_m:
            # Get wind at current position
            u, v = self.get_wind_at_point(ds, current_lat, current_lon, current_time, current_alt)

            # Update altitude
            current_alt += self.ascent_speed * dt

            # Update horizontal position based on wind
            # Wind speed in m/s, need to convert to degrees
            # At equator: 1 degree ≈ 111 km = 111000 m
            # Account for latitude: dx = 111000 * cos(lat)
            lat_rad = np.radians(current_lat)
            d_lon = (u * dt) / (111000 * np.cos(lat_rad))  # degrees
            d_lat = (v * dt) / 111000  # degrees

            current_lon += d_lon
            current_lat += d_lat

            # Update time
            current_time_seconds += dt
            current_time = start_time_idx + int(current_time_seconds / 3600)  # Convert to hours

            trajectory_path.append((current_lat, current_lon, current_alt, current_time_seconds))

            # Safety check: don't go beyond data boundaries
            if current_lat < ds.latitude.min() or current_lat > ds.latitude.max():
                break
            if current_lon < ds.longitude.min() or current_lon > ds.longitude.max():
                break

        # Phase 2: Cruise at altitude
        cruise_end_time = current_time_seconds + self.cruise_time_seconds
        while current_time_seconds < cruise_end_time:
            # Get wind at cruise altitude
            u, v = self.get_wind_at_point(ds, current_lat, current_lon, current_time, current_alt)

            # Update horizontal position
            lat_rad = np.radians(current_lat)
            d_lon = (u * dt) / (111000 * np.cos(lat_rad))
            d_lat = (v * dt) / 111000

            current_lon += d_lon
            current_lat += d_lat

            # Update time
            current_time_seconds += dt
            current_time = start_time_idx + int(current_time_seconds / 3600)

            trajectory_path.append((current_lat, current_lon, current_alt, current_time_seconds))

            # Safety check
            if current_lat < ds.latitude.min() or current_lat > ds.latitude.max():
                break
            if current_lon < ds.longitude.min() or current_lon > ds.longitude.max():
                break

        # Phase 3: Descent
        while current_alt > 0:
            # Get wind at current position
            u, v = self.get_wind_at_point(ds, current_lat, current_lon, current_time, current_alt)

            # Update altitude (descending)
            current_alt -= self.descent_speed * dt
            if current_alt < 0:
                current_alt = 0

            # Update horizontal position
            lat_rad = np.radians(current_lat)
            d_lon = (u * dt) / (111000 * np.cos(lat_rad))
            d_lat = (v * dt) / 111000

            current_lon += d_lon
            current_lat += d_lat

            # Update time
            current_time_seconds += dt
            current_time = start_time_idx + int(current_time_seconds / 3600)

            trajectory_path.append((current_lat, current_lon, current_alt, current_time_seconds))

            # Safety check
            if current_lat < ds.latitude.min() or current_lat > ds.latitude.max():
                break
            if current_lon < ds.longitude.min() or current_lon > ds.longitude.max():
                break

        return {
            'end_lat': current_lat,
            'end_lon': current_lon,
            'end_time_idx': current_time,
            'total_time_seconds': current_time_seconds,
            'path': trajectory_path
        }

    def calculate_cruise_altitude(self):
        """
        Calculate cruise altitude based on ascent speed and cruise time

        Returns:
        --------
        altitude : float
            Cruise altitude in meters
        """
        # Default simple calculation
        # Could be made more sophisticated
        return self.ascent_speed * self.cruise_time_hours * 3600
