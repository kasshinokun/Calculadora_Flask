
from flask import Blueprint, request, jsonify, session
import re
import math
from datetime import datetime

calculator_bp = Blueprint('calculator', __name__)

def safe_eval(expression):
    """
    Avalia uma expressão matemática de forma segura
    Permite apenas operações básicas: +, -, *, /, (, ), números e decimais
    """
    expression = expression.replace('x', '*')
    expression = expression.replace(':', '/')
    expression = expression.replace(' ', '')
    
    allowed_chars = re.compile(r'^[0-9+\-*/().,]+$')
    if not allowed_chars.match(expression):
        raise ValueError("Expressão contém caracteres não permitidos")
    
    expression = expression.replace(',', '.')
    
    if expression.count('(') != expression.count(')'):
        raise ValueError("Parênteses não balanceados")
    
    try:
        result = eval(expression)
        if math.isnan(result) or math.isinf(result):
            raise ValueError("Resultado inválido")
        return round(result, 2)
    except ZeroDivisionError:
        raise ValueError("Divisão por zero")
    except Exception as e:
        raise ValueError("Expressão inválida")

@calculator_bp.route('/calculate', methods=['POST'])
def calculate():
    """
    Calcula uma expressão matemática e salva no histórico da sessão
    """
    try:
        data = request.get_json()
        if not data or 'expression' not in data:
            return jsonify({'error': 'Expressão é obrigatória'}), 400
        
        expression = data['expression']
        if not expression.strip():
            return jsonify({'error': 'Expressão não pode estar vazia'}), 400
        
        result = safe_eval(expression)
        
        # Inicializa o histórico na sessão se não existir
        if 'history' not in session:
            session['history'] = []
        
        # Adiciona a nova operação ao histórico
        operation = {
            'expression': expression,
            'result': result,
            'timestamp': datetime.utcnow().isoformat()
        }
        session['history'].append(operation)
        
        # Mantém apenas as últimas 10 operações
        if len(session['history']) > 10:
            session['history'] = session['history'][-10:]
        
        # Garante que a sessão seja salva
        session.modified = True
        
        return jsonify(operation)
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Erro interno do servidor'}), 500

@calculator_bp.route('/history', methods=['GET'])
def get_history():
    """
    Retorna o histórico das últimas 10 operações da sessão
    """
    try:
        history = session.get('history', [])
        return jsonify(history)
    except Exception as e:
        return jsonify({'error': 'Erro ao buscar histórico'}), 500

@calculator_bp.route('/clear', methods=['DELETE'])
def clear_history():
    """
    Limpa todo o histórico de operações da sessão
    """
    try:
        session['history'] = []
        session.modified = True
        return jsonify({'message': 'Histórico limpo com sucesso'})
    except Exception as e:
        return jsonify({'error': 'Erro ao limpar histórico'}), 500

