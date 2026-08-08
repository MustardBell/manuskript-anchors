"""What an anchor becomes where there is no such thing as an anchor.

A forum post is one page. There is nowhere for an anchor to be and nothing
that could link to it, and BBCode says so by having no tag for either. The
raw ``<a name="scene">`` a writer typed is not markup there -- it is six
visible words in the middle of their post.

So on the way to BBCode an anchor is dropped and whatever it wrapped is
kept, and a link that pointed at one keeps its words and loses the link.
Nothing is lost that could have been carried, and nothing is left behind
that a reader would see.
"""

import re

from manuskript.plugins import MarkupRule


#: An anchor naming a place, with or without a closing tag. The pair is
#: optional and cannot reach past the next ``<``, so an unclosed anchor takes
#: nothing with it and a closing tag belonging to something else is safe.
ANCHOR = (
    r'<a\s+(?:name|id)=(["\']).*?\1[^>]*>'
    r'(?:(?P<text>[^<]*)</a>)?'
)

#: A link whose target is only a fragment: somewhere in this manuscript, and
#: therefore nowhere in a forum post. A link to another document keeps its
#: link, fragment or not, because that target still exists.
FRAGMENT_LINK = r'\[url=#[^\]]*\](?P<text>.*?)\[/url\]'


def _kept(match):
    return match.group("text") or ""


def anchor_rule():
    """The anchor goes, its words stay."""
    return MarkupRule(ANCHOR, _kept, re.IGNORECASE)


def fragment_link_rule():
    """The link goes, its words stay."""
    return MarkupRule(FRAGMENT_LINK, _kept, re.DOTALL)
