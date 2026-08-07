from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"


def test_operator_pages_count_and_sections():
    op_dir = DOCS / "codex/Book05_OperatorsAtlas/operators"
    pages = sorted(op_dir.glob("*_op_*.md"))
    assert len(pages) == 18
    required_markers = [
        "## Symbol",
        "## Name & Pillar",
        "## Type",
        "## Definition",
        "## Axioms",
        "## Invariants",
        "## Examples",
        "## Cross-References",
        "## Chapter References",
        "## Tri-Link Dashboard",
    ]
    for page in pages:
        text = page.read_text()
        for marker in required_markers:
            assert marker in text, f"{marker} missing in {page.name}"


def test_ceremony_inventory_and_guides_exist():
    c_dir = DOCS / "codex/Book09_PhoenixArchive/ceremonies"
    ceremonies = sorted(c_dir.glob("ceremony_*.md"))
    assert len(ceremonies) >= 10
    for required in ["index.md", "sigils.md", "gestures.md"]:
        assert (c_dir / required).exists()


def test_engine_and_animation_docs_exist():
    for rel in [
        "engines/phoenix_detailed.md",
        "engines/qpe_detailed.md",
        "engines/dragon_detailed.md",
        "engines/architecture.md",
        "engines/integration_guide.md",
        "diagrams/animations/plate_dynamics.md",
        "diagrams/animations/after_effects.md",
        "diagrams/animations/interactive.md",
    ]:
        assert (DOCS / rel).exists()


def test_mkdocs_nav_includes_new_sections():
    nav = (ROOT / "mkdocs.yml").read_text()
    assert "Operators Reference" in nav
    assert "Ceremonies" in nav
    assert "Phoenix Engine (Detailed)" in nav
    assert "Animations" in nav
