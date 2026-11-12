"""
paragraphs.py - Sample paragraphs for TypeMaster Typing Speed Test.
Provides a diverse collection of engaging, realistic paragraphs across various
topics (technology, science, nature, programming, literature, and productivity).
"""

import random
from typing import Dict, List, Optional

# A curated pool of 12 engaging paragraphs for the typing speed test.
# Word counts range from 65 to 110 words, ideal for standard 60-second typing tests.
SAMPLE_PARAGRAPHS: List[Dict[str, str]] = [
    {
        "id": "ai_future",
        "title": "Artificial Intelligence and the Future",
        "topic": "Technology",
        "text": (
            "Artificial intelligence is transforming the way we live and work across the globe. "
            "From diagnosing medical conditions to driving autonomous vehicles, intelligent algorithms "
            "are solving complex challenges faster than ever. However, the true promise of modern technology "
            "lies in how it empowers human creativity and collaboration rather than replacing it. "
            "As we design smarter systems, ethics, transparency, and fairness must remain our top priorities."
        ),
    },
    {
        "id": "art_of_coding",
        "title": "The Art and Craft of Programming",
        "topic": "Programming",
        "text": (
            "Writing good code is much like composing music or crafting a fine piece of literature. "
            "Every variable name, loop, and function carries purpose and intent. Experienced software engineers "
            "know that readable code is always superior to clever tricks that confuse future maintainers. "
            "When you write clean, well-tested programs, you build reliable foundations that can endure "
            "for years and bring meaningful solutions to people worldwide."
        ),
    },
    {
        "id": "deep_space",
        "title": "Cosmic Wonders and Deep Space",
        "topic": "Astronomy",
        "text": (
            "Looking up at a clear night sky reminds us of our humble place in an infinite universe. "
            "Billions of distant galaxies stretch across cosmic horizons, each harboring trillions of stars "
            "and unexplored planetary systems. Deep space telescopes capture faint light that began its long journey "
            "before our planet was even formed. Exploring the cosmos inspires curiosity and pushes humanity to dream bigger."
        ),
    },
    {
        "id": "ocean_depths",
        "title": "Mysteries of the Deep Ocean",
        "topic": "Nature",
        "text": (
            "Earth is truly an ocean planet, with more than seventy percent of its surface submerged beneath water. "
            "The mysterious midnight zone remains less explored than the surface of the Moon. In pitch-black waters, "
            "strange bioluminescent creatures glow with vibrant blue and green lights to attract prey and communicate. "
            "Protecting these fragile marine habitats is vital for preserving the delicate biological balance of our world."
        ),
    },
    {
        "id": "small_habits",
        "title": "The Power of Atomic Habits",
        "topic": "Productivity",
        "text": (
            "True personal transformation rarely happens through sudden monumental leaps. Instead, remarkable "
            "achievements are the steady compound interest of tiny everyday habits. Improving by just one percent "
            "each morning feels insignificant in the moment, but over a single year, those incremental gains multiply "
            "into profound excellence. Consistency and patience will always outperform sporadic bursts of intense effort."
        ),
    },
    {
        "id": "digital_security",
        "title": "Cybersecurity in a Connected World",
        "topic": "Cybersecurity",
        "text": (
            "In our interconnected digital landscape, safeguarding sensitive personal data has become essential. "
            "Every email, financial transaction, and cloud backup relies on cryptographic protocols to ensure confidentiality. "
            "Strong multi-factor authentication, mindful browsing habits, and prompt system updates provide essential defenses "
            "against unauthorized intrusions. Vigilance and digital literacy protect our privacy and trust online."
        ),
    },
    {
        "id": "mindfulness",
        "title": "Mindfulness and Daily Stillness",
        "topic": "Wellbeing",
        "text": (
            "Modern life frequently surrounds us with endless notifications, urgent deadlines, and sensory overload. "
            "Practicing quiet mindfulness offers a valuable refuge where our minds can rest and reset. Taking a few deep, "
            "conscious breaths before tackling a difficult task restores mental clarity and improves emotional resilience. "
            "True productivity is not about nonstop motion, but about directing steady attention where it matters most."
        ),
    },
    {
        "id": "green_energy",
        "title": "Renewable Energy and Clean Energy",
        "topic": "Environment",
        "text": (
            "Transitioning away from fossil fuels toward sustainable energy sources is the defining mission of our era. "
            "Towering offshore wind turbines and vast solar arrays harvest clean, infinite power directly from nature. "
            "Advances in modern battery storage now allow communities to preserve surplus electricity for cloudy and calm days. "
            "Investing in green technology ensures our children will inherit a cleaner, healthier, and thriving planet."
        ),
    },
    {
        "id": "joy_of_reading",
        "title": "The Timeless Joy of Reading",
        "topic": "Literature",
        "text": (
            "A good book is a portable magic portal that lets you travel across centuries and converse with the greatest thinkers. "
            "Reading exercises the imagination in ways passive screens never can, inviting your brain to envision distant kingdoms "
            "and complex emotions. Whether you enjoy ancient philosophy, gripping mysteries, or scientific discoveries, regular "
            "reading enriches your vocabulary, sharpens your focus, and expands your empathy for others."
        ),
    },
    {
        "id": "internet_history",
        "title": "The Evolution of the Global Internet",
        "topic": "History",
        "text": (
            "What began decades ago as a modest experimental research network has blossomed into the nervous system of modern humanity. "
            "Submarine fiber optic cables crisscross ocean floors, transmitting terabits of voice, video, and code across continents "
            "in the blink of an eye. The internet has democratized knowledge, enabled global commerce, and united distant families. "
            "Its open architecture proves that shared open protocols can connect diverse cultures peacefully."
        ),
    },
    {
        "id": "music_creativity",
        "title": "The Universal Language of Music",
        "topic": "Culture",
        "text": (
            "Music is a universal language that transcends geographical borders, speaking directly to the human heart. "
            "A delicate acoustic melody or a thunderous orchestral symphony can awaken memories long forgotten and soothe wounded spirits. "
            "Neuroscientists have discovered that listening to or playing instruments engages nearly every area of the brain simultaneously. "
            "Melody, harmony, and rhythm provide a timeless sanctuary for expressing our deepest hopes and vulnerabilities."
        ),
    },
    {
        "id": "quantum_leap",
        "title": "The Frontier of Quantum Computing",
        "topic": "Science",
        "text": (
            "Quantum computers harness the mysterious behavior of subatomic particles to process information in revolutionary ways. "
            "While classical computers calculate using bits of zeros and ones, quantum qubits exist in superpositions of both states. "
            "This remarkable quantum parallelism enables researchers to simulate complex molecular interactions and optimize logistics "
            "far beyond the reach of conventional supercomputers, opening exciting new horizons in science and medicine."
        ),
    },
]


def get_all_paragraphs() -> List[Dict[str, str]]:
    """Return the complete list of sample paragraphs."""
    return list(SAMPLE_PARAGRAPHS)


def get_random_paragraph(exclude_id: Optional[str] = None) -> Dict[str, str]:
    """
    Select and return a random paragraph.
    If exclude_id is provided, avoids returning the same paragraph back-to-back.
    """
    candidates = [p for p in SAMPLE_PARAGRAPHS if p["id"] != exclude_id]
    if not candidates:
        candidates = SAMPLE_PARAGRAPHS
    return random.choice(candidates)


def get_paragraph_by_id(pid: str) -> Optional[Dict[str, str]]:
    """Lookup a paragraph by its unique identifier."""
    for p in SAMPLE_PARAGRAPHS:
        if p["id"] == pid:
            return p
    return None

