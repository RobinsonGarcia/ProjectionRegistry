class CoordinateTransformer:
    @staticmethod
    def latlon_to_image_coords(lat, lon, config, shape):
        H, W = shape[:2]
        map_x = (lon - config.lon_min) / (config.lon_max - config.lon_min) * (W - 1)
        map_y = (config.lat_max - lat) / (config.lat_max - config.lat_min) * (H - 1)
        return map_x, map_y

    @staticmethod
    def xy_to_image_coords(x, y, config):
        map_x = (x - config.x_min) / (config.x_max - config.x_min) * (config.x_points - 1)
        map_y = (config.y_max - y) / (config.y_max - config.y_min) * (config.y_points - 1)
        return map_x, map_y