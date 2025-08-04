from instagrapi import Client

cl = Client()
cl.login("dailysparkshots", "PoorveshNew123*")
cl.dump_settings("insta_session.json")
print("✅ Session saved to insta_session.json")
