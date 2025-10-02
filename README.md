# Weather MCP Server

A Model Context Protocol (MCP) server that provides weather information, web search capabilities, and basic math operations using FastMCP.

## Features

### 🌤️ Weather Tools
- **get_alerts**: Get weather alerts for any US state
- **get_forecast**: Get detailed weather forecast for any location (latitude/longitude)

### 🔍 Search Tools  
- **brave_search**: Search the web using Brave Search API
- **add_numbers**: Add two numbers together

### 💡 Prompts
- **suggest_events**: Get comprehensive weather data and event suggestions for a location

## Prerequisites

- Python 3.11 or higher
- [uv](https://docs.astral.sh/uv/) package manager
- Brave Search API key (free from [Brave Search API](https://brave.com/search/api/))

## Installation

1. **Clone and navigate to the project**:
   ```bash
   cd /opt/projects/mcp-hack/weather
   ```

2. **Install dependencies**:
   ```bash
   uv sync
   ```

## Configuration

The server uses a hardcoded Brave Search API key. If you want to use your own API key, you can:

1. Get a free API key from [Brave Search API](https://brave.com/search/api/)
2. Update the `BRAVE_API_KEY` constant in `weather.py`

## Running the Server

### Method 1: Direct Python execution
```bash
uv run python weather.py
```

### Method 2: Using the main module
```bash
uv run python main.py
```

### Method 3: Using uv with module execution
```bash
uv run -m weather
```

## Usage Examples

Once the server is running, you can use the following tools:

### Weather Tools
```python
# Get weather alerts for California
get_alerts("CA")

# Get forecast for San Francisco (37.7749, -122.4194)
get_forecast(37.7749, -122.4194)
```

### Search Tool
```python
# Search the web with default 3 results
brave_search("python programming tutorials")

# Search with custom result count
brave_search("weather forecast San Francisco", 5)
```

### Math Tool
```python
# Add two numbers
add_numbers(15.5, 24.3)
```

### Prompts
```python
# Get weather-based event suggestions
suggest_events("San Francisco")
# or with coordinates
suggest_events("37.7749,-122.4194")
```

## API Integration

This server integrates with:
- **National Weather Service API**: For weather data and alerts
- **Brave Search API**: For web search functionality
- **FastMCP**: For MCP server implementation
- **LangChain Community**: For Brave Search tool integration

## Development

### Project Structure
```
weather/
├── weather.py          # Main MCP server with all tools
├── main.py            # Alternative entry point
├── pyproject.toml     # Project dependencies
├── uv.lock           # Dependency lock file
└── README.md         # This file
```

### Adding New Tools

To add new tools, follow the FastMCP pattern:

```python
@mcp.tool()
async def your_tool_name(param1: str, param2: int = 10) -> str:
    """Tool description.
    
    Args:
        param1: Description of parameter 1
        param2: Description of parameter 2 (default: 10)
    """
    # Your tool logic here
    return "Tool result"
```

## Troubleshooting

### Common Issues

1. **"BRAVE_SEARCH_API_KEY environment variable not set"**
   - The API key is hardcoded in the server, but if you see this error, check that `BRAVE_API_KEY` is properly set in `weather.py`

2. **Weather API errors**
   - Ensure you're using valid US state codes (2 letters) for alerts
   - Verify latitude/longitude coordinates are valid for forecasts

3. **Import errors**
   - Run `uv sync` to ensure all dependencies are installed
   - Make sure you're using Python 3.11 or higher

### Dependencies

Key dependencies include:
- `fastmcp`: MCP server framework
- `httpx`: HTTP client for API requests
- `langchain-community`: Brave Search integration
- `langchain-core`: Core LangChain functionality

## License

This project is part of the MCP hack and is provided as-is for educational and development purposes.
