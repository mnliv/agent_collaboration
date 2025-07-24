#!/usr/bin/env python3
"""
Unit tests for electric utility tools.
"""

import json
import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
import sys
import os

# Add the parent directory to the path to import the MCP server
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mcps.electric_mcp_server import check_bill, assign_electrician


class TestCheckBill:
    """Test cases for the check_bill function."""
    
    def test_check_bill_valid_inputs(self):
        """Test check_bill with valid inputs."""
        result = check_bill("E001", "01", "2024")
        data = json.loads(result)
        
        assert "electric_code" in data
        assert "month" in data
        assert "year" in data
        assert "amount" in data
        assert "status" in data
        
        assert data["electric_code"] == "E001"
        assert data["month"] == "01"
        assert data["year"] == "2024"
        assert isinstance(data["amount"], float)
        assert data["status"] in ["paid", "unpaid"]
        assert 10 <= data["amount"] <= 300
    
    def test_check_bill_missing_electric_code(self):
        """Test check_bill with missing electric_code."""
        result = check_bill("", "01", "2024")
        data = json.loads(result)
        
        assert "error" in data
        assert data["error"] == "Missing required parameters"
        assert "electric_code, month, and year are all required" in data["message"]
    
    def test_check_bill_missing_month(self):
        """Test check_bill with missing month."""
        result = check_bill("E001", "", "2024")
        data = json.loads(result)
        
        assert "error" in data
        assert data["error"] == "Missing required parameters"
    
    def test_check_bill_missing_year(self):
        """Test check_bill with missing year."""
        result = check_bill("E001", "01", "")
        data = json.loads(result)
        
        assert "error" in data
        assert data["error"] == "Missing required parameters"
    
    def test_check_bill_invalid_month_format(self):
        """Test check_bill with invalid month format."""
        result = check_bill("E001", "abc", "2024")
        data = json.loads(result)
        
        assert "error" in data
        assert data["error"] == "Invalid month format"
        assert "Month must be in (1-12)" in data["message"]
    
    def test_check_bill_invalid_month_range_low(self):
        """Test check_bill with month below valid range."""
        result = check_bill("E001", "0", "2024")
        data = json.loads(result)
        
        assert "error" in data
        assert data["error"] == "Invalid month format"
    
    def test_check_bill_invalid_month_range_high(self):
        """Test check_bill with month above valid range."""
        result = check_bill("E001", "13", "2024")
        data = json.loads(result)
        
        assert "error" in data
        assert data["error"] == "Invalid month format"
    
    def test_check_bill_valid_month_boundaries(self):
        """Test check_bill with valid month boundaries."""
        # Test month 1
        result = check_bill("E001", "1", "2024")
        data = json.loads(result)
        assert "error" not in data
        assert data["month"] == "1"
        
        # Test month 12
        result = check_bill("E001", "12", "2024")
        data = json.loads(result)
        assert "error" not in data
        assert data["month"] == "12"
    
    @patch('random.uniform')
    @patch('random.choice')
    def test_check_bill_deterministic_output(self, mock_choice, mock_uniform):
        """Test check_bill with mocked random functions for deterministic output."""
        mock_uniform.return_value = 150.50
        mock_choice.return_value = "paid"
        
        result = check_bill("E001", "06", "2024")
        data = json.loads(result)
        
        assert data["amount"] == 150.50
        assert data["status"] == "paid"


class TestAssignElectrician:
    """Test cases for the assign_electrician function."""
    
    def test_assign_electrician_valid_inputs(self):
        """Test assign_electrician with valid inputs."""
        result = assign_electrician("123 Main St", "Power outage")
        data = json.loads(result)
        
        assert data["success"] is True
        assert "work_order_id" in data
        assert "assigned_electrician" in data
        assert "service_details" in data
        
        # Check work order ID format
        assert data["work_order_id"].startswith("WO-")
        assert len(data["work_order_id"]) == 7  # WO-XXXX format
        
        # Check assigned electrician structure
        electrician = data["assigned_electrician"]
        assert "id" in electrician
        assert "name" in electrician
        assert "rating" in electrician
        assert "phone" in electrician
        
        # Verify electrician is from the database
        valid_electricians = ["Daniel", "KA", "Tien Ha"]
        assert electrician["name"] in valid_electricians
        
        # Check service details
        service = data["service_details"]
        assert service["address"] == "123 Main St"
        assert service["issue"] == "Power outage"
        assert service["status"] == "scheduled"
        assert "scheduled_date" in service
        assert "estimated_duration" in service
        
        # Check date format (YYYY-MM-DD HH:MM)
        scheduled_date = service["scheduled_date"]
        datetime.strptime(scheduled_date, "%Y-%m-%d %H:%M")  # Should not raise exception
        
        # Check duration format
        duration = service["estimated_duration"]
        assert duration.endswith(" hours")
        assert duration.split()[0] in ["1", "2", "3", "4"]
    
    def test_assign_electrician_missing_address(self):
        """Test assign_electrician with missing address."""
        result = assign_electrician("", "Power outage")
        data = json.loads(result)
        
        assert "error" in data
        assert data["error"] == "Missing required parameters"
        assert "Both address and issue_description are required" in data["message"]
    
    def test_assign_electrician_missing_issue(self):
        """Test assign_electrician with missing issue description."""
        result = assign_electrician("123 Main St", "")
        data = json.loads(result)
        
        assert "error" in data
        assert data["error"] == "Missing required parameters"
        assert "Both address and issue_description are required" in data["message"]
    
    def test_assign_electrician_missing_both(self):
        """Test assign_electrician with both parameters missing."""
        result = assign_electrician("", "")
        data = json.loads(result)
        
        assert "error" in data
        assert data["error"] == "Missing required parameters"
    
    @patch('random.choice')
    @patch('random.randint')
    @patch('datetime.datetime')
    def test_assign_electrician_deterministic_output(self, mock_datetime, mock_randint, mock_choice):
        """Test assign_electrician with mocked functions for deterministic output."""
        # Mock the electrician choice
        mock_electrician = {"id": "1", "name": "Daniel", "rating": 4.8, "phone": "0123"}
        mock_choice.return_value = mock_electrician
        
        # Mock the work order ID and duration
        mock_randint.side_effect = [1234, 2]  # work order ID and duration
        
        
        result = assign_electrician("123 Main St", "Power outage")
        data = json.loads(result)
        
        assert data["work_order_id"] == "WO-1234"
        assert data["assigned_electrician"]["name"] == "Daniel"
        assert data["service_details"]["estimated_duration"] == "2 hours"
    
    def test_assign_electrician_all_electricians_valid(self):
        """Test that all electricians in database have required fields."""
        # Run the function multiple times to potentially get all electricians
        electricians_found = set()
        
        for _ in range(50):  # Run enough times to likely get all 3 electricians
            result = assign_electrician("123 Main St", "Power outage")
            data = json.loads(result)
            
            electrician = data["assigned_electrician"]
            electricians_found.add(electrician["name"])
            
            # Verify structure for each electrician
            assert "id" in electrician
            assert "name" in electrician
            assert "rating" in electrician
            assert "phone" in electrician
            
            # Verify types
            assert isinstance(electrician["id"], str)
            assert isinstance(electrician["name"], str)
            assert isinstance(electrician["rating"], (int, float))
            assert isinstance(electrician["phone"], str)
        
        # We should have found at least one electrician
        assert len(electricians_found) >= 1
    
    def test_assign_electrician_work_order_uniqueness(self):
        """Test that work order IDs are likely to be unique."""
        work_order_ids = set()
        
        for _ in range(10):
            result = assign_electrician("123 Main St", "Power outage")
            data = json.loads(result)
            work_order_ids.add(data["work_order_id"])
        
        # Most work order IDs should be unique (random generation)
        # Allow for some small chance of collision
        assert len(work_order_ids) >= 8