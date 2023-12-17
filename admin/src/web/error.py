from flask import render_template

def not_found_error(e):
    kwargs = {
        "error_name": "404 not found",
        "error_description": "La URL a la que quiere acceder no existe"
    }

    return render_template("error.html", **kwargs), 404

def not_authorized_error(e):
    kwargs = {
        "error_name": "401 not authorized",
        "error_description": "No tiene permisos para acceder a esta página"
    }

    return render_template("error.html", **kwargs), 401

