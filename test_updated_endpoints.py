"""Test updated HCDP client with all endpoints."""

import asyncio
import json
from pathlib import Path
from hcdp_mcp_server.client import HCDPClient

async def test_all_updated_endpoints():
    """Test all the updated HCDP client endpoints."""
    
    client = HCDPClient()
    results = {}
    sample_data_dir = Path("sample_data")
    sample_data_dir.mkdir(exist_ok=True)
    
    print("Testing updated HCDP client endpoints...")
    
    # Test 1: Basic raster data
    print("\n1. Testing get_raster_data...")
    try:
        result = await client.get_raster_data(
            datatype="rainfall",
            date="2024-12",
            extent="bi", 
            production="new",
            period="month"
        )
        print(f"Raster data result: {type(result)} with keys: {list(result.keys()) if isinstance(result, dict) else 'Not dict'}")
        results["get_raster_data"] = "SUCCESS"
    except Exception as e:
        print(f"Error: {e}")
        results["get_raster_data"] = f"ERROR: {e}"
    
    # Test 2: Timeseries data
    print("\n2. Testing get_timeseries_data...")
    try:
        result = await client.get_timeseries_data(
            datatype="rainfall",
            start="2024-01-01",
            end="2024-03-31",
            extent="bi",
            lat=19.5,
            lng=-155.5,
            production="new",
            period="month"
        )
        print(f"Timeseries result keys: {list(result.keys()) if isinstance(result, dict) else 'Not dict'}")
        results["get_timeseries_data"] = "SUCCESS"
    except Exception as e:
        print(f"Error: {e}")
        results["get_timeseries_data"] = f"ERROR: {e}"
    
    # Test 3: Station data
    print("\n3. Testing get_station_data...")
    try:
        result = await client.get_station_data(q="{}")
        print(f"Station data result: {type(result)}")
        if isinstance(result, (list, dict)):
            print(f"Number of stations: {len(result)}")
        results["get_station_data"] = "SUCCESS"
    except Exception as e:
        print(f"Error: {e}")
        results["get_station_data"] = f"ERROR: {e}"
    
    # Test 4: Mesonet measurements
    print("\n4. Testing get_mesonet_data...")
    try:
        result = await client.get_mesonet_data(
            start_date="2024-12-01",
            end_date="2024-12-02",
            limit=5
        )
        print(f"Mesonet data result: {type(result)}")
        if isinstance(result, list):
            print(f"Number of measurements: {len(result)}")
        results["get_mesonet_data"] = "SUCCESS"
    except Exception as e:
        print(f"Error: {e}")
        results["get_mesonet_data"] = f"ERROR: {e}"
    
    # Test 5: Mesonet stations
    print("\n5. Testing get_mesonet_stations...")
    try:
        result = await client.get_mesonet_stations()
        print(f"Mesonet stations result: {type(result)}")
        if isinstance(result, list):
            print(f"Number of stations: {len(result)}")
            if result:
                print(f"First station keys: {list(result[0].keys()) if isinstance(result[0], dict) else 'Not dict'}")
        results["get_mesonet_stations"] = "SUCCESS"
    except Exception as e:
        print(f"Error: {e}")
        results["get_mesonet_stations"] = f"ERROR: {e}"
    
    # Test 6: Mesonet variables
    print("\n6. Testing get_mesonet_variables...")
    try:
        result = await client.get_mesonet_variables()
        print(f"Mesonet variables result: {type(result)}")
        if isinstance(result, list):
            print(f"Number of variables: {len(result)}")
        results["get_mesonet_variables"] = "SUCCESS"
    except Exception as e:
        print(f"Error: {e}")
        results["get_mesonet_variables"] = f"ERROR: {e}"
    
    # Test 7: Mesonet station monitor
    print("\n7. Testing get_mesonet_station_monitor...")
    try:
        result = await client.get_mesonet_station_monitor()
        print(f"Station monitor result: {type(result)}")
        results["get_mesonet_station_monitor"] = "SUCCESS"
    except Exception as e:
        print(f"Error: {e}")
        results["get_mesonet_station_monitor"] = f"ERROR: {e}"
    
    # Test 8: List production files
    print("\n8. Testing list_production_files...")
    try:
        result = await client.list_production_files(
            datatype="rainfall",
            production="new",
            period="month",
            extent="bi"
        )
        print(f"Production files result: {type(result)}")
        if isinstance(result, dict) and "files" in result:
            print(f"Number of files: {len(result['files'])}")
            if result['files']:
                print(f"First file: {result['files'][0]}")
        results["list_production_files"] = "SUCCESS"
    except Exception as e:
        print(f"Error: {e}")
        results["list_production_files"] = f"ERROR: {e}"
    
    # Test 9: Generate data package email
    print("\n9. Testing generate_data_package_email...")
    try:
        result = await client.generate_data_package_email(
            email="test@example.com",
            datatype="rainfall",
            production="new",
            period="month",
            extent="bi",
            start_date="2024-12-01",
            end_date="2024-12-01",
            zipName="test_rainfall"
        )
        print(f"Email package result: {result}")
        results["generate_data_package_email"] = "SUCCESS"
    except Exception as e:
        print(f"Error: {e}")
        results["generate_data_package_email"] = f"ERROR: {e}"
    
    # Test 10: Generate instant link
    print("\n10. Testing generate_data_package_instant_link...")
    try:
        result = await client.generate_data_package_instant_link(
            email="test@example.com",
            datatype="rainfall",
            production="new",
            period="month",
            extent="bi",
            start_date="2024-12-01",
            end_date="2024-12-01"
        )
        print(f"Instant link result: {result}")
        results["generate_data_package_instant_link"] = "SUCCESS"
    except Exception as e:
        print(f"Error: {e}")
        results["generate_data_package_instant_link"] = f"ERROR: {e}"
    
    print("\n" + "="*60)
    print("UPDATED HCDP CLIENT TEST RESULTS:")
    print("="*60)
    
    successful_tests = []
    failed_tests = []
    
    for test_name, result in results.items():
        if "SUCCESS" in result:
            successful_tests.append(test_name)
        else:
            failed_tests.append((test_name, result))
    
    print(f"\nSUMMARY:")
    print(f"Total Tests: {len(results)}")
    print(f"Successful: {len(successful_tests)}")
    print(f"Failed: {len(failed_tests)}")
    
    if successful_tests:
        print(f"\nSUCCESSFUL TESTS ({len(successful_tests)}):")
        for test in successful_tests:
            print(f"  ✓ {test}")
    
    if failed_tests:
        print(f"\nFAILED TESTS ({len(failed_tests)}):")
        for test, result in failed_tests:
            print(f"  ✗ {test}: {result}")
    
    # Save results
    results_file = sample_data_dir / "updated_client_test_results.json"
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\nDetailed results saved to: {results_file}")
    
    return results

if __name__ == "__main__":
    asyncio.run(test_all_updated_endpoints())