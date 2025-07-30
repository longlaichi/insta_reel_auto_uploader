from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()

# Try loading credentials if they already exist
gauth.LoadCredentialsFile("tokens.json")

# If no valid credentials, start browser OAuth flow
if gauth.credentials is None:
    gauth.LocalWebserverAuth()
elif gauth.access_token_expired:
    gauth.Refresh()
else:
    gauth.Authorize()

# Save the access token to a file manually
gauth.SaveCredentialsFile("tokens.json")

# Initialize drive just to verify things work
drive = GoogleDrive(gauth)

print("Token generated successfully and saved as tokens.json.")
