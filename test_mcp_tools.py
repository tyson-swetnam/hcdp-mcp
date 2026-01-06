"""Test MCP server tools."""

import asyncio
from hcdp_mcp_server.server import app

async def test_mcp_tools():
    """Test that all MCP tools are properly registered."""
    
    print("Testing MCP server tool registration...")
    
    # Import the handler function directly
    from hcdp_mcp_server.server import handle_list_tools
    
    # Get list of tools
    tools = await handle_list_tools()
    
    print(f"\nRegistered Tools ({len(tools)}):")
    print("="*50)
    
    for i, tool in enumerate(tools, 1):
        print(f"{i:2d}. {tool.name}")
        print(f"    Description: {tool.description}")
        print(f"    Schema keys: {list(tool.inputSchema.get('properties', {}).keys())}")
        print()
    
    expected_tools = [
        "get_climate_raster",
        "get_timeseries_data", 
        "get_station_data",
        "get_mesonet_data",
        "generate_data_package_email",
        "generate_data_package_instant_link",
        "generate_data_package_instant_content",
        "generate_data_package_splitlink",
        "list_production_files",
        "retrieve_production_file",
        "get_mesonet_stations",
        "get_mesonet_variables",
        "get_mesonet_station_monitor",
        "email_mesonet_measurements"
    ]
    
    registered_tools = [tool.name for tool in tools]
    
    print("TOOL REGISTRATION CHECK:")
    print("="*50)
    
    missing_tools = []
    for expected_tool in expected_tools:
        if expected_tool in registered_tools:
            print(f"✓ {expected_tool}")
        else:
            print(f"✗ {expected_tool} - MISSING")
            missing_tools.append(expected_tool)
    
    extra_tools = []
    for registered_tool in registered_tools:
        if registered_tool not in expected_tools:
            extra_tools.append(registered_tool)
    
    if extra_tools:
        print(f"\nExtra tools (not expected): {extra_tools}")
    
    if missing_tools:
        print(f"\nMissing tools: {missing_tools}")
    else:
        print("\n✓ All expected tools are registered!")
    
    return len(tools), missing_tools

if __name__ == "__main__":
    asyncio.run(test_mcp_tools())