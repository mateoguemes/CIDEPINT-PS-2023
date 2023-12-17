# src/web/controllers/configs_module.py
from flask import Blueprint, render_template, jsonify, request, flash, redirect, url_for
from src.web.helpers.auth import is_authorized
from src.models.configs import Config
from typing import Union

config_module_bp = Blueprint('config_module', __name__)

@config_module_bp.route('/config-view')
@is_authorized("configuration_show")
def view_config()->Union[dict, None]:
    """
    Returns the configuration data.
    """
    try:
        config_data = Config.get_config()
        return render_template('config_view.html', config_data=config_data), 200

    except Exception as e:
        return jsonify({'error': 'Error al obtener la configuración', 'details': str(e)}), 500

@config_module_bp.route('/config-edit', methods=['GET', 'POST'])
@is_authorized("configuration_update")
def edit_config()->None:
    """
    Updates the configuration data and renders the configuration view.
    """
    try:
        if request.method == 'POST':
            # Obtener datos del formulario y actualizar la configuración
            data = {
                'per_page': int(request.form['perPage']),
                'contact_info': request.form['contactInfo'],
                'maintenance_mode': 'maintenance' in request.form,
                'maintenance_message': request.form['maintenanceMessage'],
            }
            Config.update_config(data)
            flash('Configuración actualizada correctamente', 'success')
            return redirect(url_for('config_module.view_config'))

        # Método GET: Mostrar formulario de edición con la configuración actual
        config_data = Config.get_config()
        return render_template('config_edit.html', config_data=config_data), 200

    except Exception as e:
        return jsonify({'error': 'Error al obtener la configuración', 'details': str(e)}), 500

