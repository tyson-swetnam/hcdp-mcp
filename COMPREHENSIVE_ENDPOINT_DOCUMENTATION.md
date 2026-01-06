# HCDP MCP Server - Comprehensive Endpoint Documentation

## Overview

This document provides complete documentation for all Hawaii Climate Data Portal (HCDP) API endpoints exposed through the MCP server, including their status, parameters, and usage examples.

**Base URL**: `https://api.hcdp.ikewai.org`  
**Authentication**: Bearer Token

## Endpoint Status Summary

| Category | Endpoint | Status | MCP Tool | Notes |
|----------|----------|--------|----------|-------|
| **RASTER** | GET /raster | ✅ Working | get_climate_raster | Returns GeoTIFF files |
| | GET /raster/timeseries | ✅ Working | get_timeseries_data | Returns JSON timeseries |
| **STATIONS** | GET /stations | ⚠️ Partial | get_station_data | Works with empty query |
| **MESONET** | GET /mesonet/db/measurements | ✅ Working | get_mesonet_data | Returns measurement data |
| | GET /mesonet/db/stations | ✅ Working | get_mesonet_stations | Returns station metadata |
| | GET /mesonet/db/variables | ✅ Working | get_mesonet_variables | Returns variable definitions |
| | GET /mesonet/db/stationMonitor | ✅ Working | get_mesonet_station_monitor | Returns monitoring data |
| | POST /mesonet/db/measurements/email | ❌ Not tested | email_mesonet_measurements | Email CSV functionality |
| **FILES** | GET /files/production/list | ❌ Error 400 | list_production_files | Requires specific data format |
| | GET /files/production/retrieve | ❌ Not tested | retrieve_production_file | Depends on list working |
| **GENZIP** | POST /genzip/email | ❌ Error 400 | generate_data_package_email | Email package delivery |
| | POST /genzip/instant/content | ❌ Not tested | generate_data_package_instant_content | Direct zip content |
| | POST /genzip/instant/link | ❌ Error 400 | generate_data_package_instant_link | Download link generation |
| | POST /genzip/instant/splitlink | ❌ Not tested | generate_data_package_splitlink | Split download links |

## Working Endpoints (✅)

### 1. GET /raster - Climate Raster Data

**MCP Tool**: `get_climate_raster`

Returns GeoTIFF files containing gridded climate data.

**Parameters**:
- `datatype` (required): Climate variable type
  - `rainfall` ✅ (Working with production/period params)
  - `temp_mean` ❌ (404 errors for most combinations)
  - `temp_min` ❌ (404 errors for most combinations)
  - `temp_max` ❌ (404 errors for most combinations)
  - `rh` ❌ (404 errors for most combinations)
- `date` (required): Date in YYYY-MM format
- `extent` (required): Spatial coverage
  - `bi` (Big Island) ✅
  - `statewide` ❌ (404 for non-rainfall)
  - `oahu` ❌ (404 for non-rainfall)
  - `maui_county` ❌ (404 for non-rainfall)
- `production` (optional): Production level (`new`)
- `period` (optional): Temporal period (`month`)
- `aggregation` (optional): Temporal aggregation
- `timescale` (optional): For SPI data
- `location` (optional): `hawaii` or `american_samoa`

**Working Example**:
```python
result = await client.get_raster_data(
    datatype="rainfall",
    date="2024-12",
    extent="bi",
    production="new", 
    period="month"
)
# Returns: {"data": <binary_tiff_data>}
```

### 2. GET /raster/timeseries - Time Series Data

**MCP Tool**: `get_timeseries_data`

Returns JSON object with date/value pairs for specific coordinates.

**Parameters**:
- `datatype` (required): Climate variable type
- `start` (required): Start date (YYYY-MM-DD)
- `end` (required): End date (YYYY-MM-DD)
- `extent` (required): Spatial extent
- `lat` (optional): Latitude coordinate
- `lng` (optional): Longitude coordinate
- `location` (optional): Location (`hawaii`, `american_samoa`)
- `production` (optional): Production level
- `aggregation` (optional): Temporal aggregation
- `timescale` (optional): For SPI data
- `period` (optional): Period specification

**Working Example**:
```python
result = await client.get_timeseries_data(
    datatype="rainfall",
    start="2024-01-01",
    end="2024-12-31", 
    extent="bi",
    lat=19.7167,  # Hilo
    lng=-155.0833,
    production="new",
    period="month"
)
# Returns: {"2024-01-01T10:00:00.000Z": value1, "2024-02-01T10:00:00.000Z": value2, ...}
```

### 3. GET /stations - Station Data

**MCP Tool**: `get_station_data`

Returns station metadata using MongoDB-style queries.

**Parameters**:
- `q` (required): Query string (MongoDB-style JSON)
- `limit` (optional): Maximum number of results
- `offset` (optional): Offset for pagination

**Working Example**:
```python
result = await client.get_station_data(q="{}")
# Returns: List of station objects
```

### 4. GET /mesonet/db/measurements - Mesonet Measurements

**MCP Tool**: `get_mesonet_data`

Returns real-time weather station measurement data.

**Parameters**:
- `location` (default: "hawaii"): Geographic location
- `station_ids` (optional): Comma-separated station IDs
- `start_date` (optional): Start date (YYYY-MM-DD)
- `end_date` (optional): End date (YYYY-MM-DD)
- `var_ids` (optional): Comma-separated variable IDs
- `intervals` (optional): Time intervals
- `limit` (optional): Maximum number of results
- `offset` (optional): Offset for pagination
- `join_metadata` (default: true): Include metadata

**Working Example**:
```python
result = await client.get_mesonet_data(
    location="hawaii",
    start_date="2024-12-01",
    end_date="2024-12-02",
    limit=100
)
# Returns: List of measurement objects
```

### 5. GET /mesonet/db/stations - Mesonet Stations

**MCP Tool**: `get_mesonet_stations`

Returns mesonet weather station information and metadata.

**Parameters**:
- `location` (default: "hawaii"): Geographic location

**Working Example**:
```python
result = await client.get_mesonet_stations(location="hawaii")
# Returns: List of 103+ station objects with metadata
```

### 6. GET /mesonet/db/variables - Mesonet Variables

**MCP Tool**: `get_mesonet_variables`

Returns definitions and metadata for all available mesonet variables.

**Parameters**:
- `location` (default: "hawaii"): Geographic location

**Working Example**:
```python
result = await client.get_mesonet_variables(location="hawaii") 
# Returns: List of 285+ variable definition objects
```

### 7. GET /mesonet/db/stationMonitor - Station Monitoring

**MCP Tool**: `get_mesonet_station_monitor`

Returns real-time monitoring and status information for mesonet stations.

**Parameters**:
- `location` (default: "hawaii"): Geographic location

**Working Example**:
```python
result = await client.get_mesonet_station_monitor(location="hawaii")
# Returns: Dictionary with monitoring data
```

## Problematic Endpoints (❌/⚠️)

### Files Endpoints

Both `/files/production/list` and `/files/production/retrieve` return 400 errors, suggesting the current parameter format is incorrect. The API expects a specific data structure that differs from the current implementation.

### Genzip Endpoints

The package generation endpoints return 400 errors, indicating the request format needs adjustment. These endpoints require specific data structures for file specifications and email delivery.

### Station Queries

The stations endpoint works with empty queries but may not handle complex MongoDB-style queries correctly.

## Sample Data Files

The following sample files have been generated and saved to `sample_data/`:

1. **rainfall_2024-12_big_island_monthly.tiff** (901,160 bytes)
   - Rainfall data for Big Island, December 2024, monthly aggregation

2. **timeseries_rainfall_2024_hilo.json**
   - Rainfall time series for Hilo area, all of 2024, monthly data

3. **mesonet_stations_hawaii.json**
   - Complete metadata for 103 Hawaii mesonet weather stations

4. **mesonet_variables_hawaii.json**
   - Definitions for 285 available mesonet variables

5. **mesonet_measurements_recent.json**
   - Recent measurement data (100 records) from Hawaii mesonet network

6. **samples_index.json**
   - Index file cataloging all downloaded samples with metadata

## MCP Tools Available

All 14 MCP tools are properly registered and available:

1. `get_climate_raster` - Retrieve GeoTIFF climate data maps
2. `get_timeseries_data` - Get time series for specific coordinates  
3. `get_station_data` - Retrieve station metadata and measurements
4. `get_mesonet_data` - Access real-time mesonet measurements
5. `get_mesonet_stations` - Get station information and metadata
6. `get_mesonet_variables` - Get variable definitions
7. `get_mesonet_station_monitor` - Get station monitoring data
8. `generate_data_package_email` - Email data packages (needs fixing)
9. `generate_data_package_instant_link` - Generate download links (needs fixing)
10. `generate_data_package_instant_content` - Generate zip content (needs fixing)
11. `generate_data_package_splitlink` - Generate split links (needs fixing)
12. `list_production_files` - List available files (needs fixing)
13. `retrieve_production_file` - Retrieve specific files (needs fixing)
14. `email_mesonet_measurements` - Email CSV measurements (needs testing)

## Recommendations for Further Development

### Priority 1: Fix Data Package Generation
- Investigate correct request format for genzip endpoints
- Test different data structure formats
- Add proper error handling and response validation

### Priority 2: Fix Files Endpoints  
- Determine correct format for `/files/production/list` data parameter
- Implement file retrieval once listing works
- Add binary data handling for retrieved files

### Priority 3: Enhance Station Queries
- Test complex MongoDB-style queries
- Add query validation and error handling
- Document supported query operators

### Priority 4: Add Data Validation
- Validate date formats and ranges
- Check extent/location compatibility
- Add datatype availability validation

### Priority 5: Improve Error Handling
- Add detailed error messages for common issues
- Implement retry logic for transient failures
- Add parameter validation before API calls

## Usage Examples

See the test files for complete usage examples:
- `test_endpoints_focused.py` - Basic endpoint testing
- `test_updated_endpoints.py` - Comprehensive client testing  
- `test_working_tools.py` - MCP tools verification
- `download_comprehensive_samples.py` - Sample data generation

## API Authentication

The HCDP API requires a Bearer token for authentication:

```python
headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}
```

Current token: `e1e3af843ab98c1c2c8ffd2456d6c885`

## File Format Support

### Raster Data
- **Format**: GeoTIFF (.tiff)
- **Content-Type**: `image/tiff`
- **Usage**: Climate data grids, suitable for GIS analysis

### Timeseries Data  
- **Format**: JSON
- **Content-Type**: `application/json`
- **Structure**: `{"timestamp": value, ...}`

### Metadata
- **Format**: JSON
- **Content-Type**: `application/json`
- **Structure**: Arrays or objects with detailed metadata

This documentation provides a complete reference for the current state of HCDP MCP server implementation and identifies areas requiring further development.