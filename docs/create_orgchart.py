#!/usr/bin/env python3
"""
Create organization chart visualization for README.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

# Dark theme
plt.style.use('dark_background')

fig, ax = plt.subplots(1, 1, figsize=(14, 10))
ax.set_xlim(0, 14)
ax.set_ylim(0, 10)
ax.axis('off')

# Colors
CEO_COLOR = '#FF6B6B'      # Red - Batman
CTO_COLOR = '#4ECDC4'      # Teal - Tony
COO_COLOR = '#45B7D1'      # Blue - John Wick
CHAOS_COLOR = '#9B59B6'    # Purple - Joker
BG_COLOR = '#1a1a2e'
TEXT_COLOR = '#ffffff'

def draw_box(ax, x, y, width, height, color, name, subtitle, mbti, role):
    """Draw a styled box for an agent."""
    box = FancyBboxPatch((x - width/2, y - height/2), width, height,
                         boxstyle="round,pad=0.05,rounding_size=0.2",
                         facecolor=color, edgecolor='white', linewidth=2,
                         alpha=0.9)
    ax.add_patch(box)
    
    # Name
    ax.text(x, y + 0.35, name, fontsize=14, fontweight='bold',
            ha='center', va='center', color='white')
    # Subtitle
    ax.text(x, y + 0.05, subtitle, fontsize=10,
            ha='center', va='center', color='white', alpha=0.9)
    # MBTI
    ax.text(x, y - 0.25, f"({mbti})", fontsize=9,
            ha='center', va='center', color='white', alpha=0.7)
    # Role
    ax.text(x, y - 0.5, role, fontsize=10, fontweight='bold',
            ha='center', va='center', color='white', alpha=0.9)

def draw_arrow(ax, start, end, color='white'):
    """Draw connection arrow."""
    ax.annotate('', xy=end, xytext=start,
                arrowprops=dict(arrowstyle='->', color=color, lw=2))

# Title
ax.text(7, 9.5, 'AI PERSONALITY GENERATOR', 
        fontsize=20, fontweight='bold', ha='center', va='center', color='white')
ax.text(7, 9, 'Team Organization | MBTI + Enneagram + Wikipedia Context',
        fontsize=11, ha='center', va='center', color='#888888')

# CEO - Batman
draw_box(ax, 7, 7, 2.8, 1.4, CEO_COLOR, 'BATMAN', 'Bruce Wayne', 'INTJ 1w9', 'CEO')

# CTO - Tony Stark
draw_box(ax, 3.5, 4.5, 2.8, 1.4, CTO_COLOR, 'TONY STARK', 'Iron Man', 'ENTP 7w8', 'CTO')

# COO - John Wick  
draw_box(ax, 7, 4.5, 2.8, 1.4, COO_COLOR, 'JOHN WICK', 'Baba Yaga', 'ISTP 6w5', 'COO')

# Chaos Officer - Joker
draw_box(ax, 10.5, 4.5, 2.8, 1.4, CHAOS_COLOR, 'THE JOKER', 'Agent of Chaos', 'ENTP 7w8', 'Advisor')

# Arrows
draw_arrow(ax, (7, 6.3), (3.5, 5.2))
draw_arrow(ax, (7, 6.3), (7, 5.2))
draw_arrow(ax, (7, 6.3), (10.5, 5.2))

# Descriptions
desc_y = 2.5
ax.text(3.5, desc_y, 'INNOVATION\n"What if we tried..."', fontsize=10, ha='center', va='center', color=CTO_COLOR, fontweight='bold')
ax.text(7, desc_y, 'EXECUTION\n"Consider it done"', fontsize=10, ha='center', va='center', color=COO_COLOR, fontweight='bold')
ax.text(10.5, desc_y, 'DISRUPTION\n"Why so serious?"', fontsize=10, ha='center', va='center', color=CHAOS_COLOR, fontweight='bold')

# Franchise labels
ax.text(3.5, 3.3, 'Marvel Cinematic Universe', fontsize=8, ha='center', va='center', color='#666666', style='italic')
ax.text(7, 3.3, 'John Wick Series', fontsize=8, ha='center', va='center', color='#666666', style='italic')
ax.text(10.5, 3.3, 'DC Comics', fontsize=8, ha='center', va='center', color='#666666', style='italic')
ax.text(7, 6.0, 'DC Comics', fontsize=8, ha='center', va='center', color='#666666', style='italic')

# Legend box
legend_y = 1.0
ax.text(7, legend_y, 'INTJ = Strategy  |  ENTP = Innovation  |  ISTP = Precision', 
        fontsize=10, ha='center', color='#aaaaaa')

fig.patch.set_facecolor(BG_COLOR)
plt.tight_layout()
plt.savefig('orgchart.png', dpi=150, facecolor=BG_COLOR, bbox_inches='tight', pad_inches=0.3)
print("Saved: orgchart.png")
