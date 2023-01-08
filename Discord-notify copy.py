import requests
r = requests.post('https://discord.com/api/webhooks/', json={
'id':	"975317056301989919",
'name': "掛機行為通知",
'avatar': "null",
'channel_id': "975337620504711218",
'guild_id': "561946008452464659",
'application_id': "null",
'token': "jONaukH_iyF40G6Y4s6UX0jhk5ZXT4DJjnyGceSGa6ZcJFiGYibWdSHItLKUX",
'message': 'sdf456465',
})
print(f"Status Code: {r.status_code}, Response: {r.json()}")