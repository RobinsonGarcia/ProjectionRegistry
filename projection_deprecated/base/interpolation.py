import cv2
import numpy as np

class BaseInterpolation:
    def __init__(self, config):
        self.config = config

    def interpolate(self, input_img, map_x, map_y, mask=None):
            map_x_32 = map_x.astype(np.float32)
            map_y_32 = map_y.astype(np.float32)
            result = cv2.remap(input_img, map_x_32, map_y_32,
                            interpolation=self.config.interpolation,
                            borderMode=self.config.borderMode,
                            borderValue=self.config.borderValue)
            if mask is not None:
                result *= mask[:, :, None]
            return result