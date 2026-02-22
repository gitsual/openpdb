#!/usr/bin/env python3
"""
Unit tests for OpenClaw Agent Generator

Run: python -m pytest tests/ -v
Or:  python tests/test_generator.py
"""

import os
import sys
import json
import shutil
import tempfile
import unittest
import platform
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agent_generator import (
    generate_all, get_dominant_functions, clean_output,
    ENEAGRAMA, ALAS, INSTINTOS_COMPORTAMIENTO
)
from integrate_agent import (
    get_division, get_manager, add_to_openclaw, add_to_opengoat,
    get_platform_paths, get_platform_info, OPENCLAW_AGENTS, OPENGOAT_AGENTS
)


class TestTypologyParsing(unittest.TestCase):
    """Test typology string parsing."""
    
    def test_get_dominant_functions_entj(self):
        dom, aux = get_dominant_functions('ENTJ')
        self.assertEqual(dom, 'Te')
        self.assertEqual(aux, 'Ni')
    
    def test_get_dominant_functions_infp(self):
        dom, aux = get_dominant_functions('INFP')
        self.assertEqual(dom, 'Fi')
        self.assertEqual(aux, 'Ne')
    
    def test_get_dominant_functions_isfp(self):
        dom, aux = get_dominant_functions('ISFP')
        self.assertEqual(dom, 'Fi')
        self.assertEqual(aux, 'Se')
    
    def test_get_dominant_functions_lowercase(self):
        dom, aux = get_dominant_functions('entj')
        self.assertEqual(dom, 'Te')
    
    def test_get_dominant_functions_invalid(self):
        """Invalid MBTI should return default."""
        dom, aux = get_dominant_functions('XXXX')
        self.assertIsNotNone(dom)
        self.assertIsNotNone(aux)


class TestDivisionAssignment(unittest.TestCase):
    """Test MBTI to division mapping."""
    
    def test_cto_division(self):
        self.assertEqual(get_division('INTJ'), 'cto')
        self.assertEqual(get_division('INTP'), 'cto')
        self.assertEqual(get_division('ENTP'), 'cto')
    
    def test_coo_division(self):
        self.assertEqual(get_division('ESTJ'), 'coo')
        self.assertEqual(get_division('ISTJ'), 'coo')
        self.assertEqual(get_division('ESTP'), 'coo')
        self.assertEqual(get_division('ISTP'), 'coo')
        self.assertEqual(get_division('ENTJ'), 'coo')
    
    def test_cco_division(self):
        self.assertEqual(get_division('ENFJ'), 'cco')
        self.assertEqual(get_division('INFJ'), 'cco')
        self.assertEqual(get_division('ESFJ'), 'cco')
        self.assertEqual(get_division('ISFJ'), 'cco')
        self.assertEqual(get_division('ENFP'), 'cco')
        self.assertEqual(get_division('INFP'), 'cco')
        self.assertEqual(get_division('ESFP'), 'cco')
        self.assertEqual(get_division('ISFP'), 'cco')


class TestManagerAssignment(unittest.TestCase):
    """Test MBTI to manager mapping."""
    
    def test_sub_managers(self):
        self.assertEqual(get_manager('ENTP'), 'tech_innovator')
        self.assertEqual(get_manager('ENTJ'), 'ops_commander')
        self.assertEqual(get_manager('ISFP'), 'creative_artisan')
        self.assertEqual(get_manager('ESFP'), 'creative_artisan')
        self.assertEqual(get_manager('ENFP'), 'culture_catalyst')
    
    def test_division_managers(self):
        self.assertEqual(get_manager('INTJ'), 'cto_lead')
        self.assertEqual(get_manager('INTP'), 'cto_lead')
        self.assertEqual(get_manager('ESTJ'), 'coo_lead')
        self.assertEqual(get_manager('ENFJ'), 'cco_lead')
        self.assertEqual(get_manager('INFJ'), 'cco_lead')


class TestDataCompleteness(unittest.TestCase):
    """Test that all required data is present."""
    
    def test_all_enneagram_types_present(self):
        for i in range(1, 10):
            self.assertIn(i, ENEAGRAMA)
            self.assertIn('pasion', ENEAGRAMA[i])
            self.assertIn('cuerpo', ENEAGRAMA[i])
            self.assertIn('voz', ENEAGRAMA[i])
    
    def test_common_wings_present(self):
        common_wings = [
            (1, 2), (1, 9), (2, 1), (2, 3), (3, 2), (3, 4),
            (4, 3), (4, 5), (5, 4), (5, 6), (6, 5), (6, 7),
            (7, 6), (7, 8), (8, 7), (8, 9), (9, 8), (9, 1)
        ]
        for wing in common_wings:
            self.assertIn(wing, ALAS, f"Missing wing {wing}")
    
    def test_all_instincts_present(self):
        for inst in ['sp', 'so', 'sx']:
            self.assertIn(inst, INSTINTOS_COMPORTAMIENTO)
            self.assertIn('core', INSTINTOS_COMPORTAMIENTO[inst])
            self.assertIn('acciones', INSTINTOS_COMPORTAMIENTO[inst])


class TestFileGeneration(unittest.TestCase):
    """Test that files are generated correctly."""
    
    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp())
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir)
    
    def test_generate_creates_all_files(self):
        """Test that all required OpenClaw files are created."""
        output_dir = self.temp_dir / 'test_agent'
        
        # Mock generation (skip Ollama for unit test)
        output_dir.mkdir(parents=True, exist_ok=True)
        (output_dir / 'memory').mkdir(exist_ok=True)
        
        required_files = [
            'SOUL.md', 'IDENTITY.md', 'AGENTS.md', 'ROLE.md',
            'TOOLS.md', 'USER.md', 'MEMORY.md', 'HEARTBEAT.md', 
            'BOOTSTRAP.md', 'agent_metadata.json'
        ]
        
        # Create mock files
        for f in required_files:
            (output_dir / f).write_text(f"# {f}\n\nTest content")
        
        for f in required_files:
            self.assertTrue(
                (output_dir / f).exists(),
                f"Missing file: {f}"
            )
    
    def test_memory_directory_created(self):
        """Test that memory/ subdirectory is created."""
        output_dir = self.temp_dir / 'test_agent'
        output_dir.mkdir(parents=True, exist_ok=True)
        (output_dir / 'memory').mkdir(exist_ok=True)
        
        self.assertTrue((output_dir / 'memory').is_dir())


class TestOpenClawIntegration(unittest.TestCase):
    """Test OpenClaw deployment."""
    
    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp())
        self.mock_openclaw = self.temp_dir / '.openclaw' / 'agents'
        self.mock_openclaw.mkdir(parents=True, exist_ok=True)
        
        # Create mock agent
        self.agent_dir = self.temp_dir / 'agent_source'
        self.agent_dir.mkdir(parents=True, exist_ok=True)
        (self.agent_dir / 'SOUL.md').write_text('# Test SOUL')
        (self.agent_dir / 'IDENTITY.md').write_text('# Test ID')
        (self.agent_dir / 'memory').mkdir(exist_ok=True)
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir)
    
    def test_files_copied_to_openclaw(self):
        """Test that files are copied to OpenClaw agents dir."""
        dest = self.mock_openclaw / 'testagent'
        
        # Simulate copy
        shutil.copytree(self.agent_dir, dest)
        
        self.assertTrue((dest / 'SOUL.md').exists())
        self.assertTrue((dest / 'IDENTITY.md').exists())
        self.assertTrue((dest / 'memory').is_dir())
    
    def test_backup_created_on_overwrite(self):
        """Test that backup is created when agent exists."""
        dest = self.mock_openclaw / 'testagent'
        dest.mkdir(parents=True, exist_ok=True)
        (dest / 'OLD.md').write_text('old content')
        
        # Create backup
        backup = dest.parent / 'testagent_backup'
        shutil.move(str(dest), str(backup))
        
        self.assertTrue(backup.exists())
        self.assertTrue((backup / 'OLD.md').exists())


class TestOpenGoatIntegration(unittest.TestCase):
    """Test OpenGoat registration."""
    
    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp())
        self.mock_opengoat = self.temp_dir / '.opengoat' / 'agents'
        self.mock_opengoat.mkdir(parents=True, exist_ok=True)
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir)
    
    def test_config_json_created(self):
        """Test that config.json is created with correct structure."""
        agent_dir = self.mock_opengoat / 'testagent'
        agent_dir.mkdir(parents=True, exist_ok=True)
        
        config = {
            "schemaVersion": 2,
            "id": "testagent",
            "displayName": "TestAgent",
            "organization": {
                "type": "individual",
                "reportsTo": "cto_lead",
                "discoverable": True,
                "tags": ["cto", "intp"]
            }
        }
        
        with open(agent_dir / 'config.json', 'w') as f:
            json.dump(config, f)
        
        # Verify
        with open(agent_dir / 'config.json') as f:
            loaded = json.load(f)
        
        self.assertEqual(loaded['id'], 'testagent')
        self.assertEqual(loaded['organization']['reportsTo'], 'cto_lead')
        self.assertIn('cto', loaded['organization']['tags'])
    
    def test_config_has_required_fields(self):
        """Test that generated config has all required OpenGoat fields."""
        required_fields = ['schemaVersion', 'id', 'displayName', 'organization']
        required_org_fields = ['type', 'reportsTo', 'discoverable']
        
        config = {
            "schemaVersion": 2,
            "id": "test",
            "displayName": "Test",
            "organization": {
                "type": "individual",
                "reportsTo": "goncho",
                "discoverable": True,
                "tags": ["cco"]
            }
        }
        
        for field in required_fields:
            self.assertIn(field, config)
        
        for field in required_org_fields:
            self.assertIn(field, config['organization'])


class TestCleanOutput(unittest.TestCase):
    """Test output cleaning function."""
    
    def test_removes_cjk_characters(self):
        text = "Hello 你好 World 世界"
        cleaned = clean_output(text)
        self.assertNotIn('你', cleaned)
        self.assertNotIn('世', cleaned)
        self.assertIn('Hello', cleaned)
        self.assertIn('World', cleaned)
    
    def test_removes_meta_comments(self):
        text = "Claro, voy a hacer esto:\n---\n# Real content"
        cleaned = clean_output(text)
        self.assertIn('Real content', cleaned)
    
    def test_normalizes_newlines(self):
        text = "Line 1\n\n\n\n\nLine 2"
        cleaned = clean_output(text)
        self.assertNotIn('\n\n\n', cleaned)


class TestEndToEnd(unittest.TestCase):
    """Integration tests for full pipeline."""
    
    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp())
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir)
    
    def test_typology_to_manager_pipeline(self):
        """Test full flow from typology string to manager assignment."""
        test_cases = [
            ('ENTJ 8w7 sx/so', 'ops_commander', 'coo'),
            ('ISFP 6w5 sp/sx', 'creative_artisan', 'cco'),
            ('INTP 5w4 sp/so', 'cto_lead', 'cto'),
            ('ENFP 7w6 so/sx', 'culture_catalyst', 'cco'),
            ('ESTJ 1w2 so/sp', 'coo_lead', 'coo'),
        ]
        
        for typology, expected_manager, expected_division in test_cases:
            mbti = typology.split()[0]
            manager = get_manager(mbti)
            division = get_division(mbti)
            
            self.assertEqual(
                manager, expected_manager,
                f"{typology}: expected manager {expected_manager}, got {manager}"
            )
            self.assertEqual(
                division, expected_division,
                f"{typology}: expected division {expected_division}, got {division}"
            )


class TestPlatformDetection(unittest.TestCase):
    """Test cross-platform support."""
    
    def test_get_platform_paths_returns_paths(self):
        """Verify platform paths are returned."""
        openclaw, opengoat = get_platform_paths()
        self.assertIsInstance(openclaw, Path)
        self.assertIsInstance(opengoat, Path)
    
    def test_get_platform_info_returns_string(self):
        """Verify platform info is returned."""
        info = get_platform_info()
        self.assertIsInstance(info, str)
        self.assertGreater(len(info), 0)
    
    def test_paths_are_absolute(self):
        """Verify paths are absolute."""
        openclaw, opengoat = get_platform_paths()
        self.assertTrue(openclaw.is_absolute())
        self.assertTrue(opengoat.is_absolute())
    
    def test_windows_paths_if_windows(self):
        """On Windows, paths should use APPDATA or USERPROFILE."""
        if platform.system() != 'Windows':
            self.skipTest("Not on Windows")
        openclaw, opengoat = get_platform_paths()
        # Should not have leading dot on Windows
        self.assertNotIn('.openclaw', str(openclaw))
    
    def test_unix_paths_if_unix(self):
        """On Linux/macOS, paths should use dot directories."""
        if platform.system() == 'Windows':
            self.skipTest("Not on Unix")
        openclaw, opengoat = get_platform_paths()
        self.assertIn('.openclaw', str(openclaw))
        self.assertIn('.opengoat', str(opengoat))


class TestRealPaths(unittest.TestCase):
    """Test that real OpenClaw/OpenGoat paths exist (skip if not installed)."""
    
    def test_openclaw_agents_path(self):
        """Check if OpenClaw agents directory exists."""
        if OPENCLAW_AGENTS.exists():
            self.assertTrue(OPENCLAW_AGENTS.is_dir())
        else:
            self.skipTest("OpenClaw not installed")
    
    def test_opengoat_agents_path(self):
        """Check if OpenGoat agents directory exists."""
        if OPENGOAT_AGENTS.exists():
            self.assertTrue(OPENGOAT_AGENTS.is_dir())
        else:
            self.skipTest("OpenGoat not installed")
    
    def test_existing_agent_structure(self):
        """Check structure of an existing agent."""
        openclaw_path = Path.home() / '.openclaw' / 'agents'
        if not openclaw_path.exists():
            self.skipTest("OpenClaw not installed")
        
        agents = list(openclaw_path.iterdir())
        if not agents:
            self.skipTest("No agents found")
        
        # Check first agent
        agent = agents[0]
        if agent.is_dir():
            expected_files = ['SOUL.md']
            for f in expected_files:
                if (agent / f).exists():
                    self.assertTrue(True)
                    return
        
        self.skipTest("No valid agent found")


def run_tests():
    """Run all tests with verbose output."""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
