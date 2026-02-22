#!/usr/bin/env python3
"""
Personality Database Search Module

Search for characters/celebrities and get their MBTI + Enneagram + Instincts.
Data sourced from community-voted PDB entries.

Usage:
    from pdb_search import search, get_typology
    
    # Search for a character
    results = search("Tony Stark")
    
    # Get typology string ready for generator
    typology = get_typology("Tony Stark")  # Returns "ENTP 7w8 sx/so"
"""

import re
import csv
from pathlib import Path
from typing import Optional, List, Dict
from difflib import SequenceMatcher

# Data file location
DATA_DIR = Path(__file__).parent / "data"
PDB_FILE = DATA_DIR / "pdb_raw.csv"


def load_database() -> List[Dict]:
    """Load and parse the PDB dataset."""
    if not PDB_FILE.exists():
        raise FileNotFoundError(
            f"PDB dataset not found at {PDB_FILE}. "
            "Run: curl -sL 'https://raw.githubusercontent.com/AKAazure/character-personality-database/main/pdb_dataset.csv' -o data/pdb_raw.csv"
        )
    
    entries = []
    with open(PDB_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or ' ++$++ ' not in line:
                continue
            
            parts = line.split(' ++$++ ')
            if len(parts) != 2:
                continue
            
            name = parts[0].strip()
            typology_raw = parts[1].strip()
            
            # Parse typology: "ENTP - 7w8 - sx/so - 738 - ILE - SCUEI - VLEF - Sanguine"
            typo_parts = [p.strip() for p in typology_raw.split(' - ')]
            
            entry = {
                'name': name,
                'raw': typology_raw,
                'mbti': typo_parts[0] if len(typo_parts) > 0 else None,
                'enneagram': typo_parts[1] if len(typo_parts) > 1 else None,
                'instincts': typo_parts[2] if len(typo_parts) > 2 else None,
                'tritype': typo_parts[3] if len(typo_parts) > 3 else None,
            }
            
            # Validate MBTI format
            if entry['mbti'] and re.match(r'^[EI][NS][TF][JP]$', entry['mbti']):
                entries.append(entry)
    
    return entries


# Cache database in memory
_DB_CACHE: Optional[List[Dict]] = None


def get_db() -> List[Dict]:
    """Get cached database."""
    global _DB_CACHE
    if _DB_CACHE is None:
        _DB_CACHE = load_database()
    return _DB_CACHE


def similarity(a: str, b: str) -> float:
    """Calculate string similarity ratio."""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def search(query: str, limit: int = 10) -> List[Dict]:
    """
    Search for characters by name.
    
    Returns list of matches sorted by relevance.
    """
    db = get_db()
    query_lower = query.lower()
    
    results = []
    for entry in db:
        name_lower = entry['name'].lower()
        
        # Exact match
        if query_lower == name_lower:
            results.append((1.0, entry))
            continue
        
        # Contains match
        if query_lower in name_lower:
            score = 0.8 + (len(query) / len(entry['name'])) * 0.2
            results.append((score, entry))
            continue
        
        # Fuzzy match
        score = similarity(query, entry['name'])
        if score > 0.5:
            results.append((score, entry))
    
    # Sort by score descending
    results.sort(key=lambda x: x[0], reverse=True)
    
    return [r[1] for r in results[:limit]]


def get_typology(name: str) -> Optional[str]:
    """
    Get typology string for generator from character name.
    
    Returns format: "MBTI Xw# inst/inst" (e.g., "ENTP 7w8 sx/so")
    Returns None if not found or incomplete data.
    """
    results = search(name, limit=1)
    if not results:
        return None
    
    entry = results[0]
    
    mbti = entry.get('mbti')
    enneagram = entry.get('enneagram')
    instincts = entry.get('instincts')
    
    if not all([mbti, enneagram, instincts]):
        return None
    
    # Validate instincts format (sp/sx, sx/so, so/sp, etc.)
    if not re.match(r'^(sp|sx|so)/(sp|sx|so)$', instincts):
        return None
    
    return f"{mbti} {enneagram} {instincts}"


def format_entry(entry: Dict) -> str:
    """Format entry for display."""
    parts = [entry['name']]
    if entry.get('mbti'):
        parts.append(entry['mbti'])
    if entry.get('enneagram'):
        parts.append(entry['enneagram'])
    if entry.get('instincts'):
        parts.append(entry['instincts'])
    return " | ".join(parts)


def interactive_search():
    """Interactive search mode."""
    print("🔍 PDB Search (type 'q' to quit)")
    print(f"   Database: {len(get_db())} characters\n")
    
    while True:
        try:
            query = input("Search: ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        
        if query.lower() in ('q', 'quit', 'exit'):
            break
        
        if not query:
            continue
        
        results = search(query)
        
        if not results:
            print("   No results found.\n")
            continue
        
        print()
        for i, entry in enumerate(results, 1):
            typology = get_typology(entry['name'])
            if typology:
                print(f"   {i}. {entry['name']}")
                print(f"      → {typology}")
            else:
                print(f"   {i}. {entry['name']} (incomplete data)")
        print()


def main():
    """CLI interface."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Search Personality Database')
    parser.add_argument('query', nargs='?', help='Search query')
    parser.add_argument('-i', '--interactive', action='store_true', 
                        help='Interactive search mode')
    parser.add_argument('-t', '--typology', action='store_true',
                        help='Output typology string only (for piping)')
    parser.add_argument('-n', '--limit', type=int, default=10,
                        help='Max results to show')
    parser.add_argument('--stats', action='store_true',
                        help='Show database statistics')
    
    args = parser.parse_args()
    
    if args.stats:
        db = get_db()
        print(f"📊 PDB Statistics")
        print(f"   Total entries: {len(db)}")
        
        # Count by MBTI
        mbti_counts = {}
        for entry in db:
            mbti = entry.get('mbti', 'Unknown')
            mbti_counts[mbti] = mbti_counts.get(mbti, 0) + 1
        
        print(f"\n   By MBTI:")
        for mbti in sorted(mbti_counts.keys()):
            print(f"   {mbti}: {mbti_counts[mbti]}")
        return
    
    if args.interactive or not args.query:
        interactive_search()
        return
    
    results = search(args.query, limit=args.limit)
    
    if args.typology:
        # Output just typology for piping
        if results:
            typology = get_typology(results[0]['name'])
            if typology:
                print(typology)
        return
    
    if not results:
        print("No results found.")
        return
    
    for entry in results:
        typology = get_typology(entry['name'])
        if typology:
            print(f"{entry['name']}: {typology}")
        else:
            print(f"{entry['name']}: {entry.get('raw', 'incomplete')}")


if __name__ == '__main__':
    main()
