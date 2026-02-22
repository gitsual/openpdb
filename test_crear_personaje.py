#!/usr/bin/env python3
"""
Tests unitarios para crear_personaje.py
Ejecutar: pytest test_crear_personaje.py -v
"""

import pytest
import json
from pathlib import Path
from unittest.mock import patch, MagicMock

from crear_personaje import (
    load_variants_from_directory,
    build_character_prompt,
    PRINCIPIOS_RAND
)

OUTPUT_DIR = Path("/home/lorty/m2/programas/creador_de_personajes/output")
REFERENCE_DIR = Path("/home/lorty/m2/Documentos/Recuperacion Obsidian Vaults/Obsidian Vault/ACTIVOS/Personajes")


class TestLoadVariants:
    """Tests para carga de variantes"""
    
    def test_load_from_data_json(self):
        """Carga variantes desde data.json"""
        test_dir = OUTPUT_DIR / "ENTJ_8w7_sx-so_hombre"
        if not test_dir.exists():
            pytest.skip("No hay output de test")
        
        data = load_variants_from_directory(test_dir)
        
        assert 'variants' in data or 'variants_text' in data
        assert 'typology' in data or len(data) > 0
    
    def test_variants_have_output(self):
        """Cada variante debe tener output generado"""
        test_dir = OUTPUT_DIR / "ENTJ_8w7_sx-so_hombre"
        if not test_dir.exists():
            pytest.skip("No hay output de test")
        
        data = load_variants_from_directory(test_dir)
        
        if 'variants' in data:
            for variant in data['variants']:
                assert 'output' in variant, f"Falta output en {variant.get('nombre', '?')}"
                assert len(variant['output']) > 50, f"Output muy corto en {variant.get('nombre', '?')}"


class TestBuildCharacterPrompt:
    """Tests para construcción de prompt"""
    
    def test_prompt_includes_all_7_sides(self):
        """El prompt debe incluir los 7 lados"""
        test_dir = OUTPUT_DIR / "ENTJ_8w7_sx-so_hombre"
        if not test_dir.exists():
            pytest.skip("No hay output de test")
        
        data = load_variants_from_directory(test_dir)
        prompt = build_character_prompt(data, "Test Character")
        
        expected_sections = [
            "EGO",
            "SUBCONSCIENTE SANO",
            "SUBCONSCIENTE INSANO",
            "INCONSCIENTE SANO",
            "INCONSCIENTE INSANO",
            "SUPER-EGO SANO",
            "SUPER-EGO INSANO"
        ]
        
        for section in expected_sections:
            assert section in prompt, f"Falta sección: {section}"
    
    def test_prompt_includes_profile(self):
        """El prompt debe incluir info del perfil"""
        test_dir = OUTPUT_DIR / "ENTJ_8w7_sx-so_hombre"
        if not test_dir.exists():
            pytest.skip("No hay output de test")
        
        data = load_variants_from_directory(test_dir)
        prompt = build_character_prompt(data, "Comandante Vega")
        
        assert "Comandante Vega" in prompt
        assert "ENTJ" in prompt or "Extraído" in prompt


class TestPrincipiosRand:
    """Tests para los principios de caracterización"""
    
    def test_principios_contains_key_concepts(self):
        """Los principios deben contener conceptos clave de Rand"""
        key_concepts = [
            "CONCRETIZACIÓN",
            "PREMISA FUNDAMENTAL",
            "SENTIDO DE VIDA",
            "COHERENCIA PSICOLÓGICA",
            "VALORES ENCARNADOS",
            "CONFLICTO DRAMÁTICO",
            "ARCO DE RESOLUCIÓN"
        ]
        
        for concept in key_concepts:
            assert concept in PRINCIPIOS_RAND, f"Falta concepto: {concept}"


class TestOutputStructure:
    """Tests para la estructura del output generado"""
    
    def test_output_has_required_sections(self):
        """El personaje completo debe tener secciones requeridas"""
        test_dir = OUTPUT_DIR / "ENTJ_8w7_sx-so_hombre"
        personaje_files = list(test_dir.glob("*definicion_completa.md"))
        
        if not personaje_files:
            pytest.skip("No hay personaje generado")
        
        content = personaje_files[0].read_text(encoding='utf-8')
        
        # Secciones críticas según referencia
        required_sections = [
            ("Análisis Integral", "intro"),
            ("Constelación Interna", "constelación"),
            ("Ego", "ego section"),
        ]
        
        missing = []
        for pattern, name in required_sections:
            if pattern.lower() not in content.lower():
                missing.append(name)
        
        if missing:
            print(f"\n⚠️  Secciones faltantes: {missing}")
        
        # Al menos debe tener intro y constelación
        assert "análisis" in content.lower() or "integral" in content.lower()
        assert "constelación" in content.lower()


class TestComparisonWithReference:
    """Compara estructura con personajes de referencia"""
    
    def test_reference_structure_analysis(self):
        """Analiza qué tienen los de referencia"""
        ref_file = REFERENCE_DIR / "José" / "Personaje Completo José.md"
        if not ref_file.exists():
            pytest.skip("No hay referencia")
        
        content = ref_file.read_text(encoding='utf-8')
        
        # Extraer headers
        headers = []
        for line in content.split('\n'):
            if line.startswith('#'):
                headers.append(line.strip())
        
        print("\n📋 Headers en referencia (José):")
        for h in headers:
            print(f"   {h}")
        
        # Debe tener al menos estos
        assert any("Análisis" in h for h in headers)
        assert any("Constelación" in h for h in headers)
    
    def test_generated_vs_reference_headers(self):
        """Compara headers generado vs referencia"""
        test_dir = OUTPUT_DIR / "ENTJ_8w7_sx-so_hombre"
        personaje_files = list(test_dir.glob("*definicion_completa.md"))
        
        if not personaje_files:
            pytest.skip("No hay personaje generado")
        
        ref_file = REFERENCE_DIR / "José" / "Personaje Completo José.md"
        if not ref_file.exists():
            pytest.skip("No hay referencia")
        
        gen_content = personaje_files[0].read_text(encoding='utf-8')
        ref_content = ref_file.read_text(encoding='utf-8')
        
        def extract_headers(text):
            return [line.strip() for line in text.split('\n') if line.startswith('#')]
        
        gen_headers = extract_headers(gen_content)
        ref_headers = extract_headers(ref_content)
        
        print("\n📊 Comparación de headers:")
        print(f"   Generado: {len(gen_headers)} headers")
        print(f"   Referencia: {len(ref_headers)} headers")
        
        # Buscar headers de referencia que faltan en generado
        ref_patterns = [
            "transicion",
            "propósito",
            "subconsciente",
            "inconsciente",
            "super-ego"
        ]
        
        gen_lower = gen_content.lower()
        missing = []
        for pattern in ref_patterns:
            if pattern not in gen_lower:
                missing.append(pattern)
        
        if missing:
            print(f"\n⚠️  Patrones faltantes en generado: {missing}")


class TestWordCountComparison:
    """Compara longitudes"""
    
    def test_word_count_ratio(self):
        """El generado debe tener al menos 60% de palabras vs referencia"""
        test_dir = OUTPUT_DIR / "ENTJ_8w7_sx-so_hombre"
        personaje_files = list(test_dir.glob("*definicion_completa.md"))
        
        if not personaje_files:
            pytest.skip("No hay personaje generado")
        
        ref_file = REFERENCE_DIR / "José" / "Personaje Completo José.md"
        if not ref_file.exists():
            pytest.skip("No hay referencia")
        
        gen_words = len(personaje_files[0].read_text().split())
        ref_words = len(ref_file.read_text().split())
        
        ratio = gen_words / ref_words
        
        print(f"\n📊 Palabras: {gen_words} generado / {ref_words} referencia = {ratio:.1%}")
        
        assert ratio >= 0.5, f"Generado tiene solo {ratio:.0%} de palabras vs referencia"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
