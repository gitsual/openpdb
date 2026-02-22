#!/usr/bin/env python3
"""
Integrate Agent - Full creation and integration pipeline

1. Generate agent files (V8)
2. Add to OpenClaw (~/.openclaw/agents/<name>/)
3. Register in OpenGoat (~/.opengoat/agents/<name>/)
4. Reorganize company based on typology

Company structure:
```
CEO (ENTJ)
├── COO (ESTJ) → Operations
│   ├── Operations Lead (ENTJ)
│   └── Ops Team (xSTx types)
├── CTO (INTJ) → Strategy  
│   ├── Tech Lead (ENTP)
│   └── Tech Team (xNTx types)
└── CCO (ENFJ) → Culture
    ├── Culture Lead (ENFP)
    └── Culture Team (xNFx, xSFx types)
```
"""

import os
import sys
import json
import shutil
import subprocess
import argparse
import platform
from pathlib import Path
from datetime import datetime

# ==============================================================================
# PLATFORM DETECTION & PATHS
# ==============================================================================

def get_platform_paths():
    """
    Detect OS and return correct paths for OpenClaw and OpenGoat.
    
    Linux/macOS: ~/.openclaw/agents/, ~/.opengoat/agents/
    Windows: %APPDATA%\\openclaw\\agents\\ or %USERPROFILE%\\.openclaw\\agents\\
    """
    system = platform.system().lower()
    
    if system == 'windows':
        # Windows: prefer APPDATA, fallback to USERPROFILE
        appdata = os.environ.get('APPDATA')
        if appdata:
            base = Path(appdata)
        else:
            base = Path.home()
        
        openclaw = base / 'openclaw' / 'agents'
        opengoat = base / 'opengoat' / 'agents'
    else:
        # Linux, macOS, other Unix-like
        openclaw = Path.home() / '.openclaw' / 'agents'
        opengoat = Path.home() / '.opengoat' / 'agents'
    
    return openclaw, opengoat

def get_platform_info():
    """Return platform info for display."""
    system = platform.system()
    if system == 'Windows':
        return f"🪟 Windows ({platform.release()})"
    elif system == 'Darwin':
        return f"🍎 macOS ({platform.mac_ver()[0]})"
    else:
        return f"🐧 Linux ({platform.release().split('-')[0]})"

# Initialize paths based on platform
OPENCLAW_AGENTS, OPENGOAT_AGENTS = get_platform_paths()

# Division managers (generic role-based IDs)
DIVISION_MANAGERS = {
    'cto': 'cto_lead',      # Chief Technology Officer
    'coo': 'coo_lead',      # Chief Operations Officer
    'cco': 'cco_lead',      # Chief Culture Officer
}

# Sub-managers by MBTI (role-based, not personal names)
SUB_MANAGERS = {
    'ENTP': 'tech_innovator',    # Reports to CTO
    'ENTJ': 'ops_commander',     # Reports to COO
    'ISFP': 'creative_artisan',  # Reports to CCO
    'ESFP': 'creative_artisan',  # Reports to CCO
    'ENFP': 'culture_catalyst',  # Reports to CCO
}


def get_division(mbti: str) -> str:
    """Determine division based on MBTI."""
    mbti = mbti.upper()
    if mbti in ['INTJ', 'INTP', 'ENTP']:
        return 'cto'
    if mbti in ['ESTJ', 'ISTJ', 'ESTP', 'ISTP', 'ENTJ']:
        return 'coo'
    return 'cco'


def get_manager(mbti: str) -> str:
    """Determine direct manager based on MBTI."""
    mbti = mbti.upper()
    if mbti in SUB_MANAGERS:
        return SUB_MANAGERS[mbti]
    return DIVISION_MANAGERS[get_division(mbti)]


def generate_agent(typology: str, name: str, model: str = "qwen2.5:14b", 
                   lang: str = "es") -> Path:
    """Generate agent using V8."""
    script_dir = Path(__file__).parent
    output_dir = script_dir / 'agents' / name.lower().replace(' ', '_')
    
    cmd = [
        'python', str(script_dir / 'agent_generator.py'),
        typology, '--name', name, '--output', str(output_dir), 
        '--model', model, '--lang', lang
    ]
    
    print(f"\n📝 Generating agent '{name}'...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ Error: {result.stderr}")
        sys.exit(1)
    print(result.stdout)
    return output_dir


def add_to_openclaw(agent_dir: Path, name: str) -> bool:
    """Copy agent to OpenClaw directory."""
    agent_id = name.lower().replace(' ', '_')
    dest = OPENCLAW_AGENTS / agent_id
    
    print(f"\n🦞 Adding to OpenClaw...")
    
    # Create parent directory if it doesn't exist
    OPENCLAW_AGENTS.mkdir(parents=True, exist_ok=True)
    
    # Backup if exists
    if dest.exists():
        backup = dest.parent / f"{agent_id}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        shutil.move(str(dest), str(backup))
        print(f"   📦 Backup: {backup.name}")
    
    # Copiar archivos
    dest.mkdir(parents=True, exist_ok=True)
    for file in agent_dir.iterdir():
        if file.is_file():
            shutil.copy2(file, dest / file.name)
        elif file.is_dir() and file.name == 'memory':
            shutil.copytree(file, dest / file.name, dirs_exist_ok=True)
    
    print(f"   ✅ {dest}")
    return True


def add_to_opengoat(name: str, mbti: str, role: str = "individual") -> bool:
    """Register agent in OpenGoat."""
    agent_id = name.lower().replace(' ', '_')
    manager = get_manager(mbti)
    division = get_division(mbti)
    
    print(f"\n🐐 Registering in OpenGoat...")
    print(f"   Division: {division.upper()}")
    print(f"   Manager: {manager}")
    
    # Create parent directory if it doesn't exist
    OPENGOAT_AGENTS.mkdir(parents=True, exist_ok=True)
    
    agent_dir = OPENGOAT_AGENTS / agent_id
    agent_dir.mkdir(parents=True, exist_ok=True)
    
    # Create config.json
    config = {
        "schemaVersion": 2,
        "id": agent_id,
        "displayName": name,
        "role": "Team Member",
        "description": f"{name} - {mbti} agent",
        "organization": {
            "type": role,
            "reportsTo": manager,
            "discoverable": True,
            "tags": [division, mbti.lower()],
            "priority": 50
        },
        "runtime": {
            "provider": {"id": "openclaw"},
            "mode": "organization",
            "sessions": {
                "mainKey": "main",
                "contextMaxChars": 12000,
                "reset": {"mode": "daily", "atHour": 4},
                "pruning": {
                    "enabled": True,
                    "maxMessages": 40,
                    "maxChars": 16000,
                    "keepRecentMessages": 12
                },
                "compaction": {
                    "enabled": True,
                    "triggerMessageCount": 80,
                    "triggerChars": 32000,
                    "keepRecentMessages": 20,
                    "summaryMaxChars": 4000
                }
            },
            "skills": {
                "enabled": True,
                "includeWorkspace": False,
                "includeManaged": True,
                "assigned": [],
                "load": {"extraDirs": []},
                "prompt": {
                    "maxSkills": 12,
                    "maxCharsPerSkill": 6000,
                    "maxTotalChars": 36000,
                    "includeContent": True
                }
            }
        }
    }
    
    with open(agent_dir / 'config.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    # Create auxiliary empty files if they don't exist
    (agent_dir / 'auth.json').write_text('{}')
    (agent_dir / 'models.json').write_text('{}')
    
    print(f"   ✅ {agent_dir}")
    return True


def print_org_structure(new_agent: str, mbti: str):
    """Show updated organizational structure."""
    manager = get_manager(mbti)
    
    # Build tree with new agent highlighted
    tree = f"""
    ┌─────────────────────────────────────────────────────┐
    │                      CEO                            │
    │                    (ENTJ)                           │
    └─────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
    ┌───┴───┐           ┌───┴───┐           ┌───┴───┐
    │  COO  │           │  CTO  │           │  CCO  │
    │(ESTJ) │           │(INTJ) │           │(ENFJ) │
    │  Ops  │           │ Tech  │           │Culture│
    └───┬───┘           └───┬───┘           └───┬───┘
        │                   │                   │
   xSTx types          xNTx types          xNFx/xSFx
   ENTJ ops            ENTP innovator      ENFP catalyst
                                           ISFP artisan"""

    # Add new agent indicator
    print(f"\n📊 Organizational Structure:")
    print(tree)
    print(f"\n   🆕 {new_agent} → reports to {manager.upper()}")


def main():
    parser = argparse.ArgumentParser(description='Integrate complete OpenClaw agent')
    parser.add_argument('typology', help="Typology: 'MBTI Xw# inst/inst'")
    parser.add_argument('--name', '-n', required=True, help='Agent name')
    parser.add_argument('--model', '-m', default='qwen2.5:14b')
    parser.add_argument('--role', '-r', default='individual', choices=['manager', 'individual'])
    parser.add_argument('--lang', '-l', default='es', choices=['es', 'en'],
                        help='Output language: es (Spanish, default) or en (English)')
    parser.add_argument('--skip-generate', action='store_true')
    parser.add_argument('--agent-dir', type=Path)
    
    args = parser.parse_args()
    
    parts = args.typology.upper().split()
    mbti = parts[0]
    
    print("=" * 60)
    print(f"🚀 FULL INTEGRATION: {args.name}")
    print(f"   Platform: {get_platform_info()}")
    print(f"   Typology: {args.typology}")
    print(f"   Language: {'🇬🇧 English' if args.lang == 'en' else '🇪🇸 Spanish'}")
    print(f"   Division: {get_division(mbti).upper()}")
    print(f"   Manager: {get_manager(mbti)}")
    print(f"   OpenClaw: {OPENCLAW_AGENTS}")
    print(f"   OpenGoat: {OPENGOAT_AGENTS}")
    print("=" * 60)
    
    # 1. Generate agent
    if args.skip_generate and args.agent_dir:
        agent_dir = args.agent_dir
        print(f"\n⏭️ Using existing agent: {agent_dir}")
    else:
        agent_dir = generate_agent(args.typology, args.name, args.model, args.lang)
    
    # 2. Add to OpenClaw
    add_to_openclaw(agent_dir, args.name)
    
    # 3. Add to OpenGoat
    add_to_opengoat(args.name, mbti, args.role)
    
    # 4. Show structure
    print_org_structure(args.name, mbti)
    
    print("\n" + "=" * 60)
    print(f"✅ {args.name} fully integrated")
    print(f"   OpenClaw: ~/.openclaw/agents/{args.name.lower()}/")
    print(f"   OpenGoat: ~/.opengoat/agents/{args.name.lower()}/")
    print("=" * 60)


if __name__ == '__main__':
    main()
