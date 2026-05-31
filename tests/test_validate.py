from smd import parse_text, validate


def codes(issues):
    return {issue.code for issue in issues}


def test_valid_document_passes_without_errors():
    doc = parse_text(
        """---
title: Demo
---

# Opening

::scene id=intro
:::claim id=main source=note#main
Claim.
::
:::beat id=first reveal=1 source=note#first
First.
::
:::takeaway id=takeaway
Remember this.
::
"""
    )

    issues = validate(doc, strict=True)
    assert not [issue for issue in issues if issue.level == "error"]


def test_duplicate_ids_are_errors():
    doc = parse_text(
        """# Opening

::scene id=intro
:::claim id=same
Claim.
::
:::takeaway id=same
Remember this.
::
"""
    )

    assert "duplicate-id" in codes(validate(doc))


def test_strict_claim_source_warning():
    doc = parse_text(
        """# Opening

::scene id=intro
:::claim id=main
Claim.
::
"""
    )

    assert "claim-missing-source" in codes(validate(doc, strict=True))


def test_non_contiguous_reveals_warns():
    doc = parse_text(
        """# Opening

::scene id=intro
:::beat id=one reveal=1
One.
::
:::beat id=three reveal=3
Three.
::
:::takeaway id=takeaway
Remember.
::
"""
    )

    assert "non-contiguous-reveals" in codes(validate(doc))
