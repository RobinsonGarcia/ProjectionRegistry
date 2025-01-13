# **Package Mechanics and File-by-File Explanation**

Below is a **comprehensive overview** of how all the files in your **gnomonic** projection package fit together and interact, from the highest-level `__init__.py` down through each sub-package and base class.

---

## 1. Package Overview

Your **gnomonic** projection package is structured around the concept of different **projections** (Gnomonic, Mercator, Oblique Mercator, etc.). Each projection has distinct modules for **configuration**, **grid generation**, **strategy** (math routines for forward/backward projection), and **transform** (converting projection-plane coordinates to image pixel coordinates).  

At the core, everything is orchestrated by:
- A central **registry** (`ProjectionRegistry` in `registry.py`) that can register and retrieve any projection by name.
- A **processor** (`ProjectionProcessor` in `processor.py`) that uses a projection’s configured components to perform **forward** (equirectangular → projected) and **backward** (projected → equirectangular) transformations on images.

The sections below detail each module’s purpose and how they fit together.

---

## 2. Top-Level Files

### `projection/__init__.py`
- **Purpose**: Acts as the entry point for the package, sets up logging, and automatically registers default projections (Gnomonic, Mercator, Oblique Mercator, etc.).
- **Key elements**:
  - Imports `ProjectionRegistry` and `register_default_projections`.
  - Calls `setup_logging()` to configure loggers.
  - Runs `register_default_projections()`, so that “gnomonic,” “mercator,” and “oblique_mercator” are known to the registry as soon as someone imports this package.
  - Exports `ProjectionRegistry` so users can do:
    ```python
    from projection import ProjectionRegistry
    ```

### `projection/logging_config.py`
- **Purpose**: Configures logging for the entire `gnomonic_projection` namespace.
- **Mechanism**:  
  - Defines `setup_logging()`, setting log levels and handlers (console vs. file).
  - Ensures that logs are displayed on the console at INFO level (and saved to file at DEBUG level).

### `projection/exceptions.py`
- **Purpose**: Central location for custom exceptions used throughout the package (e.g., `ConfigurationError`, `ProcessingError`, `GridGenerationError`, etc.).
- **Usage**: 
  - **ConfigurationError** is raised if something goes wrong validating or setting config parameters.
  - **RegistrationError** if a projection is incorrectly registered or not found.
  - **ProcessingError** for issues during forward/backward transformations.
  - **GridGenerationError**, **TransformationError**, **InterpolationError** are more specialized errors.

---

## 3. Base Modules (the `base/` directory)

These files define abstract classes and foundational components that other projections inherit or build upon.

### `projection/base/__init__.py`
- **Purpose**: Collects and re-exports the core abstract/base classes and exceptions from the package’s `base/` folder.
- **Exports**:  
  - `BaseProjectionConfig`, `BaseProjectionStrategy`, `BaseGridGeneration`, `BaseInterpolation`, `BaseCoordinateTransformer` — all abstract or base classes.  
  - Various custom exceptions from `exceptions.py`.

### `projection/base/config.py`
- **Purpose**:  
  - Declares a **pydantic** model (`BaseProjectionConfigModel`) with minimal fields for interpolation, border mode, etc.  
  - Provides the `BaseProjectionConfig` class, which acts as a **generic** container for a projection’s configuration data.
- **Highlights**:
  - `BaseProjectionConfig` expects a `config_object` with a `.config` attribute (a pydantic model).  
  - `create_projection()`, `create_grid_generation()`, and `create_transformer()` are placeholders. Real projection classes override or dynamically attach these methods.  
  - `update()` can dynamically alter config values.  
  - `__getattr__` looks up fields in `.params`, `.extra_params`, or `.config_object`.

### `projection/base/grid.py`
- **Purpose**:  
  - Defines the `BaseGridGeneration` class for generating forward/backward grids.  
  - Real implementations override `projection_grid()` and `spherical_grid()`.
- **Highlights**:
  - Each projection implements a custom `projection_grid()` (e.g., for Gnomonic, x/y in a tangent plane) and `spherical_grid()` (lon/lat grids for inverse transformations).

### `projection/base/interpolation.py`
- **Purpose**:  
  - Declares `BaseInterpolation`, which wraps **OpenCV’s remap** functionality (`cv2.remap`) to warp images based on `(map_x, map_y)` coordinate transforms.
- **Highlights**:
  - Checks that the config has `interpolation`, `borderMode`, and `borderValue`.  
  - Provides `interpolate()` to map an input image to a new projection space, optionally applying a mask.

### `projection/base/strategy.py`
- **Purpose**:  
  - `BaseProjectionStrategy` defines abstract methods for forward/backward transformations between lat/lon and x/y.  
  - The derived classes (e.g., `GnomonicProjectionStrategy`) do the real math.
- **Highlights**:
  - `from_spherical_to_projection(...)`: Typically lat/lon → x/y (forward).  
  - `from_projection_to_spherical(...)`: x/y → lat/lon (inverse).  
  - Raises `NotImplementedError` unless a subclass overrides.

### `projection/base/transform.py`
- **Purpose**:  
  - `BaseCoordinateTransformer` with placeholders (`spherical_to_image_coords` and `projection_to_image_coords`).  
  - The specialized projection transform classes (e.g., Gnomonic, Mercator) override these to convert from lat/lon or x/y ranges into pixel coordinates for final images.
- **Highlights**:
  - `__init__` just stores `config`.
  - In real sub-classes, you compute how lat/lon or x/y scale to `[0, width]` / `[0, height]`.

### `projection/base/registry.py`
- **Purpose**:  
  - Demonstrates a **metaclass** `RegistryBase` that registers classes automatically into `REGISTRY`.  
  - Contains `BaseRegisteredClass` which new classes can subclass to get auto-registration.  
  - (This is separate from the `ProjectionRegistry` in `registry.py` at the root, which is used for registering projection components. This base registry concept is not strictly the same as the top-level `ProjectionRegistry`.)

---

## 4. Default Projections

### `projection/default_projections.py`
- **Purpose**:  
  - Defines a function `register_default_projections()` that calls `ProjectionRegistry.register(...)` for each known projection type: *gnomonic*, *mercator*, and *oblique_mercator*.
  - Each dictionary passed to `register(name, { ... })` includes references to the relevant classes:  
    - `"config"`: e.g., `GnomonicConfig`  
    - `"grid_generation"`: e.g., `GnomonicGridGeneration`  
    - `"projection_strategy"`: e.g., `GnomonicProjectionStrategy`  
    - `"interpolation"`: e.g., `BaseInterpolation` (or a custom class)  
    - `"transformer"`: e.g., `GnomonicTransformer`
- **Mechanics**: 
  - By default, once `register_default_projections()` is called (in `__init__.py`), these names become accessible:
    ```python
    ProjectionRegistry.get_projection("gnomonic", ...)
    ProjectionRegistry.get_projection("mercator", ...)
    ProjectionRegistry.get_projection("oblique_mercator", ...)
    ```
- **Error Handling**:  
  - Catches `RegistrationError` or any other exception during the process.

---

## 5. Individual Projection Packages

Each projection is organized into a folder with its own `config.py`, `grid.py`, `strategy.py`, and `transform.py`. They typically follow the pattern:

1. **`config.py`**:  
   - Contains a Pydantic model (e.g., `GnomonicConfigModel`, `MercatorConfigModel`, etc.) specifying the projection’s unique parameters.  
   - A wrapper class (e.g. `GnomonicConfig`), which the rest of the code references as the “config object.”

2. **`grid.py`**:  
   - Subclass of `BaseGridGeneration` that actually implements `projection_grid()` and `spherical_grid()`.  
   - Typically uses the config’s bounding box and resolution to produce x/y or lon/lat arrays.

3. **`strategy.py`**:  
   - Subclass of `BaseProjectionStrategy` with the actual forward/backward math.  
   - For example, `GnomonicProjectionStrategy` uses spherical trigonometry to compute how lat/lon → x/y.

4. **`transform.py`**:  
   - Subclass of `BaseCoordinateTransformer` that maps lat/lon or x/y into final image pixel coordinates.  
   - Uses config’s dimension fields (e.g., `x_points`, `y_points`) and bounding boxes to scale numeric coordinates into `[0 .. width-1]` or `[0 .. height-1]`.

Below are your specific projections:

### 5.1. `gnomonic/`
- **`gnomonic/config.py`**:  
  - `GnomonicConfigModel` has fields like `R`, `phi1_deg`, `lam0_deg`, `fov_deg`, etc.  
  - `GnomonicConfig` is the wrapper that holds an instance of `GnomonicConfigModel`.

- **`gnomonic/grid.py`**:  
  - `GnomonicGridGeneration` extends `BaseGridGeneration`.  
  - `projection_grid()` calculates tangent-plane x/y, bounded by `± R * tan(fov/2)`.  
  - `spherical_grid()` is a standard lon/lat mesh for the inverse transform.

- **`gnomonic/strategy.py`**:  
  - `GnomonicProjectionStrategy` handles the forward transform (lat/lon → x/y) and inverse transform (x/y → lat/lon).  
  - In forward mode, it calculates:
    \[
      x = R \cdot \frac{\cos(\phi)\sin(\lambda - \lambda_0)}{\dots} , \quad
      y = R \cdot \frac{\dots}{\dots}
    \]
  - In backward mode, it solves for \(\phi\) and \(\lambda\).

- **`gnomonic/transform.py`**:  
  - `GnomonicTransformer` uses the config’s parameters to map (lat, lon) or (x, y) into pixel coordinates.  
  - In the code, it normalizes coordinate values from `[lon_min, lon_max]` to `[0, width-1]`, etc.

### 5.2. `mercator/`
- Similarly has `MercatorConfig`, `MercatorGridGeneration`, `MercatorProjectionStrategy`, `MercatorTransformer`.

### 5.3. `oblique_mercator/`
- Likewise, `ObliqueMercatorConfig`, `ObliqueMercatorGridGeneration`, `ObliqueMercatorProjectionStrategy`, `ObliqueMercatorTransformer`.

---

## 6. The `processor.py`

### `ProjectionProcessor`
- **Purpose**: Provides convenient `forward()` and `backward()` methods for any projection.  
- **Mechanics**:
  1. Takes a `BaseProjectionConfig` in its constructor.  
  2. Calls `create_projection()`, `create_grid_generation()`, `create_interpolation()`, `create_transformer()` to get all the necessary components.  
  3. **Forward** workflow:  
     - `grid_generation.projection_grid()` to get a forward grid (x_grid, y_grid).  
     - `projection.from_projection_to_spherical(x_grid, y_grid)` to get lat/lon.  
     - `transformer.spherical_to_image_coords(lat, lon, shape)` → `(map_x, map_y)`.  
     - `interpolation.interpolate(img, map_x, map_y)` → final warped image.  
  4. **Backward** workflow:  
     - `grid_generation.spherical_grid()` → (lon_grid, lat_grid).  
     - `projection.from_spherical_to_projection(lat_grid, lon_grid)` → (x, y, mask).  
     - `transformer.projection_to_image_coords(x, y, config_object)` → `(map_x, map_y)`.  
     - `interpolation.interpolate(rect_img, map_x, map_y, mask)` → final warped image.
- **Exception handling**:  
  - Raises `ProcessingError` if components fail.  
  - Raises `ValueError` if input images aren’t valid `numpy` arrays.  
  - Raises specialized exceptions (`GridGenerationError`, `TransformationError`, etc.) as appropriate.

---

## 7. The `registry.py` (Top-Level)

### `ProjectionRegistry`
- **Purpose**: The main class that **manages** registrations of projection types by name and returns either a config object or a `ProjectionProcessor`.
- **Mechanics**:
  - `ProjectionRegistry.register("name", {...})`:  
    - Expects a dict containing `"config"`, `"grid_generation"`, `"projection_strategy"`, and optionally `"interpolation"` and `"transformer"`.  
    - Validates these classes.  
    - Stores them in an internal `_registry` dictionary keyed by the name (e.g., “gnomonic”).
  - `ProjectionRegistry.get_projection("gnomonic", return_processor=True, **kwargs)`:  
    - Instantiates the config class with any `**kwargs` overrides.  
    - Wraps that config in a `BaseProjectionConfig`.  
    - Dynamically injects the `create_*()` methods, which instantiate the correct strategy, grid, etc. for that projection.  
    - If `return_processor=True`, returns a `ProjectionProcessor`, fully ready for `processor.forward()` or `processor.backward()`.  
    - Otherwise returns the config object itself.

This is how your system supports multiple projection types with a consistent interface.

---

## **Summary**

- **`__init__.py`**: Orchestrates logging and default registrations.  
- **`logging_config.py`**: Central logger setup.  
- **`exceptions.py`**: Shared custom exceptions.  
- **`base/*`**: Abstract/base classes for config, grid generation, interpolation, strategies, transforms, plus a mini metaclass-based registry.  
- **`default_projections.py`**: Registers known projections (gnomonic, mercator, oblique_mercator).  
- **`gnomonic/`, `mercator/`, `oblique_mercator/`**: Each folder provides the actual classes for that specific projection.  
- **`processor.py`**: Encapsulates forward/backward projection logic in an easy-to-use interface.  
- **`registry.py`** (at the root): A global registry for “projection name” ↔ “component classes.”

Each of these parts works together to let you easily define new projections (by providing config, grid, strategy, transform classes), register them, and then perform forward/backward projections by simply referring to the projection name via `ProjectionRegistry`.