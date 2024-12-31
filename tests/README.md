# Gnomonic Projection Testing Documentation

This document provides a comprehensive guide to the tests included in the Gnomonic Projection project and instructions on how to run and analyze them.

---

## Table of Contents

- [Introduction](#introduction)
- [Testing Overview](#testing-overview)
- [Installation](#installation)
- [Running Tests](#running-tests)
- [Test Types](#test-types)
  - [Unit Tests](#unit-tests)
  - [Integration Tests](#integration-tests)
  - [Performance Tests](#performance-tests)
  - [Exception Handling Tests](#exception-handling-tests)
- [Analyzing Test Results](#analyzing-test-results)
- [Continuous Integration (CI)](#continuous-integration-ci)

---

## Introduction

This project implements a Gnomonic Projection framework, providing functionalities such as grid generation, coordinate transformations, and image interpolation. The testing framework ensures robustness, reliability, and performance across all modules.

---

## Testing Overview

The tests are categorized into:

1. **Unit Tests:** Focus on individual components, such as configuration, grid generation, and interpolation.
2. **Integration Tests:** Validate interactions between components.
3. **Performance Tests:** Assess computational efficiency.
4. **Exception Handling Tests:** Ensure meaningful error messages and correct handling of edge cases.

---

## Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/gnomonic.git
   cd gnomonic
   # Gnomonic Projection Testing Documentation

This document provides a comprehensive guide to the tests included in the Gnomonic Projection project and instructions on how to run and analyze them.

---

## Table of Contents

- [Introduction](#introduction)
- [Testing Overview](#testing-overview)
- [Installation](#installation)
- [Running Tests](#running-tests)
- [Test Types](#test-types)
  - [Unit Tests](#unit-tests)
  - [Integration Tests](#integration-tests)
  - [Performance Tests](#performance-tests)
  - [Exception Handling Tests](#exception-handling-tests)
- [Analyzing Test Results](#analyzing-test-results)
- [Continuous Integration (CI)](#continuous-integration-ci)

---

## Introduction

This project implements a Gnomonic Projection framework, providing functionalities such as grid generation, coordinate transformations, and image interpolation. The testing framework ensures robustness, reliability, and performance across all modules.

---

## Testing Overview

The tests are categorized into:

1. **Unit Tests:** Focus on individual components, such as configuration, grid generation, and interpolation.
2. **Integration Tests:** Validate interactions between components.
3. **Performance Tests:** Assess computational efficiency.
4. **Exception Handling Tests:** Ensure meaningful error messages and correct handling of edge cases.

---

## Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/gnomonic.git
   cd gnomonic
    ```    
2.	Set Up the Virtual Environment
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows:         venv\Scripts\activate
    ```
3.	Install Dependencies
    ```bash
    pip install -r requirements.txt 
    ```
4.	Install Development Dependencies
    ```
    pip install -r requirements-dev.txt
    ```

# Running Tests

Tests are managed using pytest. Run the tests with the following commands:
1.	Run All Tests
    ```bash
    pytest
    ```
2.	Run Specific Test File
    ```bash
    pytest tests/test_config.py
    ```
3.	Run Tests with Detailed Output
    ```bash
    pytest -v
    ```
4.	Generate Coverage Report
    ```bash
    pytest --cov=projection --cov-report=html
    ```



