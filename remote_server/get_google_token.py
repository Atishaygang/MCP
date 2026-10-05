from google_auth_oauthlib.flow import InstalledAppFlow


SCOPES = [
    "https://www.googleapis.com/auth/drive.file"
]


flow = InstalledAppFlow.from_client_secrets_file(
    "client_secret.json",
    SCOPES
)


credentials = flow.run_local_server(
    port=0,
    access_type="offline",
    prompt="consent"
)


print("\nGOOGLE_CLIENT_ID:")
print(credentials.client_id)

print("\nGOOGLE_CLIENT_SECRET:")
print(credentials.client_secret)

print("\nGOOGLE_REFRESH_TOKEN:")
print(credentials.refresh_token)