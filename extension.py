"""The anchor work, as something python-markdown will run.

Separated from the work itself so the rules can be read and tested without a
Markdown pipeline, and so the pipeline's requirements -- what an extension
is, where a postprocessor sits -- stay in one small file.
"""

from markdown import Extension
from markdown.postprocessors import Postprocessor

from .anchors import cleaned


#: Just after ``raw_html`` (30), which is what puts the anchors back into the
#: text. Before it there is nothing to find; the placeholders are opaque.
PRIORITY = 25


class Anchors(Extension):
    """Anchors a writer typed, rendered as anchors a page can use."""

    def extendMarkdown(self, md):
        md.postprocessors.register(_AnchorPostprocessor(md), "anchors", PRIORITY)


class _AnchorPostprocessor(Postprocessor):
    def run(self, text):
        return cleaned(text)
