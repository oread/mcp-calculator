# Dataverse Authentication Setup

## Overview
The Dataverse MCP tool now uses OAuth 2.0 client credentials flow for authentication instead of requiring a pre-configured access token.

## Prerequisites

### 1. Register an Azure AD Application

1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to **Azure Active Directory** > **App registrations** > **New registration**
3. Provide a name (e.g., "Dataverse MCP Tool")
4. Click **Register**

### 2. Create Client Secret

1. In your app registration, go to **Certificates & secrets**
2. Click **New client secret**
3. Add a description and select expiration period
4. Click **Add**
5. **Copy the secret value immediately** (it won't be shown again)

### 3. Grant API Permissions

1. In your app registration, go to **API permissions**
2. Click **Add a permission** > **Dynamics CRM**
3. Select **Delegated permissions** or **Application permissions** depending on your use case
4. Add **user_impersonation** permission
5. Click **Grant admin consent**

### 4. Get Your Tenant ID

1. In Azure AD, go to **Overview**
2. Copy the **Tenant ID** (also called Directory ID)

## Configuration

### Required Information

You need to collect the following:

- **Dataverse URL**: Your organization's Dataverse URL (e.g., `https://yourorg.crm.dynamics.com`)
- **Client ID**: The Application (client) ID from your Azure AD app registration
- **Client Secret**: The client secret value you created
- **Tenant ID**: Your Azure AD tenant ID

### Using the Tool

1. **Configure the connection** by calling the `configure_dataverse` tool:

```python
{
  "dataverse_url": "https://yourorg.crm.dynamics.com",
  "client_id": "your-client-id-here",
  "client_secret": "your-client-secret-here",
  "tenant_id": "your-tenant-id-here"
}
```

This will:
- Save your credentials
- Automatically obtain an OAuth access token
- Cache the token for future requests
- Return success/failure status

2. **Use any Dataverse operations**:
   - `query_dataverse` - Query entities
   - `create_dataverse_record` - Create records
   - `update_dataverse_record` - Update records
   - `delete_dataverse_record` - Delete records

The tool will automatically:
- Request access tokens when needed
- Cache tokens to avoid unnecessary requests
- Refresh expired tokens automatically
- Include proper OAuth headers in all API calls

## Token Management

- Access tokens are cached and reused until they expire
- Tokens automatically refresh 5 minutes before expiration
- Each token is valid for approximately 1 hour
- No manual token management required

## Security Best Practices

1. **Never commit credentials** to version control
2. **Use environment variables** or secure vaults for secrets
3. **Rotate client secrets** regularly
4. **Grant minimum required permissions**
5. **Monitor application usage** in Azure AD

## Troubleshooting

### Authentication Errors

If you get authentication errors:
- Verify your client ID, secret, and tenant ID are correct
- Ensure the Azure AD app has proper API permissions
- Confirm admin consent was granted for the permissions
- Check that the client secret hasn't expired

### API Call Errors

If API calls fail after successful authentication:
- Verify the Dataverse URL is correct
- Ensure the app has permissions for the specific operations
- Check that the entity names are correct (use logical names)

## Running the Tool

```bash
# Set the MCP endpoint
export MCP_ENDPOINT="wss://api.xiaozhi.me/mcp/?token=YOUR_TOKEN"

# Run the Dataverse MCP tool
python mcp_pipe.py dataverse.py
```

Then configure it using the AI model with the `configure_dataverse` tool before performing any operations.
