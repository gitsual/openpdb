#!/usr/bin/env python3
"""
Organization Optimizer for OpenGoat Integration.

Determines optimal hierarchical structure for N agents based on:
- MBTI type (leadership, strategic, operational, cultural fit)
- Enneagram type (motivation, stress behavior, growth)
- Instinctual variants (sp/so/sx priorities)

Outputs reportsTo relationships and role assignments for OpenGoat.
"""

import json
import os
from dataclasses import dataclass, field
from typing import Optional
from pathlib import Path


# =============================================================================
# PERSONALITY SCORING MATRICES
# =============================================================================

# MBTI Leadership/Role Scores (0-10)
MBTI_SCORES = {
    # Type: (CEO, CTO, COO, CCO, IC)
    # CEO = Strategic vision, IC = Individual Contributor
    "ENTJ": (10, 7, 6, 4, 3),   # Natural leader, strategic
    "INTJ": (7, 10, 5, 3, 6),   # Mastermind, architect
    "ENTP": (6, 9, 4, 6, 7),    # Innovator, debater
    "INTP": (4, 10, 3, 2, 9),   # Analyst, theorist
    "ENFJ": (8, 4, 5, 10, 4),   # Teacher, mentor
    "INFJ": (6, 5, 4, 9, 7),    # Advocate, counselor
    "ENFP": (5, 6, 4, 8, 7),    # Campaigner, inspirer
    "INFP": (3, 5, 3, 7, 9),    # Mediator, idealist
    "ESTJ": (8, 5, 10, 4, 4),   # Executive, organizer
    "ISTJ": (5, 6, 9, 3, 7),    # Inspector, duty-focused
    "ESFJ": (5, 3, 7, 9, 5),    # Consul, caregiver
    "ISFJ": (3, 4, 7, 8, 7),    # Defender, protector
    "ESTP": (6, 6, 8, 5, 7),    # Entrepreneur, doer
    "ISTP": (4, 8, 7, 2, 9),    # Virtuoso, craftsman
    "ESFP": (4, 4, 6, 7, 7),    # Entertainer, performer
    "ISFP": (3, 5, 5, 6, 9),    # Adventurer, artist
}

# Enneagram modifiers for roles
ENNEAGRAM_MODIFIERS = {
    # Type: (CEO_mod, CTO_mod, COO_mod, CCO_mod, IC_mod)
    "1": (1.1, 1.0, 1.2, 1.1, 1.0),   # Perfectionist - good at standards
    "2": (0.9, 0.8, 1.0, 1.3, 1.0),   # Helper - people-focused
    "3": (1.2, 1.0, 1.1, 1.0, 0.9),   # Achiever - results-driven
    "4": (0.8, 0.9, 0.8, 1.1, 1.2),   # Individualist - creative
    "5": (0.9, 1.3, 0.9, 0.8, 1.2),   # Investigator - analytical
    "6": (0.9, 1.0, 1.2, 1.0, 1.1),   # Loyalist - security-focused
    "7": (1.0, 1.1, 0.9, 1.1, 1.0),   # Enthusiast - visionary
    "8": (1.3, 1.0, 1.1, 0.9, 0.8),   # Challenger - powerful leader
    "9": (0.8, 0.9, 1.0, 1.2, 1.1),   # Peacemaker - harmonizer
}

# Wing influences (adds flavor but less weight)
WING_BONUS = {
    "w1": {"COO": 0.1, "CCO": 0.05},
    "w2": {"CCO": 0.1, "COO": 0.05},
    "w3": {"CEO": 0.1, "CTO": 0.05},
    "w4": {"IC": 0.1, "CCO": 0.05},
    "w5": {"CTO": 0.1, "IC": 0.05},
    "w6": {"COO": 0.1, "CTO": 0.05},
    "w7": {"CEO": 0.05, "CCO": 0.1},
    "w8": {"CEO": 0.1, "COO": 0.05},
    "w9": {"CCO": 0.1, "IC": 0.05},
}

# Compatibility matrix for reporting relationships
# Higher = better compatibility as direct report
COMPATIBILITY = {
    # Boss MBTI -> Best subordinate types
    "ENTJ": ["INTJ", "INTP", "ISTJ", "ISTP", "ESTJ"],
    "INTJ": ["INTP", "ISTJ", "ISTP", "INFJ", "ENTJ"],
    "ESTJ": ["ISTJ", "ISFJ", "ESTP", "ISTP", "ESFJ"],
    "ENFJ": ["INFJ", "INFP", "ENFP", "ISFJ", "ESFJ"],
    "ENTP": ["INTP", "INTJ", "ENFP", "ISTP", "ESTP"],
    "INFJ": ["INFP", "ISFJ", "INTJ", "ENFP", "INTP"],
}

# Role titles by function
ROLE_TITLES = {
    "CEO": [
        "CEO - Strategic Leadership",
        "CEO - Visionary Leadership", 
        "Chief Executive Officer",
        "President & CEO",
    ],
    "CTO": [
        "CTO - Chief Technology Officer",
        "CTO - Technical Strategy",
        "CTO - Innovation & R&D",
        "VP Engineering",
    ],
    "COO": [
        "COO - Operations",
        "COO - Field Operations",
        "Chief Operating Officer",
        "VP Operations",
    ],
    "CCO": [
        "CCO - Culture & People",
        "CCO - Culture & Ethics",
        "Chief Culture Officer",
        "VP People & Culture",
    ],
    "IC": [
        "Senior Specialist",
        "Principal Contributor",
        "Technical Lead",
        "Domain Expert",
    ],
}


@dataclass
class Agent:
    """Represents an agent with personality data."""
    id: str
    name: str
    mbti: str
    enneagram: str  # e.g., "8w7", "5w4"
    instincts: str = "sp/so"  # e.g., "sx/so", "sp/sx"
    skills: list = field(default_factory=list)
    
    # Computed scores
    role_scores: dict = field(default_factory=dict)
    assigned_role: str = ""
    reports_to: Optional[str] = None
    
    def __post_init__(self):
        self.role_scores = self._compute_scores()
    
    def _compute_scores(self) -> dict:
        """Compute role fitness scores based on personality."""
        # Base MBTI scores
        mbti_base = str(self.mbti).upper()
        if mbti_base not in MBTI_SCORES:
            mbti_base = "INTJ"  # Default fallback
        
        ceo, cto, coo, cco, ic = MBTI_SCORES[mbti_base]
        
        # Parse enneagram (e.g., "8w7" -> type="8", wing="w7")
        ennea_str = str(self.enneagram) if self.enneagram else "5w4"
        ennea_type = ennea_str[0] if ennea_str else "5"
        wing = "w" + ennea_str[2] if len(ennea_str) >= 3 else None
        
        # Apply enneagram modifiers
        if ennea_type in ENNEAGRAM_MODIFIERS:
            mods = ENNEAGRAM_MODIFIERS[ennea_type]
            ceo *= mods[0]
            cto *= mods[1]
            coo *= mods[2]
            cco *= mods[3]
            ic *= mods[4]
        
        scores = {
            "CEO": round(ceo, 2),
            "CTO": round(cto, 2),
            "COO": round(coo, 2),
            "CCO": round(cco, 2),
            "IC": round(ic, 2),
        }
        
        # Apply wing bonuses
        if wing and wing in WING_BONUS:
            for role, bonus in WING_BONUS[wing].items():
                if role in scores:
                    scores[role] = round(scores[role] + bonus, 2)
        
        return scores
    
    def best_role(self, exclude: list = None) -> str:
        """Get best available role for this agent."""
        exclude = exclude or []
        available = {k: v for k, v in self.role_scores.items() if k not in exclude}
        if not available:
            return "IC"
        return max(available, key=available.get)


class OrgOptimizer:
    """
    Optimizes organizational structure for a set of agents.
    """
    
    def __init__(self, agents: list[Agent]):
        self.agents = agents
        self.structure = {}  # agent_id -> {role, reports_to, title}
    
    def optimize(self) -> dict:
        """
        Determine optimal organization structure.
        
        Returns dict with structure:
        {
            "agent_id": {
                "role": "CEO",
                "title": "CEO - Strategic Leadership",
                "reports_to": null,
                "direct_reports": ["agent2", "agent3"]
            }
        }
        """
        if not self.agents:
            return {}
        
        # Sort agents by CEO score (highest first)
        agents_by_ceo = sorted(
            self.agents, 
            key=lambda a: a.role_scores.get("CEO", 0), 
            reverse=True
        )
        
        # Assign CEO (highest CEO score)
        ceo = agents_by_ceo[0]
        ceo.assigned_role = "CEO"
        ceo.reports_to = None
        
        self.structure[ceo.id] = {
            "role": "CEO",
            "title": self._pick_title("CEO", ceo),
            "reports_to": None,
            "direct_reports": [],
        }
        
        remaining = agents_by_ceo[1:]
        
        if not remaining:
            return self.structure
        
        # Determine org size and depth
        n = len(self.agents)
        
        if n <= 4:
            # Small team: CEO + direct reports
            self._assign_flat(ceo, remaining)
        elif n <= 8:
            # Medium team: CEO + C-suite + ICs
            self._assign_two_tier(ceo, remaining)
        else:
            # Large team: CEO + C-suite + Managers + ICs
            self._assign_three_tier(ceo, remaining)
        
        return self.structure
    
    def _assign_flat(self, ceo: Agent, remaining: list[Agent]):
        """All agents report directly to CEO."""
        used_roles = {"CEO"}
        
        for agent in remaining:
            role = agent.best_role(exclude=list(used_roles))
            if role != "IC":
                used_roles.add(role)
            
            agent.assigned_role = role
            agent.reports_to = ceo.id
            
            self.structure[agent.id] = {
                "role": role,
                "title": self._pick_title(role, agent),
                "reports_to": ceo.id,
                "direct_reports": [],
            }
            self.structure[ceo.id]["direct_reports"].append(agent.id)
    
    def _assign_two_tier(self, ceo: Agent, remaining: list[Agent]):
        """CEO -> C-suite -> ICs"""
        # Pick best CTO, COO, CCO
        c_suite = {}
        used_roles = {"CEO"}
        
        for role in ["CTO", "COO", "CCO"]:
            best = max(remaining, key=lambda a: a.role_scores.get(role, 0))
            if best.assigned_role:
                continue
            
            best.assigned_role = role
            best.reports_to = ceo.id
            c_suite[role] = best
            used_roles.add(role)
            
            self.structure[best.id] = {
                "role": role,
                "title": self._pick_title(role, best),
                "reports_to": ceo.id,
                "direct_reports": [],
            }
            self.structure[ceo.id]["direct_reports"].append(best.id)
            remaining = [a for a in remaining if a.id != best.id]
        
        # Distribute remaining as ICs under best-fit C-suite
        for agent in remaining:
            if agent.assigned_role:
                continue
            
            agent.assigned_role = "IC"
            
            # Find best manager based on MBTI compatibility
            best_manager = self._find_best_manager(agent, list(c_suite.values()))
            agent.reports_to = best_manager.id
            
            self.structure[agent.id] = {
                "role": "IC",
                "title": self._pick_title("IC", agent),
                "reports_to": best_manager.id,
                "direct_reports": [],
            }
            self.structure[best_manager.id]["direct_reports"].append(agent.id)
    
    def _assign_three_tier(self, ceo: Agent, remaining: list[Agent]):
        """CEO -> C-suite -> Directors -> ICs (for large orgs)"""
        # Similar to two-tier but with additional management layer
        self._assign_two_tier(ceo, remaining[:7])  # Simplified for now
    
    def _find_best_manager(self, agent: Agent, managers: list[Agent]) -> Agent:
        """Find best manager for an agent based on compatibility."""
        if not managers:
            return self.agents[0]  # Fallback to CEO
        
        best_score = -1
        best_manager = managers[0]
        
        for manager in managers:
            # Check if agent's MBTI is compatible with manager
            compatible_types = COMPATIBILITY.get(manager.mbti.upper(), [])
            score = 10 if agent.mbti.upper() in compatible_types else 5
            
            # Prefer managers with fewer reports (balance)
            report_count = len(self.structure.get(manager.id, {}).get("direct_reports", []))
            score -= report_count * 0.5
            
            if score > best_score:
                best_score = score
                best_manager = manager
        
        return best_manager
    
    def _pick_title(self, role: str, agent: Agent) -> str:
        """Pick appropriate title based on role and personality."""
        titles = ROLE_TITLES.get(role, ROLE_TITLES["IC"])
        # Could be smarter here based on agent personality
        return titles[hash(agent.id) % len(titles)]
    
    def to_opengoat_config(self) -> dict:
        """
        Generate OpenGoat-compatible agent configurations.
        
        Returns dict mapping agent_id -> agent.json content
        """
        configs = {}
        
        for agent in self.agents:
            info = self.structure.get(agent.id, {})
            
            config = {
                "id": agent.id,
                "displayName": agent.name,
                "role": info.get("title", "Team Member"),
                "type": "manager" if info.get("direct_reports") else "individual",
                "skills": agent.skills,
            }
            
            if info.get("reports_to"):
                config["reportsTo"] = info["reports_to"]
            
            configs[agent.id] = config
        
        return configs
    
    def print_org_chart(self):
        """Print ASCII org chart."""
        def print_node(agent_id, indent=0):
            info = self.structure.get(agent_id, {})
            agent = next((a for a in self.agents if a.id == agent_id), None)
            if not agent:
                return
            
            prefix = "  " * indent + ("└── " if indent > 0 else "")
            mbti_ennea = f"{agent.mbti} {agent.enneagram}"
            print(f"{prefix}{agent.name} [{info.get('role', '?')}] ({mbti_ennea})")
            
            for report_id in info.get("direct_reports", []):
                print_node(report_id, indent + 1)
        
        # Find root (CEO)
        roots = [a.id for a in self.agents if not self.structure.get(a.id, {}).get("reports_to")]
        for root in roots:
            print_node(root)


def load_agents_from_examples(examples_dir: str) -> list[Agent]:
    """Load agents from generated example folders."""
    agents = []
    examples_path = Path(examples_dir)
    
    # Mapping folder names to full display names (for known characters)
    DISPLAY_NAMES = {
        "batman": "Batman",
        "tony_stark": "Tony Stark",
        "john_wick": "John Wick",
        "joker": "The Joker",
        "daenerys": "Daenerys Targaryen",
        "ripley": "Ellen Ripley",
        "katniss": "Katniss Everdeen",
        "wonder_woman": "Wonder Woman",
    }
    
    for folder in examples_path.iterdir():
        if not folder.is_dir():
            continue
        
        # Try to load agent_metadata.json
        metadata_file = folder / "agent_metadata.json"
        identity_file = folder / "IDENTITY.md"
        
        agent_id = folder.name.replace("_", "-")
        # Use display name mapping or format folder name
        name = DISPLAY_NAMES.get(folder.name, folder.name.replace("_", " ").title())
        mbti = "INTJ"  # Default
        enneagram = "5w4"  # Default
        
        if metadata_file.exists():
            try:
                with open(metadata_file) as f:
                    meta = json.load(f)
                    # Only use metadata name if no display name mapping exists
                    if folder.name not in DISPLAY_NAMES:
                        name = meta.get("name", name)
                    mbti = meta.get("mbti", mbti)
                    # Handle both "8w7" format and separate enneagram/wing fields
                    ennea = meta.get("enneagram", "5")
                    wing = meta.get("wing", "")
                    if wing:
                        enneagram = f"{ennea}w{wing}"
                    else:
                        enneagram = str(ennea)
            except:
                pass
        
        # Fallback: parse IDENTITY.md for MBTI/enneagram if not in metadata
        if identity_file.exists() and mbti == "INTJ":
            try:
                content = identity_file.read_text()
                import re
                mbti_match = re.search(r'\b([EI][SN][TF][JP])\b', content)
                if mbti_match:
                    mbti = mbti_match.group(1)
                ennea_match = re.search(r'\b(\d)w(\d)\b', content)
                if ennea_match:
                    enneagram = ennea_match.group(0)
            except:
                pass
        
        agents.append(Agent(
            id=agent_id,
            name=name,
            mbti=mbti,
            enneagram=enneagram,
        ))
    
    return agents


def optimize_examples(examples_dir: str = "examples") -> dict:
    """
    Load examples and compute optimal organization.
    
    Returns the optimized structure.
    """
    agents = load_agents_from_examples(examples_dir)
    
    if not agents:
        print("No agents found in examples/")
        return {}
    
    print(f"Found {len(agents)} agents:")
    for a in agents:
        print(f"  - {a.name}: {a.mbti} {a.enneagram}")
    print()
    
    optimizer = OrgOptimizer(agents)
    structure = optimizer.optimize()
    
    print("Optimal Organization:")
    print("=" * 50)
    optimizer.print_org_chart()
    print()
    
    return optimizer.to_opengoat_config()


def export_to_opengoat(configs: dict, examples_dir: str, opengoat_home: str = None):
    """
    Export optimized structure to OpenGoat.
    
    Creates agent.json files in OPENGOAT_HOME/agents/<agent_id>/
    and copies workspace files from examples.
    """
    import shutil
    
    if opengoat_home is None:
        opengoat_home = os.environ.get("OPENGOAT_HOME", os.path.expanduser("~/.opengoat"))
    
    opengoat_path = Path(opengoat_home)
    agents_dir = opengoat_path / "agents"
    workspaces_dir = opengoat_path / "workspaces"
    examples_path = Path(examples_dir)
    
    print(f"\nExporting to OpenGoat: {opengoat_path}")
    
    for agent_id, config in configs.items():
        # Determine source folder (handle - vs _ in names)
        folder_name = agent_id.replace("-", "_")
        source = examples_path / folder_name
        if not source.exists():
            source = examples_path / agent_id
        
        if not source.exists():
            print(f"  ⚠ Source not found for {agent_id}, skipping")
            continue
        
        # Create agent config directory
        agent_config_dir = agents_dir / agent_id
        agent_config_dir.mkdir(parents=True, exist_ok=True)
        
        # Write agent.json
        agent_json = {
            "id": agent_id,
            "displayName": config.get("displayName", agent_id),
            "role": config.get("role", "Team Member"),
            "type": config.get("type", "individual"),
            "skills": config.get("skills", []),
            "workspaceDir": str(workspaces_dir / agent_id),
            "provider": "ollama",
            "model": "qwen2.5:14b",
        }
        
        if config.get("reportsTo"):
            agent_json["reportsTo"] = config["reportsTo"]
        
        with open(agent_config_dir / "agent.json", "w") as f:
            json.dump(agent_json, f, indent=2)
        
        # Copy workspace files
        workspace_dest = workspaces_dir / agent_id
        if workspace_dest.exists():
            shutil.rmtree(workspace_dest)
        shutil.copytree(source, workspace_dest)
        
        role_indicator = "👑" if "CEO" in config.get("role", "") else "📁"
        reports = f" → {config.get('reportsTo')}" if config.get("reportsTo") else " (root)"
        print(f"  {role_indicator} {agent_id}: {config.get('role', 'IC')}{reports}")
    
    print(f"\n✅ Exported {len(configs)} agents to OpenGoat")
    print(f"   Restart OpenGoat UI to see changes")


# =============================================================================
# CLI
# =============================================================================

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Optimize organization structure for OpenGoat",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze examples and show optimal structure
  python org_optimizer.py -d examples
  
  # Export to OpenGoat
  python org_optimizer.py -d examples --export-opengoat
  
  # Export to custom OpenGoat home
  python org_optimizer.py -d examples --export-opengoat --opengoat-home /tmp/demo
  
  # Save configs to JSON
  python org_optimizer.py -d examples -o org_structure.json
        """
    )
    parser.add_argument("-d", "--dir", default="examples", help="Examples directory")
    parser.add_argument("-o", "--output", help="Output JSON file for configs")
    parser.add_argument("--export-opengoat", action="store_true", 
                        help="Export to OpenGoat (creates agent.json files)")
    parser.add_argument("--opengoat-home", help="OpenGoat home directory (default: ~/.opengoat)")
    parser.add_argument("--json", action="store_true", help="Print configs as JSON")
    
    args = parser.parse_args()
    
    configs = optimize_examples(args.dir)
    
    if args.output:
        with open(args.output, "w") as f:
            json.dump(configs, f, indent=2)
        print(f"\nSaved configs to {args.output}")
    
    if args.json:
        print("\nOpenGoat Configs:")
        print(json.dumps(configs, indent=2))
    
    if args.export_opengoat:
        export_to_opengoat(configs, args.dir, args.opengoat_home)
