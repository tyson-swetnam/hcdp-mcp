"""Focused HCDP API endpoint tests."""

import asyncio
import json
import httpx
from pathlib import Path

# Test configuration
BASE_URL = "https://api.hcdp.ikewai.org"
API_TOKEN = "e1e3af843ab98c1c2c8ffd2456d6c885"
SAMPLE_DATA_DIR = Path("sample_data")

headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

async def test_basic_endpoints():
    """Test basic functionality of key endpoints."""
    
    print("Testing HCDP API endpoints...")
    results = {}
    
    # 1. Test basic raster endpoint
    print("\n1. Testing GET /raster (rainfall)...")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{BASE_URL}/raster",
                params={
                    "datatype": "rainfall",
                    "date": "2024-12",
                    "extent": "bi",
                    "production": "new",
                    "period": "month"
                },
                headers=headers,
                timeout=30.0
            )
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                print(f"Content type: {response.headers.get('content-type')}")
                print(f"Content length: {len(response.content)}")
                results["raster_basic"] = "SUCCESS"
                
                # Save sample
                SAMPLE_DATA_DIR.mkdir(exist_ok=True)
                with open(SAMPLE_DATA_DIR / "test_raster_basic.tiff", "wb") as f:
                    f.write(response.content)
                print("Saved sample raster data")
            else:
                print(f"Error: {response.text}")
                results["raster_basic"] = f"ERROR: {response.status_code}"
    except Exception as e:
        print(f"Exception: {e}")
        results["raster_basic"] = f"EXCEPTION: {e}"
    
    # 2. Test timeseries endpoint
    print("\n2. Testing GET /raster/timeseries...")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{BASE_URL}/raster/timeseries",
                params={
                    "datatype": "rainfall",
                    "start": "2024-01-01",
                    "end": "2024-12-31",
                    "extent": "bi",
                    "lat": 19.5,
                    "lng": -155.5,
                    "production": "new",
                    "period": "month"
                },
                headers=headers,
                timeout=30.0
            )
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"Data keys: {list(data.keys()) if isinstance(data, dict) else 'Not dict'}")
                results["timeseries"] = "SUCCESS"
            else:
                print(f"Error: {response.text}")
                results["timeseries"] = f"ERROR: {response.status_code}"
    except Exception as e:
        print(f"Exception: {e}")
        results["timeseries"] = f"EXCEPTION: {e}"
    
    # 3. Test stations endpoint
    print("\n3. Testing GET /stations...")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{BASE_URL}/stations",
                params={"q": "{}"},
                headers=headers,
                timeout=30.0
            )
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"Data type: {type(data)}")
                if isinstance(data, list):
                    print(f"Number of stations: {len(data)}")
                elif isinstance(data, dict):
                    print(f"Data keys: {list(data.keys())}")
                results["stations"] = "SUCCESS"
            else:
                print(f"Error: {response.text}")
                results["stations"] = f"ERROR: {response.status_code}"
    except Exception as e:
        print(f"Exception: {e}")
        results["stations"] = f"EXCEPTION: {e}"
    
    # 4. Test mesonet measurements
    print("\n4. Testing GET /mesonet/db/measurements...")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{BASE_URL}/mesonet/db/measurements",
                params={
                    "location": "hawaii",
                    "start_date": "2024-12-01",
                    "end_date": "2024-12-02",
                    "limit": 5
                },
                headers=headers,
                timeout=30.0
            )
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"Data type: {type(data)}")
                if isinstance(data, list):
                    print(f"Number of measurements: {len(data)}")
                elif isinstance(data, dict):
                    print(f"Data keys: {list(data.keys())}")
                results["mesonet_measurements"] = "SUCCESS"
            else:
                print(f"Error: {response.text}")
                results["mesonet_measurements"] = f"ERROR: {response.status_code}"
    except Exception as e:
        print(f"Exception: {e}")
        results["mesonet_measurements"] = f"EXCEPTION: {e}"
    
    # 5. Test files list
    print("\n5. Testing GET /files/production/list...")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{BASE_URL}/files/production/list",
                params={
                    "datatype": "rainfall",
                    "production": "new",
                    "period": "month",
                    "extent": "bi"
                },
                headers=headers,
                timeout=30.0
            )
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"Data type: {type(data)}")
                if isinstance(data, dict) and "files" in data:
                    print(f"Number of files: {len(data['files'])}")
                    if data['files']:
                        print(f"First file: {data['files'][0]}")
                results["files_list"] = "SUCCESS"
            else:
                print(f"Error: {response.text}")
                results["files_list"] = f"ERROR: {response.status_code}"
    except Exception as e:
        print(f"Exception: {e}")
        results["files_list"] = f"EXCEPTION: {e}"
    
    # 6. Test instant genzip link
    print("\n6. Testing POST /genzip/instant/link...")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{BASE_URL}/genzip/instant/link",
                json={
                    "data": json.dumps({
                        "datatype": "rainfall",
                        "production": "new",
                        "period": "month",
                        "extent": "bi",
                        "start_date": "2024-12-01",
                        "end_date": "2024-12-01"
                    })
                },
                headers=headers,
                timeout=60.0
            )
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"Data type: {type(data)}")
                print(f"Response: {data}")
                results["genzip_instant"] = "SUCCESS"
            else:
                print(f"Error: {response.text}")
                results["genzip_instant"] = f"ERROR: {response.status_code}"
    except Exception as e:
        print(f"Exception: {e}")
        results["genzip_instant"] = f"EXCEPTION: {e}"
    
    print("\n" + "="*50)
    print("ENDPOINT TEST RESULTS:")
    print("="*50)
    for endpoint, result in results.items():
        status_symbol = "✓" if "SUCCESS" in result else "✗"
        print(f"{status_symbol} {endpoint}: {result}")
    
    return results

if __name__ == "__main__":
    asyncio.run(test_basic_endpoints())