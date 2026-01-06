"""Test the working MCP tools."""

import asyncio
import json
import base64
from pathlib import Path
from hcdp_mcp_server.server import handle_call_tool

async def test_working_tools():
    """Test the working MCP tools through the server interface."""
    
    sample_data_dir = Path("sample_data")
    sample_data_dir.mkdir(exist_ok=True)
    
    print("Testing working MCP tools through server interface...")
    
    # Test 1: Get climate raster 
    print("\n1. Testing get_climate_raster tool...")
    try:
        result = await handle_call_tool(
            name="get_climate_raster",
            arguments={
                "datatype": "rainfall",
                "date": "2024-12",
                "extent": "bi",
                "production": "new", 
                "period": "month"
            }
        )
        print(f"Result type: {type(result)}")
        print(f"Number of content items: {len(result)}")
        if result and hasattr(result[0], 'text'):
            response_data = json.loads(result[0].text)
            print(f"Response data keys: {list(response_data.keys())}")
            if 'data' in response_data and isinstance(response_data['data'], bytes):
                print(f"Binary data size: {len(response_data['data'])} bytes")
        print("✓ get_climate_raster SUCCESS")
    except Exception as e:
        print(f"✗ get_climate_raster ERROR: {e}")
    
    # Test 2: Get timeseries data
    print("\n2. Testing get_timeseries_data tool...")
    try:
        result = await handle_call_tool(
            name="get_timeseries_data",
            arguments={
                "datatype": "rainfall",
                "start": "2024-01-01", 
                "end": "2024-03-31",
                "extent": "bi",
                "lat": 19.5,
                "lng": -155.5,
                "production": "new",
                "period": "month"
            }
        )
        print(f"Result type: {type(result)}")
        if result and hasattr(result[0], 'text'):
            response_data = json.loads(result[0].text)
            print(f"Response data keys: {list(response_data.keys())}")
        print("✓ get_timeseries_data SUCCESS")
    except Exception as e:
        print(f"✗ get_timeseries_data ERROR: {e}")
    
    # Test 3: Get mesonet stations
    print("\n3. Testing get_mesonet_stations tool...")
    try:
        result = await handle_call_tool(
            name="get_mesonet_stations", 
            arguments={"location": "hawaii"}
        )
        print(f"Result type: {type(result)}")
        if result and hasattr(result[0], 'text'):
            response_data = json.loads(result[0].text)
            if isinstance(response_data, list):
                print(f"Number of stations: {len(response_data)}")
                if response_data:
                    print(f"First station keys: {list(response_data[0].keys())}")
        print("✓ get_mesonet_stations SUCCESS")
    except Exception as e:
        print(f"✗ get_mesonet_stations ERROR: {e}")
    
    # Test 4: Get mesonet variables
    print("\n4. Testing get_mesonet_variables tool...")
    try:
        result = await handle_call_tool(
            name="get_mesonet_variables",
            arguments={"location": "hawaii"}
        )
        print(f"Result type: {type(result)}")
        if result and hasattr(result[0], 'text'):
            response_data = json.loads(result[0].text)
            if isinstance(response_data, list):
                print(f"Number of variables: {len(response_data)}")
        print("✓ get_mesonet_variables SUCCESS")
    except Exception as e:
        print(f"✗ get_mesonet_variables ERROR: {e}")
    
    # Test 5: Get mesonet data
    print("\n5. Testing get_mesonet_data tool...")
    try:
        result = await handle_call_tool(
            name="get_mesonet_data",
            arguments={
                "location": "hawaii",
                "start_date": "2024-12-01",
                "end_date": "2024-12-02",
                "limit": 5
            }
        )
        print(f"Result type: {type(result)}")
        if result and hasattr(result[0], 'text'):
            response_data = json.loads(result[0].text)
            if isinstance(response_data, list):
                print(f"Number of measurements: {len(response_data)}")
        print("✓ get_mesonet_data SUCCESS")
    except Exception as e:
        print(f"✗ get_mesonet_data ERROR: {e}")
    
    print(f"\n{'='*60}")
    print("MCP TOOLS WORKING VERIFICATION COMPLETE")
    print(f"{'='*60}")

if __name__ == "__main__":
    asyncio.run(test_working_tools())