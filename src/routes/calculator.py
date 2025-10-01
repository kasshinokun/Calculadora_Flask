from flask import Blueprint, request, jsonify
from src.models.user import db
from src.models.calculator import Operation
import re
import math

calculator_bp = Blueprint('calculator', __name__)

def safe_eval(expression):
    """
    Avalia uma expressão matemática de forma segura
    Permite apenas operações básicas: +, -, *, /, (, ), números e decimais
    """
    # Substitui x por *  
    expression = expression.replace('x', '*')
    
    # Substitui : por /  
    expression = expression.replace(':', '/')
    
    # Remove espaços
    expression = expression.replace(' ', '')
    
    # Verifica se a expressão contém apenas caracteres permitidos
    allowed_chars = re.compile(r'^[0-9+\-*/().,]+$')
    if not allowed_chars.match(expression):
        raise ValueError("Expressão contém caracteres não permitidos")
    
    # Substitui vírgulas por pontos para decimais
    expression = expression.replace(',', '.')
    
    # Verifica se há parênteses balanceados
    if expression.count('(') != expression.count(')'):
        raise ValueError("Parênteses não balanceados")
    
    # Avalia a expressão
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
    Calcula uma expressão matemática e salva no histórico
    """
    try:
        data = request.get_json()
        if not data or 'expression' not in data:
            return jsonify({'error': 'Expressão é obrigatória'}), 400
        
        expression = data['expression']
        if not expression.strip():
            return jsonify({'error': 'Expressão não pode estar vazia'}), 400
        
        # Calcula o resultado
        result = safe_eval(expression)
        
        # Salva no banco de dados
        operation = Operation(expression=expression, result=result)
        db.session.add(operation)
        db.session.commit()
        
        # Mantém apenas as últimas 10 operações
        total_operations = Operation.query.count()
        if total_operations > 10:
            oldest_operations = Operation.query.order_by(Operation.timestamp.asc()).limit(total_operations - 10).all()
            for op in oldest_operations:
                db.session.delete(op)
            db.session.commit()
        
        return jsonify({
            'expression': expression,
            'result': result,
            'timestamp': operation.timestamp.isoformat()
        })
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Erro interno do servidor'}), 500

@calculator_bp.route('/history', methods=['GET'])
def get_history():
    """
    Retorna o histórico das últimas 10 operações
    """
    try:
        operations = Operation.query.order_by(Operation.timestamp.desc()).limit(10).all()
        return jsonify([op.to_dict() for op in operations])
    except Exception as e:
        return jsonify({'error': 'Erro ao buscar histórico'}), 500

@calculator_bp.route('/clear', methods=['DELETE'])
def clear_history():
    """
    Limpa todo o histórico de operações
    """
    try:
        Operation.query.delete()
        db.session.commit()
        return jsonify({'message': 'Histórico limpo com sucesso'})
    except Exception as e:
        return jsonify({'error': 'Erro ao limpar histórico'}), 500
