#!/usr/bin/env python3
"""
Electric Utility MCP Server

Provides tools for checking electricity bills and assigning electricians.
"""
import sys
import os
project_root = os.path.join(os.path.dirname(__file__), '..')
print(f"Project root: {project_root}")
sys.path.append(project_root)

import json
import logging
import random

from mcp.server.fastmcp import FastMCP
from datetime import datetime
from typing import Dict, List, Optional

from settings.config import Config

# Create MCP server
mcp = FastMCP(
    "Electric Utility Server",
    port=Config.MCP.port,
    host="localhost",
    )

@mcp.tool()
def check_bill(electric_code: str, month: str, year: str) -> str:
    """
    Check electricity bill for a specific customer and month/year.
    
    Args:
        electric_code (Required): Customer's electric utility code (e.g., "E001")
        month (Required): Month in MM format (e.g., "01" for January, "12" for December)
        year (Required): Year in YYYY format (e.g., "2024")
    
    Returns:
        JSON string with bill information including amount, status, and due date
    """
    try:
        # Validate inputs
        if not electric_code or not month or not year:
            return json.dumps({
                "error": "Missing required parameters",
                "message": "electric_code, month, and year are all required"
            })
        
        # Validate month format and value
        if not month.isdigit() or not (1 <= int(month) <= 12):
            return json.dumps({
                "error": "Invalid month format",
                "message": "Month must be in (1-12)"
            })
        
        amount = round(random.uniform(10, 300), 2)
        status = random.choice(["paid", "unpaid"])
        return json.dumps({
            "electric_code": electric_code,
            "month": month,
            "year": year,
            "amount": amount,
            "status": status,
        })
    except Exception as e:
        return json.dumps({
            "error": "Internal error",
            "message": str(e)
        })

@mcp.tool()
def assign_electrician(address: str, issue_description: str) -> str:
    """
    Assign an electrician to a service request based on address and issue description.
    
    Args:
        address (Required): Customer's address where electrical work is needed
        issue_description (Required): Description of the electrical issue or work needed
    
    Returns:
        JSON string with assigned electrician information and work order details
    """
    # return "Tien Ha is going on the way to your address"
    try:
        # Validate inputs
        if not address or not issue_description:
            return json.dumps({
                "error": "Missing required parameters",
                "message": "Both address and issue_description are required"
            })
        
        ELECTTRICIANS_DATABASE = [
            {"id": "1", "name": "Hung Do", "rating": 4.8, "phone": "0123" },
            {"id": "2", "name": "Quy To", "rating": 4.5, "phone": "0456" },
            {"id": "3", "name": "Tien Ha", "rating": 1, "phone": "0789" },   
        ]
        # Randomly select an electrician
        best_electrician = random.choice(ELECTTRICIANS_DATABASE)

        # Generate a fake work order
        work_order_id = f"WO-{random.randint(1000,9999)}"
        work_order = {
            "scheduled_date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "estimated_duration": f"{random.randint(1,4)} hours"
        }

        return json.dumps({
            "success": True,
            "work_order_id": work_order_id,
            "assigned_electrician": {
                "id": best_electrician["id"],
                "name": best_electrician["name"],
                "rating": best_electrician["rating"],
                "phone": best_electrician["phone"],
            },
            "service_details": {
                "address": address,
                "issue": issue_description,
                "scheduled_date": work_order["scheduled_date"],
                "estimated_duration": work_order["estimated_duration"],
                "status": "scheduled"
            }
        })
        
    except Exception as e:
        return json.dumps({
            "error": "Internal error",
            "message": str(e)
        })

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport=Config.MCP.transport,)
