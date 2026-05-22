import os
import json
from flask import Flask, jsonify, request
from flask_cors import CORS
from google import genai
from google.genai import types
from dotenv import load_dotenv

from config import WORLDBUILD_SCHEMA, SYSTEM_INSTRUCTION, EXTRA_QUESTION_ORDER

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

def build_world_prompt(instr, extras=None):
    instrucoes = ", ".join(instr)
    conteudo_prompt = f"Crie um mundo obrigatoriamente usando esses itens: {instrucoes}."

    if extras and isinstance(extras, dict):
        detalhes = []
        for key, label in EXTRA_QUESTION_ORDER:
            value = extras.get(key)
            if value:
                if isinstance(value, list):
                    value = "; ".join(str(item) for item in value if item)
                detalhes.append(f"{label}: {value}")

        if detalhes:
            conteudo_prompt += " Use também estes detalhes adicionais como sementes criativas: " + " ".join(detalhes) + "."

    conteudo_prompt += (
        " Se algum aspecto não foi especificado, invente-o de forma criativa "
        "e coerente para preencher todas as chaves exigidas no JSON."
    )
    return conteudo_prompt


def world_const(instr, extras=None):
    conteudo_prompt = build_world_prompt(instr, extras)
    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=conteudo_prompt,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
            response_mime_type="application/json",
            response_schema=WORLDBUILD_SCHEMA,
        )
    )
    return response.text

app = Flask(__name__)
CORS(app)

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
    detalhes = data.get("detalhes", {})
    
    if not isinstance(pedidos, list) or len(pedidos) < 3:
        return jsonify({
            "status": "error",
            "message": "Você precisa fornecer no mínimo 3 pedidos."
        }), 400

    if detalhes and not isinstance(detalhes, dict):
        return jsonify({
            "status": "error",
            "message": "Os detalhes adicionais devem ser enviados como um objeto JSON."
        }), 400
    
    try:
        mundo_json_string = world_const(pedidos, detalhes)
        world_build = json.loads(mundo_json_string)
        
        return jsonify({
            "status": "success",
            "pedidos_enviados": pedidos,
            "detalhes_enviados": detalhes,
            "dados_historia": world_build
        }), 200
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Erro ao gerar o mundo: {str(e)}"
        }), 500

if __name__ == "__main__":
    app.run(debug=True)
