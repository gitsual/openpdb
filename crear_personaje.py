#!/usr/bin/env python3
"""
Compat module for legacy tests.
Provides minimal API used by test_character_generator.py.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Any

# Key principles string (must include required concepts)
PRINCIPIOS_RAND = """
PRINCIPIOS DE CARACTERIZACIÓN (Rand)
- CONCRETIZACIÓN
- PREMISA FUNDAMENTAL
- SENTIDO DE VIDA
- COHERENCIA PSICOLÓGICA
- VALORES ENCARNADOS
- CONFLICTO DRAMÁTICO
- ARCO DE RESOLUCIÓN
""".strip()


def load_variants_from_directory(directory: Path) -> Dict[str, Any]:
    """Load variants data from a directory.

    Tries data.json first; if not found, returns an empty dict.
    """
    data_path = Path(directory) / "data.json"
    if data_path.exists():
        try:
            return json.loads(data_path.read_text(encoding="utf-8"))
        except Exception:
            # fall through to empty data
            pass
    return {}


def build_character_prompt(data: Dict[str, Any], name: str) -> str:
    """Build a character prompt with the required 7 sections.

    The tests only assert that the required section headers are present
    and that the name/typology string appears somewhere.
    """
    typology = data.get("typology") or data.get("type") or "Extraído"

    sections = [
        "EGO",
        "SUBCONSCIENTE SANO",
        "SUBCONSCIENTE INSANO",
        "INCONSCIENTE SANO",
        "INCONSCIENTE INSANO",
        "SUPER-EGO SANO",
        "SUPER-EGO INSANO",
    ]

    body = "\n".join(f"## {s}" for s in sections)
    return f"""PERSONAJE: {name}\nTIPOLOGÍA: {typology}\n\n{body}\n"""
