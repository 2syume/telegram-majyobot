from google.oauth2 import service_account

from ..config import config 

cred_file = config.get("GoogleCloud", "CredentialPath")
credentials = service_account.Credentials.from_service_account_file(cred_file)
scoped_credentials = credentials.with_scopes([
    'https://www.googleapis.com/auth/devstorage.read_write'
])
