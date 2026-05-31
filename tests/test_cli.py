import json

from smd.cli import main


def test_cli_parse_outputs_json(tmp_path, capsys):
    path = tmp_path / "demo.smd"
    path.write_text(
        """---
title: Demo
---

# Opening

::scene id=intro
:::takeaway id=takeaway
Remember.
::
""",
        encoding="utf-8",
    )

    assert main(["parse", str(path)]) == 0
    out = json.loads(capsys.readouterr().out)
    assert out["metadata"]["title"] == "Demo"
    assert out["scenes"][0]["id"] == "intro"
