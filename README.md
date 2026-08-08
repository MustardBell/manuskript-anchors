# Anchors

A Manuskript plugin. Name a place in your manuscript, and link to it.

```
<a name="the-reveal"></a>

## The reveal

...and as promised in [the reveal](#the-reveal), ...
```

## Why it is needed

Markdown has no anchor syntax. It never did, and every implementation either
passes raw HTML through or invents something of its own — so the only way to
name a place that other tools also understand is to write the HTML that has
meant this for twenty years: `<a name="...">`.

Markdown does pass it through, and that is where it stops:

- `name` on an anchor is obsolete in HTML5. Browsers and Qt still follow it,
  but it does not validate, and nothing new is obliged to honour it.
- An anchor written on a line of its own becomes a paragraph containing
  nothing — a blank gap in the page, sitting *above* the heading it was
  supposed to name, so a link to it arrives just short of the point.
- In BBCode it is not markup at all. A forum post is one page: there is
  nowhere for an anchor to be, and no tag for one. The raw
  `<a name="the-reveal">` becomes visible words in the middle of the post.

This plugin finishes what Markdown starts, per destination.

## What it does

**To HTML** — the reading view, the HTML export, anything rendered from
Markdown:

| written | rendered |
|---|---|
| `<a name="x">text</a>` | `<a id="x">text</a>` |
| `<a name="x"></a>` above `## Heading` | `<h2 id="x">Heading</h2>` |
| `<a name="x"></a>` above a paragraph | the anchor moves inside it |

The anchor ends up on the thing it names, and the empty paragraph is gone.

**To BBCode** — the anchor is dropped and the words it wrapped are kept, and
a link whose target is only a fragment keeps its words and loses the link. A
forum reader sees the writing and none of the machinery.

## What it leaves alone

- **Links.** An `<a>` with an `href` is somewhere the writer meant to go, not
  a name for where they are. Untouched, however it is spelled.
- **Links to other documents.** `[there](http://example.com#scene)` keeps its
  link in BBCode too — that target still exists.
- **A heading that already has an `id`.** Overwriting it would break whatever
  links to it, so the anchor is kept beside it instead.
- **Lists, tables and code blocks.** An anchor written above one stays where
  it is: `<a>` directly inside `<ul>` is invalid HTML, and inside a code
  block it is markup the reader can see. A blank line is the smaller problem.
- **Everything with no anchor in it.** Asserted against unaugmented output
  rather than a written-out expectation, so "unchanged" keeps meaning what
  Markdown means by it.

## What it does not do

It does not invent a syntax. `{#id}`-style anchors would be shorter to type
and would leave the raw file saying something only this plugin understands;
`<a name>` already works in every other Markdown tool you might open the file
with, which is the point of writing it that way.

It does not touch the editor. While you are typing, an anchor is raw text and
looks like raw text. Making it look like a marker is a job for the editor, not
for a conversion.

## Requires

Manuskript with plugin API version 1 and the `conversion_augmentation`
contribution kind. No capabilities are requested: the plugin reads nothing,
writes nothing, and holds no state.

The routes it augments — `text/markdown` to `text/html`, and `text/markdown`
to `text/x-bbcode` — are declared in the contributions, not implied by the
kind. Both are the same mechanism; each says what an anchor can mean where it
is going.

## Install

Clone into a `anchors` subdirectory of Manuskript's plugin root, then enable
it in **Tools → Plugins → Manage Plugins…**.

```bash
cd /path/to/manuskript
git clone https://github.com/MustardBell/manuskript-anchors.git manuskript/plugins/anchors
```

Or, if you track plugins as submodules:

```bash
git submodule add https://github.com/MustardBell/manuskript-anchors.git manuskript/plugins/anchors
```

## Tests

```
python3 -m pytest
```

The HTML tests need only `markdown`. The BBCode tests need Manuskript
importable, because a rule for that route is the host's `MarkupRule` and
inventing a second version of it would test the wrong thing; they skip
themselves when it is absent.

## Licence

GPL-3.0-or-later. See `LICENSE`.
