import requests
headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI1IiwiZXhwIjoxNzkwODA4NTM4fQ.qKRHveEcl78siD6fkWfEJ3L9DpRtKB8tby6vG9KY2Ws"
}
requisicao = requests.get('http://127.0.0.1:8000/auth/refresh', headers=headers)
print(requisicao)
print(requisicao.json())