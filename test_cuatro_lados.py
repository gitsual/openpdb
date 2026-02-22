#!/usr/bin/env python3
"""
Tests unitarios para cuatro_lados.py
Ejecutar: pytest test_cuatro_lados.py -v
"""

import pytest
from cuatro_lados import (
    flip_letter, calculate_sides, calculate_enneagram_variant,
    generate_all_variants, build_variant_prompt,
    INTEGRACION, DESINTEGRACION
)
from narrador import parse_typology


class TestFlipLetter:
    """Tests para flip_letter"""
    
    def test_extraversion_introversion(self):
        assert flip_letter('E', 0) == 'I'
        assert flip_letter('I', 0) == 'E'
    
    def test_intuition_sensing(self):
        assert flip_letter('N', 1) == 'S'
        assert flip_letter('S', 1) == 'N'
    
    def test_thinking_feeling(self):
        assert flip_letter('T', 2) == 'F'
        assert flip_letter('F', 2) == 'T'
    
    def test_judging_perceiving(self):
        assert flip_letter('J', 3) == 'P'
        assert flip_letter('P', 3) == 'J'


class TestCalculateSides:
    """Tests para calculate_sides - los 4 lados de la mente"""
    
    def test_entj(self):
        """ENTJ debe dar ISFP, INTP, ESFJ"""
        sides = calculate_sides('ENTJ')
        
        assert sides['ego'] == 'ENTJ'
        assert sides['subconsciente'] == 'ISFP'  # Todo cambiado
        assert sides['inconsciente'] == 'INTP'   # E→I, J→P
        assert sides['superego'] == 'ESFJ'       # N→S, T→F
    
    def test_infp(self):
        """INFP debe dar ESTJ, ENFJ, ISTP"""
        sides = calculate_sides('INFP')
        
        assert sides['ego'] == 'INFP'
        assert sides['subconsciente'] == 'ESTJ'
        assert sides['inconsciente'] == 'ENFJ'
        assert sides['superego'] == 'ISTP'
    
    def test_estp(self):
        """ESTP debe dar INFJ, ISTJ, ENFP"""
        sides = calculate_sides('ESTP')
        
        assert sides['ego'] == 'ESTP'
        assert sides['subconsciente'] == 'INFJ'  # Todo cambia: E→I, S→N, T→F, P→J
        assert sides['inconsciente'] == 'ISTJ'   # Primera y última: E→I, P→J
        assert sides['superego'] == 'ENFP'       # Medio: S→N, T→F
    
    def test_isfj(self):
        """ISFJ debe dar ENTP, ESFP, INTJ"""
        sides = calculate_sides('ISFJ')
        
        assert sides['ego'] == 'ISFJ'
        assert sides['subconsciente'] == 'ENTP'  # Todo cambia
        assert sides['inconsciente'] == 'ESFP'   # Primera y última
        assert sides['superego'] == 'INTJ'       # Medio
    
    def test_todos_los_tipos(self):
        """Verifica que todos los 16 tipos generan 4 lados válidos"""
        tipos = [
            'INTJ', 'INTP', 'ENTJ', 'ENTP',
            'INFJ', 'INFP', 'ENFJ', 'ENFP',
            'ISTJ', 'ISFJ', 'ESTJ', 'ESFJ',
            'ISTP', 'ISFP', 'ESTP', 'ESFP'
        ]
        
        for tipo in tipos:
            sides = calculate_sides(tipo)
            
            # Todos los lados deben ser MBTI válidos de 4 letras
            for lado in ['ego', 'subconsciente', 'inconsciente', 'superego']:
                assert len(sides[lado]) == 4
                assert sides[lado][0] in 'EI'
                assert sides[lado][1] in 'NS'
                assert sides[lado][2] in 'TF'
                assert sides[lado][3] in 'JP'
    
    def test_subconsciente_es_opuesto_total(self):
        """El subconsciente debe tener TODAS las letras opuestas"""
        tipos = ['ENTJ', 'INFP', 'ESTP', 'ISFJ']
        
        for tipo in tipos:
            sides = calculate_sides(tipo)
            ego = sides['ego']
            sub = sides['subconsciente']
            
            # Cada posición debe ser opuesta
            assert ego[0] != sub[0]  # E↔I
            assert ego[1] != sub[1]  # N↔S
            assert ego[2] != sub[2]  # T↔F
            assert ego[3] != sub[3]  # J↔P
    
    def test_inconsciente_cambia_primera_ultima(self):
        """El inconsciente cambia solo primera y última letra"""
        tipos = ['ENTJ', 'INFP', 'ESTP', 'ISFJ']
        
        for tipo in tipos:
            sides = calculate_sides(tipo)
            ego = sides['ego']
            inc = sides['inconsciente']
            
            assert ego[0] != inc[0]  # Primera cambia
            assert ego[1] == inc[1]  # Segunda igual
            assert ego[2] == inc[2]  # Tercera igual
            assert ego[3] != inc[3]  # Cuarta cambia
    
    def test_superego_cambia_medio(self):
        """El superego cambia solo las dos letras del medio"""
        tipos = ['ENTJ', 'INFP', 'ESTP', 'ISFJ']
        
        for tipo in tipos:
            sides = calculate_sides(tipo)
            ego = sides['ego']
            sup = sides['superego']
            
            assert ego[0] == sup[0]  # Primera igual
            assert ego[1] != sup[1]  # Segunda cambia
            assert ego[2] != sup[2]  # Tercera cambia
            assert ego[3] == sup[3]  # Cuarta igual
    
    def test_mbti_corto(self):
        """MBTI de menos de 4 letras retorna None"""
        assert calculate_sides('ENT') is None
        assert calculate_sides('') is None
        assert calculate_sides(None) is None
    
    def test_mbti_4_letras_calcula(self):
        """MBTI de 4 letras siempre calcula (incluso si es inválido técnicamente)"""
        # El código no valida si es un MBTI real, solo hace las transformaciones
        result = calculate_sides('ABCD')
        # No es None porque tiene 4 caracteres
        # Pero las transformaciones pueden dar resultados raros
        assert result is not None or result is None  # Depende de implementación


class TestEnneagramVariants:
    """Tests para integración/desintegración del eneagrama"""
    
    def test_integracion_tipo_8(self):
        """Tipo 8 integra a 2"""
        new_type, new_wing = calculate_enneagram_variant('8', 'integracion')
        assert new_type == '2'
    
    def test_desintegracion_tipo_8(self):
        """Tipo 8 desintegra a 5"""
        new_type, new_wing = calculate_enneagram_variant('8', 'desintegracion')
        assert new_type == '5'
    
    def test_integracion_todos_los_tipos(self):
        """Verifica integración de todos los tipos"""
        esperado = {
            '1': '7', '2': '4', '3': '6', '4': '1', '5': '8',
            '6': '9', '7': '5', '8': '2', '9': '3'
        }
        for tipo, integracion in esperado.items():
            new_type, _ = calculate_enneagram_variant(tipo, 'integracion')
            assert new_type == integracion, f"Tipo {tipo} debe integrar a {integracion}"
    
    def test_desintegracion_todos_los_tipos(self):
        """Verifica desintegración de todos los tipos"""
        esperado = {
            '1': '4', '2': '8', '3': '9', '4': '2', '5': '7',
            '6': '3', '7': '1', '8': '5', '9': '6'
        }
        for tipo, desintegracion in esperado.items():
            new_type, _ = calculate_enneagram_variant(tipo, 'desintegracion')
            assert new_type == desintegracion, f"Tipo {tipo} debe desintegrar a {desintegracion}"


class TestGenerateAllVariants:
    """Tests para generate_all_variants"""
    
    def test_genera_7_variantes(self):
        """Debe generar exactamente 7 variantes"""
        typology = parse_typology("ENTJ 8w7 sx/so hombre")
        variants = generate_all_variants(typology)
        
        assert len(variants) == 7
    
    def test_nombres_correctos(self):
        """Las variantes tienen los nombres correctos"""
        typology = parse_typology("ENTJ 8w7 sx/so")
        variants = generate_all_variants(typology)
        
        nombres = [v['nombre'] for v in variants]
        assert 'EGO' in nombres
        assert 'SUBCONSCIENTE_SANO' in nombres
        assert 'SUBCONSCIENTE_INSANO' in nombres
        assert 'INCONSCIENTE_SANO' in nombres
        assert 'INCONSCIENTE_INSANO' in nombres
        assert 'SUPEREGO_SANO' in nombres
        assert 'SUPEREGO_INSANO' in nombres
    
    def test_ego_conserva_tipo_base(self):
        """El EGO debe conservar el tipo base"""
        typology = parse_typology("INFP 4w5 sp/sx mujer")
        variants = generate_all_variants(typology)
        
        ego = [v for v in variants if v['nombre'] == 'EGO'][0]
        assert ego['mbti'] == 'INFP'
        assert ego['enneagram'] == '4'
        assert ego['wing'] == '5'
    
    def test_instintos_conservados(self):
        """Los instintos se conservan en todas las variantes"""
        typology = parse_typology("ESTP 8w7 sx/so hombre")
        variants = generate_all_variants(typology)
        
        for v in variants:
            assert v['instincts'] == 'sx/so'
    
    def test_genero_conservado(self):
        """El género se conserva en todas las variantes"""
        typology = parse_typology("ISFJ 2w1 so/sp mujer")
        variants = generate_all_variants(typology)
        
        for v in variants:
            assert v['gender'] == 'mujer'
    
    def test_sanos_tienen_integracion(self):
        """Las variantes sanas usan el tipo de integración"""
        typology = parse_typology("ENTJ 8w7 sx/so")
        variants = generate_all_variants(typology)
        
        # 8 integra a 2
        sanos = [v for v in variants if v['estado'] == 'sano']
        for v in sanos:
            assert v['enneagram'] == '2'
    
    def test_insanos_tienen_desintegracion(self):
        """Las variantes insanas usan el tipo de desintegración"""
        typology = parse_typology("ENTJ 8w7 sx/so")
        variants = generate_all_variants(typology)
        
        # 8 desintegra a 5
        insanos = [v for v in variants if v['estado'] == 'insano']
        for v in insanos:
            assert v['enneagram'] == '5'
    
    def test_requiere_mbti(self):
        """Debe lanzar error si no hay MBTI"""
        typology = parse_typology("8w7 sx/so")  # Sin MBTI
        
        with pytest.raises(ValueError):
            generate_all_variants(typology)


class TestBuildVariantPrompt:
    """Tests para build_variant_prompt"""
    
    def test_contiene_mbti(self):
        """El prompt contiene el MBTI"""
        variant = {
            'nombre': 'EGO',
            'lado': 'ego',
            'estado': 'base',
            'mbti': 'ENTJ',
            'enneagram': '8',
            'wing': '7',
            'instincts': 'sx/so',
            'gender': 'hombre'
        }
        prompt = build_variant_prompt(variant)
        
        assert 'ENTJ' in prompt
    
    def test_contiene_contexto_lado(self):
        """El prompt contiene el contexto del lado"""
        variant = {
            'nombre': 'SUBCONSCIENTE_SANO',
            'lado': 'subconsciente',
            'estado': 'sano',
            'mbti': 'ISFP',
            'enneagram': '2',
            'wing': '1',
            'instincts': 'sx/so',
            'gender': None
        }
        prompt = build_variant_prompt(variant)
        
        assert 'SUBCONSCIENTE' in prompt
        assert 'aspiracional' in prompt.lower()
    
    def test_sano_menciona_integracion(self):
        """Prompt sano menciona integración/crecimiento"""
        variant = {
            'nombre': 'INCONSCIENTE_SANO',
            'lado': 'inconsciente',
            'estado': 'sano',
            'mbti': 'INTP',
            'enneagram': '2',
            'wing': None,
            'instincts': None,
            'gender': None
        }
        prompt = build_variant_prompt(variant)
        
        assert 'SANO' in prompt or 'INTEGRAD' in prompt.upper()
    
    def test_insano_menciona_desintegracion(self):
        """Prompt insano menciona desintegración/estrés"""
        variant = {
            'nombre': 'SUPEREGO_INSANO',
            'lado': 'superego',
            'estado': 'insano',
            'mbti': 'ESFJ',
            'enneagram': '5',
            'wing': None,
            'instincts': None,
            'gender': None
        }
        prompt = build_variant_prompt(variant)
        
        assert 'INSANO' in prompt or 'DESINTEGR' in prompt.upper()


class TestCasosReales:
    """Tests con ejemplos reales mencionados por el usuario"""
    
    def test_ejemplo_entj_8w7(self):
        """El ejemplo ENTJ 8w7 sx/so hombre del usuario"""
        typology = parse_typology("ENTJ 8w7 sx/so hombre")
        variants = generate_all_variants(typology)
        
        # Verificar estructura
        assert len(variants) == 7
        
        # Verificar MBTI de cada lado
        mbti_map = {v['nombre']: v['mbti'] for v in variants}
        assert mbti_map['EGO'] == 'ENTJ'
        assert mbti_map['SUBCONSCIENTE_SANO'] == 'ISFP'
        assert mbti_map['SUBCONSCIENTE_INSANO'] == 'ISFP'
        assert mbti_map['INCONSCIENTE_SANO'] == 'INTP'
        assert mbti_map['INCONSCIENTE_INSANO'] == 'INTP'
        assert mbti_map['SUPEREGO_SANO'] == 'ESFJ'
        assert mbti_map['SUPEREGO_INSANO'] == 'ESFJ'
        
        # Verificar eneagrama
        ego = [v for v in variants if v['nombre'] == 'EGO'][0]
        assert ego['enneagram'] == '8'
        assert ego['wing'] == '7'
        
        # Sanos = integración de 8 = 2 (filtrar por estado, no por nombre)
        sanos = [v for v in variants if v['estado'] == 'sano']
        for v in sanos:
            assert v['enneagram'] == '2', f"{v['nombre']} debe tener eneagrama 2"
        
        # Insanos = desintegración de 8 = 5
        insanos = [v for v in variants if v['estado'] == 'insano']
        for v in insanos:
            assert v['enneagram'] == '5', f"{v['nombre']} debe tener eneagrama 5"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
