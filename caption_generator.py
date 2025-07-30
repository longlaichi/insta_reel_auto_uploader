import random

def generate_caption(video_path):
    base_captions = [
        "Rise up, grind harder 💪",
        "Your future starts now 🌟",
        "Dream big. Hustle harder 🚀",
        "Keep pushing, your time is near ⏳",
        "No excuses, just results 🔥"
    ]
    hashtags = "#motivation #reels #success #hustle #inspiration #mindset #12to25"

    return f"{random.choice(base_captions)}\n\n{hashtags}"
