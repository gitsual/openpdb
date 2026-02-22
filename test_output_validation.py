#!/usr/bin/env python3
"""
Tests de Validación de Outputs
Verifica que los outputs generados sean similares a los ejemplos de referencia
de Obsidian (/ACTIVOS/Personajes/)

Ejecutar: pytest test_output_validation.py -v
"""

import pytest
import os
import re
import json
from pathlib import Path
from typing import List, Dict, Tuple
from dataclasses import dataclass

# Rutas
REFERENCE_DIR = Path("/home/lorty/m2/Documentos/Recuperacion Obsidian Vaults/Obsidian Vault/ACTIVOS/Personajes")
OUTPUT_DIR = Path("/home/lorty/m2/programas/creador_de_personajes/output")


@dataclass
class NarradorMetrics:
    """Métricas de calidad de un narrador"""
    word_count: int
    char_count: int
    starts_correctly: bool
    has_cultural_reference: bool
    has_paradox_structure: bool
    has_observable_behavior: bool
    has_mask_break: bool  # "pequeños detalles donde se rompe la máscara"
    has_power_form: bool  # forma de ejercer poder/influencia
    has_potent_ending: bool
    
    @property
    def score(self) -> float:
        """Score de calidad 0-10"""
        points = 0
        # Longitud (2 puntos)
        if 100 <= self.word_count <= 300:
            points += 2
        elif 50 <= self.word_count <= 400:
            points += 1
        
        # Estructura (8 puntos)
        if self.starts_correctly:
            points += 1.5
        if self.has_cultural_reference:
            points += 1.5
        if self.has_paradox_structure:
            points += 1.5
        if self.has_observable_behavior:
            points += 1
        if self.has_mask_break:
            points += 1
        if self.has_power_form:
            points += 0.5
        if self.has_potent_ending:
            points += 0.5
        
        return points


@dataclass  
class PersonajeCompletoMetrics:
    """Métricas de un personaje completo"""
    has_intro: bool
    has_constelacion: bool
    has_ego_section: bool
    has_inconsciente_section: bool
    has_subconsciente_section: bool
    has_superego_section: bool
    has_sano_insano_variants: bool
    has_transiciones: bool
    has_proposito: bool
    has_quotes: bool
    word_count: int
    
    @property
    def score(self) -> float:
        """Score de completitud 0-10"""
        points = 0
        if self.has_intro:
            points += 1
        if self.has_constelacion:
            points += 1
        if self.has_ego_section:
            points += 1
        if self.has_inconsciente_section:
            points += 1
        if self.has_subconsciente_section:
            points += 1
        if self.has_superego_section:
            points += 1
        if self.has_sano_insano_variants:
            points += 1
        if self.has_transiciones:
            points += 1
        if self.has_proposito:
            points += 1
        if self.has_quotes:
            points += 0.5
        # Longitud mínima
        if self.word_count >= 1500:
            points += 0.5
        return points


def load_reference_narradores() -> List[Tuple[str, str]]:
    """Carga todos los narradores simples de referencia"""
    narradores = []
    for f in REFERENCE_DIR.glob("*.md"):
        # Solo archivos que no son personajes completos
        if "Personaje Completo" not in f.name and f.is_file():
            content = f.read_text(encoding='utf-8')
            narradores.append((f.name, content))
    return narradores


def load_reference_personajes() -> List[Tuple[str, str]]:
    """Carga los personajes completos de referencia"""
    personajes = []
    for subdir in REFERENCE_DIR.iterdir():
        if subdir.is_dir():
            for f in subdir.glob("Personaje Completo*.md"):
                content = f.read_text(encoding='utf-8')
                personajes.append((f.name, content))
    return personajes


def analyze_narrador(text: str) -> NarradorMetrics:
    """Analiza un texto de narrador y extrae métricas"""
    words = text.split()
    
    return NarradorMetrics(
        word_count=len(words),
        char_count=len(text),
        starts_correctly=text.strip().startswith("Debe ser un narrador como"),
        has_cultural_reference=bool(re.search(
            r'(?:como|igual que|similar a|recuerda a|estilo de|tipo de)\s+[A-Z][a-záéíóú]+',
            text, re.IGNORECASE
        )) or bool(re.search(r'(Tony Stark|Tesla|House|Joker|villano|líder|general|científico|profesor)', text, re.IGNORECASE)),
        has_paradox_structure=bool(re.search(
            r'(pero|sin embargo|aunque|mientras que|por fuera.*por dentro|muestra.*oculta|parece.*pero)',
            text, re.IGNORECASE
        )),
        has_observable_behavior=bool(re.search(
            r'(observar|notar|ver|detectar|pequeños detalles|gestos|forma en que|cuando|se nota)',
            text, re.IGNORECASE
        )),
        has_mask_break=bool(re.search(
            r'(rompe la máscara|se esconde|detrás de|oculta|solo.*si|solo lo notas|solo lo detectas)',
            text, re.IGNORECASE
        )),
        has_power_form=bool(re.search(
            r'(ejerce|influencia|poder|domina|controla|manipula|seduce|atrae|lidera)',
            text, re.IGNORECASE
        )),
        has_potent_ending=bool(re.search(
            r'[.!]$', text.strip()
        ))
    )


def analyze_personaje_completo(text: str) -> PersonajeCompletoMetrics:
    """Analiza un documento de personaje completo"""
    text_lower = text.lower()
    
    return PersonajeCompletoMetrics(
        has_intro=bool(re.search(r'^#\s+\w+.*análisis|integral|definición', text, re.IGNORECASE | re.MULTILINE)),
        has_constelacion=bool(re.search(r'constelación\s+interna', text_lower)),
        has_ego_section=bool(re.search(r'##.*ego', text_lower)),
        has_inconsciente_section=bool(re.search(r'(##.*inconsciente|inconsciente.*sano|inconsciente.*insano)', text_lower)),
        has_subconsciente_section=bool(re.search(r'(##.*subconsciente|subconsciente.*sano|subconsciente.*insano)', text_lower)),
        has_superego_section=bool(re.search(r'(##.*super.?ego|superego.*sano|superego.*insano)', text_lower)),
        has_sano_insano_variants="sano" in text_lower and "insano" in text_lower,
        has_transiciones=bool(re.search(r'transicion', text_lower)),
        has_proposito=bool(re.search(r'propósito|proposito', text_lower)),
        has_quotes=bool(re.search(r'["""].*debe ser un narrador.*["""]', text_lower)) or text.count('"') >= 4,
        word_count=len(text.split())
    )


class TestReferenceNarradores:
    """Tests que analizan los narradores de referencia para establecer baseline"""
    
    @pytest.fixture
    def reference_narradores(self):
        return load_reference_narradores()
    
    def test_reference_structure(self, reference_narradores):
        """Verifica que los narradores de referencia tengan la estructura esperada"""
        scores = []
        for name, content in reference_narradores[:20]:  # Sample de 20
            metrics = analyze_narrador(content)
            scores.append(metrics.score)
            
        avg_score = sum(scores) / len(scores) if scores else 0
        print(f"\n📊 Score promedio de referencia: {avg_score:.2f}/10")
        print(f"   Rango: {min(scores):.2f} - {max(scores):.2f}")
        
        # Los de referencia deberían tener score alto
        assert avg_score >= 6.0, f"El score promedio de referencia ({avg_score}) es muy bajo"
    
    def test_reference_word_count_distribution(self, reference_narradores):
        """Analiza la distribución de longitudes en los de referencia"""
        word_counts = []
        for name, content in reference_narradores:
            words = len(content.split())
            word_counts.append(words)
        
        avg_words = sum(word_counts) / len(word_counts) if word_counts else 0
        print(f"\n📊 Palabras promedio en referencia: {avg_words:.0f}")
        print(f"   Rango: {min(word_counts)} - {max(word_counts)}")
        
        # Los de referencia típicamente tienen 100-250 palabras
        assert 80 <= avg_words <= 350


class TestReferencePersonajes:
    """Tests que analizan los personajes completos de referencia"""
    
    @pytest.fixture
    def reference_personajes(self):
        return load_reference_personajes()
    
    def test_reference_completitud(self, reference_personajes):
        """Verifica la estructura de los personajes de referencia"""
        scores = []
        for name, content in reference_personajes:
            metrics = analyze_personaje_completo(content)
            scores.append(metrics.score)
            print(f"\n  {name}: {metrics.score:.1f}/10 ({metrics.word_count} palabras)")
        
        if scores:
            avg_score = sum(scores) / len(scores)
            print(f"\n📊 Score promedio de personajes: {avg_score:.2f}/10")
            assert avg_score >= 7.0


class TestGeneratedNarradores:
    """Tests para los outputs de narrador.py"""
    
    def test_generated_ego_format(self):
        """Verifica que el EGO generado tenga formato correcto"""
        ego_file = OUTPUT_DIR / "ENTJ_8w7_sx-so_hombre" / "01_EGO.md"
        if not ego_file.exists():
            pytest.skip("No hay output generado")
        
        content = ego_file.read_text(encoding='utf-8')
        
        # Extraer solo la descripción
        if "## Descripción" in content:
            desc = content.split("## Descripción")[1].strip()
        else:
            desc = content
        
        metrics = analyze_narrador(desc)
        
        print(f"\n📊 Métricas del EGO generado:")
        print(f"   Palabras: {metrics.word_count}")
        print(f"   Empieza correcto: {metrics.starts_correctly}")
        print(f"   Ref cultural: {metrics.has_cultural_reference}")
        print(f"   Paradoja: {metrics.has_paradox_structure}")
        print(f"   Score: {metrics.score:.2f}/10")
        
        assert metrics.starts_correctly, "Debe empezar con 'Debe ser un narrador como'"
        assert metrics.word_count >= 80, f"Muy corto: {metrics.word_count} palabras"
        assert metrics.score >= 5.0, f"Score muy bajo: {metrics.score}"
    
    def test_all_7_variants_exist(self):
        """Verifica que se generen las 7 variantes"""
        output_folder = OUTPUT_DIR / "ENTJ_8w7_sx-so_hombre"
        if not output_folder.exists():
            pytest.skip("No hay output generado")
        
        expected = [
            "01_EGO.md",
            "02_SUBCONSCIENTE_SANO.md",
            "03_SUBCONSCIENTE_INSANO.md",
            "04_INCONSCIENTE_SANO.md",
            "05_INCONSCIENTE_INSANO.md",
            "06_SUPEREGO_SANO.md",
            "07_SUPEREGO_INSANO.md"
        ]
        
        for filename in expected:
            filepath = output_folder / filename
            assert filepath.exists(), f"Falta: {filename}"
    
    def test_all_variants_quality(self):
        """Verifica la calidad de todas las variantes"""
        output_folder = OUTPUT_DIR / "ENTJ_8w7_sx-so_hombre"
        if not output_folder.exists():
            pytest.skip("No hay output generado")
        
        variants = list(output_folder.glob("0*.md"))
        scores = []
        
        for variant in sorted(variants):
            if variant.name.startswith("00_"):
                continue
            content = variant.read_text(encoding='utf-8')
            if "## Descripción" in content:
                desc = content.split("## Descripción")[1].strip()
            else:
                desc = content
            
            metrics = analyze_narrador(desc)
            scores.append((variant.name, metrics.score))
            
        print(f"\n📊 Scores por variante:")
        for name, score in scores:
            status = "✓" if score >= 5.0 else "✗"
            print(f"   {status} {name}: {score:.2f}/10")
        
        avg = sum(s for _, s in scores) / len(scores) if scores else 0
        print(f"\n   Promedio: {avg:.2f}/10")
        
        assert avg >= 4.5, f"Score promedio muy bajo: {avg}"


class TestGeneratedPersonajeCompleto:
    """Tests para los outputs de crear_personaje.py"""
    
    def test_personaje_completo_structure(self):
        """Verifica la estructura del personaje completo generado"""
        output_folder = OUTPUT_DIR / "ENTJ_8w7_sx-so_hombre"
        personaje_file = list(output_folder.glob("*definicion_completa.md"))
        
        if not personaje_file:
            pytest.skip("No hay personaje completo generado")
        
        content = personaje_file[0].read_text(encoding='utf-8')
        metrics = analyze_personaje_completo(content)
        
        print(f"\n📊 Métricas del personaje completo:")
        print(f"   Intro: {metrics.has_intro}")
        print(f"   Constelación: {metrics.has_constelacion}")
        print(f"   Ego: {metrics.has_ego_section}")
        print(f"   Inconsciente: {metrics.has_inconsciente_section}")
        print(f"   Subconsciente: {metrics.has_subconsciente_section}")
        print(f"   Super-ego: {metrics.has_superego_section}")
        print(f"   Sano/Insano: {metrics.has_sano_insano_variants}")
        print(f"   Transiciones: {metrics.has_transiciones}")
        print(f"   Propósito: {metrics.has_proposito}")
        print(f"   Citas: {metrics.has_quotes}")
        print(f"   Palabras: {metrics.word_count}")
        print(f"   Score: {metrics.score:.2f}/10")
        
        assert metrics.score >= 6.0, f"Score muy bajo: {metrics.score}"
        assert metrics.word_count >= 800, f"Muy corto: {metrics.word_count} palabras"


class TestSimilarityToReference:
    """Compara outputs generados con ejemplos de referencia"""
    
    def test_narrador_similarity_to_reference(self):
        """Compara un narrador generado con su equivalente de referencia"""
        # Output generado
        ego_file = OUTPUT_DIR / "ENTJ_8w7_sx-so_hombre" / "01_EGO.md"
        if not ego_file.exists():
            pytest.skip("No hay output generado")
        
        generated = ego_file.read_text(encoding='utf-8')
        if "## Descripción" in generated:
            generated_desc = generated.split("## Descripción")[1].strip()
        else:
            generated_desc = generated
        
        # Referencia
        ref_file = REFERENCE_DIR / "ENTJ 8w7 sx-so H.md"
        if not ref_file.exists():
            pytest.skip("No hay archivo de referencia")
        
        reference = ref_file.read_text(encoding='utf-8')
        
        gen_metrics = analyze_narrador(generated_desc)
        ref_metrics = analyze_narrador(reference)
        
        print(f"\n📊 Comparación Generado vs Referencia:")
        print(f"   {'':20} {'Generado':>12} {'Referencia':>12}")
        print(f"   {'Palabras':20} {gen_metrics.word_count:>12} {ref_metrics.word_count:>12}")
        print(f"   {'Empieza correcto':20} {str(gen_metrics.starts_correctly):>12} {str(ref_metrics.starts_correctly):>12}")
        print(f"   {'Ref cultural':20} {str(gen_metrics.has_cultural_reference):>12} {str(ref_metrics.has_cultural_reference):>12}")
        print(f"   {'Paradoja':20} {str(gen_metrics.has_paradox_structure):>12} {str(ref_metrics.has_paradox_structure):>12}")
        print(f"   {'Score':20} {gen_metrics.score:>12.2f} {ref_metrics.score:>12.2f}")
        
        # El generado debe tener al menos 70% del score de referencia
        ratio = gen_metrics.score / ref_metrics.score if ref_metrics.score > 0 else 0
        print(f"\n   Ratio: {ratio:.2%}")
        
        assert ratio >= 0.6, f"El generado tiene solo {ratio:.0%} del score de referencia"
    
    def test_personaje_similarity_to_reference(self):
        """Compara personaje completo generado con referencia"""
        output_folder = OUTPUT_DIR / "ENTJ_8w7_sx-so_hombre"
        gen_files = list(output_folder.glob("*definicion_completa.md"))
        
        if not gen_files:
            pytest.skip("No hay personaje generado")
        
        generated = gen_files[0].read_text(encoding='utf-8')
        
        # Buscar un personaje de referencia similar
        ref_file = REFERENCE_DIR / "José" / "Personaje Completo José.md"
        if not ref_file.exists():
            pytest.skip("No hay archivo de referencia")
        
        reference = ref_file.read_text(encoding='utf-8')
        
        gen_metrics = analyze_personaje_completo(generated)
        ref_metrics = analyze_personaje_completo(reference)
        
        print(f"\n📊 Comparación Personaje Completo:")
        print(f"   {'':20} {'Generado':>12} {'Referencia':>12}")
        print(f"   {'Palabras':20} {gen_metrics.word_count:>12} {ref_metrics.word_count:>12}")
        print(f"   {'Score':20} {gen_metrics.score:>12.2f} {ref_metrics.score:>12.2f}")
        
        ratio = gen_metrics.score / ref_metrics.score if ref_metrics.score > 0 else 0
        print(f"\n   Ratio: {ratio:.2%}")
        
        assert ratio >= 0.5, f"El generado tiene solo {ratio:.0%} de la completitud de referencia"


# Ejecutar con estadísticas
if __name__ == "__main__":
    print("=" * 60)
    print("🧪 Análisis de Calidad de Outputs")
    print("=" * 60)
    
    # Analizar referencias
    print("\n📚 NARRADORES DE REFERENCIA")
    narradores = load_reference_narradores()
    print(f"   Encontrados: {len(narradores)}")
    
    if narradores:
        scores = [analyze_narrador(c).score for _, c in narradores]
        print(f"   Score promedio: {sum(scores)/len(scores):.2f}/10")
        print(f"   Rango: {min(scores):.2f} - {max(scores):.2f}")
    
    print("\n📚 PERSONAJES DE REFERENCIA")
    personajes = load_reference_personajes()
    print(f"   Encontrados: {len(personajes)}")
    
    if personajes:
        scores = [analyze_personaje_completo(c).score for _, c in personajes]
        print(f"   Score promedio: {sum(scores)/len(scores):.2f}/10")
    
    print("\n📦 OUTPUTS GENERADOS")
    if OUTPUT_DIR.exists():
        outputs = list(OUTPUT_DIR.iterdir())
        print(f"   Carpetas: {len(outputs)}")
        for out in outputs:
            variants = list(out.glob("0*.md"))
            personaje = list(out.glob("*definicion*.md"))
            print(f"   - {out.name}: {len(variants)} variantes, {len(personaje)} personaje completo")
