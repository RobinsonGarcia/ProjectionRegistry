# projection/oblique_mercator/strategy.py
import numpy as np
import math
import logging

from ..base.strategy import BaseProjectionStrategy

logger = logging.getLogger("projection.oblique_mercator.strategy")

class ObliqueMercatorProjectionStrategy(BaseProjectionStrategy):
    """
    Implements the forward (lat, lon -> x, y) and inverse (x, y -> lat, lon) 
    for an Oblique Mercator projection (Snyder, USGS Paper 1395).
    """

    def __init__(self, config):
        """
        We'll store intermediate parameters (φp, λp, etc.) for the oblique transformation.
        """
        super().__init__(config)
        # Precompute some radians:
        self.phi_c = math.radians(self.config.center_lat)
        self.lam_c = math.radians(self.config.center_lon)
        self.beta  = math.radians(self.config.azimuth_deg)
        self.R     = self.config.R
        self.k0    = self.config.k0

        # Following Snyder eqn (9-7),(9-8) for a single center lat/lon & azimuth:
        #   φp = arcsin(cos φc sin β) 
        #   λp = λc + arctan[ - cos β / (- sin φc sin β) ] 
        # We'll store them for use in forward/backward.

        self.phi_p = math.asin(math.cos(self.phi_c)*math.sin(self.beta))

        top = -math.cos(self.beta)
        bot = -math.sin(self.phi_c)*math.sin(self.beta)
        delta_lam = math.atan2(top, bot)
        self.lam_p = self.lam_c + delta_lam

        # For convenience, define λ0 = λp + π/2:
        self.lam0 = self.lam_p + math.pi / 2

        logger.debug(f"ObliqueMercatorProjectionStrategy: phi_p={self.phi_p}, lam_p={self.lam_p}, lam0={self.lam0}")

    def from_spherical_to_projection(self, lat: np.ndarray, lon: np.ndarray):
        """
        Forward: (lat, lon) in degrees -> (x, y) in projection coords.
        Return (x, y, mask).
        """
        # Convert to radians
        lat_rad = np.radians(lat)
        lon_rad = np.radians(lon)

        phi_p = self.phi_p
        lam0  = self.lam0
        R     = self.R
        k0    = self.k0

        # Eqn (9-6) A = sin φp sin φ - cos φp cos φ sin(λ - λ0)
        A = (np.sin(phi_p)*np.sin(lat_rad)
             - np.cos(phi_p)*np.cos(lat_rad)*np.sin(lon_rad - lam0))

        # Eqn (9-3): x = Rk0 arctan( B ), B = [tan φp + sin φp sin(λ-λ0)] / cos(λ-λ0)
        # We'll define partial for B:
        top    = np.tan(phi_p) + np.sin(phi_p)*np.sin(lon_rad - lam0)
        bottom = np.cos(lon_rad - lam0)
        B      = top / bottom
        x      = R * k0 * np.arctan(B)

        # Eqn (9-4): y = (R k0 / 2) ln( (1 + A)/(1 - A) ), or Rk0 atanh(A)
        with np.errstate(divide='ignore', invalid='ignore'):
            denom = (1 - A)
            numer = (1 + A)
            y = R * k0 * 0.5 * np.log(np.where(denom != 0, numer / denom, 1e15))

        # Mask: we can define valid region if |A|<1, for instance
        mask = np.abs(A) < 1.0

        return x, y, mask

    def from_projection_to_spherical(self, x: np.ndarray, y: np.ndarray):
        """
        Inverse: (x, y) -> (lat, lon) in degrees.
        Using eqns (9-9),(9-10).
        """
        phi_p = self.phi_p
        lam0  = self.lam0
        R     = self.R
        k0    = self.k0

        xi  = x / (R*k0)
        eta = y / (R*k0)

        # eqn (9-9): φ = arcsin[ sin φp tanh(eta) + cos φp sin(xi)/cosh(eta) ]
        sin_phi_p = math.sin(phi_p)
        cos_phi_p = math.cos(phi_p)

        # We'll compute them in vectorized form using np:
        sinh_eta = np.sinh(eta)
        cosh_eta = np.cosh(eta)
        sin_xi   = np.sin(xi)
        inside   = sin_phi_p*(sinh_eta/cosh_eta) + cos_phi_p*(sin_xi/cosh_eta)
        lat_rad  = np.arcsin(inside)

        # eqn (9-10): λ = λ0 + atan2( sin φp sin(xi) - cos φp tanh(eta),
        #                            cos φp cos(xi) )
        top = sin_phi_p*np.sin(xi) - cos_phi_p*(sinh_eta/cosh_eta)
        bot = cos_phi_p*np.cos(xi)
        lon_rad = lam0 + np.arctan2(top, bot)

        lat_deg = np.degrees(lat_rad)
        lon_deg = np.degrees(lon_rad)

        return lat_deg, lon_deg