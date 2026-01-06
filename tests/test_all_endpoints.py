"""Comprehensive tests for all HCDP API endpoints."""

import asyncio
import json
import os
import pytest
from typing import Dict, Any
import httpx
from pathlib import Path

# Test configuration
BASE_URL = "https://api.hcdp.ikewai.org"
API_TOKEN = "e1e3af843ab98c1c2c8ffd2456d6c885"
SAMPLE_DATA_DIR = Path("/home/tswetnam/github/hcdp-mcp/sample_data")

headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

class HCDPEndpointTester:
    """Comprehensive HCDP API endpoint tester."""
    
    def __init__(self):
        self.base_url = BASE_URL
        self.headers = headers
        self.results = {}
        
    async def test_raster_endpoints(self):
        """Test all raster-related endpoints."""
        print("\n=== TESTING RASTER ENDPOINTS ===")
        
        # Test 1: GET /raster - Basic rainfall data
        await self._test_endpoint(
            "GET /raster - Rainfall",
            "GET",
            "/raster",
            params={
                "datatype": "rainfall",
                "date": "2024-12",
                "extent": "bi",
                "production": "new",
                "period": "month"
            }
        )
        
        # Test 2: GET /raster - Temperature data
        await self._test_endpoint(
            "GET /raster - Temperature",
            "GET", 
            "/raster",
            params={
                "datatype": "temp_mean",
                "date": "2024-12",
                "extent": "bi",
                "aggregation": "month"
            }
        )
        
        # Test 3: GET /raster - Humidity data
        await self._test_endpoint(
            "GET /raster - Relative Humidity",
            "GET",
            "/raster", 
            params={
                "datatype": "rh",
                "date": "2024-12",
                "extent": "bi",
                "aggregation": "month"
            }
        )
        
        # Test 4: GET /raster/timeseries - Time series with coordinates
        await self._test_endpoint(
            "GET /raster/timeseries - With coordinates",
            "GET",
            "/raster/timeseries",
            params={
                "datatype": "rainfall",
                "start": "2024-01-01",
                "end": "2024-12-31",
                "extent": "bi",
                "lat": 19.5,
                "lng": -155.5,
                "production": "new",
                "period": "month"
            }
        )
        
    async def test_genzip_endpoints(self):
        """Test all genzip-related endpoints."""
        print("\n=== TESTING GENZIP ENDPOINTS ===")
        
        # Test 1: POST /genzip/email - Email package
        await self._test_endpoint(
            "POST /genzip/email - Email package",
            "POST",
            "/genzip/email",
            json_data={
                "email": "test@example.com",
                "data": json.dumps({
                    "datatype": "rainfall",
                    "production": "new", 
                    "period": "month",
                    "extent": "bi",
                    "start_date": "2024-12-01",
                    "end_date": "2024-12-31"
                }),
                "zipName": "test_rainfall_data"
            }
        )
        
        # Test 2: POST /genzip/instant/content - Instant download content
        await self._test_endpoint(
            "POST /genzip/instant/content - Instant content",
            "POST",
            "/genzip/instant/content",
            json_data={
                "data": json.dumps({
                    "datatype": "rainfall",
                    "production": "new",
                    "period": "month", 
                    "extent": "bi",
                    "start_date": "2024-12-01",
                    "end_date": "2024-12-01"
                })
            }
        )
        
        # Test 3: POST /genzip/instant/link - Instant download link
        await self._test_endpoint(
            "POST /genzip/instant/link - Instant link",
            "POST", 
            "/genzip/instant/link",
            json_data={
                "data": json.dumps({
                    "datatype": "rainfall",
                    "production": "new",
                    "period": "month",
                    "extent": "bi", 
                    "start_date": "2024-12-01",
                    "end_date": "2024-12-01"
                })
            }
        )
        
        # Test 4: POST /genzip/instant/splitlink - Split links
        await self._test_endpoint(
            "POST /genzip/instant/splitlink - Split links",
            "POST",
            "/genzip/instant/splitlink",
            json_data={
                "data": json.dumps({
                    "datatype": "rainfall",
                    "production": "new",
                    "period": "month",
                    "extent": "bi",
                    "start_date": "2024-12-01", 
                    "end_date": "2024-12-31"
                })
            }
        )
        
    async def test_files_endpoints(self):
        """Test all files-related endpoints."""
        print("\n=== TESTING FILES ENDPOINTS ===")
        
        # Test 1: GET /files/production/list - List files
        await self._test_endpoint(
            "GET /files/production/list - List files",
            "GET",
            "/files/production/list",
            params={
                "datatype": "rainfall",
                "production": "new",
                "period": "month",
                "extent": "bi"
            }
        )
        
        # Test 2: GET /files/production/retrieve - Retrieve specific file
        # First get file list, then retrieve one
        list_result = await self._get_file_list()
        if list_result and "files" in list_result:
            file_path = list_result["files"][0] if list_result["files"] else None
            if file_path:
                await self._test_endpoint(
                    "GET /files/production/retrieve - Retrieve file",
                    "GET",
                    "/files/production/retrieve",
                    params={"file_path": file_path}
                )
        
    async def test_stations_endpoints(self):
        """Test stations endpoint."""
        print("\n=== TESTING STATIONS ENDPOINTS ===")
        
        # Test 1: GET /stations - Basic query
        await self._test_endpoint(
            "GET /stations - Basic query", 
            "GET",
            "/stations",
            params={"q": "{}"}
        )
        
        # Test 2: GET /stations - Query with filters
        await self._test_endpoint(
            "GET /stations - With filters",
            "GET", 
            "/stations",
            params={
                "q": json.dumps({"observer": "NWS"}),
                "limit": 10
            }
        )
        
    async def test_mesonet_endpoints(self):
        """Test all mesonet-related endpoints.""" 
        print("\n=== TESTING MESONET ENDPOINTS ===")
        
        # Test 1: GET /mesonet/db/measurements - Basic measurements
        await self._test_endpoint(
            "GET /mesonet/db/measurements - Basic",
            "GET",
            "/mesonet/db/measurements",
            params={
                "location": "hawaii",
                "start_date": "2024-12-01",
                "end_date": "2024-12-02",
                "limit": 10
            }
        )
        
        # Test 2: GET /mesonet/db/stations - Station info
        await self._test_endpoint(
            "GET /mesonet/db/stations - Station info",
            "GET",
            "/mesonet/db/stations",
            params={"location": "hawaii"}
        )
        
        # Test 3: GET /mesonet/db/variables - Variable definitions
        await self._test_endpoint(
            "GET /mesonet/db/variables - Variables",
            "GET",
            "/mesonet/db/variables",
            params={"location": "hawaii"}
        )
        
        # Test 4: GET /mesonet/db/stationMonitor - Station monitoring
        await self._test_endpoint(
            "GET /mesonet/db/stationMonitor - Monitor",
            "GET", 
            "/mesonet/db/stationMonitor",
            params={"location": "hawaii"}
        )
        
        # Test 5: POST /mesonet/db/measurements/email - Email measurements
        await self._test_endpoint(
            "POST /mesonet/db/measurements/email - Email CSV",
            "POST",
            "/mesonet/db/measurements/email",
            json_data={
                "email": "test@example.com",
                "location": "hawaii",
                "start_date": "2024-12-01",
                "end_date": "2024-12-02"
            }
        )
    
    async def _test_endpoint(self, name: str, method: str, endpoint: str, 
                           params: Dict = None, json_data: Dict = None):
        """Test a specific endpoint."""
        print(f"\nTesting: {name}")
        print(f"Endpoint: {method} {endpoint}")
        
        try:
            async with httpx.AsyncClient() as client:
                if method == "GET":
                    response = await client.get(
                        f"{self.base_url}{endpoint}",
                        params=params,
                        headers=self.headers,
                        timeout=120.0
                    )
                elif method == "POST":
                    response = await client.post(
                        f"{self.base_url}{endpoint}",
                        json=json_data,
                        headers=self.headers,
                        timeout=120.0
                    )
                    
                print(f"Status Code: {response.status_code}")
                print(f"Content Type: {response.headers.get('content-type', 'Unknown')}")
                
                if response.status_code == 200:
                    content_type = response.headers.get('content-type', '')
                    if 'application/json' in content_type:
                        result = response.json()
                        print(f"Response: {json.dumps(result, indent=2)[:500]}...")
                        self.results[name] = {"status": "success", "data": result}
                    elif 'application/octet-stream' in content_type or 'image/' in content_type:
                        # Handle binary data (like TIFF files)
                        content_length = len(response.content)
                        print(f"Binary response length: {content_length} bytes")
                        
                        # Save binary data to sample_data directory
                        safe_name = name.replace(" ", "_").replace("/", "_")
                        filename = f"{safe_name}.tiff"
                        filepath = SAMPLE_DATA_DIR / filename
                        SAMPLE_DATA_DIR.mkdir(exist_ok=True)
                        
                        with open(filepath, 'wb') as f:
                            f.write(response.content)
                        print(f"Saved binary data to: {filepath}")
                        
                        self.results[name] = {
                            "status": "success", 
                            "data": f"Binary data saved to {filepath}",
                            "size": content_length
                        }
                    else:
                        text_result = response.text
                        print(f"Text response: {text_result[:500]}...")
                        self.results[name] = {"status": "success", "data": text_result}
                else:
                    print(f"Error: {response.status_code} - {response.text}")
                    self.results[name] = {
                        "status": "error",
                        "code": response.status_code,
                        "message": response.text
                    }
                    
        except Exception as e:
            print(f"Exception: {str(e)}")
            self.results[name] = {"status": "exception", "error": str(e)}
    
    async def _get_file_list(self):
        """Helper to get file list for testing file retrieval."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/files/production/list",
                    params={
                        "datatype": "rainfall",
                        "production": "new", 
                        "period": "month",
                        "extent": "bi"
                    },
                    headers=self.headers,
                    timeout=60.0
                )
                if response.status_code == 200:
                    return response.json()
        except Exception:
            pass
        return None
    
    async def run_all_tests(self):
        """Run comprehensive tests on all endpoints."""
        print("Starting comprehensive HCDP API endpoint tests...")
        print(f"Base URL: {self.base_url}")
        
        await self.test_raster_endpoints()
        await self.test_genzip_endpoints()
        await self.test_files_endpoints()
        await self.test_stations_endpoints()
        await self.test_mesonet_endpoints()
        
        return self.results
    
    def generate_report(self):
        """Generate a comprehensive test report."""
        print("\n" + "="*80)
        print("COMPREHENSIVE HCDP API ENDPOINT TEST REPORT")
        print("="*80)
        
        successful_tests = []
        failed_tests = []
        error_tests = []
        
        for test_name, result in self.results.items():
            if result["status"] == "success":
                successful_tests.append(test_name)
            elif result["status"] == "error":
                failed_tests.append((test_name, result))
            else:
                error_tests.append((test_name, result))
        
        print(f"\nSUMMARY:")
        print(f"Total Tests: {len(self.results)}")
        print(f"Successful: {len(successful_tests)}")
        print(f"Failed: {len(failed_tests)}")
        print(f"Errors: {len(error_tests)}")
        
        if successful_tests:
            print(f"\nSUCCESSFUL TESTS ({len(successful_tests)}):")
            for test in successful_tests:
                print(f"  ✓ {test}")
        
        if failed_tests:
            print(f"\nFAILED TESTS ({len(failed_tests)}):")
            for test, result in failed_tests:
                print(f"  ✗ {test}: {result.get('code')} - {result.get('message', '')[:100]}")
        
        if error_tests:
            print(f"\nERROR TESTS ({len(error_tests)}):")
            for test, result in error_tests:
                print(f"  ! {test}: {result.get('error', '')[:100]}")
        
        # Save detailed results to file
        report_file = SAMPLE_DATA_DIR / "endpoint_test_results.json"
        with open(report_file, 'w') as f:
            json.dump(self.results, f, indent=2, default=str)
        print(f"\nDetailed results saved to: {report_file}")

async def main():
    """Main test runner."""
    tester = HCDPEndpointTester()
    results = await tester.run_all_tests()
    tester.generate_report()
    return results

if __name__ == "__main__":
    asyncio.run(main())