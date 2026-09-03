import json
import urllib.request
from appconfig import GROQ_API_KEY

req = urllib.request.Request(
    'https://api.groq.com/openai/v1/models',
    headers={
        'Authorization': 'Bearer ' + GROQ_API_KEY,
        'User-Agent': 'python-urllib',
    },
)
with urllib.request.urlopen(req, timeout=60) as r:
    data = json.loads(r.read().decode())

for item in sorted(data.get('data', []), key=lambda x: x.get('id', '')):
    print(item.get('id'))
