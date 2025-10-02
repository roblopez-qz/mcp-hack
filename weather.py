from typing import Any
import httpx
import os
from fastmcp import FastMCP
from langchain_community.tools import BraveSearch

# Initialize FastMCP server
mcp = FastMCP("weather")

# Constants
NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"
BRAVE_API_KEY = ""


# Helper Functions
async def make_nws_request(url: str) -> dict[str, Any] | None:
    """Make a request to the NWS API with proper error handling."""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/geo+json"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None

def format_alert(feature: dict) -> str:
    """Format an alert feature into a readable string."""
    props = feature["properties"]
    return f"""
Event: {props.get('event', 'Unknown')}
Area: {props.get('areaDesc', 'Unknown')}
Severity: {props.get('severity', 'Unknown')}
Description: {props.get('description', 'No description available')}
Instructions: {props.get('instruction', 'No specific instructions provided')}
"""

# MCP Tools 

@mcp.tool()
async def get_alerts(state: str) -> str:
    """Get weather alerts for a US state.

    Args:
        state: Two-letter US state code (e.g. CA, NY)
    """
    url = f"{NWS_API_BASE}/alerts/active/area/{state}"
    data = await make_nws_request(url)

    if not data or "features" not in data:
        return "Unable to fetch alerts or no alerts found."

    if not data["features"]:
        return "No active alerts for this state."

    alerts = [format_alert(feature) for feature in data["features"]]
    return "\n---\n".join(alerts)

@mcp.tool()
async def get_forecast(latitude: float, longitude: float) -> str:
    """Get weather forecast for a location.

    Args:
        latitude: Latitude of the location
        longitude: Longitude of the location
    """
    # First get the forecast grid endpoint
    points_url = f"{NWS_API_BASE}/points/{latitude},{longitude}"
    points_data = await make_nws_request(points_url)

    if not points_data:
        return "Unable to fetch forecast data for this location."

    # Get the forecast URL from the points response
    forecast_url = points_data["properties"]["forecast"]
    forecast_data = await make_nws_request(forecast_url)

    if not forecast_data:
        return "Unable to fetch detailed forecast."

    # Format the periods into a readable forecast
    periods = forecast_data["properties"]["periods"]
    forecasts = []
    for period in periods[:5]:  # Only show next 5 periods
        forecast = f"""
{period['name']}:
Temperature: {period['temperature']}°{period['temperatureUnit']}
Wind: {period['windSpeed']} {period['windDirection']}
Forecast: {period['detailedForecast']}
"""
        forecasts.append(forecast)

    return "\n---\n".join(forecasts)

@mcp.tool()
async def add_numbers(a: float, b: float) -> str:
    """Add two numbers together.

    Args:
        a: First number to add
        b: Second number to add
    """
    result = a + b
    return f"The sum of {a} and {b} is {result}"

@mcp.tool()
async def brave_search(query: str, count: int = 3) -> str:
    """Search the web using Brave Search API.

    Args:
        query: The search query to execute
        count: Number of search results to return (default: 3, max: 20)
    """
    try:
        # Get API key from environment variable
        api_key = BRAVE_API_KEY
        if not api_key:
            return "Error: BRAVE_SEARCH_API_KEY environment variable not set. Please set your Brave Search API key."
        
        # Initialize Brave Search tool
        search_tool = BraveSearch.from_api_key(api_key=api_key, search_kwargs={"count": min(count, 20)})
        
        # Execute search
        results = search_tool.run(query)
        
        return f"Search results for '{query}':\n\n{results}"
        
    except Exception as e:
        return f"Error performing search: {str(e)}"


# MCP Prompts
@mcp.prompt()
async def suggest_events(location: str) -> str:
    """Get comprehensive weather data for a location to enable intelligent event suggestions.
    
    Args:
        location: Location name or coordinates (latitude,longitude)
    """
    try:
        # Parse coordinates if provided
        if ',' in location:
            lat, lon = map(float, location.split(','))
        else:
            # Let the LLM determine the best coordinates for the location
            return f"""
Location: {location}

Please provide the latitude and longitude coordinates for this location in the format: latitude,longitude

For example:
- New York City: 40.7128,-74.0060
- Los Angeles: 34.0522,-118.2437
- London: 51.5074,-0.1278

Once you provide coordinates, I'll fetch the weather data and suggest appropriate events.
"""
        
        # Get detailed forecast for the next few days
        forecast = await get_forecast(lat, lon)
        
        # Combine data for comprehensive weather context
        weather_context = f"""
Location: {location} ({lat}, {lon})
Current Alerts: {alerts}

Detailed Forecast:
{forecast}

Based on this weather data, suggest appropriate events and activities for the next few days.
"""
        return weather_context
        
    except Exception as e:
        return f"Error gathering weather data: {e}"


# Run the MCP server
if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')