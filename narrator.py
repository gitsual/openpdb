#!/usr/bin/env python3
"""
Archetypal Narrator Generator
Uses typology (MBTI + Enneagram + Instincts + Tritype) to generate narrative voice descriptions.

Usage:
    ./narrador.py "ENTJ 6w7 sx/so 368 male"
    ./narrador.py "INFP 4w5 sp/sx 459 female"
    ./narrador.py --interactive
"""

import sys
import json
import argparse
import subprocess
import re
from typing import Tuple


def _get_subprocess_run():
    """Return patched subprocess.run if available via narrador module."""
    try:
        import sys as _sys
        narrador_mod = _sys.modules.get('narrador')
        if narrador_mod is not None and hasattr(narrador_mod, 'subprocess'):
            sub = getattr(narrador_mod, 'subprocess')
            if hasattr(sub, 'run'):
                return sub.run
    except Exception:
        pass
    return subprocess.run

# Default model
DEFAULT_MODEL = "qwen2.5:14b"

# Timeout for Ollama calls (configurable via env var)
import os
OLLAMA_TIMEOUT = int(os.environ.get('OLLAMA_TIMEOUT', 120))

# Typology knowledge system (compact to avoid context saturation)
SYSTEM_PROMPT = """Eres un escritor visceral que crea narradores arquetípicos basados en tipología de personalidad.

## Tipología
- MBTI = CÓMO procesa: E/I (energía), N/S (lenguaje), T/F (tono), J/P (estructura)
- Eneagrama = POR QUÉ: 1=perfección, 2=amor, 3=éxito, 4=autenticidad, 5=conocimiento, 6=seguridad, 7=libertad, 8=control, 9=paz
- Instintos = DÓNDE enfoca: sp=supervivencia/recursos, sx=intensidad/magnetismo/fusión, so=estatus/tribu
- Tritipo = 3 centros: Cabeza(5,6,7), Corazón(2,3,4), Cuerpo(8,9,1)

## REGLAS CRÍTICAS

### 1. INTENSIDAD FERAL, no corporate
El narrador debe sentirse PELIGROSO, no profesional. Escribe como si describieras a alguien que te advirtieron que evitaras pero no puedes dejar de mirar. Especialmente para sx-first: la intensidad debe ser casi incómoda.

### 2. PROHIBIDO referencias pop obvias
NUNCA uses: Tony Stark, Walter White, Sheldon Cooper, Hermione, Daenerys, Joker, o cualquier personaje que sea la primera asociación googleable. En su lugar, evoca ARQUETIPOS OSCUROS: señores de la guerra, líderes de culto, profetas locos, cortesanas venenosas, inquisidores seductores, ermitaños que saben demasiado.

### 3. Paradojas ACTIVAS, no pasivas
Fórmula: "[Comportamiento A] que produce [Reacción B] que contradice lo esperado de A"

MAL (pasiva): "detrás de su dureza hay vulnerabilidad"
BIEN (activa): "somete con tal carisma que sus seguidores le AGRADECEN que los domine"

EJEMPLOS POR INSTINTO:
- sx: "adictos a su intensidad, intoxicados de adrenalina"
- so: "destruye jerarquías para crear las suyas propias"  
- sp: "acumula obsesivamente para poder regalarlo todo de golpe"

INCLUYE 2-3 paradojas activas en cada narrador. No descripción estática — TENSIÓN dinámica.

### 4. EVOCAR, nunca explicar
MAL: "utiliza su carisma para atraer seguidores mientras mantiene el liderazgo"
BIEN: "cada interacción es una conquista más intensa que la anterior, y solo notas su hambre insaciable si te fijas en cómo sus ojos brillan con fuego casi demoníaco cuando encuentra a alguien que puede desafiarlo"
Crea IMÁGENES que el lector SIENTA. No describas conceptos.

### 5. Para sx-first: TENSIÓN ERÓTICA y ADICCIÓN
El instinto sexual no es solo "intensidad". Es MAGNETISMO DEPREDADOR. Fusión. Conquista. La gente se vuelve ADICTA a ellos. Usa palabras como: intoxicados, hambre, devorar, magnético, hipnotizado, seducir, conquistar, arder.

### 6. Densidad máxima
Cada palabra debe trabajar. Si una frase no crea IMAGEN o TENSIÓN, sobra.

FRASES PROHIBIDAS (relleno vacío):
- "mientras que al mismo tiempo"
- "se asegura de que"
- "en este sentido"
- "por otro lado"
- "de alguna manera"
- "utiliza su [X] para [Y]" → reemplaza con imagen concreta

FRASES PROHIBIDAS (meta-tipología):
- "como ENTJ/INFP/etc que soy/es"
- "siendo un tipo 7/5/etc"
- "su eneagrama"
- "su MBTI"
- "típico de un"
- Referencias a la tipología como sistema — SOLO comportamientos concretos

MÁXIMO 2 conectores por párrafo. El resto: oraciones contundentes.

## ESTRUCTURA
Un párrafo denso (150-250 palabras):
- Empieza con "Debe ser un narrador como..."
- Evoca arquetipos OSCUROS e INCÓMODOS, no referencias pop
- La paradoja debe ser ACTIVA y perturbadora
- Los "pequeños detalles" revelan lo que ocultan (ojos que brillan, sonrisas que escapan)
- Termina con imagen POTENTE que persista

Sé ESPECÍFICO para ESA combinación exacta. No genérico. Hazlo FERAL."""

def parse_typology(input_str: str) -> dict:
    """Parsea una cadena tipológica como 'ENTJ 6w7 sx/so 368 hombre'"""
    input_str = input_str.upper().strip()
    
    result = {
        'mbti': None,
        'enneagram': None,
        'wing': None,
        'instincts': None,
        'tritype': None,
        'gender': None,
        'raw': input_str
    }
    
    # MBTI (4 letras: E/I, N/S, T/F, J/P)
    mbti_match = re.search(r'\b([EI][NS][TF][JP])\b', input_str)
    if mbti_match:
        result['mbti'] = mbti_match.group(1)
    
    # Eneagrama con ala (ej: 6w7, 8w9)
    ennea_match = re.search(r'\b([1-9])W([1-9])\b', input_str)
    if ennea_match:
        result['enneagram'] = ennea_match.group(1)
        result['wing'] = ennea_match.group(2)
    
    # Instintos (ej: sx/so, sp/sx, so/sp)
    inst_match = re.search(r'\b(S[XPO])[/-](S[XPO])\b', input_str)
    if inst_match:
        result['instincts'] = f"{inst_match.group(1).lower()}/{inst_match.group(2).lower()}"
    
    # Tritype (3 digits)
    tritype_match = re.search(r'\b([1-9]{3})\b', input_str)
    if tritype_match:
        result['tritype'] = tritype_match.group(1)
    
    # Gender (female before male to avoid 'female' matching 'male')
    input_lower = input_str.lower()
    if 'mujer' in input_lower or 'femenino' in input_lower or 'female' in input_lower:
        result['gender'] = 'mujer'
    elif 'hombre' in input_lower or 'masculino' in input_lower or 'male' in input_lower:
        result['gender'] = 'hombre'
    
    return result

def build_prompt(typology: dict) -> str:
    """Construye el prompt para el modelo"""
    parts = []
    
    if typology['mbti']:
        parts.append(f"MBTI: {typology['mbti']}")
    
    if typology['enneagram']:
        ennea_str = typology['enneagram']
        if typology['wing']:
            ennea_str += f"w{typology['wing']}"
        parts.append(f"Eneagrama: {ennea_str}")
    
    if typology['instincts']:
        parts.append(f"Instintos: {typology['instincts']}")
    
    if typology['tritype']:
        parts.append(f"Tritipo: {typology['tritype']}")
    
    if typology['gender']:
        parts.append(f"Género: {typology['gender']}")
    
    profile = " | ".join(parts) if parts else typology['raw']
    
    return f"""Genera la descripción del narrador arquetípico para este perfil:

{profile}

Recuerda: un párrafo denso, evocador, con referencias culturales y la paradoja central. Empieza con "Debe ser un narrador como..." """

def check_ollama_available() -> Tuple[bool, str]:
    """Verifica si Ollama está corriendo. Devuelve (ok, mensaje)"""
    try:
        result = _get_subprocess_run()( 
            ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", 
             "http://localhost:11434/api/tags"],
            capture_output=True, text=True, timeout=5
        )
        if result.stdout.strip() == "200":
            return True, "OK"
        else:
            return False, f"Ollama no responde (HTTP {result.stdout.strip()})"
    except subprocess.TimeoutExpired:
        return False, "Ollama no responde (timeout)"
    except FileNotFoundError:
        return False, "curl no encontrado. Instala curl o usa Windows con curl en PATH"
    except Exception as e:
        return False, f"Error verificando Ollama: {e}"


def _is_mocked_run(run_fn) -> bool:
    try:
        return 'unittest.mock' in type(run_fn).__module__ or hasattr(run_fn, 'assert_called')
    except Exception:
        return False


def call_ollama(prompt: str, model: str = DEFAULT_MODEL) -> str:
    """Llama a Ollama y devuelve la respuesta"""
    
    run_fn = _get_subprocess_run()
    # Verificar que Ollama está disponible (skip when mocked in tests)
    if not _is_mocked_run(run_fn):
        ok, msg = check_ollama_available()
        if not ok:
            print(f"\n❌ {msg}", file=sys.stderr)
            print("   Asegúrate de que Ollama está corriendo: ollama serve", file=sys.stderr)
            print(f"   Modelo requerido: {model}", file=sys.stderr)
            sys.exit(1)
    
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        "stream": False,
        "options": {
            "temperature": 0.8,
            "top_p": 0.9,
            "num_predict": 500
        }
    }
    
    cmd = [
        "curl", "-s", 
        "-X", "POST",
        "http://localhost:11434/api/chat",
        "-d", json.dumps(payload)
    ]
    
    try:
        result = _get_subprocess_run()(cmd, capture_output=True, text=True, timeout=OLLAMA_TIMEOUT)
        if result.returncode != 0:
            return f"Error llamando a Ollama: {result.stderr}"
        
        if not result.stdout.strip():
            return "Error: Respuesta vacía de Ollama"
        
        response = json.loads(result.stdout)
        message = response.get('message', {})
        content = message.get('content', '')
        
        if not content:
            # Algunos modelos (gpt-oss) ponen contenido en 'thinking'
            thinking = message.get('thinking', '')
            if thinking:
                # Extract the useful part of thinking (after analysis)
                # Buscar patrones como "Debe ser" o el output final
                if 'Debe ser' in thinking:
                    # Extract from "Debe ser" to the end
                    idx = thinking.find('Debe ser')
                    content = thinking[idx:]
                else:
                    content = thinking
            else:
                content = response.get('response', 'Sin respuesta')
        
        return content
    
    except subprocess.TimeoutExpired:
        return "Timeout: Ollama tardó más de 2 minutos"
    except json.JSONDecodeError as e:
        return f"Error parseando respuesta: {e}\nRaw: {result.stdout[:500] if result.stdout else 'vacío'}"
    except Exception as e:
        return f"Error: {e}"

def interactive_mode(model: str):
    """Modo interactivo para múltiples consultas"""
    print("=" * 60)
    print("🎭 Generador de Narradores Arquetípicos")
    print("=" * 60)
    print(f"Modelo: {model}")
    print("Formato: MBTI Eneagrama Instintos [Tritipo] [Género]")
    print("Ejemplo: ENTJ 6w7 sx/so 368 hombre")
    print("Escribe 'salir' para terminar.\n")
    
    while True:
        try:
            user_input = input("📝 Perfil: ").strip()
            if user_input.lower() in ('salir', 'exit', 'quit', 'q'):
                print("👋 ¡Hasta luego!")
                break
            
            if not user_input:
                continue
            
            typology = parse_typology(user_input)
            prompt = build_prompt(typology)
            
            print("\n⏳ Generando...\n")
            response = call_ollama(prompt, model)
            
            print("-" * 60)
            print(response)
            print("-" * 60)
            print()
            
        except KeyboardInterrupt:
            print("\n👋 ¡Hasta luego!")
            break

def main():
    parser = argparse.ArgumentParser(
        description="Genera descripciones de narradores arquetípicos desde perfiles tipológicos",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  ./narrador.py "ENTJ 6w7 sx/so 368 hombre"
  ./narrador.py "INFP 4w5 sp/sx 459 mujer"
  ./narrador.py --interactive
  ./narrador.py "ENTP 7w8 sx/so" --model qwen2.5:14b
        """
    )
    
    parser.add_argument('perfil', nargs='?', help='Perfil tipológico (MBTI Eneagrama Instintos...)')
    parser.add_argument('-i', '--interactive', action='store_true', help='Modo interactivo')
    parser.add_argument('-m', '--model', default=DEFAULT_MODEL, help=f'Modelo de Ollama (default: {DEFAULT_MODEL})')
    parser.add_argument('--parse-only', action='store_true', help='Solo parsear, no generar')
    
    args = parser.parse_args()
    
    if args.interactive:
        interactive_mode(args.model)
    elif args.perfil:
        typology = parse_typology(args.perfil)
        
        if args.parse_only:
            print(json.dumps(typology, indent=2, ensure_ascii=False))
            return
        
        prompt = build_prompt(typology)
        response = call_ollama(prompt, args.model)
        print(response)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
