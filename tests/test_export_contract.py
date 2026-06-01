from smd import parse_file


def test_export_contract_top_level_shape():
    doc = parse_file("examples/contextfit.smd")
    data = doc.to_dict()

    assert set(data) == {
        "metadata",
        "title",
        "preamble",
        "directives",
        "scenes",
    }
    assert data["title"]
    assert data["scenes"]


def test_export_contract_scene_and_directive_shape():
    doc = parse_file("examples/contextfit.smd")
    data = doc.to_dict()

    for scene in data["scenes"]:
        assert {"id", "title", "attrs", "content", "directives", "line"} <= set(scene)
        for directive in scene["directives"]:
            assert {"name", "attrs", "content", "line"} <= set(directive)
