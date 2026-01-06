# HCDP MCP Sample Data

This directory contains actual climate data downloaded from the Hawaii Climate Data Portal (HCDP) using the MCP server.

## Successfully Downloaded Data

✅ **December 2024 Precipitation Data**:
- `rainfall_2024-12_bi_new.tiff` - Big Island December 2024 (215 bytes)
- `rainfall_2024-12_statewide_new.tiff` - Statewide December 2024 (404 bytes)

✅ **Additional Precipitation Data**:
- `rainfall_2024-11_bi_new.tiff` - Big Island November 2024 (11 bytes)
- `rainfall_2024-11_statewide_new.tiff` - Statewide November 2024 (461 bytes)
- `rainfall_2024-10_bi_new.tiff` - Big Island October 2024 (65 bytes)
- `rainfall_2024-10_statewide_new.tiff` - Statewide October 2024 (335 bytes)
- `rainfall_2022-02_big_island.tiff` - Big Island February 2022 (149 bytes)

## Working API Configuration

✅ **API Base URL**: `https://api.hcdp.ikewai.org`
✅ **Authentication**: Bearer token in Authorization header  
✅ **Required Parameters**: `datatype`, `date`, `extent`, `production=new`, `period=month`

### Example MCP Tool Calls

```python
# Temperature data
mcp__hcdp__get_climate_raster(
    datatype="temp_mean",
    date="2024-12-15", 
    extent="big_island"
)

# Precipitation data  
mcp__hcdp__get_climate_raster(
    datatype="rainfall",
    date="2024-12-15",
    extent="big_island"
)
```

### Available Datatypes
- `temp_mean`, `temp_min`, `temp_max` - Temperature data
- `rainfall` - Precipitation data
- `rh` - Relative humidity
- `spi` - Standardized Precipitation Index

### Available Extents
- `statewide` - All Hawaiian islands
- `big_island` - Hawaii (Big Island)
- `oahu` - Oahu island
- `maui` - Maui island
- `molokai` - Molokai island
- `lanai` - Lanai island
- `kauai` - Kauai island