#!/usr/bin/env python3
"""Direct test of HCDP API with corrected settings."""

import asyncio
import os
from hcdp_mcp_server.client import HCDPClient

async def test_hcdp_api():
    """Test HCDP API directly."""
    
    print("Testing HCDP API with corrected configuration...")
    print("=" * 50)
    
    client = HCDPClient()
    print(f"Base URL: {client.base_url}")
    print(f"API Token: {client.api_token[:10]}...")
    
    # Test rainfall data for February 2022 (matching the API docs example)
    try:
        print(f"\n1. Testing rainfall data for February 2022, Big Island:")
        result = await client.get_raster_data(
            datatype="rainfall",
            date="2022-02", 
            extent="bi",
            production="new",
            period="month"
        )
        print("✓ Success! Rainfall data retrieved")
        print(f"Response type: {type(result)}")
        if isinstance(result, dict):
            print(f"Keys: {list(result.keys())}")
            
    except Exception as e:
        print(f"✗ Error: {e}")
        
    # Test temperature data 
    try:
        print(f"\n2. Testing temperature data for February 2022, Big Island:")
        result = await client.get_raster_data(
            datatype="temp_mean",
            date="2022-02",
            extent="bi", 
            production="new",
            period="month"
        )
        print("✓ Success! Temperature data retrieved")
        print(f"Response type: {type(result)}")
        if isinstance(result, dict):
            print(f"Keys: {list(result.keys())}")
            
    except Exception as e:
        print(f"✗ Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_hcdp_api())