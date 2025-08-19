from __future__ import annotations

from flask import Blueprint, jsonify
from flask_jwt_extended import get_jwt, jwt_required

from .db import get_db_session
from .models import Order, OrderItem, Product, User


admin_bp = Blueprint("admin", __name__)


@admin_bp.get("/summary")
@jwt_required()
def summary():
    claims = get_jwt()
    if not claims.get("is_admin"):
        return jsonify({"error": "Admin required"}), 403

    session = get_db_session()
    total_users = session.query(User).count()
    total_products = session.query(Product).count()
    total_orders = session.query(Order).count()
    total_items = session.query(OrderItem).count()

    return jsonify({
        "total_users": total_users,
        "total_products": total_products,
        "total_orders": total_orders,
        "total_items": total_items,
    })
