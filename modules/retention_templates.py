import random
from typing import List

HOOK_PATTERNS = [
    "What if I told you {topic} is easier than you think?",
    "Nobody talks about this {topic} truth.",
    "This one idea about {topic} will change your mind.",
    "If you want better {topic} results, watch this.",
]

CURIOSITY_FRAMES = [
    "You won't believe how simple this is.",
    "Stay tuned, because the payoff is coming next.",
    "This surprising insight is what most people miss.",
    "There's one detail that makes the difference.",
]

PAYOFF_LINES = [
    "In the end, the real change comes from one small shift.",
    "Now you know what to do next.",
    "That’s how you make {topic} work for you.",
    "Use this right away and you'll see a difference.",
]

PATTERN_INTERRUPTS = [
    "Wait, this part matters most.",
    "Here's the twist.",
    "Hang on, listen carefully.",
    "Don't skip this next step.",
]

OPEN_LOOP_PROMPTS = [
    "In a moment, I'll share the exact step to change everything.",
    "Later I'll reveal the mistake most people make.",
    "Keep watching because the payoff is worth it.",
    "I’ll show you the best way to use this in just seconds.",
]


def create_retention_script(topic: str, hook: str, body: str, cta: str) -> str:
    hook_line = hook.format(topic=topic)
    payoff_line = random.choice(PAYOFF_LINES).format(topic=topic)
    open_loop = random.choice(OPEN_LOOP_PROMPTS)
    return f"{hook_line}\n\n{open_loop}\n\n{body}\n\n{random.choice(PATTERN_INTERRUPTS)}\n\n{payoff_line}\n\n{cta}"


def add_pattern_interrupts(script_text: str) -> str:
    parts = [part.strip() for part in script_text.split("\n\n") if part.strip()]
    if len(parts) < 2:
        return script_text
    index = min(len(parts) - 1, 1)
    parts.insert(index, random.choice(PATTERN_INTERRUPTS))
    return "\n\n".join(parts)


def style_pacing(script_text: str) -> str:
    lines = [line.strip() for line in script_text.split("\n") if line.strip()]
    paced_lines = []
    for idx, line in enumerate(lines):
        paced_lines.append(line)
        if idx % 2 == 1:
            paced_lines.append(random.choice(OPEN_LOOP_PROMPTS))
    return "\n\n".join(paced_lines)


def choose_hook(topic: str) -> str:
    return random.choice(HOOK_PATTERNS).format(topic=topic)
