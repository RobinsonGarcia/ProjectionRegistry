import numpy as np
import cv2
import matplotlib.pyplot as plt
from .logging_config import setup_logging

import os
def rotate_equirectangular_image(image: np.ndarray, delta_lat: float, delta_lon: float) -> np.ndarray:
    """
    Rotate an equirectangular image by delta_lat degrees in latitude and delta_lon degrees in longitude.

    Args:
        image (np.ndarray): Input equirectangular image in RGB format with shape (H, W, C).
        delta_lat (float): Rotation angle in degrees for latitude. Positive shifts north, negative shifts south.
        delta_lon (float): Rotation angle in degrees for longitude. Positive shifts east, negative shifts west.

    Returns:
        np.ndarray: Rotated equirectangular image in RGB format with shape (H, W, C).
    """
    if image.ndim != 3 or image.shape[2] not in [1, 3, 4]:
        raise ValueError("Input image must be a 3D array with 1, 3, or 4 channels.")
    
    H, W, C = image.shape

    # Create a grid of pixel coordinates (x, y)
    logger = setup_logging()
    logger.debug(f"Image dimensions: Height={H}, Width={W}, Channels={C}")

    # Generate normalized pixel coordinates
    x = np.linspace(0, W - 1, W)
    y = np.linspace(0, H - 1, H)
    xv, yv = np.meshgrid(x, y)

    # Convert pixel coordinates to geographic coordinates (lat, lon)
    # Equirectangular projection:
    # x: 0 to W-1 maps to lon: -180 to +180
    # y: 0 to H-1 maps to lat: +90 to -90
    lon = (xv / (W - 1)) * 360.0 - 180.0
    lat = 90.0 - (yv / (H - 1)) * 180.0

    logger.debug("Converted pixel coordinates to geographic coordinates.")

    # Apply rotation
    lon_rot = lon + delta_lon
    lat_rot = lat + delta_lat

    logger.debug(f"Applied rotation: delta_lat={delta_lat}, delta_lon={delta_lon}")

    # Handle longitude wrapping
    lon_rot = (lon_rot + 180) % 360 - 180  # Wrap to [-180, 180)
    logger.debug("Wrapped rotated longitudes to [-180, 180) degrees.")

    # Handle latitude clamping
    lat_rot = np.clip(lat_rot, -90, 90)
    logger.debug("Clamped rotated latitudes to [-90, 90] degrees.")

    # Convert rotated geographic coordinates back to pixel coordinates in the input image
    x_rot = ((lon_rot + 180.0) / 360.0) * (W - 1)
    y_rot = ((90.0 - lat_rot) / 180.0) * (H - 1)

    logger.debug("Converted rotated geographic coordinates back to pixel coordinates.")

    # Create the mapping for remap function
    map_x = x_rot.astype(np.float32)
    map_y = y_rot.astype(np.float32)

    logger.debug("Created mapping arrays for remapping.")

    # Remap the input image to get the rotated image
    rotated_image = cv2.remap(
        image,
        map_x,
        map_y,
        interpolation=cv2.INTER_LINEAR,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=0
    )

    logger.debug("Remapped the image to obtain the rotated image.")

    return rotated_image

# Example Usage
if __name__ == "__main__":
    import logging

    # Configure logging
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger("rotate_equirectangular_image")

    # Path to input equirectangular image
    input_image_path = "data/image1.png"  # Replace with your image path

    # Load the image using OpenCV
    input_img_bgr = cv2.imread(input_image_path)
    if input_img_bgr is None:
        raise FileNotFoundError(f"Image not found at path: {input_image_path}")

    # Convert from BGR to RGB
    input_img = cv2.cvtColor(input_img_bgr, cv2.COLOR_BGR2RGB)

    # Define rotation angles
    delta_lat = 0.0  # Shift 10 degrees north
    delta_lon = -98.0  # Shift 30 degrees east

    logger.info(f"Rotating image by delta_lat={delta_lat}, delta_lon={delta_lon}")

    # Perform rotation
    rotated_img = rotate_equirectangular_image(input_img, delta_lat, delta_lon)

    # Convert back to BGR for saving with OpenCV
    rotated_img_bgr = cv2.cvtColor(rotated_img, cv2.COLOR_RGB2BGR)

    # Define output path
    output_image_path = "results/rotated_image.png"
    os.makedirs(os.path.dirname(output_image_path), exist_ok=True)

    # Save the rotated image
    cv2.imwrite(output_image_path, rotated_img_bgr)
    logger.info(f"Rotated image saved to {output_image_path}")

    # Display original and rotated images using Matplotlib
    plt.figure(figsize=(15, 7))

    plt.subplot(1, 2, 1)
    plt.title("Original Equirectangular Image")
    plt.imshow(input_img)
    plt.axis('off')

    plt.subplot(1, 2, 2)
    plt.title(f"Rotated Image (Δlat={delta_lat}°, Δlon={delta_lon}°)")
    plt.imshow(rotated_img)
    plt.axis('off')

    plt.tight_layout()
    plt.show()