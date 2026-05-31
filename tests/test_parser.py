from smd import parse_text


def test_parse_frontmatter_scene_and_blocks():
    doc = parse_text(
        """---
title: Demo
---

# Opening {#opening}

::scene id=intro role=hook
::layout mode=hero

:::claim id=main source=note#main
This is the claim.
::
"""
    )

    assert doc.metadata["title"] == "Demo"
    assert doc.title == "Opening"
    assert len(doc.scenes) == 1
    scene = doc.scenes[0]
    assert scene.id == "intro"
    assert scene.title == "Opening"
    assert scene.attrs["role"] == "hook"
    assert [directive.name for directive in scene.directives] == ["layout", "claim"]
    assert scene.directives[1].content == "This is the claim."


def test_parse_arrays_booleans_and_integers():
    doc = parse_text(
        """# Demo

::scene id=intro
:::beat id=proof reveal=2 active=true tags=[a,b]
Proof.
::
"""
    )

    beat = doc.scenes[0].directives[0]
    assert beat.attrs["reveal"] == 2
    assert beat.attrs["active"] is True
    assert beat.attrs["tags"] == ["a", "b"]


def test_heading_before_scene_titles_new_scene_not_previous_content():
    doc = parse_text(
        """# First

::scene id=first
:::takeaway id=first-takeaway
One.
::

## Second

::scene id=second
:::takeaway id=second-takeaway
Two.
::
"""
    )

    assert doc.scenes[0].content == ""
    assert doc.scenes[1].title == "Second"
