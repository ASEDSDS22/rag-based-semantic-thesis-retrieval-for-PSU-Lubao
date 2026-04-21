"""Utility functions for data processing"""
from typing import Dict, Any


def row_to_text(row: Dict[str, Any]) -> str:
    """
    Convert thesis row to searchable text format.
    Reused from original data_loader.py
    """
    return f"""
Title: {row.get('title_clean', 'N/A')}
Journal: {row.get('journal_clean', 'N/A')}
Year: {row.get('year', 'N/A')}
Authors: {row.get('authors', 'N/A')}
Keywords: {row.get('keyword', 'N/A')}
"""
