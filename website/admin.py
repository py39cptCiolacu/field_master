from __future__ import annotations

from flask import Blueprint, render_template, request, jsonify

admin = Blueprint("admin", __name__)

points = [] # dc l am initializat pe asta aici? 

@admin.route("/admin_login")
def admin_login():
    pass    

@admin.route("/admin_register")
def admin_register():
    pass


@admin.route("/admin_logout")
def admin_logout():
    pass


@admin.route("admin_panel")
def admin_panel():
    pass




