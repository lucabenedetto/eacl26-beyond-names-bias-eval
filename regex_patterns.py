from constants import (
    GPT_3_5,
    GPT_4o_MINI,
    GEMINI_1_5_FLASH,
    GEMINI_1_5_FLASH_8B,
    CLAUDE_3_5_HAIKU,
)

REGEX_PATTERNS = {
    GPT_3_5: [
        r'-\s(.+)',  # Pattern for bullet-point list
        r'\d+\.\s([^\d]+)',  # Pattern for numbered list
    ],
#     pattern = r'-\s(.+)'
#     # -    --> Matches the literal hyphen at the beginning of each line.
#     # \s   --> Matches the space following the hyphen.
#     # (.+) --> Captures everything after the space until the end of the line (the course name).
#     pattern = r'\d+\.\s([^\d]+)'
#     # \d+ - Matches one or more digits (the numbering of the courses).
#     # \. - Matches the literal period after the number.
#     # \s - Matches the space following the period.
#     # ([^\d]+) - Captures everything that is not a digit (the course name) until the next number is encountered.
    GPT_4o_MINI: [
        r'\*\*(.*?)\*\*',
        r'-\s(.+)',  # Pattern for bullet-point list (same as GPT_3_5)
    ],
    GEMINI_1_5_FLASH: [
        r'\*\*(.*?):\*\*',  # same as the one for GPT-4o-mini, but with the column (:) between the double asterisks.
    ],
    GEMINI_1_5_FLASH_8B: [
        r'\*\*(.*?):?\*\*:?',  # similar as the one for GPT-4o-mini, but with the two columns (:) are optional (between or out of the asterisks).
        r'\*\s(.+)',  # Pattern for bullet-point list (almost the same as GPT_3_5, but with asterisk instead of dash)
    ],
    CLAUDE_3_5_HAIKU: [
        r'•\s(.+)',  # Pattern for bullet-point list (almost the same as GPT_3_5, but with • instead of dash)
    ],
}
