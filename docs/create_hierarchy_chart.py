#!/usr/bin/env python3
"""
Orgchart Visual - Creador de Personajes
Genera un diagrama jerárquico vertical de la organización.
"""

from graphviz import Digraph
import os

# Jerarquía extraída de OpenGoat
HIERARCHY = {
    'ani': None,  # CEO - raíz
    'chuche': 'ani',
    'rulog': 'ani',
    'goncho': 'ani',
    'abueloluis': 'ani',
    # Bajo CHUCHE (CTO)
    'sanz': 'chuche',
    'cesar': 'chuche',
    'martor': 'chuche',
    'sergio': 'chuche',
    'marco': 'chuche',
    'caba': 'chuche',
    'tony': 'chuche',
    'tony-stark': 'chuche',
    'walter-white': 'chuche',
    'presi': 'caba',
    'hermione-granger': 'sanz',
    # Bajo RULOG (COO)
    'fuego': 'rulog',
    'elvira': 'rulog',
    'tin': 'rulog',
    'coordinador': 'rulog',
    'morga': 'fuego',
    'mosko': 'fuego',
    'ejecutor1': 'fuego',
    'marius': 'elvira',
    'luisgon': 'elvira',
    # Bajo GONCHO (CCO)
    'aranda': 'goncho',
    'klaudia': 'goncho',
    'amira': 'goncho',
    'claurs': 'goncho',
    'wengel': 'goncho',
    'kelly': 'goncho',
    'rodri': 'goncho',
    'tarragona': 'goncho',
    'puma': 'kelly',
    'jose': 'rodri',
    'majano': 'rodri',
    'lorena': 'rodri',
    'luna-lovegood': 'wengel',
}

# Roles especiales
ROLES = {
    'ani': 'CEO',
    'chuche': 'CTO',
    'rulog': 'COO',
    'goncho': 'CCO',
}

def get_level(agent, hierarchy):
    """Calcula el nivel jerárquico de un agente."""
    level = 0
    current = agent
    while current and hierarchy.get(current):
        current = hierarchy[current]
        level += 1
    return level

def get_color(agent, level):
    """Retorna color según nivel jerárquico."""
    if agent == 'ani':
        return '#e74c3c', 'white'  # CEO: Rojo
    elif level == 1:
        return '#3498db', 'white'  # C-Suite: Azul
    elif level == 2:
        return '#27ae60', 'white'  # Directors/Managers: Verde
    elif level == 3:
        return '#95a5a6', 'black'  # ICs nivel 3: Gris
    else:
        return '#bdc3c7', 'black'  # ICs nivel 4+: Gris claro

def create_orgchart():
    """Genera el orgchart visual."""
    dot = Digraph(comment='Orgchart - Creador de Personajes')
    
    # Configuración global para layout vertical
    dot.attr(rankdir='TB')  # Top to Bottom
    dot.attr('graph', 
             fontname='Helvetica',
             fontsize='14',
             bgcolor='white',
             pad='0.5',
             nodesep='0.4',
             ranksep='0.8',
             splines='ortho')
    
    dot.attr('node', 
             shape='box',
             style='filled,rounded',
             fontname='Helvetica',
             fontsize='11',
             margin='0.2,0.1')
    
    dot.attr('edge',
             color='#7f8c8d',
             penwidth='1.5')
    
    # Crear nodos
    for agent, manager in HIERARCHY.items():
        level = get_level(agent, HIERARCHY)
        fillcolor, fontcolor = get_color(agent, level)
        
        # Etiqueta con rol si existe
        role = ROLES.get(agent)
        if role:
            label = f'{agent.upper()}\\n({role})'
        else:
            label = agent.upper()
        
        dot.node(agent, 
                 label=label,
                 fillcolor=fillcolor,
                 fontcolor=fontcolor)
    
    # Crear edges (conexiones)
    for agent, manager in HIERARCHY.items():
        if manager:
            dot.edge(manager, agent)
    
    # Agrupar por niveles para mantener estructura
    with dot.subgraph() as s:
        s.attr(rank='same')
        s.node('chuche')
        s.node('rulog')
        s.node('goncho')
    
    # Guardar
    output_path = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(output_path, 'hierarchy_chart')
    
    dot.render(output_file, format='png', cleanup=True)
    print(f'✓ Orgchart generado: {output_file}.png')
    
    return dot

if __name__ == '__main__':
    create_orgchart()
