#!/usr/bin/env python3
"""
Create full team organization chart - 8 characters unified.
"""

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

plt.style.use('dark_background')

fig, ax = plt.subplots(1, 1, figsize=(16, 12))
ax.set_xlim(0, 16)
ax.set_ylim(0, 12)
ax.axis('off')

BG_COLOR = '#1a1a2e'

# Colors by role
CEO_COLOR = '#E74C3C'
CTO_COLOR = '#3498DB'
COO_COLOR = '#27AE60'
CHAOS_COLOR = '#9B59B6'
CCO_COLOR = '#F39C12'

def draw_box(ax, x, y, width, height, color, name, subtitle, mbti, franchise):
    box = FancyBboxPatch((x - width/2, y - height/2), width, height,
                         boxstyle="round,pad=0.05,rounding_size=0.15",
                         facecolor=color, edgecolor='white', linewidth=2,
                         alpha=0.9)
    ax.add_patch(box)
    ax.text(x, y + 0.3, name, fontsize=11, fontweight='bold',
            ha='center', va='center', color='white')
    ax.text(x, y, subtitle, fontsize=8,
            ha='center', va='center', color='white', alpha=0.9)
    ax.text(x, y - 0.25, f"({mbti})", fontsize=7,
            ha='center', va='center', color='white', alpha=0.7)
    ax.text(x, y - 0.5, franchise, fontsize=7,
            ha='center', va='center', color='white', alpha=0.6, style='italic')

def draw_arrow(ax, start, end):
    ax.annotate('', xy=end, xytext=start,
                arrowprops=dict(arrowstyle='->', color='white', lw=1.5))

# Title
ax.text(8, 11.5, 'THE FULL TEAM: 8 ICONIC PERSONALITIES', 
        fontsize=18, fontweight='bold', ha='center', va='center', color='white')
ax.text(8, 11, '6 Franchises | 4 MBTI Types | Real Collaboration',
        fontsize=11, ha='center', va='center', color='#888888')

# CEO Level - Co-CEOs
draw_box(ax, 5.5, 9, 2.4, 1.1, CEO_COLOR, 'BATMAN', 'Strategy', 'INTJ 1w9', 'DC')
draw_box(ax, 10.5, 9, 2.4, 1.1, CEO_COLOR, 'DAENERYS', 'Vision', 'ENFJ 1w2', 'GoT')
ax.text(8, 9, '+', fontsize=20, fontweight='bold', ha='center', va='center', color='white')

# Division line
ax.plot([2, 14], [7.8, 7.8], color='#444', linestyle='--', linewidth=1)

# CTO Division (left)
ax.text(4, 7.5, 'CTO DIVISION', fontsize=10, fontweight='bold', ha='center', color=CTO_COLOR)
draw_box(ax, 2.5, 6.2, 2.2, 1.0, CTO_COLOR, 'TONY STARK', 'Innovation', 'ENTP 7w8', 'MCU')
draw_box(ax, 5.5, 6.2, 2.2, 1.0, CTO_COLOR, 'RIPLEY', 'Analysis', 'INTJ 8w9', 'Alien')

# COO Division (center)
ax.text(8, 7.5, 'COO DIVISION', fontsize=10, fontweight='bold', ha='center', color=COO_COLOR)
draw_box(ax, 8, 6.2, 2.2, 1.0, COO_COLOR, 'JOHN WICK', 'Execution', 'ISTP 6w5', 'Action')
draw_box(ax, 8, 4.8, 2.2, 1.0, COO_COLOR, 'KATNISS', 'Survival', 'ISTP 6w5', 'HG')

# CCO Division (right)
ax.text(12, 7.5, 'CCO DIVISION', fontsize=10, fontweight='bold', ha='center', color=CCO_COLOR)
draw_box(ax, 11, 6.2, 2.2, 1.0, CCO_COLOR, 'WONDER WOMAN', 'Diplomacy', 'ENFJ 2w1', 'DC')
draw_box(ax, 13, 6.2, 2.2, 1.0, CHAOS_COLOR, 'JOKER', 'Disruption', 'ENTP 7w8', 'DC')

# Arrows from CEOs
draw_arrow(ax, (5.5, 8.45), (4, 7.6))
draw_arrow(ax, (8, 8.5), (8, 7.6))
draw_arrow(ax, (10.5, 8.45), (12, 7.6))

# Bottom: Value proposition
ax.text(8, 3.2, 'WHY THIS WORKS', fontsize=12, fontweight='bold', ha='center', color='white')

props = [
    ('INTJ + ENFJ', 'Strategy meets Inspiration'),
    ('ENTP + ISTP', 'Ideas meet Execution'),
    ('Order + Chaos', 'Plans get stress-tested'),
]

for i, (pair, desc) in enumerate(props):
    x = 4 + i * 4
    ax.text(x, 2.5, pair, fontsize=10, fontweight='bold', ha='center', color='#aaa')
    ax.text(x, 2.1, desc, fontsize=9, ha='center', color='#666')

# Legend
ax.text(8, 1.0, 'Each character brings their fictional world into their work style',
        fontsize=10, ha='center', color='#888', style='italic')

fig.patch.set_facecolor(BG_COLOR)
plt.tight_layout()
plt.savefig('full_team.png', dpi=150, facecolor=BG_COLOR, bbox_inches='tight', pad_inches=0.3)
print("Saved: full_team.png")
