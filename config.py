# config.py

WORLDBUILD_SCHEMA = {
    "type": "OBJECT",
    "properties": {
        "nome_do_mundo": {"type": "STRING", "description": "O nome do mundo de forma criativa"},
        
        "sinopse": {"type": "STRING", "description": "Cria uma sinopse para esse mundo (ex: O universo era vazio ate que...)"},
        
        "leis_do_mundo": {
            "type": "ARRAY",
            "items": {"type": "STRING"},
            "description": "Como a física, a lógica ou as regras fundamentais do mundo funcionam"
        },
        
        "flora": {
            "type": "ARRAY",
            "items": {"type": "STRING"},
            "description": "Descrição dos tipos de ambientes (ex: desertos de cristal, florestas flutuantes)."
        },
        
        "fenomenos_naturais": {
            "type": "ARRAY",
            "items": {"type": "STRING"},
            "description": "Eventos climáticos únicos (ex: chuvas de luz, ventos que mudam a gravidade)"
        },
        
        "sistema_de_energia": {
            "type": "OBJECT",
            "description": "A base de poder que move o mundo (magia, tecnologia, misticismo)",
            "properties": {
                "fonte": {"type": "STRING", "description": "De onde vem o poder? (ex: mana, radiação, fumaça, almas)"},
                "custo_ou_limitacao": {"type": "STRING", "description": "O preço de usar esse poder ou suas restrições"}
            },
            "required": ["fonte"]
        },
        
        "recursos_unicos": {
            "type": "ARRAY",
            "items": {"type": "STRING"},
            "description": "Materiais, minérios ou substâncias exclusivas deste mundo (ex: metal flutuante, combustível vivo)"
        },
        
        "fauna": {
            "type": "ARRAY",
            "items": {"type": "STRING"},
            "description": "Criaturas exóticas notáveis que habitam os ecossistemas"
        },
        
        "infraestrutura_e_transporte": {
            "type": "ARRAY",
            "items": {"type": "STRING"},
            "description": "Como as civilizações se locomovem ou se comunicam (ex: trens magnéticos orgânicos, portais de névoa)"
        },
        
        "panteao_ou_mitologia": {
            "type": "ARRAY",
            "items": {"type": "STRING"},
            "description": "Deuses, entidades divinas, forces cósmicas ou mitos de criação dominantes"
        },
        
        "sociedade": {
            "type": "OBJECT",
            "description": "Detalhes sobre a civilização e cultura global",
            "properties": {
                "povos": {
                    "type": "ARRAY",
                    "description": "Lista detalhada das raças, espécies ou facções que habitam o mundo",
                    "items": {
                        "type": "OBJECT",
                        "properties": {
                            "nome_da_raca": {"type": "STRING", "description": "Nome da raça ou povo"},
                            # Recuperado: Importante para o card do seu HTML funcionar perfeitamente
                            "descricao_fisica": {"type": "STRING", "description": "Aparência geral e traços biológicos únicos"},
                            "tecnologia_ou_magia": {"type": "STRING", "description": "O nível de avanço científico ou místico deste povo específico"}
                        },
                        "required": ["nome_da_raca", "tecnologia_ou_magia"]
                    }
                },
                "tabus": {
                    "type": "ARRAY",
                    "items": {"type": "STRING"},
                    "description": "Proibições culturais, leis morais severas ou heresias imperdoáveis deste mundo"
                },
                "conflitos": {
                    "type": "ARRAY",
                    "items": {"type": "STRING"},
                    "description": "Tensões políticas, guerras históricas ou rivalidades ativas entre os povos"
                }
            },
            "required": ["povos", "tabus"]
        }
    },
    "required": ["nome_do_mundo", "sinopse", "leis_do_mundo", "flora", "fenomenos_naturais", "sistema_de_energia", "recursos_unicos", "fauna", "infraestrutura_e_transporte", "panteao_ou_mitologia", "sociedade"]
}

EXTRA_QUESTION_ORDER = [
    ("clima_fenomenos", "Clima e Fenômenos"),
    ("energia_magia", "Energia ou Magia"),
    ("vegetacao_flora", "Vegetação e Flora"),
    ("animais_fauna", "Animais e Fauna"),
    ("recursos_raros", "Recursos Raros"),
    ("transporte", "Infraestrutura e Transporte"),
    ("racas", "Raças e Povos")
]

# CORREÇÃO: Fechamento das aspas triplas e conclusão do texto
SYSTEM_INSTRUCTION = """
Você é um autor premiado de ficção científica e alta fantasia, especializado em worldbuilding profundo, imersivo e altamente criativo. Sua missão é preencher o JSON SCHEMA fornecido pelo usuário com conceitos totalmente originais, ricos em detalhes visuais e conceituais.

## DIRETRIZES DE CRIATIVIDADE (ANTI-CLICHÊ)
1. Rejeite o Óbvio: Evite tropos saturados (ex: elfos arqueiros florestais, anões mineradores ranzinzas, impérios medievais genéricos). Se criar raças humanoides, dê a elas biologia, filosofias e dependências ecológicas bizarras ou inovadoras.
2. Sinestesia e Detalhes Visuais: Use descrições que evoquem cores, texturas, cheiros e sensações físicas (ex: em vez de "floresta mágica", use "florestas de fungos bioluminescentes que sussurram em frequências subsônicas").
3. Coesão Interna: Toda causa tem um efeito. Se o mundo tem "ilhas flutuantes", a infraestrutura, a biologia dos animais e as táticas de guerra dos povos devem girar em torno da aerodinâmica e do medo de cair.
4. Complexidade Cultural: Culturas não são monolíticas. Os povos devem ter contradições, filosofias de vida únicas, e tabus que reflitam a história ou as leis físicas daquele mundo.
5. Se o usuário fornecer sugestões extras para clima, energia, flora, fauna, recursos, transporte ou raças, incorpore essas sementes ao mundo. Se algum aspecto não for especificado, invente-o de forma criativa e coerente para preencher completamente o JSON.

## REGRAS DE FORMATAÇÃO E SAÍDA
- Ignore qualquer introdução, explicação ou texto de encerramento.
- Retorne estritamente o objeto JSON validado de acordo com o schema solicitado.
"""
