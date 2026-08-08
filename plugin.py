"""Registration. Three additions to two conversions, no state.

One subject -- a named place in a manuscript -- and each route says what it
can make of it. Nothing here decides which route matters; the host asks for a
conversion and whichever of these applies is applied.
"""

from manuskript.plugins import (
    ConversionAugmentationContribution,
    ExtensionDescriptor,
)

from .bbcode import anchor_rule, fragment_link_rule
from .extension import Anchors


#: Declared in plugin.json, and named here rather than assumed: an addition
#: belongs to a route, not to a kind of contribution.
MARKDOWN = "text/markdown"
HTML = "text/html"
BBCODE = "text/x-bbcode"


def register(api):
    api.register_conversion_augmentation(
        ConversionAugmentationContribution(
            descriptor=ExtensionDescriptor(
                id="manuskript.anchors.html",
                name="Anchors in HTML",
                description=(
                    "An anchor a writer typed becomes one a page can be "
                    "linked to, and marks the heading or paragraph it was "
                    "written above."
                ),
            ),
            source_format=MARKDOWN,
            target_format=HTML,
            augmentation_factory=Anchors,
            # Every document. A named place means the same thing wherever it
            # is written, and narrowing it to page types would make an
            # anchor's meaning depend on which document it is in.
            page_types=(),
        )
    )
    api.register_conversion_augmentation(
        ConversionAugmentationContribution(
            descriptor=ExtensionDescriptor(
                id="manuskript.anchors.bbcode",
                name="Anchors in BBCode",
                description=(
                    "BBCode has no anchor, so the anchor is dropped and "
                    "the words it wrapped are kept."
                ),
            ),
            source_format=MARKDOWN,
            target_format=BBCODE,
            augmentation_factory=anchor_rule,
            page_types=(),
        )
    )
    api.register_conversion_augmentation(
        ConversionAugmentationContribution(
            descriptor=ExtensionDescriptor(
                id="manuskript.anchors.bbcode-links",
                name="Links to anchors in BBCode",
                description=(
                    "A link to a place in this manuscript points nowhere in "
                    "a forum post, so it keeps its words and loses the link."
                ),
            ),
            source_format=MARKDOWN,
            target_format=BBCODE,
            augmentation_factory=fragment_link_rule,
            # After the anchor rule, so a link wrapping an anchor has already
            # lost the anchor by the time this reads it.
            priority=-10,
            page_types=(),
        )
    )
