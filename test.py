import requests, os

requests.post('https://api.mynotifier.app', {
    "apiKey": os.environ.get("MYNOTIFIER_API_KEY"),
    "message": "Test",
    "description": "Test",
    "type": "info", # info, error, warning or success
})