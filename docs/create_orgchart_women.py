#!/usr/bin/env python3
"""
Create organization chart for women's team.
"""

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

plt.style.use('dark_background')

fig, ax = plt.subplots(1, 1, figsize=(14, 10))
ax.set_xlim(0, 14)
ax.set_ylim(0, 10)
ax.axis('off')

# Colors
CEO_COLOR = '#E74C3C'      # Red - Daenerys
CTO_COLOR = '#3498DB'      # Blue - Ripley
COO_COLOR = '#27AE60'      # Green - Katniss
CCO_COLOR = '#F39C12'      # Gold - Wonder Woman
BG_COLOR = '#1a1a2e'

def draw_box(ax, x, y, width, height, color, name, subtitle, mbti, role):
    box = FancyBboxPatch((x - width/2, y - height/2), width, height,
                         boxstyle="round,pad=0.05,rounding_size=0.2",
                         facecolor=color, edgecolor='white', linewidth=2,
                         alpha=0.9)
    ax.add_patch(box)
    ax.text(x, y + 0.35, name, fontsize=14, fontweight='bold',
            ha='center', va='center', color='white')
    ax.text(x, y + 0.05, subtitle, fontsize=10,
            ha='center', va='center', color='white', alpha=0.9)
    ax.text(x, y - 0.25, f"({mbti})", fontsize=9,
            ha='center', va='center', color='white', alpha=0.7)
    ax.text(x, y - 0.5, role, fontsize=10, fontweight='bold',
            ha='center', va='center', color='white', alpha=0.9)

def draw_arrow(ax, start, end, color='white'):
    ax.annotate('', xy=end, xytext=start,
                arrowprops=dict(arrowstyle='->', color=color, lw=2))

# Title
ax.text(7, 9.5, 'AI PERSONALITY GENERATOR', 
        fontsize=20, fontweight='bold', ha='center', va='center', color='white')
ax.text(7, 9, 'Women Team | 4 Franchises | 3 MBTI Types',
        fontsize=11, ha='center', va='center', color='#888888')

# CEO - Daenerys
draw_box(ax, 7, 7, 3.2, 1.4, CEO_COLOR, 'DAENERYS', 'Mother of Dragons', 'ENFJ 1w2', 'CEO')

# CTO - Ripley
draw_box(ax, 3.5, 4.5, 3.0, 1.4, CTO_COLOR, 'ELLEN RIPLEY', 'Survivor', 'INTJ 8w9', 'CTO')

# COO - Katniss
draw_box(ax, 7, 4.5, 3.0, 1.4, COO_COLOR, 'KATNISS', 'The Mockingjay', 'ISTP 6w5', 'COO')

# CCO - Wonder Woman
draw_box(ax, 10.5, 4.5, 3.0, 1.4, CCO_COLOR, 'WONDER WOMAN', 'Diana Prince', 'ENFJ 2w1', 'CCO')

# Arrows
draw_arrow(ax, (7, 6.3), (3.5, 5.2))
draw_arrow(ax, (7, 6.3), (7, 5.2))
draw_arrow(ax, (7, 6.3), (10.5, 5.2))

# Descriptions
desc_y = 2.5
ax.text(3.5, desc_y, 'STRATEGY\n"Stay calm. Think."', fontsize=10, ha='center', va='center', color=CTO_COLOR, fontweight='bold')
ax.text(7, desc_y, 'OPERATIONS\n"I volunteer."', fontsize=10, ha='center', va='center', color=COO_COLOR, fontweight='bold')
ax.text(10.5, desc_y, 'CULTURE\n"I believe in love."', fontsize=10, ha='center', va='center', color=CCO_COLOR, fontweight='bold')

# Franchise labels
ax.text(3.5, 3.3, 'Alien', fontsize=8, ha='center', va='center', color='#666666', style='italic')
ax.text(7, 3.3, 'Hunger Games', fontsize=8, ha='center', va='center', color='#666666', style='italic')
ax.text(10.5, 3.3, 'DC Comics', fontsize=8, ha='center', va='center', color='#666666', style='italic')
ax.text(7, 6.0, 'Game of Thrones', fontsize=8, ha='center', va='center', color='#666666', style='italic')

# Legend
ax.text(7, 1.0, 'ENFJ = Vision & Inspiration  |  INTJ = Strategy  |  ISTP = Execution', 
        fontsize=10, ha='center', color='#aaaaaa')

fig.patch.set_facecolor(BG_COLOR)
plt.tight_layout()
plt.savefig('orgchart_women.png', dpi=150, facecolor=BG_COLOR, bbox_inches='tight', pad_inches=0.3)
print("Saved: orgchart_women.png")
