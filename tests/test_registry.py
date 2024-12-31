import pytest
from projection.registry import ProjectionRegistry
from projection.gnomonic.config import GnomonicConfig
from projection.gnomonic.grid import GnomonicGridGeneration
from projection.gnomonic.strategy import GnomonicProjectionStrategy
from projection.base.interpolation import BaseInterpolation
from projection.exceptions import RegistrationError
from projection.processor import ProjectionProcessor  # Added import
import logging

def test_register_projection_success():
    ProjectionRegistry._registry = {}  # Reset registry for test
    ProjectionRegistry.register("test_projection", {
        "config": GnomonicConfig,
        "grid_generation": GnomonicGridGeneration,
        "projection_strategy": GnomonicProjectionStrategy,
        "interpolation": BaseInterpolation,
    })
    assert "test_projection" in ProjectionRegistry._registry

def test_register_projection_missing_components():
    ProjectionRegistry._registry = {}
    with pytest.raises(RegistrationError) as exc_info:
        ProjectionRegistry.register("incomplete_projection", {
            "config": GnomonicConfig,
            "grid_generation": GnomonicGridGeneration,
            # Missing 'projection_strategy'
        })
    assert "Components must include {'grid_generation', 'projection_strategy', 'config'}. Missing keys: {'projection_strategy'}" in str(exc_info.value)

def test_register_projection_invalid_component_type():
    ProjectionRegistry._registry = {}
    with pytest.raises(RegistrationError) as exc_info:
        ProjectionRegistry.register("invalid_component_projection", {
            "config": GnomonicConfig,
            "grid_generation": "NotAClass",  # Invalid type
            "projection_strategy": GnomonicProjectionStrategy,
        })
    assert "'grid_generation' component must be a class type." in str(exc_info.value)

def test_get_projection_success():
    ProjectionRegistry._registry = {}
    ProjectionRegistry.register("test_projection", {
        "config": GnomonicConfig,
        "grid_generation": GnomonicGridGeneration,
        "projection_strategy": GnomonicProjectionStrategy,
        "interpolation": BaseInterpolation,
    })
    projection = ProjectionRegistry.get_projection("test_projection")
    assert hasattr(projection, "create_projection")
    assert hasattr(projection, "create_grid_generation")
    assert hasattr(projection, "create_interpolation")

def test_get_projection_not_registered():
    ProjectionRegistry._registry = {}
    with pytest.raises(RegistrationError) as exc_info:
        ProjectionRegistry.get_projection("nonexistent_projection")
    assert "Projection 'nonexistent_projection' not found in the registry." in str(exc_info.value)

def test_get_projection_with_processor():
    ProjectionRegistry._registry = {}
    ProjectionRegistry.register("test_projection", {
        "config": GnomonicConfig,
        "grid_generation": GnomonicGridGeneration,
        "projection_strategy": GnomonicProjectionStrategy,
        "interpolation": BaseInterpolation,
    })
    projection_processor = ProjectionRegistry.get_projection("test_projection", return_processor=True)
    assert isinstance(projection_processor, ProjectionProcessor)

def test_list_projections():
    ProjectionRegistry._registry = {}
    ProjectionRegistry.register("proj1", {
        "config": GnomonicConfig,
        "grid_generation": GnomonicGridGeneration,
        "projection_strategy": GnomonicProjectionStrategy,
    })
    ProjectionRegistry.register("proj2", {
        "config": GnomonicConfig,
        "grid_generation": GnomonicGridGeneration,
        "projection_strategy": GnomonicProjectionStrategy,
    })
    projections = ProjectionRegistry.list_projections()
    assert "proj1" in projections
    assert "proj2" in projections
    assert len(projections) == 2