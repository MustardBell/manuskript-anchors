"""What a writer typed, and what a reader ends up with.

Every test names a document somebody could write and the thing they wanted
from it. Where a claim is "Markdown's own output, unchanged", it is asserted
against unaugmented output rather than a written-out expectation, so the
claim keeps meaning what Markdown means by it.
"""

import pytest

markdown = pytest.importorskip("markdown")

from anchors.extension import Anchors  # noqa: E402


def rendered(source):
    return markdown.markdown(source, extensions=[Anchors()])


def plain(source):
    return markdown.markdown(source)


# ------------------------------------------------- a place worth linking to

def test_an_anchor_becomes_one_a_page_can_link_to():
    """``name`` is obsolete on an anchor; ``id`` is what HTML5 has. Both
    work in browsers and in Qt's rich text, so nothing that worked before
    stops working -- but only one of them validates.
    """
    html = rendered('Text <a name="scene">here</a> and on.')

    assert '<a id="scene">here</a>' in html
    assert "name=" not in html


def test_an_anchor_marks_the_heading_it_was_written_above():
    """The idiom this exists for. An anchor on its own line above a heading
    means that heading, and a link to it should arrive at the heading rather
    than at an empty line above it.
    """
    html = rendered('Before.\n\n<a name="scene"></a>\n\n## The scene\n\nAfter.')

    assert '<h2 id="scene">The scene</h2>' in html
    assert "<p></p>" not in html
    assert "<a" not in html


def test_an_anchor_marks_the_paragraph_it_was_written_above():
    """Not every place worth naming has a heading. Left alone this is a
    paragraph containing nothing: a blank gap in the page, above the
    paragraph it was meant to name.
    """
    html = rendered('Before.\n\n<a name="aside"></a>\n\nThe aside itself.')

    assert '<p><a id="aside"></a>The aside itself.</p>' in html


def test_no_anchor_is_dropped_when_several_name_one_heading():
    """Two names for the same place, because something links by each. The
    heading takes one; the other stays inside it rather than vanishing.
    """
    html = rendered('<a name="one"></a>\n<a name="two"></a>\n\n## Both')

    assert 'id="one"' in html
    assert 'id="two"' in html


def test_a_heading_that_already_names_itself_is_left_alone():
    """Its ``id`` came from somewhere -- another extension, or the writer.
    Overwriting it would break whatever links to it, so the anchor is kept
    beside it instead.
    """
    html = markdown.markdown(
        '<a name="mine"></a>\n\n## Titled {#theirs}',
        extensions=[Anchors(), "attr_list"],
    )

    assert 'id="theirs"' in html
    assert 'id="mine"' in html


def test_an_anchor_with_nothing_after_it_is_kept_as_it_is():
    """There is nothing for it to mark. Keeping the paragraph is worse
    looking than moving it and better than losing a link target.
    """
    html = rendered('## Heading\n\n<a name="tail"></a>')

    assert 'id="tail"' in html


# ------------------------------------------------------- what is left alone

def test_a_link_is_not_an_anchor_and_is_untouched():
    """``href`` means the writer meant to go somewhere. However the tag is
    spelled, it is not a name for this place.
    """
    source = 'A <a href="http://example.com" name="odd">link</a>.'

    assert rendered(source) == plain(source)


def test_a_link_to_an_anchor_still_points_at_it():
    source = "See [the scene](#scene)."

    assert rendered(source) == plain(source)
    assert 'href="#scene"' in rendered(source)


@pytest.mark.parametrize("source", [
    "An ordinary paragraph.",
    "## A heading\n\nAnd text.",
    "- one\n- two",
    "1. one\n2. two",
    "> quoted\n\ntext",
    "    indented code <a name=\"x\"></a>",
    "```\nfenced <a name=\"x\"></a>\n```",
    "Text with an ampersand & a < sign.",
])
def test_documents_without_anchors_render_exactly_as_markdown_renders_them(
    source,
):
    """Including the two places an anchor is not markup at all. A rule that
    reaches into code blocks would rewrite the very thing somebody was
    quoting in order to explain it.
    """
    assert rendered(source) == plain(source)


def test_an_anchor_between_list_items_is_not_moved_into_the_list():
    """A ``<a>`` directly inside ``<ul>`` is invalid HTML, and inside a code
    block it is markup the reader can see. An unhelpful blank line is a
    smaller problem than either, so those blocks are left alone.
    """
    html = rendered('<a name="list"></a>\n\n- one\n- two')

    assert '<p><a id="list"></a></p>' in html
    assert "<ul>" in html
    assert "<li><a" not in html
