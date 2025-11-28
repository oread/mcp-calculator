# dataverse.py
from fastmcp import FastMCP
import sys
import logging
import json
import requests
from typing import Optional, Dict, Any
from datetime import datetime, timedelta

logger = logging.getLogger('Dataverse')

# Fix UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stderr.reconfigure(encoding='utf-8')
    sys.stdout.reconfigure(encoding='utf-8')

# Create an MCP server
mcp = FastMCP("Dataverse")

# Dataverse API configuration
DATAVERSE_URL = ""  # e.g., "https://yourorg.crm.dynamics.com"
CLIENT_ID = ""      # Azure AD Application (client) ID
CLIENT_SECRET = ""  # Azure AD Application client secret
TENANT_ID = ""      # Azure AD Tenant ID
ACCESS_TOKEN = ""   # Cached OAuth token
TOKEN_EXPIRY = None # Token expiration time


def get_access_token() -> str:
    """
    Get a valid access token, refreshing if necessary.
    Uses OAuth 2.0 client credentials flow.
    
    Returns:
        Valid access token string
    """
    global ACCESS_TOKEN, TOKEN_EXPIRY
    
    # Check if we have a valid cached token
    if ACCESS_TOKEN and TOKEN_EXPIRY and datetime.now() < TOKEN_EXPIRY:
        return ACCESS_TOKEN
    
    # Request a new token
    if not CLIENT_ID or not CLIENT_SECRET or not TENANT_ID:
        raise ValueError("Client ID, Client Secret, and Tenant ID must be configured")
    
    token_url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
    
    token_data = {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'scope': f'{DATAVERSE_URL}/.default'
    }
    
    try:
        response = requests.post(token_url, data=token_data)
        response.raise_for_status()
        
        token_response = response.json()
        ACCESS_TOKEN = token_response['access_token']
        
        # Set expiry time with 5-minute buffer
        expires_in = token_response.get('expires_in', 3600)
        TOKEN_EXPIRY = datetime.now() + timedelta(seconds=expires_in - 300)
        
        logger.info("Successfully obtained new access token")
        return ACCESS_TOKEN
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to obtain access token: {str(e)}")
        raise


@mcp.tool()
def query_dataverse(
    entity_name: str,
    select_fields: Optional[str] = None,
    filter_query: Optional[str] = None,
    top: Optional[int] = 10
) -> dict:
    """
    Query Dataverse entities using OData syntax.
    
    Args:
        entity_name: The logical name of the entity to query (e.g., 'accounts', 'contacts')
        select_fields: Comma-separated list of fields to select (e.g., 'name,accountid')
        filter_query: OData filter query (e.g., "revenue gt 100000")
        top: Maximum number of records to return (default: 10)
    
    Returns:
        Dictionary with success status and query results
    """
    try:
        if not DATAVERSE_URL:
            return {
                "success": False,
                "error": "Dataverse URL must be configured"
            }
        
        # Get access token
        token = get_access_token()
        
        # Build the query URL
        url = f"{DATAVERSE_URL}/api/data/v9.2/{entity_name}"
        
        # Build query parameters
        params = {}
        if select_fields:
            params['$select'] = select_fields
        if filter_query:
            params['$filter'] = filter_query
        if top:
            params['$top'] = top
        
        # Make the request
        headers = {
            'Authorization': f'Bearer {token}',
            'Accept': 'application/json',
            'OData-MaxVersion': '4.0',
            'OData-Version': '4.0'
        }
        
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        
        data = response.json()
        logger.info(f"Query successful: {entity_name}, returned {len(data.get('value', []))} records")
        
        return {
            "success": True,
            "data": data.get('value', []),
            "count": len(data.get('value', []))
        }
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Query failed: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }


@mcp.tool()
def create_dataverse_record(
    entity_name: str,
    record_data: str
) -> dict:
    """
    Create a new record in Dataverse.
    
    Args:
        entity_name: The logical name of the entity (e.g., 'accounts', 'contacts')
        record_data: JSON string containing the record data
    
    Returns:
        Dictionary with success status and created record ID
    """
    try:
        if not DATAVERSE_URL:
            return {
                "success": False,
                "error": "Dataverse URL must be configured"
            }
        
        # Get access token
        token = get_access_token()
        
        # Parse the record data
        data = json.loads(record_data)
        
        # Build the URL
        url = f"{DATAVERSE_URL}/api/data/v9.2/{entity_name}"
        
        # Make the request
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'OData-MaxVersion': '4.0',
            'OData-Version': '4.0'
        }
        
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        
        # Get the created record ID from the response header
        record_url = response.headers.get('OData-EntityId', '')
        record_id = record_url.split('(')[-1].rstrip(')') if record_url else None
        
        logger.info(f"Record created successfully in {entity_name}, ID: {record_id}")
        
        return {
            "success": True,
            "record_id": record_id,
            "record_url": record_url
        }
        
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON data: {str(e)}")
        return {
            "success": False,
            "error": f"Invalid JSON data: {str(e)}"
        }
    except requests.exceptions.RequestException as e:
        logger.error(f"Create failed: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }


@mcp.tool()
def update_dataverse_record(
    entity_name: str,
    record_id: str,
    record_data: str
) -> dict:
    """
    Update an existing record in Dataverse.
    
    Args:
        entity_name: The logical name of the entity (e.g., 'accounts', 'contacts')
        record_id: The GUID of the record to update
        record_data: JSON string containing the fields to update
    
    Returns:
        Dictionary with success status
    """
    try:
        if not DATAVERSE_URL:
            return {
                "success": False,
                "error": "Dataverse URL must be configured"
            }
        
        # Get access token
        token = get_access_token()
        
        # Parse the record data
        data = json.loads(record_data)
        
        # Build the URL
        url = f"{DATAVERSE_URL}/api/data/v9.2/{entity_name}({record_id})"
        
        # Make the request
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'OData-MaxVersion': '4.0',
            'OData-Version': '4.0'
        }
        
        response = requests.patch(url, headers=headers, json=data)
        response.raise_for_status()
        
        logger.info(f"Record updated successfully in {entity_name}, ID: {record_id}")
        
        return {
            "success": True,
            "record_id": record_id
        }
        
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON data: {str(e)}")
        return {
            "success": False,
            "error": f"Invalid JSON data: {str(e)}"
        }
    except requests.exceptions.RequestException as e:
        logger.error(f"Update failed: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }


@mcp.tool()
def delete_dataverse_record(
    entity_name: str,
    record_id: str
) -> dict:
    """
    Delete a record from Dataverse.
    
    Args:
        entity_name: The logical name of the entity (e.g., 'accounts', 'contacts')
        record_id: The GUID of the record to delete
    
    Returns:
        Dictionary with success status
    """
    try:
        if not DATAVERSE_URL:
            return {
                "success": False,
                "error": "Dataverse URL must be configured"
            }
        
        # Get access token
        token = get_access_token()
        
        # Build the URL
        url = f"{DATAVERSE_URL}/api/data/v9.2/{entity_name}({record_id})"
        
        # Make the request
        headers = {
            'Authorization': f'Bearer {token}',
            'Accept': 'application/json',
            'OData-MaxVersion': '4.0',
            'OData-Version': '4.0'
        }
        
        response = requests.delete(url, headers=headers)
        response.raise_for_status()
        
        logger.info(f"Record deleted successfully from {entity_name}, ID: {record_id}")
        
        return {
            "success": True,
            "record_id": record_id
        }
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Delete failed: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }


@mcp.tool()
def configure_dataverse(
    dataverse_url: str,
    client_id: str,
    client_secret: str,
    tenant_id: str
) -> dict:
    """
    Configure Dataverse connection settings using OAuth client credentials.
    
    Args:
        dataverse_url: The Dataverse organization URL (e.g., 'https://yourorg.crm.dynamics.com')
        client_id: Azure AD Application (client) ID
        client_secret: Azure AD Application client secret
        tenant_id: Azure AD Tenant ID
    
    Returns:
        Dictionary with success status
    """
    global DATAVERSE_URL, CLIENT_ID, CLIENT_SECRET, TENANT_ID, ACCESS_TOKEN, TOKEN_EXPIRY
    
    try:
        DATAVERSE_URL = dataverse_url.rstrip('/')
        CLIENT_ID = client_id
        CLIENT_SECRET = client_secret
        TENANT_ID = tenant_id
        
        # Clear cached token
        ACCESS_TOKEN = ""
        TOKEN_EXPIRY = None
        
        # Test the configuration by obtaining a token
        try:
            token = get_access_token()
            logger.info(f"Dataverse configured and authenticated: {DATAVERSE_URL}")
            
            return {
                "success": True,
                "message": "Dataverse connection configured and authenticated successfully"
            }
        except Exception as auth_error:
            logger.error(f"Authentication failed: {str(auth_error)}")
            return {
                "success": False,
                "error": f"Configuration saved but authentication failed: {str(auth_error)}"
            }
        
    except Exception as e:
        logger.error(f"Configuration failed: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }


# Start the server
if __name__ == "__main__":
    mcp.run(transport="stdio")
