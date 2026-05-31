# metadata.py
import random
from datetime import datetime

TITLE_TEMPLATES = [
    "{topic} Explained Fast",
    "Top {n} {topic} Tips You Need",
    "{topic} Hacks That Work",
    "How to {topic} in {minutes} Minutes",
    "I Tried {topic} So You Don't Have To",
    "{topic} Mistakes to Avoid"
]

DESCRIPTION_TEMPLATES = [
    "In this video we cover {topic}. Watch till the end for a bonus tip.",
    "Quick guide to {topic}. Timestamped sections below.",
    "{topic} tutorial with practical examples and steps.",
    "Short, actionable tips on {topic}. Subscribe for more."
]

TAG_POOLS = {
    "default": ["howto","tutorial","automation","tech","tips","guide"],
    "niche": ["nicheA","nicheB","nicheC"]
}

def _clean_topic_from_filename(file_path):
    base = file_path.split("/")[-1].rsplit(".",1)[0]
    topic = base.replace("_"," ").replace("-"," ").title()
    return topic[:80]

def generate_metadata(file_path, channel_name):
    topic = _clean_topic_from_filename(file_path)
    title_template = random.choice(TITLE_TEMPLATES)
    title = title_template.format(topic=topic, n=random.randint(3,7), minutes=random.randint(2,15))
    description_template = random.choice(DESCRIPTION_TEMPLATES)
    description = description_template.format(topic=topic)
    # add dynamic CTA and timestamp placeholder
    description += "\n\nSubscribe for more: https://www.youtube.com/channel/" + channel_name
    # tags: mix default, niche, and channel token
    tags = random.sample(TAG_POOLS["default"], min(3, len(TAG_POOLS["default"])))
    tags += random.sample(TAG_POOLS["niche"], min(2, len(TAG_POOLS["niche"])))
    tags.append(channel_name)
    # A/B test token
    ab_variant = random.choice(["A","B","C"])
    title = f"[{ab_variant}] {title}"
    return title, description, tags
