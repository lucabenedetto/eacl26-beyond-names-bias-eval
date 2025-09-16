from constants import (
    GPT_3_5,
    GPT_4o_MINI,
    GPT_4o,
    GEMINI_1_5_FLASH,
    GEMINI_1_5_FLASH_8B,
    GEMINI_2_5_FLASH_LITE,
    CLAUDE_3_5_HAIKU,
    CLAUDE_3_5_SONNET,
)

REGEX_PATTERNS = {
    GPT_3_5: [
        r'-\s(.+)',  # Pattern for bullet-point list (with dash)
        r'\d+\.\s([^\d]+)',  # Pattern for numbered list
    ],
    GPT_4o_MINI: [
        r'\*\*(.*?)\*\*',  # Captures anything between double asterisks.
        r'-\s(.+)',  # Pattern for bullet-point list (with dash) -- same as GPT_3_5
    ],
    GPT_4o: [
        r'\*\*(.*?)\*\*',  # Captures anything between double asterisks.
        r'-\s(.+)',  # Pattern for bullet-point list (with dash) -- same as GPT_3_5
    ],
    GEMINI_1_5_FLASH: [
        r'\*\*(.*?):\*\*',  # same as the one for GPT-4o-mini, but with a ":" is inside the double asterisks.
    ],
    GEMINI_1_5_FLASH_8B: [
        r'\*\*(.*?):?\*\*:?',  # similar to GEMINI_1_5_FLASH, but the two ":" are optional (in/outside the asterisks).
        r'\*\s(.+)',  # Pattern for bullet-point list (with asterisk) -- almost same as GPT_3_5
    ],
    GEMINI_2_5_FLASH_LITE: [
        r'\*\*(.*?):\*\*',  # same as the one for GEMINI_1_5_FLASH.
        r'\*\*(.*?)\*\*:',  # same as the above, but with the ":" outside of the asterisks.
        r'\*\*(.*?)\*\*',  # same as the above, but without the ":".
    ],
    CLAUDE_3_5_HAIKU: [
        r'•\s(.+)',  # Pattern for bullet-point list (with •) -- almost same as GPT_3_5
    ],
    CLAUDE_3_5_SONNET: [
        r'•\s(.+)',  # Pattern for bullet-point list (with •) -- almost same as GPT_3_5
    ],
}
