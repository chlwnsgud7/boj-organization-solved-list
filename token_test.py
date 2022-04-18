import requests

headerDict = {}
headerDict.setdefault('solvedacToken','eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJoYW5kbGUiOiJzaW9udGFtYSIsImlhdCI6MTY0OTkyMzkyNn0.HAJLzpWR5GRoTdtE0aIkGZ33hX9BVGHAh5-bEpZAI8U')
url = f"https://solved.ac/api/v3/account/verify_credentials"
print(requests.get(url, headers=headerDict))