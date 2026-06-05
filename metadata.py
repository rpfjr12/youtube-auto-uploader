# metadata.py
import random
from datetime import datetime
from modules.randomization_engine import randomize_tag_order, randomize_description_blocks
from modules.reuse_protection import ensure_unique_metadata

TITLE_TEMPLATES = [
    "{topic} Explained Fast",
    "Top {n} {topic} Tips You Need",
    "{topic} Hacks That Work",
    "How to {topic} in {minutes} Minutes",
    "I Tried {topic} So You Don't Have To",
    "{topic} Mistakes to Avoid",
    "The Truth About {topic}",
    "Why {topic} Matters"
]

DESCRIPTION_TEMPLATES = [
    "In this video we cover {topic}. Watch till the end for a bonus tip.",
    "Quick guide to {topic}. Timestamped sections below.",
    "{topic} tutorial with practical examples and steps.",
    "Short, actionable tips on {topic}. Subscribe for more.",
    "Everything you need to know about {topic} in one video.",
    "This {topic} principle changed my life. Watch to learn more."
]

HASHTAGS = [
    "#shorts", "#viral", "#motivation", "#moneytips", "#psychology",
    "#sidehustle", "#entrepreneur", "#success", "#tips", "#learnonline",
    "#personaldevelopment", "#wealth", "#habits", "#productivity"
]

TAG_POOLS = {
    "default": ["howto","tutorial","automation","tech","tips","guide","shorts","viral","motivational"],
    "finance": ["money","invest","wealth","rich","financial","business","entrepreneur"],
    "psychology": ["psychology","mindset","habits","motivation","success","personal-development"],
    "lifestyle": ["lifestyle","daily","routine","productivity","wellness","health"]
}

def _clean_topic_from_filename(file_path):
    base = file_path.split("/")[-1].rsplit(".",1)[0]
    topic = base.replace("_"," ").replace("-"," ").title()
    return topic[:80]

def generate_metadata_from_script(script_dict, channel_name="MyChannel"):
    """
    Generate metadata from a script dictionary (output of script_generator).
    
    Args:
        script_dict: dict with keys 'title', 'description', 'tags', 'script_text', 'topic'
        channel_name: Name or ID of channel
    
    Returns:
        tuple: (title, description, tags, hashtags_text)
    """
    topic = script_dict.get("topic", "General")
    
    # Use script-provided title and enhance it
    base_title = script_dict.get("title", f"{topic} Tips")
    ab_variant = random.choice(["A","B","C"])
    title = f"[{ab_variant}] {base_title}"
    
    # Use script-provided description and add CTA
    description = script_dict.get("description", "")
    description += f"\n\n✅ Subscribe for more {topic} content\n"
    description += f"👍 Drop a like if this helped you\n"
    description += f"💬 Comment your thoughts below\n"
    description += f"\nChannel: {channel_name}"
    
    # Use script tags and add common tags
    tags = script_dict.get("tags", [])[:8]  # YouTube allows max 500 chars, ~8-10 tags typical
    topic_key = "default"
    if "money" in topic.lower() or "financial" in topic.lower():
        topic_key = "finance"
    elif "psychology" in topic.lower() or "mindset" in topic.lower():
        topic_key = "psychology"
    elif "lifestyle" in topic.lower():
        topic_key = "lifestyle"
    
    # Add topic-specific tags
    topic_tags = random.sample(TAG_POOLS.get(topic_key, TAG_POOLS["default"]), 
                               min(3, len(TAG_POOLS.get(topic_key, TAG_POOLS["default"]))))
    tags = list(dict.fromkeys(tags + topic_tags))[:12]  # Combine, dedupe and limit
    tags = randomize_tag_order(tags)
    description = randomize_description_blocks(description)
    
    # Generate hashtags for description
    hashtags = random.sample(HASHTAGS, min(5, len(HASHTAGS)))
    hashtags_text = " ".join(hashtags)
    
    title, description, tags = ensure_unique_metadata(title, description, tags)
    return title, description, tags, hashtags_text


def generate_metadata(file_path, channel_name):
    """
    Legacy function: Generate metadata from filename (for backward compatibility).
    
    Args:
        file_path: Path to video file
        channel_name: Channel name or ID
    
    Returns:
        tuple: (title, description, tags)
    """
    topic = _clean_topic_from_filename(file_path)
    title_template = random.choice(TITLE_TEMPLATES)
    title = title_template.format(topic=topic, n=random.randint(3,7), minutes=random.randint(2,15))
    description_template = random.choice(DESCRIPTION_TEMPLATES)
    description = description_template.format(topic=topic)
    # add dynamic CTA and timestamp placeholder
    description += "\n\nSubscribe for more: https://www.youtube.com/channel/" + channel_name
    # tags: mix default and channel token
    tags = random.sample(TAG_POOLS["default"], min(3, len(TAG_POOLS["default"])))
    tags.append(topic.lower())
    # A/B test token
    ab_variant = random.choice(["A","B","C"])
    title = f"[{ab_variant}] {title}"
    return title, description, tags
