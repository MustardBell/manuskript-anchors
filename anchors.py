"""Named places in a manuscript, written the only way Markdown allows.

Markdown has no syntax for an anchor. Every implementation either passes raw
HTML through or invents something of its own, so a writer who wants a place
worth linking to types ``<a name="scene">`` -- which is what HTML meant for
twenty years, and what other tools still understand. Nothing is invented
here: the raw source stays raw source that any Markdown reader accepts.

What Markdown does with it is pass it through untouched, and that is the
problem. ``name`` on an anchor is obsolete in HTML5 and a validator rejects
it, while an anchor written on a line of its own becomes a paragraph
containing nothing -- a blank gap above the thing it was meant to mark.

So this reads the anchors the writer wrote and finishes the job: the name
becomes an ``id``, and an anchor alone on a line marks the heading or
paragraph that follows it instead of standing between them.

Why a postprocessor
-------------------

Python-Markdown does not parse raw HTML. It hides each fragment behind a
placeholder before the tree is built and restores it after the tree is
serialised, so a treeprocessor -- the usual place for this kind of work --
sees ``wzxhzdk:0`` where the anchor is and can do nothing with it. The
anchors exist as HTML only once the ``raw_html`` postprocessor has put them
back, which is why this runs after it and works on text.

Text, then, and narrowly: these patterns match a shape python-markdown has
just emitted, one line, one tag at a time. They are not a general-purpose
HTML parser and must not be given work that would need one.
"""

import re


#: An anchor naming a place -- ``name`` and no ``href``. An anchor with an
#: ``href`` is a link somebody wrote, however it is spelled, and is left as
#: it is: the author meant to go somewhere, not to be arrived at.
NAMED = re.compile(
    r'<a(?![^>]*\shref=)([^>]*?)\sname=(?P<quote>["\'])(?P<id>.*?)(?P=quote)',
    re.IGNORECASE,
)

#: A paragraph holding nothing but empty anchors, and the block after it.
#:
#: Only a heading or a paragraph may take them in. Moving an anchor into a
#: list, a table or a code block would either be invalid HTML or would put
#: markup where the reader can see it, and an unhelpful blank line is a far
#: smaller problem than either.
STRANDED = re.compile(
    r'<p>\s*(?P<anchors>(?:<a [^>]*>\s*</a>\s*)+)</p>\s*'
    r'(?P<open><(?P<tag>h[1-6]|p)\b[^>]*>)'
)

#: One empty anchor with an id, inside the paragraph matched above.
ANCHOR = re.compile(
    r'<a\s[^>]*\bid=(?P<quote>["\'])(?P<id>.*?)(?P=quote)[^>]*>\s*</a>',
    re.IGNORECASE,
)

EMPTY_ANCHOR = '<a id="{}"></a>'


def name_becomes_id(text):
    """``<a name="scene">`` says ``<a id="scene">`` instead.

    The same anchor, in the spelling HTML5 accepts. Qt's rich text engine and
    every browser find either, so nothing that worked stops working.
    """
    return NAMED.sub(
        lambda match: '<a{} id="{}"'.format(
            match.group(1), match.group("id"),
        ),
        text,
    )


def anchors_mark_what_follows(text):
    """An anchor alone on a line marks the next heading or paragraph.

    Which is what the writer meant by putting it there. Left alone it is a
    paragraph with no content: a blank line in the page, and a target that
    lands above the heading rather than on it.

    A heading takes the first anchor as its own ``id``, because that is the
    thing being named. Anything left over is kept, inside the block, so no
    anchor a document links to is ever dropped.
    """
    return STRANDED.sub(_attach, text)


def _attach(match):
    ids = [found[1] for found in ANCHOR.findall(match.group("anchors"))]
    if not ids:
        return match.group(0)
    opening = match.group("open")
    if match.group("tag").lower().startswith("h") and " id=" not in opening:
        opening = '{} id="{}">'.format(opening[:-1], ids[0])
        ids = ids[1:]
    return opening + "".join(EMPTY_ANCHOR.format(one) for one in ids)


def cleaned(text):
    """Both passes, in the order they depend on.

    The second looks for anchors carrying an ``id``, which is what the first
    one produces.
    """
    return anchors_mark_what_follows(name_becomes_id(text))
