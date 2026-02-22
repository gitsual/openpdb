#!/usr/bin/env python3
"""
Integration tests - actually run the generator and verify output.

These tests require Ollama to be running with qwen2.5:14b.
Skip with: pytest tests/test_integration.py -k "not slow"
"""

import os
import sys
import json
import shutil
import tempfile
import unittest
import subprocess
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


def ollama_available():
    """Check if Ollama is running."""
    try:
        result = subprocess.run(
            ['ollama', 'list'],
            capture_output=True, text=True, timeout=5
        )
        return result.returncode == 0
    except:
        return False


def model_available(model='qwen2.5:14b'):
    """Check if specific model is available."""
    try:
        result = subprocess.run(
            ['ollama', 'list'],
            capture_output=True, text=True, timeout=5
        )
        return model.split(':')[0] in result.stdout
    except:
        return False


@unittest.skipUnless(ollama_available(), "Ollama not running")
@unittest.skipUnless(model_available(), "Model not available")
class TestRealGeneration(unittest.TestCase):
    """Tests that actually generate agents."""
    
    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp())
        self.script_dir = Path(__file__).parent.parent
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir)
    
    def test_generate_entj_agent(self):
        """Generate ENTJ 8w7 sx/so agent."""
        output_dir = self.temp_dir / 'commander'
        
        result = subprocess.run([
            'python', str(self.script_dir / 'agent_generator.py'),
            'ENTJ 8w7 sx/so',
            '--name', 'Commander',
            '--output', str(output_dir)
        ], capture_output=True, text=True, timeout=300)
        
        self.assertEqual(result.returncode, 0, f"Failed: {result.stderr}")
        
        # Check files exist
        self.assertTrue((output_dir / 'SOUL.md').exists())
        self.assertTrue((output_dir / 'IDENTITY.md').exists())
        self.assertTrue((output_dir / 'AGENTS.md').exists())
        
        # Check SOUL.md has content
        soul = (output_dir / 'SOUL.md').read_text()
        self.assertGreater(len(soul), 500, "SOUL.md too short")
    
    def test_generate_isfp_agent(self):
        """Generate ISFP 6w5 sp/sx agent."""
        output_dir = self.temp_dir / 'guardian'
        
        result = subprocess.run([
            'python', str(self.script_dir / 'agent_generator.py'),
            'ISFP 6w5 sp/sx',
            '--name', 'Guardian',
            '--output', str(output_dir)
        ], capture_output=True, text=True, timeout=300)
        
        self.assertEqual(result.returncode, 0, f"Failed: {result.stderr}")
        self.assertTrue((output_dir / 'SOUL.md').exists())
    
    def test_generated_soul_has_no_meta_labels(self):
        """Verify generated SOUL.md doesn't have meta-labels."""
        output_dir = self.temp_dir / 'test_agent'
        
        subprocess.run([
            'python', str(self.script_dir / 'agent_generator.py'),
            'INTP 5w4 sp/so',
            '--name', 'Analyst',
            '--output', str(output_dir)
        ], capture_output=True, text=True, timeout=300)
        
        if (output_dir / 'SOUL.md').exists():
            soul = (output_dir / 'SOUL.md').read_text().lower()
            
            # Should NOT contain these meta-labels
            bad_patterns = [
                'mi ala 5', 'my wing 5',
                'mi instinto sp', 'my sp instinct',
                'mi función', 'my function',
                'como intp', 'as an intp'
            ]
            
            for pattern in bad_patterns:
                self.assertNotIn(
                    pattern, soul,
                    f"Found meta-label: '{pattern}'"
                )
    
    def test_metadata_json_valid(self):
        """Verify agent_metadata.json is valid JSON."""
        output_dir = self.temp_dir / 'meta_test'
        
        subprocess.run([
            'python', str(self.script_dir / 'agent_generator.py'),
            'ENFJ 2w3 so/sx',
            '--name', 'Helper',
            '--output', str(output_dir)
        ], capture_output=True, text=True, timeout=300)
        
        if (output_dir / 'agent_metadata.json').exists():
            with open(output_dir / 'agent_metadata.json') as f:
                meta = json.load(f)
            
            self.assertEqual(meta['name'], 'Helper')
            self.assertEqual(meta['mbti'], 'ENFJ')
            self.assertEqual(meta['enneagram'], 2)
            self.assertEqual(meta['wing'], 3)


@unittest.skipUnless(ollama_available(), "Ollama not running")
class TestIntegrationPipeline(unittest.TestCase):
    """Test full integration pipeline."""
    
    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp())
        self.script_dir = Path(__file__).parent.parent
        
        # Create mock OpenClaw/OpenGoat directories
        self.mock_openclaw = self.temp_dir / '.openclaw' / 'agents'
        self.mock_opengoat = self.temp_dir / '.opengoat' / 'agents'
        self.mock_openclaw.mkdir(parents=True, exist_ok=True)
        self.mock_opengoat.mkdir(parents=True, exist_ok=True)
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir)
    
    def test_integrate_agent_creates_files(self):
        """Test integrate_agent.py creates all necessary files."""
        # This would require modifying integrate_agent.py to accept
        # custom paths, or mocking the paths. For now, skip.
        self.skipTest("Requires path mocking in integrate_agent.py")


class TestCLIInterface(unittest.TestCase):
    """Test command-line interface."""
    
    def setUp(self):
        self.script_dir = Path(__file__).parent.parent
    
    def test_generator_help(self):
        """Test that --help works."""
        result = subprocess.run([
            'python', str(self.script_dir / 'agent_generator.py'),
            '--help'
        ], capture_output=True, text=True, timeout=10)
        
        self.assertEqual(result.returncode, 0)
        self.assertIn('--name', result.stdout)
        self.assertIn('--output', result.stdout)
    
    def test_integrate_help(self):
        """Test that integrate_agent.py --help works."""
        result = subprocess.run([
            'python', str(self.script_dir / 'integrate_agent.py'),
            '--help'
        ], capture_output=True, text=True, timeout=10)
        
        self.assertEqual(result.returncode, 0)
        self.assertIn('--name', result.stdout)
    
    def test_generator_no_args_shows_usage(self):
        """Test that running without args shows usage."""
        result = subprocess.run([
            'python', str(self.script_dir / 'agent_generator.py')
        ], capture_output=True, text=True, timeout=10)
        
        # Should exit with error but show usage
        self.assertNotEqual(result.returncode, 0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
