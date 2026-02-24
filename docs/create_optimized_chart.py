#!/usr/bin/env python3
"""
Create organization chart for the optimized team.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch

# Dark theme
plt.style.use('dark_background')

fig, ax = plt.subplots(1, 1, figsize=(16, 12))
ax.set_xlim(0, 16)
ax.set_ylim(0, 12)
ax.axis('off')

# Colors by role
CEO_COLOR = '#FF6B6B'      # Red
CTO_COLOR = '#4ECDC4'      # Teal
COO_COLOR = '#45B7D1'      # Blue
CCO_COLOR = '#9B59B6'      # Purple
IC_COLOR = '#95A5A6'       # Gray

def draw_box(ax, x, y, width, height, color, name, role, mbti, score=None):
    """Draw a styled box for an agent."""
    box = FancyBboxPatch((x - width/2, y - height/2), width, height,
                         boxstyle="round,pad=0.05,rounding_size=0.2",
                         facecolor=color, edgecolor='white', linewidth=2,
                         alpha=0.9)
    ax.add_patch(box)
    
    # Name
    ax.text(x, y + 0.3, name, fontsize=12, fontweight='bold',
            ha='center', va='center', color='white')
    # Role
    ax.text(x, y, role, fontsize=9,
            ha='center', va='center', color='white', alpha=0.9)
    # MBTI
    ax.text(x, y - 0.3, f"({mbti})", fontsize=8,
            ha='center', va='center', color='white', alpha=0.7)

def draw_arrow(ax, start, end, color='white'):
    """Draw connection line."""
    ax.annotate('', xy=end, xytext=start,
                arrowprops=dict(arrowstyle='-', color=color, lw=1.5, alpha=0.5))

# Title
ax.text(8, 11.5, '🎭 AI Personality Generator - Optimized Organization', 
        fontsize=16, fontweight='bold', ha='center', va='center', color='white')
ax.text(8, 11, 'Hierarchy determined by MBTI + Enneagram scoring', 
        fontsize=10, ha='center', va='center', color='#888888')

# CEO - Ellen Ripley (INTJ 8w9)
draw_box(ax, 8, 9, 3, 1.2, CEO_COLOR, 'Ellen Ripley', 'CEO', 'INTJ 8w9')

# C-Suite level
# CTO - Batman (INTJ 1w9)
draw_box(ax, 3, 6.5, 2.8, 1.2, CTO_COLOR, 'Batman', 'CTO', 'INTJ 1w9')
# COO - Katniss (ISTP 6w5)
draw_box(ax, 8, 6.5, 2.8, 1.2, COO_COLOR, 'Katniss', 'COO', 'ISTP 6w5')
# CCO - Wonder Woman (ENFJ 2w1)
draw_box(ax, 13, 6.5, 2.8, 1.2, CCO_COLOR, 'Wonder Woman', 'CCO', 'ENFJ 2w1')

# IC level - under Batman
draw_box(ax, 1.5, 3.5, 2.5, 1.1, IC_COLOR, 'Daenerys', 'IC', 'ENFJ 1w2')
draw_box(ax, 4.5, 3.5, 2.5, 1.1, IC_COLOR, 'John Wick', 'IC', 'ISTP 6w5')

# IC level - under Katniss
draw_box(ax, 8, 3.5, 2.5, 1.1, IC_COLOR, 'Tony Stark', 'IC', 'ENTP 7w8')

# IC level - under Wonder Woman
draw_box(ax, 13, 3.5, 2.5, 1.1, IC_COLOR, 'The Joker', 'IC', 'ENTP 7w8')

# Draw connections
# CEO to C-Suite
draw_arrow(ax, (8, 8.4), (3, 7.1))
draw_arrow(ax, (8, 8.4), (8, 7.1))
draw_arrow(ax, (8, 8.4), (13, 7.1))

# CTO to ICs
draw_arrow(ax, (3, 5.9), (1.5, 4.1))
draw_arrow(ax, (3, 5.9), (4.5, 4.1))

# COO to ICs
draw_arrow(ax, (8, 5.9), (8, 4.1))

# CCO to ICs
draw_arrow(ax, (13, 5.9), (13, 4.1))

# Legend
legend_y = 1.5
ax.text(1, legend_y + 0.8, 'Role Assignment Logic:', fontsize=10, fontweight='bold', color='white')
ax.text(1, legend_y, '• INTJ 8w9 → CEO: Strategic thinking + Leadership drive', fontsize=8, color='#cccccc')
ax.text(1, legend_y - 0.4, '• INTJ 1w9 → CTO: Analytical + Perfectionist', fontsize=8, color='#cccccc')
ax.text(1, legend_y - 0.8, '• ISTP 6w5 → COO: Practical + Security-focused', fontsize=8, color='#cccccc')
ax.text(1, legend_y - 1.2, '• ENFJ 2w1 → CCO: Empathetic + Helper', fontsize=8, color='#cccccc')

# Color legend
ax.add_patch(FancyBboxPatch((10, 1.8), 0.4, 0.4, facecolor=CEO_COLOR, edgecolor='white'))
ax.text(10.6, 2, 'CEO', fontsize=8, color='white', va='center')
ax.add_patch(FancyBboxPatch((12, 1.8), 0.4, 0.4, facecolor=CTO_COLOR, edgecolor='white'))
ax.text(12.6, 2, 'CTO', fontsize=8, color='white', va='center')
ax.add_patch(FancyBboxPatch((10, 1.2), 0.4, 0.4, facecolor=COO_COLOR, edgecolor='white'))
ax.text(10.6, 1.4, 'COO', fontsize=8, color='white', va='center')
ax.add_patch(FancyBboxPatch((12, 1.2), 0.4, 0.4, facecolor=CCO_COLOR, edgecolor='white'))
ax.text(12.6, 1.4, 'CCO', fontsize=8, color='white', va='center')
ax.add_patch(FancyBboxPatch((14, 1.5), 0.4, 0.4, facecolor=IC_COLOR, edgecolor='white'))
ax.text(14.6, 1.7, 'IC', fontsize=8, color='white', va='center')

plt.tight_layout()
plt.savefig('optimized_orgchart.png', dpi=150, bbox_inches='tight', 
            facecolor='#1a1a2e', edgecolor='none')
print("✅ Saved optimized_orgchart.png")
