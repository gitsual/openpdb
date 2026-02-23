#!/usr/bin/env python3
"""
Character Context Module

Fetches biographical and personality context for fictional characters
to enrich generated profiles beyond just typology.

Sources (in order of preference):
1. Wikipedia API - Reliable, structured summaries
2. Manual context - User-provided via --context flag

Usage:
    from character_context import get_context
    
    context = get_context("Walter White")
    # Returns dict with 'summary', 'source', etc.
"""

import re
import json
import urllib.request
import urllib.parse
from typing import Optional, Dict, Any


def fetch_wikipedia_summary(query: str) -> Optional[Dict[str, Any]]:
    """
    Fetch character summary from Wikipedia API.
    
    Tries multiple search strategies:
    1. Direct page lookup with character suffix
    2. Search API for best match
    """
    # Common suffixes for character pages
    character_suffixes = [
        "(character)",
        "(Breaking Bad)",
        "(Harry Potter)",
        "(Marvel Cinematic Universe)",
        "(Marvel Comics)",
        "(DC Comics)",
        "(Disney)",
        "(The Office)",
        "(Game of Thrones)",
        "(Lord of the Rings)",
        "(Star Wars)",
    ]
    
    # Try direct lookup first
    base_url = "https://en.wikipedia.org/api/rest_v1/page/summary/"
    
    # Try with common suffixes
    attempts = [query] + [f"{query} {suffix}" for suffix in character_suffixes]
    
    for attempt in attempts:
        encoded = urllib.parse.quote(attempt.replace(" ", "_"))
        url = f"{base_url}{encoded}"
        
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'CharacterContext/1.0'})
            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.loads(response.read().decode('utf-8'))
                
                if data.get('type') == 'standard' and data.get('extract'):
                    # Check if it's actually about a character (not disambiguation)
                    extract = data['extract']
                    if len(extract) > 100:  # Reasonable content
                        return {
                            'summary': extract,
                            'title': data.get('title', query),
                            'source': 'wikipedia',
                            'url': data.get('content_urls', {}).get('desktop', {}).get('page', ''),
                        }
        except Exception:
            continue
    
    # Try Wikipedia search API as fallback
    search_url = "https://en.wikipedia.org/w/api.php"
    params = {
        'action': 'query',
        'list': 'search',
        'srsearch': f'{query} fictional character',
        'format': 'json',
        'srlimit': 3,
    }
    
    try:
        search_req_url = f"{search_url}?{urllib.parse.urlencode(params)}"
        req = urllib.request.Request(search_req_url, headers={'User-Agent': 'CharacterContext/1.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode('utf-8'))
            
            results = data.get('query', {}).get('search', [])
            for result in results:
                title = result.get('title', '')
                # Try to fetch this page's summary
                encoded = urllib.parse.quote(title.replace(" ", "_"))
                summary_url = f"{base_url}{encoded}"
                
                try:
                    req2 = urllib.request.Request(summary_url, headers={'User-Agent': 'CharacterContext/1.0'})
                    with urllib.request.urlopen(req2, timeout=5) as resp2:
                        page_data = json.loads(resp2.read().decode('utf-8'))
                        if page_data.get('extract') and len(page_data['extract']) > 100:
                            return {
                                'summary': page_data['extract'],
                                'title': page_data.get('title', title),
                                'source': 'wikipedia',
                                'url': page_data.get('content_urls', {}).get('desktop', {}).get('page', ''),
                            }
                except Exception:
                    continue
    except Exception:
        pass
    
    return None


def extract_key_details(summary: str) -> Dict[str, str]:
    """
    Extract key character details from summary text.
    
    Returns dict with:
    - franchise: The fictional universe (Harry Potter, MCU, etc.)
    - role: Main role/occupation
    - relationships: Key relationships mentioned
    - traits: Personality traits mentioned
    """
    details = {
        'franchise': '',
        'role': '',
        'relationships': '',
        'traits': '',
    }
    
    # Detect franchise from common patterns
    franchise_patterns = [
        (r'Harry Potter', 'Harry Potter (Wizarding World)'),
        (r'Marvel Cinematic Universe|MCU', 'Marvel Cinematic Universe'),
        (r'Marvel Comics', 'Marvel Comics'),
        (r'Breaking Bad', 'Breaking Bad'),
        (r'Game of Thrones', 'Game of Thrones'),
        (r'Star Wars', 'Star Wars'),
        (r'Lord of the Rings|Middle-earth', 'Lord of the Rings'),
        (r'DC Comics|Batman|Superman', 'DC Comics'),
        (r'Disney|Pixar', 'Disney'),
        (r'The Office', 'The Office'),
    ]
    
    for pattern, franchise in franchise_patterns:
        if re.search(pattern, summary, re.IGNORECASE):
            details['franchise'] = franchise
            break
    
    return details


def get_context(name: str, manual_context: Optional[str] = None) -> Dict[str, Any]:
    """
    Get character context from available sources.
    
    Args:
        name: Character name to search
        manual_context: Optional user-provided context
    
    Returns:
        Dict with:
        - summary: Character description
        - source: Where context came from
        - franchise: Detected fictional universe
        - has_context: Whether meaningful context was found
    """
    result = {
        'name': name,
        'summary': '',
        'source': 'none',
        'franchise': '',
        'has_context': False,
    }
    
    # Priority 1: Manual context
    if manual_context:
        result['summary'] = manual_context
        result['source'] = 'manual'
        result['has_context'] = True
        return result
    
    # Priority 2: Wikipedia
    wiki_data = fetch_wikipedia_summary(name)
    if wiki_data:
        result['summary'] = wiki_data['summary']
        result['source'] = f"wikipedia ({wiki_data.get('title', name)})"
        result['has_context'] = True
        
        # Extract additional details
        details = extract_key_details(wiki_data['summary'])
        result['franchise'] = details['franchise']
        
        return result
    
    return result


def format_context_for_prompt(context: Dict[str, Any]) -> str:
    """
    Format context dict into a string suitable for including in LLM prompt.
    """
    if not context.get('has_context'):
        return ""
    
    parts = []
    
    if context.get('franchise'):
        parts.append(f"FICTIONAL UNIVERSE: {context['franchise']}")
    
    if context.get('summary'):
        parts.append(f"CHARACTER BACKGROUND:\n{context['summary']}")
    
    if context.get('source') and context['source'] != 'manual':
        parts.append(f"(Source: {context['source']})")
    
    return "\n\n".join(parts)


def main():
    """CLI interface for testing."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Get character context')
    parser.add_argument('name', help='Character name to search')
    parser.add_argument('--context', '-c', help='Manual context to use instead')
    parser.add_argument('--json', '-j', action='store_true', help='Output as JSON')
    
    args = parser.parse_args()
    
    result = get_context(args.name, args.context)
    
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        if result['has_context']:
            print(f"✅ Found context for: {result['name']}")
            print(f"   Source: {result['source']}")
            if result['franchise']:
                print(f"   Franchise: {result['franchise']}")
            print(f"\n{result['summary'][:500]}...")
        else:
            print(f"❌ No context found for: {result['name']}")


if __name__ == '__main__':
    main()
