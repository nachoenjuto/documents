# /// script
# requires-python = ">=3.10"
# dependencies = ["reportlab", "pillow", "pypdf", "pymupdf"]
# ///
"""Genera los documentos ficticios «_large». Uso: uv run generar_docs_large.py [dd seguros laboral subvenciones contratos fraude]"""
import importlib, sys

TODOS = ["dd", "seguros", "laboral", "subvenciones", "contratos", "fraude", "offline", "offline_suite"]
if __name__ == "__main__":
    for m in sys.argv[1:] or TODOS:
        importlib.import_module(f"generador_large.{m}").generar()
        print("OK", m)
