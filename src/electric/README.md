# Electric Utility MCP Server

An MCP (Model Context Protocol) server for electric utility operations, providing tools for checking electricity bills and assigning electricians.

## Features

### Tools
1. **check_bill(electric_code, month, year)** - Check electricity bill for a customer
2. **assign_electrician(address, issue_description)** - Assign an electrician to a service request

### Resources
- **electricians://available** - List of currently available electricians
- **work_orders://recent** - Recent work orders

### Prompts
- **bill_inquiry_prompt** - Helper for bill inquiries
- **service_request_prompt** - Helper for service requests

## Installation

1. Create and activate a virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate  # On macOS/Linux
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Testing

## Testing

### Test Coverage
The project includes comprehensive test coverage with **19 passing tests**:

- **12 Unit Tests** (`test_electric_tools.py`):
  - 5 tests for `check_bill` functionality
  - 5 tests for `assign_electrician` functionality  
  - 2 tests for data integrity validation

- **7 Integration Tests** (`test_mcp_integration.py`):
  - Server initialization and connection
  - Tool listing and execution
  - Resource reading and listing
  - Prompt template functionality

### Run Unit Tests
```bash
source .venv/bin/activate
python3 -m pytest tests/test_electric_tools.py -v
```

### Run Integration Tests
```bash
source .venv/bin/activate
python3 -m pytest tests/test_mcp_integration.py -v
```

### Run All Tests
```bash
source .venv/bin/activate
python3 -m pytest tests/ -v
```

### Manual Testing
```bash
source .venv/bin/activate
python3 manual_test_server.py
```

### Running the Server

#### Development Mode (with MCP Inspector)
```bash
source .venv/bin/activate
mcp dev electric_mcp/electric_mcp_server.py
```

#### Direct Execution
```bash
source .venv/bin/activate
python3 mcps/electric_mcp_server.py
```
## Tool Examples

### Check Bill
```python
# Check bill for customer E001 for March 2024
result = check_bill("E001", "03", "2024")
```

Example response:
```json
{
  "success": true,
  "electric_code": "E001",
  "period": "2024-03",
  "amount": 128.90,
  "status": "overdue",
  "due_date": "2024-04-15",
  "currency": "USD"
}
```

### Assign Electrician
```python
# Assign electrician for outlet repair
result = assign_electrician(
    "123 Main St, Downtown", 
    "Power outlet in kitchen not working, urgent repair needed"
)
```

Example response:
```json
{
  "success": true,
  "work_order_id": "WO0001",
  "assigned_electrician": {
    "id": "ELEC004",
    "name": "Sarah Johnson",
    "rating": 4.6,
    "specialties": ["emergency", "troubleshooting", "repairs"]
  },
  "service_details": {
    "address": "123 Main St, Downtown",
    "issue": "Power outlet in kitchen not working, urgent repair needed",
    "scheduled_date": "2024-06-06",
    "estimated_duration": "2-4 hours",
    "status": "scheduled"
  },
  "contact_info": {
    "phone": "+1-555-ELECTRIC",
    "email": "service@electricutility.com"
  }
}
```

## Sample Data

The server includes sample data for testing:

### Customer Codes
- **E001** - Residential customer with moderate usage
- **E002** - Commercial customer with higher usage  
- **E003** - Small residential customer

### Available Electricians
- **John Smith** (ELEC001) - Residential wiring specialist
- **Maria Rodriguez** (ELEC002) - Commercial/industrial specialist
- **David Chen** (ELEC003) - Smart home and lighting specialist
- **Sarah Johnson** (ELEC004) - Emergency services specialist

### Time Periods
Bills are available for months 01-05 of 2024 for all customers.

## Integration with Claude Desktop

To use this server with Claude Desktop:

### Option 1: Using the provided configuration
1. Copy the contents of `claude_desktop_config.json` to your Claude Desktop configuration file:
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`

2. Update the path in the configuration to match your installation location.

### Option 2: Manual configuration
Add this to your Claude Desktop configuration file:

```json
{
  "mcpServers": {
    "electric-utility": {
      "command": "python",
      "args": ["/path/to/your/electric_mcp/electric_mcp_server.py"],
      "env": {
        "PYTHONPATH": "/path/to/your/electric"
      }
    }
  }
}
```

### Features Available in Claude Desktop:
- **Check electricity bills** for any customer (E001, E002, E003)
- **Assign electricians** based on issue type and specialist expertise
- **View available electricians** and their specialties
- **Review recent work orders** and service history
- **Get prompted assistance** for bill inquiries and service requests

## Error Handling

The server includes comprehensive error handling for:
- Missing or invalid parameters
- Customer not found scenarios
- No available electricians
- Invalid date formats
- Internal server errors

All errors are returned in a consistent JSON format with descriptive messages.
