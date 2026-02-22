#!/usr/bin/env python3
"""
Integrate Agent - Flujo completo de creación e integración

1. Genera archivos del agente (V8)
2. Añade a OpenClaw (~/.openclaw/agents/<nombre>/)
3. Registra en OpenGoat (~/.opengoat/agents/<nombre>/)
4. Reorganiza empresa según tipología

Estructura de la empresa:
```
ANI (CEO - ENTJ 8w9)
├── RULOG (COO - ESTJ 3w2) → Operaciones
│   ├── FUEGO, ELVIRA, TIN
│   └── Morga, Mosko, Marius, LuisGon
├── CHUCHE (CTO - INTJ 1w2) → Estrategia
│   ├── SANZ, CÉSAR, MARTOR, SERGIO
│   └── CABA → Presi
└── GONCHO (CCO - ENFJ 7w6) → Cultura
    ├── ARANDA, KLAUDIA, AMIRA, CLAURS, WENGEL
    ├── KELLY → Puma
    └── RODRI → José, Majano, Lorena
```
"""

import os
import sys
import json
import shutil
import subprocess
import argparse
from pathlib import Path
from datetime import datetime

# Rutas
OPENCLAW_AGENTS = Path.home() / '.openclaw' / 'agents'
OPENGOAT_AGENTS = Path.home() / '.opengoat' / 'agents'

# Managers por división
DIVISION_MANAGERS = {
    'cto': 'chuche',
    'coo': 'rulog',
    'cco': 'goncho',
}

# Sub-managers específicos por MBTI
SUB_MANAGERS = {
    'ENTP': 'caba',
    'ENTJ': 'fuego',
    'ISFP': 'rodri',
    'ESFP': 'rodri',
    'ENFP': 'kelly',
}


def get_division(mbti: str) -> str:
    """Determina la división según MBTI."""
    mbti = mbti.upper()
    if mbti in ['INTJ', 'INTP', 'ENTP']:
        return 'cto'
    if mbti in ['ESTJ', 'ISTJ', 'ESTP', 'ISTP', 'ENTJ']:
        return 'coo'
    return 'cco'


def get_manager(mbti: str) -> str:
    """Determina el manager directo según MBTI."""
    mbti = mbti.upper()
    if mbti in SUB_MANAGERS:
        return SUB_MANAGERS[mbti]
    return DIVISION_MANAGERS[get_division(mbti)]


def generate_agent(typology: str, name: str, model: str = "qwen2.5:14b", 
                   lang: str = "es") -> Path:
    """Genera el agente usando V8."""
    script_dir = Path(__file__).parent
    output_dir = script_dir / 'agents' / name.lower().replace(' ', '_')
    
    cmd = [
        'python', str(script_dir / 'agent_generator.py'),
        typology, '--name', name, '--output', str(output_dir), 
        '--model', model, '--lang', lang
    ]
    
    print(f"\n📝 Generando agente '{name}'...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ Error: {result.stderr}")
        sys.exit(1)
    print(result.stdout)
    return output_dir


def add_to_openclaw(agent_dir: Path, name: str) -> bool:
    """Copia el agente a OpenClaw."""
    agent_id = name.lower().replace(' ', '_')
    dest = OPENCLAW_AGENTS / agent_id
    
    print(f"\n🦞 Añadiendo a OpenClaw...")
    
    # Backup si existe
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
    """Registra el agente en OpenGoat."""
    agent_id = name.lower().replace(' ', '_')
    manager = get_manager(mbti)
    division = get_division(mbti)
    
    print(f"\n🐐 Registrando en OpenGoat...")
    print(f"   División: {division.upper()}")
    print(f"   Manager: {manager}")
    
    agent_dir = OPENGOAT_AGENTS / agent_id
    agent_dir.mkdir(parents=True, exist_ok=True)
    
    # Crear config.json
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
    
    # Crear archivos auxiliares vacíos si no existen
    (agent_dir / 'auth.json').write_text('{}')
    (agent_dir / 'models.json').write_text('{}')
    
    print(f"   ✅ {agent_dir}")
    return True


def print_org_structure(new_agent: str, mbti: str):
    """Muestra la estructura organizacional actualizada."""
    manager = get_manager(mbti)
    
    # Construir árbol con el nuevo agente resaltado
    tree = f"""
    ┌─────────────────────────────────────────────────────┐
    │                    ANI (CEO)                        │
    └─────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
    ┌───┴───┐           ┌───┴───┐           ┌───┴───┐
    │ RULOG │           │CHUCHE │           │GONCHO │
    │  COO  │           │  CTO  │           │  CCO  │
    └───┬───┘           └───┬───┘           └───┬───┘
        │                   │                   │
   ┌────┼────┐         ┌────┼────┐         ┌────┼────┐
   │    │    │         │    │    │         │    │    │
 FUEGO ELVIRA TIN    SANZ CESAR CABA    KELLY RODRI ARANDA
   │         │              │    │         │    │
 Morga     Marius         MARTOR Presi   Puma José
 Mosko     LuisGon        SERGIO              Majano
                                              Lorena"""

    # Añadir indicador del nuevo agente
    print(f"\n📊 Estructura Organizacional:")
    print(tree)
    print(f"\n   🆕 {new_agent} → reporta a {manager.upper()}")


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
    print(f"🚀 INTEGRACIÓN COMPLETA: {args.name}")
    print(f"   Tipología: {args.typology}")
    print(f"   División: {get_division(mbti).upper()}")
    print(f"   Manager: {get_manager(mbti)}")
    print("=" * 60)
    
    # 1. Generar agente
    if args.skip_generate and args.agent_dir:
        agent_dir = args.agent_dir
        print(f"\n⏭️ Using existing agent: {agent_dir}")
    else:
        agent_dir = generate_agent(args.typology, args.name, args.model, args.lang)
    
    # 2. Añadir a OpenClaw
    add_to_openclaw(agent_dir, args.name)
    
    # 3. Añadir a OpenGoat
    add_to_opengoat(args.name, mbti, args.role)
    
    # 4. Mostrar estructura
    print_org_structure(args.name, mbti)
    
    print("\n" + "=" * 60)
    print(f"✅ {args.name} integrado completamente")
    print(f"   OpenClaw: ~/.openclaw/agents/{args.name.lower()}/")
    print(f"   OpenGoat: ~/.opengoat/agents/{args.name.lower()}/")
    print("=" * 60)


if __name__ == '__main__':
    main()
