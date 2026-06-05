# script_generator.py
import random
from datetime import datetime
from modules.reuse_protection import ensure_unique_script
from modules.retention_templates import create_retention_script, add_pattern_interrupts, style_pacing, choose_hook

TOPICS = {
    "money": {
        "hooks": [
            "Most people don't understand how money actually works.",
            "Here's the one money secret wealthy people know.",
            "This money principle changed my life.",
            "You've been lied to about money.",
            "The richest people do this with money."
        ],
        "bodies": [
            "First, understand that compound interest is your best friend. Start investing early, even with small amounts. The earlier you start, the more time your money has to grow exponentially.",
            "Second, automate your savings. Set up automatic transfers to a savings or investment account. You won't miss money you don't see.",
            "Third, diversify your income streams. Don't rely on a single source of income. Side hustles, investments, and passive income are key.",
            "Finally, spend intentionally. Every dollar you spend should align with your values. Cut unnecessary expenses and reinvest the savings."
        ],
        "ctas": [
            "What's your biggest money challenge? Let me know in the comments.",
            "If this helped, smash that like button and subscribe for more money tips.",
            "Drop a comment if you found this useful!"
        ]
    },
    "motivation": {
        "hooks": [
            "If you're feeling stuck, this is for you.",
            "Success starts with a single decision.",
            "You have more potential than you realize.",
            "Stop waiting for the perfect moment. It doesn't exist.",
            "Your future self is watching your decisions today."
        ],
        "bodies": [
            "First, define your vision. Know exactly what you want. Without a clear goal, you'll drift aimlessly.",
            "Second, break it down into small steps. Big goals feel overwhelming. But small, daily actions compound.",
            "Third, embrace failure. Every successful person has failed. It's not failure that stops people—it's giving up after failure.",
            "Finally, surround yourself with the right people. Your environment shapes your mindset. Find people who uplift and inspire you."
        ],
        "ctas": [
            "What's one goal you're working towards? Tell me below.",
            "Share this with someone who needs the motivation today.",
            "Subscribe if you're on a journey of self-improvement!"
        ]
    },
    "psychology": {
        "hooks": [
            "Psychology reveals why you make the decisions you do.",
            "Your brain is playing tricks on you. Here's why.",
            "This psychological principle explains human behavior.",
            "Understanding psychology changes everything.",
            "Most people don't realize how their mind works against them."
        ],
        "bodies": [
            "First, understand confirmation bias. Your brain seeks information that confirms what you already believe and ignores contradicting evidence.",
            "Second, know about the availability heuristic. We overestimate the likelihood of things that come to mind easily.",
            "Third, recognize social proof. People look to others' actions to determine their own. This is why trends go viral.",
            "Finally, understand sunk cost fallacy. Don't keep investing in something just because you've already invested time or money."
        ],
        "ctas": [
            "Which psychology principle affects you most? Comment below.",
            "Send this to someone who needs to understand psychology better.",
            "Like and subscribe for more psychology insights!"
        ]
    },
    "side-hustles": {
        "hooks": [
            "Anyone can start a side hustle. Here's how.",
            "These side hustles require almost no startup capital.",
            "Stop leaving money on the table. Start a side hustle.",
            "The best time to start a side hustle was yesterday. The second best time is today.",
            "Your side hustle could become your main income."
        ],
        "bodies": [
            "First, freelancing. Offer your skills online. Writing, design, coding, social media management—there's huge demand.",
            "Second, content creation. Start a YouTube channel, TikTok, or blog. Monetization takes time, but passive income follows.",
            "Third, e-commerce. Sell physical or digital products. Drop shipping, print-on-demand, or digital courses.",
            "Finally, skill-based services. Tutoring, coaching, consulting. Leverage your expertise to help others and earn."
        ],
        "ctas": [
            "Which side hustle will you start? Tell me in the comments.",
            "Drop a like if you're ready to earn extra income.",
            "Subscribe and turn that side hustle into real revenue!"
        ]
    }
}

def generate_script(topic=None, duration_seconds=45):
    """
    Generate a short-form video script (30–60 seconds).
    
    Args:
        topic: One of 'money', 'motivation', 'psychology', 'side-hustles', or None for random.
        duration_seconds: Desired duration (30-60).
    
    Returns:
        dict with keys: title, description, tags, script_text, topic
    """
    if topic is None:
        topic = random.choice(list(TOPICS.keys()))
    
    if topic not in TOPICS:
        raise ValueError(f"Unknown topic: {topic}")

    def build_script():
        pool = TOPICS[topic]
        hook = choose_hook(topic)
        body = random.choice(pool["bodies"])
        cta = random.choice(pool["ctas"])

        script_text = create_retention_script(topic, hook, body, cta)
        if random.random() < 0.4:
            script_text = add_pattern_interrupts(script_text)
        script_text = style_pacing(script_text)

        title_words = [
            f"{topic.title()} Secret",
            f"Why {topic.title()} Matters",
            f"The Truth About {topic.title()}",
            f"{topic.title()} Explained",
            f"This {topic.title()} Hack Works"
        ]
        title = f"{random.choice(title_words)}"
        description = f"Learn about {topic} in this short video. {script_text.split(chr(10))[0]}"
        tags = [topic, "shorts", "viral", "tips", "howto", topic.replace("-", "")]

        return {
            "title": title,
            "description": description,
            "tags": tags,
            "script_text": script_text,
            "topic": topic
        }

    script_dict = build_script()
    return ensure_unique_script(script_dict, build_script)


if __name__ == "__main__":
    script = generate_script()
    print(f"Topic: {script['topic']}")
    print(f"Title: {script['title']}")
    print(f"Description: {script['description']}")
    print(f"Tags: {script['tags']}")
    print(f"\nScript:\n{script['script_text']}")
