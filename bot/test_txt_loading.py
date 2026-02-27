#!/usr/bin/env python3
"""Test the new txt-based festival loading"""

from app.doc_loader import load_fest_documents

print("=" * 60)
print("Testing TXT Festival Loading")
print("=" * 60)

sections = load_fest_documents("data/festivals.txt")

print(f"\n\u2705 Total sections loaded: {len(sections)}\n")

for i, section in enumerate(sections, 1):
    print(f"\n--- Section {i} ({len(section)} chars) ---")
    print(section[:200] + "..." if len(section) > 200 else section)

print("\n" + "=" * 60)
