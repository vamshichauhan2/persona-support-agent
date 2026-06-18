# API Authentication Guide

If API requests return 401 Unauthorized:

1. Verify Bearer token is included.
2. Check token expiration.
3. Ensure Authorization header format:

Authorization: Bearer YOUR_TOKEN

4. Verify API key permissions.
5. Regenerate credentials if necessary.