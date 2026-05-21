#!/usr/bin/env python3
"""Aplica grupos de macros en Mainsail y Fluidd vía API de Moonraker."""

from __future__ import annotations

import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

CONFIG_PATH = Path(__file__).resolve().parents[1] / "macros_ui.json"
DEFAULT_MOONRAKER = "http://127.0.0.1:7125"


def api(method: str, url: str, body: dict | None = None) -> dict:
    data = None
    headers = {"Content-Type": "application/json"}
    if body is not None:
        data = json.dumps(body).encode()
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        raise SystemExit(f"HTTP {e.code}: {e.read().decode()}") from e
    except urllib.error.URLError as e:
        raise SystemExit(f"No se pudo conectar a Moonraker ({url}): {e}") from e


def get_namespace(base: str, namespace: str) -> dict:
    url = f"{base}/server/database/item?namespace={namespace}"
    result = api("GET", url)
    return result.get("result", {}).get("value", {}) or {}


def post_item(base: str, namespace: str, key: str, value) -> None:
    url = f"{base}/server/database/item"
    api("POST", url, {"namespace": namespace, "key": key, "value": value})


def build_mainsail_macros(cfg: dict) -> dict:
    macrogroups = {}
    for gid, group in cfg["groups"].items():
        macros = []
        for pos, name in enumerate(group["macros"]):
            macros.append({
                "pos": pos,
                "name": name,
                "color": "group",
                "showInStandby": True,
                "showInPrinting": name not in (
                    "START_PRINT", "CALIBRAR_TODO", "CALIBRAR_Z",
                    "CALIBRAR_CAMA", "BLTOUCH_TEST", "MESH_GUARDAR",
                    "TORNILLOS", "IR_TORNILLO", "PURGA_MANUAL",
                ),
                "showInPause": True,
            })
        macrogroups[gid] = {
            "id": gid,
            "name": group["name"],
            "color": group["mainsail_color"],
            "showInStandby": True,
            "showInPrinting": True,
            "showInPause": True,
            "macros": macros,
        }
    return {
        "mode": "expert",
        "hiddenMacros": cfg.get("hidden_macros", []),
        "macrogroups": macrogroups,
    }


def build_fluidd_macros(cfg: dict, existing: dict) -> dict:
    categories = []
    stored_by_name = {m["name"]: dict(m) for m in existing.get("stored", []) if "name" in m}

    for gid, group in cfg["groups"].items():
        categories.append({
            "id": gid,
            "name": group["name"],
            "visible": len(group["macros"]),
        })
        for order, name in enumerate(group["macros"]):
            entry = stored_by_name.get(name, {"name": name})
            entry.update({
                "name": name,
                "visible": True,
                "categoryId": gid,
                "color": group["fluidd_color"],
                "order": order,
                "disabledWhilePrinting": name in (
                    "START_PRINT", "CALIBRAR_TODO", "CALIBRAR_Z",
                    "CALIBRAR_CAMA", "BLTOUCH_TEST", "MESH_GUARDAR",
                    "TORNILLOS", "IR_TORNILLO", "PURGA_MANUAL",
                ),
            })
            stored_by_name[name] = entry

    for name in cfg.get("hidden_macros", []):
        if name in stored_by_name:
            stored_by_name[name]["visible"] = False

    stored = sorted(stored_by_name.values(), key=lambda m: (m.get("categoryId", "zzz"), m.get("order", 99)))
    return {
        "stored": stored,
        "categories": categories,
        "expanded": list(range(len(categories))),
    }


def main() -> None:
    base = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_MOONRAKER
    cfg = json.loads(CONFIG_PATH.read_text())

    mainsail_db = get_namespace(base, "mainsail")
    mainsail_db["macros"] = build_mainsail_macros(cfg)
    post_item(base, "mainsail", "macros", mainsail_db["macros"])
    print("✓ Mainsail: grupos de macros aplicados (modo Expert)")

    fluidd_existing = get_namespace(base, "fluidd").get("macros", {})
    fluidd_macros = build_fluidd_macros(cfg, fluidd_existing)
    post_item(base, "fluidd", "macros", fluidd_macros)
    print("✓ Fluidd: categorías de macros aplicadas")

    print("\nRecarga Mainsail/Fluidd en el navegador (F5) para ver los paneles.")


if __name__ == "__main__":
    main()
