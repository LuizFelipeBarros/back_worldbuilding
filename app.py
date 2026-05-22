import os
import json
from flask import Flask, jsonify, request
from flask_cors import CORS
from google import genai
from google.genai import types
from dotenv import load_dotenv

from config import WORLDBUILD_SCHEMA, SYSTEM_INSTRUCTION

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

app = Flask(__name__)
CORS(app)

def world_const(instr, extras=None, racas=None):
    instrucoes = ", ".join(instr)
    conteudo_prompt = f"Crie um mundo obrigatoriamente usando esses itens: {instrucoes}."

    # Ordem e descrições das perguntas extras que podem ser abertas pelo botão ➕
    extras_order = [
        ("clima_e_fenomenos", "Clima e Fenômenos (ex: chuvas de luz, ventos que mudam o tempo)"),
        ("energia_ou_magia", "Energia ou Magia (ex: magia baseada em música, pilhas de cristal)"),
        ("vegetacao_e_flora", "Vegetação e Flora (ex: florestas de fungos gigantes, plantas elétricas)"),
        ("animais_e_fauna", "Animais e Fauna (ex: monstros de pedra, baleias voadoras)"),
        ("recursos_raros", "Recursos Raros (ex: metal que flutua, combustível vivo)"),
        ("transporte", "Transporte (ex: trens orgânicos, portais de névoa)")
    ]

    if extras and isinstance(extras, dict):
        for key, desc in extras_order:
            val = extras.get(key)
            if val:
                conteudo_prompt += f" Considere também {desc}: {val}."

    # Instrução sobre raças: se o usuário forneceu, force a inclusão; caso contrário peça ao modelo para gerar
    if racas:
        if isinstance(racas, list):
            racas_str = ", ".join(racas)
        else:
            racas_str = str(racas)
        conteudo_prompt += f" Inclua explicitamente as raças/tribos a seguir em sociedade.povos: {racas_str}."
    else:
        conteudo_prompt += " Inclua pelo menos três povos distintos no campo sociedade.povos, a menos que o usuário especifique raças específicas."

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=conteudo_prompt,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
            response_mime_type="application/json",
            response_schema=WORLDBUILD_SCHEMA,
        )
    )
    return response.text

@app.route("/")
def root():
    return jsonify({
        "status": "success",
        # CORREÇÃO: Mensagem contextualizada para o Gerador de Mundos
        "message": "API Gerador de Mundos (Worldbuilding) funcionando!",
        "version": "1.0"
    }), 200

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    
    if not data or "pedidos" not in data:
        return jsonify({
            "status": "error",
            "message": "Por favor, envie uma lista de pedidos no formato JSON."
        }), 400
        
    pedidos = data.get("pedidos", [])
    extras = data.get("extras", {})
    racas = data.get("racas", None)

    if not isinstance(pedidos, list) or len(pedidos) < 1:
        return jsonify({
            "status": "error",
            "message": "Você precisa fornecer ao menos 1 pedido."
        }), 400
    
    try:
        mundo_json_string = world_const(pedidos)
        world_build = json.loads(mundo_json_string)
        
        return jsonify({
            "status": "success",
            "pedidos_enviados": pedidos,
            "dados_historia": world_build
        }), 200
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Erro ao gerar o mundo: {str(e)}"
        }), 500

if __name__ == "__main__":
    app.run(debug=True)
