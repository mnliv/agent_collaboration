#!/usr/bin/env python3
"""
Integration tests for the Electric Utility MCP Server.
"""

import json
import pytest
import asyncio
from unittest.mock import patch, MagicMock
import sys
import os

# Add the parent directory to the path to import the MCP server
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mcps.electric_mcp_server import mcp, check_bill, assign_electrician


class TestMCPServerIntegration:
    """Integration tests for the MCP server."""
    
    def test_server_initialization(self):
        """Test that the MCP server is properly initialized."""
        assert mcp is not None
        assert mcp.name == "Electric Utility Server"
        # Note: In real integration tests, you might want to check server configuration
    
    @pytest.mark.asyncio
    async def test_tools_registration(self):
        """Test that tools are properly registered with the MCP server."""
        # Get the list of registered tools
        tools = await mcp.list_tools()
        tool_names = [tool.name for tool in tools]
        
        assert "check_bill" in tool_names
        assert "assign_electrician" in tool_names
    
    @pytest.mark.asyncio
    async def test_check_bill_tool_schema(self):
        """Test the check_bill tool schema."""
        tools = await mcp.list_tools()
        check_bill_tool = next(tool for tool in tools if tool.name == "check_bill")
        
        assert check_bill_tool.description is not None
        assert "electric_code" in str(check_bill_tool.inputSchema)
        assert "month" in str(check_bill_tool.inputSchema)
        assert "year" in str(check_bill_tool.inputSchema)
    
    @pytest.mark.asyncio
    async def test_assign_electrician_tool_schema(self):
        """Test the assign_electrician tool schema."""
        tools = await mcp.list_tools()
        assign_tool = next(tool for tool in tools if tool.name == "assign_electrician")
        
        assert assign_tool.description is not None
        assert "address" in str(assign_tool.inputSchema)
        assert "issue_description" in str(assign_tool.inputSchema)
    
    @pytest.mark.asyncio
    async def test_tool_execution_check_bill(self):
        """Test executing the check_bill tool through MCP."""
        request = {
            "name": "check_bill",
            "arguments": {
                "electric_code": "E001",
                "month": "01",
                "year": "2024"
            }
        }
        
        result = await mcp.call_tool(name=request["name"], arguments=request["arguments"])
        assert result is not None
        
        # Parse the result content
        data = json.loads(result[0].text)
        assert data["electric_code"] == "E001"
        assert data["month"] == "01"
        assert data["year"] == "2024"
    
    @pytest.mark.asyncio
    async def test_tool_execution_assign_electrician(self):
        """Test executing the assign_electrician tool through MCP."""
        request = {
            "name": "assign_electrician", 
            "arguments": {
                "address": "123 Main St",
                "issue_description": "Power outage"
            }
        }
        
        result = await mcp.call_tool(name=request["name"], arguments=request["arguments"])
        assert result is not None
        # Parse the result content
        data = json.loads(result[0].text)
        assert data["success"] is True
        assert data["service_details"]["address"] == "123 Main St"
        assert data["service_details"]["issue"] == "Power outage"


class TestEndToEndScenarios:
    """End-to-end test scenarios."""
    
    def test_customer_bill_inquiry_scenario(self):
        """Test a complete customer bill inquiry scenario."""
        # Customer wants to check their bill
        electric_code = "E12345"
        month = "06"
        year = "2024"
        
        result = check_bill(electric_code, month, year)
        data = json.loads(result)
        
        # Verify the complete response structure
        assert "error" not in data
        assert data["electric_code"] == electric_code
        assert data["month"] == month
        assert data["year"] == year
        assert isinstance(data["amount"], float)
        assert data["status"] in ["paid", "unpaid"]
        
        # Customer should get a valid bill amount
        assert 10 <= data["amount"] <= 300
    
    def test_service_request_scenario(self):
        """Test a complete service request scenario."""
        # Customer reports an electrical issue
        address = "456 Oak Avenue, Apt 2B"
        issue = "Circuit breaker keeps tripping in kitchen"
        
        result = assign_electrician(address, issue)
        data = json.loads(result)
        
        # Verify the complete service assignment
        assert "error" not in data
        assert data["success"] is True
        
        # Check work order details
        assert data["work_order_id"].startswith("WO-")
        
        # Check electrician assignment
        electrician = data["assigned_electrician"]
        assert electrician["name"] in ["Daniel", "KA", "Tien Ha"]
        assert isinstance(electrician["rating"], (int, float))
        assert electrician["phone"] is not None
        
        # Check service details
        service = data["service_details"]
        assert service["address"] == address
        assert service["issue"] == issue
        assert service["status"] == "scheduled"
        assert "scheduled_date" in service
        assert "estimated_duration" in service
    
    def test_multiple_bill_checks_different_customers(self):
        """Test checking bills for multiple customers."""
        customers = [
            ("E001", "01", "2024"),
            ("E002", "02", "2024"),
            ("E003", "12", "2023")
        ]
        
        results = []
        for electric_code, month, year in customers:
            result = check_bill(electric_code, month, year)
            data = json.loads(result)
            results.append(data)
        
        # All requests should succeed
        for i, (expected_code, expected_month, expected_year) in enumerate(customers):
            assert "error" not in results[i]
            assert results[i]["electric_code"] == expected_code
            assert results[i]["month"] == expected_month
            assert results[i]["year"] == expected_year
    
    def test_multiple_service_requests(self):
        """Test multiple service requests for different issues."""
        requests = [
            ("123 Main St", "Power outage"),
            ("456 Oak Ave", "Flickering lights"),
            ("789 Pine Rd", "Need new outlet installed")
        ]
        
        results = []
        work_order_ids = set()
        
        for address, issue in requests:
            result = assign_electrician(address, issue)
            data = json.loads(result)
            results.append(data)
            work_order_ids.add(data["work_order_id"])
        
        # All requests should succeed
        assert len(results) == 3
        for data in results:
            assert "error" not in data
            assert data["success"] is True
        
        # Work order IDs should be unique
        assert len(work_order_ids) == 3
    
    def test_error_recovery_scenarios(self):
        """Test error recovery in various scenarios."""
        # Test invalid bill request followed by valid request
        invalid_result = check_bill("", "01", "2024")
        invalid_data = json.loads(invalid_result)
        assert "error" in invalid_data
        
        # Valid request should still work
        valid_result = check_bill("E001", "01", "2024")
        valid_data = json.loads(valid_result)
        assert "error" not in valid_data
        
        # Test invalid service request followed by valid request
        invalid_service = assign_electrician("", "Power outage")
        invalid_service_data = json.loads(invalid_service)
        assert "error" in invalid_service_data
        
        # Valid service request should still work
        valid_service = assign_electrician("123 Main St", "Power outage")
        valid_service_data = json.loads(valid_service)
        assert "error" not in valid_service_data


class TestDataConsistency:
    """Test data consistency and integrity."""
    
    def test_electrician_database_consistency(self):
        """Test that the electrician database is consistent."""
        electricians_found = {}
        
        # Run multiple assignments to collect all possible electricians
        for _ in range(50):
            result = assign_electrician("123 Test St", "Test issue")
            data = json.loads(result)
            electrician = data["assigned_electrician"]
            
            name = electrician["name"]
            if name not in electricians_found:
                electricians_found[name] = electrician
            else:
                # Same electrician should have same details
                assert electricians_found[name]["id"] == electrician["id"]
                assert electricians_found[name]["rating"] == electrician["rating"]
                assert electricians_found[name]["phone"] == electrician["phone"]
        
        # Should find at least one electrician
        assert len(electricians_found) >= 1
        
        # All electricians should have valid ratings
        for electrician in electricians_found.values():
            assert isinstance(electrician["rating"], (int, float))
            assert 0 <= electrician["rating"] <= 5
    
    def test_bill_amount_consistency(self):
        """Test that bill amounts are within expected ranges."""
        amounts = []
        
        for i in range(20):
            result = check_bill(f"E{i:03d}", "01", "2024")
            data = json.loads(result)
            amounts.append(data["amount"])
        
        # All amounts should be within the expected range
        for amount in amounts:
            assert 10 <= amount <= 300
            assert isinstance(amount, float)
            # Should be rounded to 2 decimal places
            assert round(amount, 2) == amount
    
    def test_work_order_id_format_consistency(self):
        """Test that work order IDs follow consistent format."""
        work_order_ids = []
        
        for i in range(10):
            result = assign_electrician(f"Address {i}", f"Issue {i}")
            data = json.loads(result)
            work_order_ids.append(data["work_order_id"])
        
        for work_order_id in work_order_ids:
            # Should follow WO-XXXX format
            assert work_order_id.startswith("WO-")
            assert len(work_order_id) == 7
            # Numbers part should be 4 digits
            number_part = work_order_id[3:]
            assert number_part.isdigit()
            assert 1000 <= int(number_part) <= 9999
