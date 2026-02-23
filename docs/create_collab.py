#!/usr/bin/env python3
"""
Create collaboration flow visualization.
"""

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
import matplotlib.patches as mpatches

# Dark theme
plt.style.use('dark_background')

fig, ax = plt.subplots(1, 1, figsize=(14, 8))
ax.set_xlim(0, 14)
ax.set_ylim(0, 8)
ax.axis('off')

BG_COLOR = '#1a1a2e'
BATMAN_COLOR = '#FF6B6B'
TONY_COLOR = '#4ECDC4'
WICK_COLOR = '#45B7D1'
JOKER_COLOR = '#9B59B6'

# Title
ax.text(7, 7.5, 'COLLABORATION FLOW: Security System Redesign', 
        fontsize=16, fontweight='bold', ha='center', va='center', color='white')

# Task box
task_box = FancyBboxPatch((4.5, 6), 5, 1, boxstyle="round,pad=0.1,rounding_size=0.2",
                          facecolor='#2d2d44', edgecolor='#555', linewidth=2)
ax.add_patch(task_box)
ax.text(7, 6.5, 'TASK: Design new authentication system', fontsize=12, ha='center', va='center', color='white')

# Agent contributions - circular layout
def draw_agent(x, y, color, name, role, quote):
    circle = Circle((x, y), 0.6, facecolor=color, edgecolor='white', linewidth=2)
    ax.add_patch(circle)
    ax.text(x, y + 0.1, name, fontsize=10, fontweight='bold', ha='center', va='center', color='white')
    ax.text(x, y - 0.15, role, fontsize=8, ha='center', va='center', color='white', alpha=0.8)
    
    # Quote box
    quote_box = FancyBboxPatch((x - 1.8, y - 1.5), 3.6, 0.8, boxstyle="round,pad=0.05,rounding_size=0.1",
                               facecolor=color, edgecolor='white', linewidth=1, alpha=0.3)
    ax.add_patch(quote_box)
    ax.text(x, y - 1.1, f'"{quote}"', fontsize=9, ha='center', va='center', color='white', style='italic')

# Batman - top center (decision maker)
draw_agent(7, 4.5, BATMAN_COLOR, 'BATMAN', 'Decision', 'We need complete control')

# Tony - left
draw_agent(2.5, 3.5, TONY_COLOR, 'TONY', 'Innovation', 'Biometric + AI combo?')

# John Wick - bottom center  
draw_agent(7, 1.5, WICK_COLOR, 'JOHN', 'Execution', 'Three layers. No gaps.')

# Joker - right
draw_agent(11.5, 3.5, JOKER_COLOR, 'JOKER', 'Challenge', 'What if WE hack it first?')

# Arrows showing flow
props = dict(arrowstyle='->', color='white', lw=1.5, connectionstyle='arc3,rad=0.1')

# From task to Batman
ax.annotate('', xy=(7, 5.1), xytext=(7, 6), arrowprops=props)

# From Batman to others
ax.annotate('', xy=(3.1, 3.9), xytext=(6.4, 4.3), arrowprops=props)
ax.annotate('', xy=(7, 2.1), xytext=(7, 3.9), arrowprops=props)
ax.annotate('', xy=(10.9, 3.9), xytext=(7.6, 4.3), arrowprops=props)

# Labels for flow
ax.text(4.5, 4.3, '1. Ideate', fontsize=8, color='#888888', ha='center')
ax.text(7, 3.2, '2. Plan', fontsize=8, color='#888888', ha='center')
ax.text(9.5, 4.3, '3. Stress Test', fontsize=8, color='#888888', ha='center')

# Result box
result_box = FancyBboxPatch((4, 0.2), 6, 0.6, boxstyle="round,pad=0.05,rounding_size=0.1",
                            facecolor='#2d5a2d', edgecolor='#4a4', linewidth=2)
ax.add_patch(result_box)
ax.text(7, 0.5, 'RESULT: Multi-factor auth with AI anomaly detection', fontsize=10, ha='center', va='center', color='white')

fig.patch.set_facecolor(BG_COLOR)
plt.tight_layout()
plt.savefig('collaboration.png', dpi=150, facecolor=BG_COLOR, bbox_inches='tight', pad_inches=0.2)
print("Saved: collaboration.png")
