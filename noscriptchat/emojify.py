import unittest
import re
import unicodedata
from typing import Dict, List


class Emojify:

    _RE_EMOJI = re.compile(r":([a-z]+[a-z0-9_\-]*):", re.IGNORECASE)
    _ALIASES = {}

    def __init__(self):

        self.emoji_map: Dict[str, int] = {}
        self.emoji_map_concat: Dict[str, int] = {}
        for c in range(32, 0x110000):
            ch = chr(c)
            cat = unicodedata.category(ch)
            try:
                if cat == "So":
                    name = self._normalize_name(unicodedata.name(ch))
                    self.emoji_map[name] = c
                    if "-" in name:
                        self.emoji_map_concat[name.replace("-", "")] = c
            except ValueError:
                pass

    def emojify(self, text: str):
        return self._RE_EMOJI.sub(self._replace_tags, text)

    def _replace_tags(self, match: re.Match):
        name = self._normalize_name(match.groups()[0])

        emoji_code = self.emoji_map.get(name, self.emoji_map_concat.get(name))
        if emoji_code is not None:
            return chr(emoji_code)

        return f":{match.groups()[0]}:"

    def _normalize_name(self, name: str) -> str:
        name = (
            name.lower()
            .replace(" ", "-")
            .replace("_", "-")
        )
        if name.endswith("-face"):
            name = name[:-5]
        return name


singleton = Emojify()


def emojify(text: str) -> str:
    """
    Static method to convert :emoji: tags to unicode
    """
    return singleton.emojify(text)


class TestEmojify(unittest.TestCase):

    def test_100_emojify(self):
        self.assertEqual(
            "text bla bla",
            emojify("text bla bla"),
        )
        self.assertEqual(
            "text ⚘ bla bla",
            emojify("text :flower: bla bla"),
        )
        self.assertEqual(
            "text ⚘X: bla bla",
            emojify("text :flower:X: bla bla"),
        )
