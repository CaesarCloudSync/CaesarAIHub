import re
from CaesarAIConstants import CaesarAIConstants
class CaesarAIUtils:
    @staticmethod
    def sanitize_text(text):
        value = text.strip()
        value = re.sub(CaesarAIConstants.TEXT_SANITIZE_REGEX, " ", text)
        return value