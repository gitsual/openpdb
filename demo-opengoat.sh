#!/bin/bash
# =============================================================================
# Launch OpenGoat with DEMO instance (fictional characters)
# Completely isolated from your real OpenGoat
# =============================================================================

export OPENGOAT_HOME="/home/lorty/m2/programas/creador_de_personajes/.opengoat-demo"

echo "🎭 OpenGoat DEMO - Fictional Characters"
echo "   Home: $OPENGOAT_HOME"
echo ""

# Configurar jerarquía si no existe
if [[ ! -f "$OPENGOAT_HOME/.hierarchy_set" ]]; then
    echo "📊 Setting up hierarchy..."
    
    # Crear configs con jerarquía
    for agent in ripley batman katniss wonder-woman tony-stark john-wick daenerys joker; do
        config="$OPENGOAT_HOME/agents/$agent/config.json"
        
        case $agent in
            ripley)
                cat > "$config" << 'EOF'
{"name":"ripley","role":"CEO - Strategic Leadership (INTJ 8w9)","reportsTo":null,"runtime":{"model":"ollama/qwen3-coder"}}
EOF
                ;;
            batman)
                cat > "$config" << 'EOF'
{"name":"batman","role":"CTO - Technical Strategy (INTJ 1w9)","reportsTo":"ripley","runtime":{"model":"ollama/qwen3-coder"}}
EOF
                ;;
            katniss)
                cat > "$config" << 'EOF'
{"name":"katniss","role":"COO - Operations (ISTP 6w5)","reportsTo":"ripley","runtime":{"model":"ollama/qwen3-coder"}}
EOF
                ;;
            wonder-woman)
                cat > "$config" << 'EOF'
{"name":"wonder-woman","role":"CCO - Culture & People (ENFJ 2w1)","reportsTo":"ripley","runtime":{"model":"ollama/qwen3-coder"}}
EOF
                ;;
            tony-stark)
                cat > "$config" << 'EOF'
{"name":"tony-stark","role":"IC - Innovation (ENTP 7w8)","reportsTo":"batman","runtime":{"model":"ollama/qwen3-coder"}}
EOF
                ;;
            john-wick)
                cat > "$config" << 'EOF'
{"name":"john-wick","role":"IC - Execution (ISTP 6w5)","reportsTo":"batman","runtime":{"model":"ollama/qwen3-coder"}}
EOF
                ;;
            daenerys)
                cat > "$config" << 'EOF'
{"name":"daenerys","role":"IC - Vision (ENFJ 1w2)","reportsTo":"wonder-woman","runtime":{"model":"ollama/qwen3-coder"}}
EOF
                ;;
            joker)
                cat > "$config" << 'EOF'
{"name":"joker","role":"IC - Disruption (ENTP 7w8)","reportsTo":"wonder-woman","runtime":{"model":"ollama/qwen3-coder"}}
EOF
                ;;
        esac
    done
    
    touch "$OPENGOAT_HOME/.hierarchy_set"
    echo "✅ Jerarquía configurada"
fi

echo ""
echo "🚀 Lanzando OpenGoat..."
echo "   URL: http://127.0.0.1:19124"
echo ""

# Lanzar en puerto diferente para no chocar con tu OpenGoat real
exec opengoat start --port 19124
