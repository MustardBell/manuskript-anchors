"""What becomes of an anchor on the way to a forum post.

These need Manuskript importable: a rule for this route is a ``MarkupRule``,
which is the host's, and taking it from anywhere else would be inventing a
second version of the host's contract. Cloned on its own, the plugin still
tests everything that does not depend on that.
"""

import pytest

pytest.importorskip("manuskript.plugins")

from manuskript.converters.markdownToBBCode import BBCodeConverter  # noqa: E402

from anchors.bbcode import anchor_rule, fragment_link_rule  # noqa: E402


def converted(source):
    """The host's conversion with this plugin's additions, as the host
    assembles it: core's rules first, then whatever was contributed."""
    return BBCodeConverter().extended(
        anchor_rule(), fragment_link_rule(),
    ).convert(source)


def plain(source):
    return BBCodeConverter().convert(source)


def test_an_anchor_leaves_no_trace_in_a_post():
    """Untouched, the tag is not markup in a forum -- it is six visible
    words in the middle of somebody's paragraph.
    """
    assert converted('Before <a name="scene"></a> after.') == (
        "Before  after."
    )
    assert "<a" in plain('Before <a name="scene"></a> after.')


def test_words_inside_an_anchor_are_kept():
    """The anchor was a name for the place; the words were the writing."""
    assert converted('A <a name="scene">whole scene</a> follows.') == (
        "A whole scene follows."
    )


def test_an_anchor_with_no_closing_tag_takes_nothing_with_it():
    """Written ``<a name="x"/>``, or written wrongly. Either way the rest of
    the paragraph is somebody's prose.
    """
    assert converted('Before <a name="scene"/> after.') == "Before  after."
    assert converted('Before <a name="scene"> after.') == "Before  after."


def test_a_closing_tag_belonging_to_something_else_is_safe():
    """The pair can only be claimed when nothing else opens in between."""
    converted_text = converted(
        '<a name="one"/> text <a href="http://x">link</a>'
    )

    assert 'href="http://x"' in converted_text
    assert "link" in converted_text


def test_a_link_to_a_place_in_this_manuscript_keeps_its_words():
    """There is no such place in a forum post. A link that goes nowhere is
    worse than no link: it reads as one and does nothing.
    """
    assert converted("See [the scene](#scene) for that.") == (
        "See the scene for that."
    )


def test_a_link_to_another_document_keeps_its_link():
    """Its target still exists, fragment or not."""
    assert "[url=http://example.com#scene]" in converted(
        "See [there](http://example.com#scene)."
    )


def test_ordinary_markup_converts_as_it_did():
    source = "**Bold** and *italic* and [a link](http://example.com)."

    assert converted(source) == plain(source)
