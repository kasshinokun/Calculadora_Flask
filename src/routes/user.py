from flask import Blueprint, request, jsonify
from src.models.user import db, User

user_bp = Blueprint("user", __name__)

@user_bp.route("/users", methods=["GET"])
def get_users():
    """
    Retorna todos os usuários
    """
    try:
        users = User.query.all()
        return jsonify([{"id": user.id, "username": user.username, "email": user.email} for user in users])
    except Exception as e:
        return jsonify({"error": "Erro ao buscar usuários"}), 500

@user_bp.route("/users", methods=["POST"])
def create_user():
    """
    Cria um novo usuário
    """
    try:
        data = request.get_json()
        if not data or "username" not in data or "email" not in data:
            return jsonify({"error": "Username e email são obrigatórios"}), 400
        
        user = User(username=data["username"], email=data["email"])
        db.session.add(user)
        db.session.commit()
        
        return jsonify({"id": user.id, "username": user.username, "email": user.email}), 201
    except Exception as e:
        return jsonify({"error": "Erro ao criar usuário"}), 500
