# /Users/robinsongarcia/projects/AzimutalEquidistant/projection/AzimutalEquidistant/__init__.py


import logging

from .config import AzimutalEquidistantConfig
from .strategy import AzimutalEquidistantProjectionStrategy
from .grid import AzimutalEquidistantGridGeneration
from .transform import AzimutalEquidistantTransformer
from ..logging_config import setup_logging

# Initialize logger for this module
logger = logging.getLogger('azimutal_equidistant_projection.AzimutalEquidistant')

def initialize_azimutal_equidistant_module():
    """
    Initialize the AzimutalEquidistant Projection module.

    This initialization sets up any module-specific configurations or prerequisites.
    Currently, it primarily logs the initialization status.
    """
    logger.debug("Initializing Azimutal Equidistant Projection Module.")
    # Any module-specific initialization can be done here
    logger.info("Azimutal Equidistant Projection Module initialized successfully.")

# Call the initialization function upon import
initialize_azimutal_equidistant_module()

__all__ = [
    "AzimutalEquidistantConfig",
    "AzimutalEquidistantProjectionStrategy",
    "AzimutalEquidistantGridGeneration",
    "AzimutalEquidistantTransformer"
]