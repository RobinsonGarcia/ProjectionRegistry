from ..base.strategy import BaseProjectionStrategy
from .config import GnomonicConfig
import numpy as np

class GnomonicProjectionStrategy(BaseProjectionStrategy):
    def __init__(self, config: GnomonicConfig):
        self.config = config

    def forward(self, x, y):
        phi1, lam0 = map(np.deg2rad, [self.config.phi1_deg, self.config.lam0_deg])
        rho = np.sqrt(x**2 + y**2)
        c = np.arctan2(rho, self.config.R)
        sin_c, cos_c = np.sin(c), np.cos(c)
        phi = np.arcsin(cos_c * np.sin(phi1) - (y * sin_c * np.cos(phi1)) / rho)
        lam = lam0 + np.arctan2(x * sin_c, rho * np.cos(phi1) * cos_c + y * np.sin(phi1) * sin_c)
        return np.rad2deg(phi), np.rad2deg(lam)

    def backward(self, lat, lon):
        phi1, lam0 = map(np.deg2rad, [self.config.phi1_deg, self.config.lam0_deg])
        phi, lam = map(np.deg2rad, [lat, lon])
        cos_c = np.sin(phi1) * np.sin(phi) + np.cos(phi1) * np.cos(phi) * np.cos(lam - lam0)
        x = self.config.R * np.cos(phi) * np.sin(lam - lam0) / cos_c
        y = self.config.R * (np.cos(phi1) * np.sin(phi) - np.sin(phi1) * np.cos(phi) * np.cos(lam - lam0)) / cos_c
        return x, y, cos_c > 0