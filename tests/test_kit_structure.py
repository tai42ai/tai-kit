"""Structural gates: the leaf rule (kit imports only tai42_contract) and the
eviction of app/deployment settings that are not leaf."""

from __future__ import annotations

import ast
from pathlib import Path

import tai42_kit

_SRC = Path(tai42_kit.__path__[0])

_EVICTED = (
    "BackendSettings",
    "MetricsSettings",
    "ConfigModeSettings",
    "K8sConfigSettings",
    "TemplateCacheSettings",
    "base_backend_settings",
    "metrics_settings",
    "config_mode",
    "k8s_config_settings",
    "template_cache_settings",
)


def test_leaf_rule_imports_only_tai_contract():
    offenders: list[str] = []
    for path in _SRC.rglob("*.py"):
        tree = ast.parse(path.read_text())
        for node in ast.walk(tree):
            names = (
                [a.name for a in node.names]
                if isinstance(node, ast.Import)
                else [node.module]
                if isinstance(node, ast.ImportFrom) and node.module
                else []
            )
            for name in names:
                top = name.split(".")[0]
                if top.startswith("tai42_") and top not in ("tai42_kit", "tai42_contract"):
                    offenders.append(f"{path.name}: {name}")
    assert not offenders, offenders


def test_no_central_config_package():
    assert not (_SRC / "config").exists(), "the central config/ settings dump must be dissolved"


def test_evicted_settings_are_absent():
    blob = "\n".join(p.read_text() for p in _SRC.rglob("*.py"))
    present = [name for name in _EVICTED if name in blob]
    assert not present, f"evicted (non-leaf) settings still present: {present}"
