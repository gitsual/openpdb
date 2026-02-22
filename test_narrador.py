#!/usr/bin/env python3
"""
Tests unitarios para narrador.py
Ejecutar: pytest test_narrador.py -v
"""

import pytest
import json
import subprocess
from unittest.mock import patch, MagicMock

# Importar funciones del módulo
from narrador import parse_typology, build_prompt, call_ollama, DEFAULT_MODEL


class TestParseTypology:
    """Tests para la función parse_typology"""
    
    def test_perfil_completo(self):
        """Parsea perfil completo con todos los componentes"""
        result = parse_typology("ENTJ 6w7 sx/so 368 hombre")
        
        assert result['mbti'] == 'ENTJ'
        assert result['enneagram'] == '6'
        assert result['wing'] == '7'
        assert result['instincts'] == 'sx/so'
        assert result['tritype'] == '368'
        assert result['gender'] == 'hombre'
    
    def test_perfil_minusulas(self):
        """Convierte a mayúsculas automáticamente"""
        result = parse_typology("infp 4w5 sp/sx mujer")
        
        assert result['mbti'] == 'INFP'
        assert result['enneagram'] == '4'
        assert result['wing'] == '5'
        assert result['instincts'] == 'sp/sx'
        assert result['gender'] == 'mujer'
    
    def test_solo_mbti(self):
        """Parsea solo MBTI"""
        result = parse_typology("ENTP")
        
        assert result['mbti'] == 'ENTP'
        assert result['enneagram'] is None
        assert result['wing'] is None
        assert result['instincts'] is None
        assert result['tritype'] is None
        assert result['gender'] is None
    
    def test_solo_eneagrama(self):
        """Parsea solo eneagrama con ala"""
        result = parse_typology("8w7")
        
        assert result['mbti'] is None
        assert result['enneagram'] == '8'
        assert result['wing'] == '7'
    
    def test_instintos_con_guion(self):
        """Acepta instintos con guión en lugar de barra"""
        result = parse_typology("INTJ so-sp")
        
        assert result['mbti'] == 'INTJ'
        assert result['instincts'] == 'so/sp'
    
    def test_orden_aleatorio(self):
        """Parsea correctamente sin importar el orden"""
        result = parse_typology("mujer 459 sp/sx INFP 4w5")
        
        assert result['mbti'] == 'INFP'
        assert result['enneagram'] == '4'
        assert result['wing'] == '5'
        assert result['instincts'] == 'sp/sx'
        assert result['tritype'] == '459'
        assert result['gender'] == 'mujer'
    
    def test_genero_masculino_variantes(self):
        """Reconoce variantes de género masculino"""
        for term in ['hombre', 'masculino', 'male', 'HOMBRE', 'Male']:
            result = parse_typology(f"ENTJ {term}")
            assert result['gender'] == 'hombre', f"Falló con '{term}'"
    
    def test_genero_femenino_variantes(self):
        """Reconoce variantes de género femenino"""
        for term in ['mujer', 'femenino', 'female', 'MUJER', 'Female']:
            result = parse_typology(f"ENTJ {term}")
            assert result['gender'] == 'mujer', f"Falló con '{term}'"
    
    def test_input_vacio(self):
        """Maneja input vacío"""
        result = parse_typology("")
        
        assert result['mbti'] is None
        assert result['enneagram'] is None
        assert result['raw'] == ''
    
    def test_input_invalido(self):
        """Maneja input que no matchea nada"""
        result = parse_typology("esto no es tipología")
        
        assert result['mbti'] is None
        assert result['enneagram'] is None
        assert result['raw'] == 'ESTO NO ES TIPOLOGÍA'
    
    def test_todos_los_mbti(self):
        """Reconoce los 16 tipos MBTI"""
        tipos = [
            'INTJ', 'INTP', 'ENTJ', 'ENTP',
            'INFJ', 'INFP', 'ENFJ', 'ENFP',
            'ISTJ', 'ISFJ', 'ESTJ', 'ESFJ',
            'ISTP', 'ISFP', 'ESTP', 'ESFP'
        ]
        for tipo in tipos:
            result = parse_typology(tipo)
            assert result['mbti'] == tipo, f"Falló con '{tipo}'"
    
    def test_todos_los_eneagramas(self):
        """Reconoce eneagramas del 1 al 9"""
        for i in range(1, 10):
            result = parse_typology(f"{i}w{(i % 9) + 1}")
            assert result['enneagram'] == str(i), f"Falló con tipo {i}"
    
    def test_todas_las_combinaciones_instintos(self):
        """Reconoce todas las combinaciones de instintos"""
        combinaciones = ['sp/sx', 'sp/so', 'sx/sp', 'sx/so', 'so/sp', 'so/sx']
        for combo in combinaciones:
            result = parse_typology(combo.upper())
            assert result['instincts'] == combo, f"Falló con '{combo}'"
    
    def test_tritipo_valido(self):
        """Reconoce tritipos válidos (3 dígitos 1-9)"""
        tritipos = ['369', '458', '279', '136', '825']
        for tri in tritipos:
            result = parse_typology(tri)
            assert result['tritype'] == tri, f"Falló con '{tri}'"
    
    def test_tritipo_no_confunde_con_año(self):
        """No confunde números de 4+ dígitos con tritipo"""
        result = parse_typology("ENTJ 1985")
        assert result['tritype'] is None  # 1985 tiene 4 dígitos
    
    def test_raw_siempre_presente(self):
        """El campo raw siempre contiene el input original (en mayúsculas)"""
        result = parse_typology("ENTJ 8w7 sx/so")
        assert result['raw'] == 'ENTJ 8W7 SX/SO'


class TestBuildPrompt:
    """Tests para la función build_prompt"""
    
    def test_prompt_completo(self):
        """Construye prompt con todos los campos"""
        typology = {
            'mbti': 'ENTJ',
            'enneagram': '8',
            'wing': '7',
            'instincts': 'sx/so',
            'tritype': '836',
            'gender': 'hombre',
            'raw': 'ENTJ 8W7 SX/SO 836 HOMBRE'
        }
        
        prompt = build_prompt(typology)
        
        assert 'MBTI: ENTJ' in prompt
        assert 'Eneagrama: 8w7' in prompt
        assert 'Instintos: sx/so' in prompt
        assert 'Tritipo: 836' in prompt
        assert 'Género: hombre' in prompt
        assert 'Debe ser un narrador como...' in prompt
    
    def test_prompt_parcial(self):
        """Construye prompt con campos parciales"""
        typology = {
            'mbti': 'INFP',
            'enneagram': '4',
            'wing': '5',
            'instincts': None,
            'tritype': None,
            'gender': None,
            'raw': 'INFP 4W5'
        }
        
        prompt = build_prompt(typology)
        
        assert 'MBTI: INFP' in prompt
        assert 'Eneagrama: 4w5' in prompt
        assert 'Instintos' not in prompt
        assert 'Tritipo' not in prompt
        assert 'Género' not in prompt
    
    def test_prompt_vacio_usa_raw(self):
        """Si no hay campos parseados, usa el raw"""
        typology = {
            'mbti': None,
            'enneagram': None,
            'wing': None,
            'instincts': None,
            'tritype': None,
            'gender': None,
            'raw': 'ALGO RARO'
        }
        
        prompt = build_prompt(typology)
        
        assert 'ALGO RARO' in prompt
    
    def test_prompt_contiene_instrucciones(self):
        """El prompt contiene las instrucciones necesarias"""
        typology = parse_typology("ENTJ")
        prompt = build_prompt(typology)
        
        assert 'párrafo' in prompt.lower()
        assert 'narrador' in prompt.lower()


class TestCallOllama:
    """Tests para la función call_ollama (con mocks)"""
    
    @patch('narrador.subprocess.run')
    def test_llamada_exitosa(self, mock_run):
        """Procesa respuesta exitosa de Ollama"""
        mock_response = {
            'message': {
                'role': 'assistant',
                'content': 'Debe ser un narrador como un líder visionario...'
            }
        }
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout=json.dumps(mock_response),
            stderr=''
        )
        
        result = call_ollama("test prompt", "test-model")
        
        assert 'Debe ser un narrador' in result
        mock_run.assert_called_once()
    
    @patch('narrador.subprocess.run')
    def test_respuesta_vacia(self, mock_run):
        """Maneja respuesta vacía"""
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout='',
            stderr=''
        )
        
        result = call_ollama("test prompt")
        
        assert 'Error' in result or 'vacía' in result.lower()
    
    @patch('narrador.subprocess.run')
    def test_error_curl(self, mock_run):
        """Maneja error de curl"""
        mock_run.return_value = MagicMock(
            returncode=1,
            stdout='',
            stderr='Connection refused'
        )
        
        result = call_ollama("test prompt")
        
        assert 'Error' in result
    
    @patch('narrador.subprocess.run')
    def test_timeout(self, mock_run):
        """Maneja timeout"""
        mock_run.side_effect = subprocess.TimeoutExpired(cmd='curl', timeout=120)
        
        result = call_ollama("test prompt")
        
        assert 'Timeout' in result
    
    @patch('narrador.subprocess.run')
    def test_json_invalido(self, mock_run):
        """Maneja JSON inválido en respuesta"""
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout='esto no es json',
            stderr=''
        )
        
        result = call_ollama("test prompt")
        
        assert 'Error' in result
    
    @patch('narrador.subprocess.run')
    def test_contenido_en_thinking(self, mock_run):
        """Extrae contenido de thinking si content está vacío (gpt-oss)"""
        mock_response = {
            'message': {
                'role': 'assistant',
                'content': '',
                'thinking': 'Analizando... Debe ser un narrador como un líder audaz...'
            }
        }
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout=json.dumps(mock_response),
            stderr=''
        )
        
        result = call_ollama("test prompt")
        
        assert 'Debe ser un narrador' in result
    
    @patch('narrador.subprocess.run')
    def test_thinking_sin_debe_ser(self, mock_run):
        """Usa thinking completo si no contiene 'Debe ser'"""
        mock_response = {
            'message': {
                'role': 'assistant',
                'content': '',
                'thinking': 'Este narrador es un visionario rebelde...'
            }
        }
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout=json.dumps(mock_response),
            stderr=''
        )
        
        result = call_ollama("test prompt")
        
        assert 'visionario rebelde' in result
    
    @patch('narrador.subprocess.run')
    def test_payload_correcto(self, mock_run):
        """Verifica que el payload enviado es correcto"""
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout='{"message":{"content":"test"}}',
            stderr=''
        )
        
        call_ollama("mi prompt", "mi-modelo")
        
        # Extraer el payload del comando
        call_args = mock_run.call_args[0][0]
        payload_str = call_args[-1]  # Último argumento es el -d payload
        payload = json.loads(payload_str)
        
        assert payload['model'] == 'mi-modelo'
        assert payload['stream'] == False
        assert len(payload['messages']) == 2
        assert payload['messages'][0]['role'] == 'system'
        assert payload['messages'][1]['role'] == 'user'
        assert 'mi prompt' in payload['messages'][1]['content']


class TestIntegracion:
    """Tests de integración (requieren Ollama corriendo)"""
    
    @pytest.fixture
    def ollama_available(self):
        """Verifica si Ollama está disponible"""
        try:
            result = subprocess.run(
                ['curl', '-s', 'http://localhost:11434/api/tags'],
                capture_output=True,
                timeout=5
            )
            return result.returncode == 0 and result.stdout
        except:
            return False
    
    @pytest.mark.skipif(
        not subprocess.run(
            ['curl', '-s', 'http://localhost:11434/api/tags'],
            capture_output=True
        ).returncode == 0,
        reason="Ollama no está corriendo"
    )
    def test_generacion_real(self):
        """Test de integración real con Ollama (skip si no disponible)"""
        typology = parse_typology("ENTP 7w8 sx/so")
        prompt = build_prompt(typology)
        
        # Usar modelo pequeño para test rápido
        result = call_ollama(prompt, "qwen2.5:14b")
        
        # Verificar que devolvió algo razonable
        assert len(result) > 50
        assert 'Error' not in result or 'narrador' in result.lower()


class TestCasosEspeciales:
    """Tests para casos edge y especiales"""
    
    def test_espacios_extra(self):
        """Maneja espacios extra en el input"""
        result = parse_typology("  ENTJ   8w7   sx/so  ")
        
        assert result['mbti'] == 'ENTJ'
        assert result['enneagram'] == '8'
    
    def test_caracteres_especiales(self):
        """Maneja caracteres especiales"""
        result = parse_typology("ENTJ (8w7) [sx/so]")
        
        assert result['mbti'] == 'ENTJ'
        assert result['enneagram'] == '8'
        assert result['instincts'] == 'sx/so'
    
    def test_texto_mixto(self):
        """Extrae tipología de texto con otras palabras"""
        result = parse_typology("Quiero un ENTJ tipo 8w7 con instintos sx/so")
        
        assert result['mbti'] == 'ENTJ'
        assert result['enneagram'] == '8'
        assert result['instincts'] == 'sx/so'
    
    def test_eneagrama_sin_ala(self):
        """Solo número de eneagrama sin ala"""
        result = parse_typology("ENTJ tipo 8")
        
        assert result['mbti'] == 'ENTJ'
        # Sin el formato XwY, no debería capturar eneagrama
        assert result['enneagram'] is None
    
    def test_mbti_invalido_no_captura(self):
        """No captura MBTI inválidos"""
        # ABCD no es MBTI válido
        result = parse_typology("ABCD 8w7")
        
        assert result['mbti'] is None
        assert result['enneagram'] == '8'


class TestRegresion:
    """Tests de regresión para bugs encontrados"""
    
    def test_ejemplo_original(self):
        """El ejemplo del usuario original funciona"""
        result = parse_typology("ENTJ 6w7 sx/so 368 hombre")
        
        assert result['mbti'] == 'ENTJ'
        assert result['enneagram'] == '6'
        assert result['wing'] == '7'
        assert result['instincts'] == 'sx/so'
        assert result['tritype'] == '368'
        assert result['gender'] == 'hombre'
    
    def test_build_prompt_no_crashea_con_nones(self):
        """build_prompt no crashea con todos los campos None"""
        typology = {
            'mbti': None,
            'enneagram': None,
            'wing': None,
            'instincts': None,
            'tritype': None,
            'gender': None,
            'raw': ''
        }
        
        # No debe lanzar excepción
        prompt = build_prompt(typology)
        assert isinstance(prompt, str)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
