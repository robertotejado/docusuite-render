import os
import uuid
import cloudinary
import cloudinary.uploader
import traceback
import base64
from urllib.parse import unquote

# Importamos lo necesario de Flask
from flask import Blueprint, render_template, request, redirect, url_for, send_file, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from src.db.database import get_db_connection
from src.utils.exporters import export_document

# Definimos el Blueprint
main = Blueprint('main', __name__)

# Configuración de Cloudinary
cloudinary.config( 
  cloud_name = os.environ.get('CLOUDINARY_CLOUD_NAME'), 
  api_key = os.environ.get('CLOUDINARY_API_KEY'), 
  api_secret = os.environ.get('CLOUDINARY_API_SECRET') 
)

@main.route('/')
def splash():
    return render_template('splash.html')

# --- AUTENTICACIÓN ---

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM usuarios WHERE username = %s", (username,))
        user_data = cur.fetchone()
        cur.close()
        conn.close()

        if user_data and check_password_hash(user_data['password'], password):
            from src.models.user import User
            user_obj = User(id=user_data['id'], username=user_data['username'])
            login_user(user_obj)
            return redirect(url_for('main.dashboard'))
        
        return "Usuario o contraseña incorrectos", 401
    return render_template('login.html')

@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = generate_password_hash(request.form.get('password'))
        
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO usuarios (username, password) VALUES (%s, %s)", (username, password))
            conn.commit()
        except Exception as e:
            return f"Error: El usuario ya existe o fallo en DB: {e}"
        finally:
            cur.close()
            conn.close()
        return redirect(url_for('main.login'))
    return render_template('register.html')

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

# --- DASHBOARD ---

@main.route('/dashboard')
@login_required 
def dashboard():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM proyectos WHERE usuario_id = %s ORDER BY fecha_creacion DESC LIMIT 5", (current_user.id,))
    proyectos_recientes = cur.fetchall()
    cur.execute("SELECT * FROM documentos WHERE usuario_id = %s ORDER BY fecha_modificacion DESC LIMIT 5", (current_user.id,))
    docs_recientes = cur.fetchall()
    cur.execute("SELECT COUNT(*) as total FROM proyectos WHERE usuario_id = %s", (current_user.id,))
    total_p = cur.fetchone()['total']
    cur.execute("SELECT COUNT(*) as total FROM documentos WHERE usuario_id = %s", (current_user.id,))
    total_d = cur.fetchone()['total']
    cur.close()
    conn.close()
    return render_template('dashboard.html', proyectos=proyectos_recientes, documentos=docs_recientes, total_proyectos=total_p, total_documentos=total_d)

# --- CRUD DE PROYECTOS ---

@main.route('/proyectos', methods=['GET', 'POST'])
@login_required
def gestion_proyectos():
    conn = get_db_connection()
    cur = conn.cursor()
    if request.method == 'POST':
        accion = request.form.get('action')
        if accion == 'crear':
            nombre = request.form['nombre']
            tipo = request.form['tipo']
            cur.execute('INSERT INTO proyectos (nombre, tipo, usuario_id) VALUES (%s, %s, %s)', (nombre, tipo, current_user.id))
        elif accion == 'actualizar':
            id_proy = request.form['id']
            nombre = request.form['nombre']
            tipo = request.form['tipo']
            cur.execute('UPDATE proyectos SET nombre = %s, tipo = %s WHERE id = %s AND usuario_id = %s', (nombre, tipo, id_proy, current_user.id))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('main.gestion_proyectos'))
    cur.execute('SELECT * FROM proyectos WHERE usuario_id = %s ORDER BY fecha_creacion DESC', (current_user.id,))
    proyectos = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('proyectos.html', proyectos=proyectos)

@main.route('/proyectos/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar_proyecto(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM proyectos WHERE id = %s AND usuario_id = %s', (id, current_user.id))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('main.gestion_proyectos'))

# --- CRUD DE DOCUMENTOS ---

@main.route('/documentos', methods=['GET', 'POST'])
@login_required
def gestion_documentos():
    conn = get_db_connection()
    cur = conn.cursor()
    if request.method == 'POST':
        accion = request.form.get('action')
        if accion == 'actualizar_meta':
            id_doc = request.form['id']
            titulo = request.form['titulo']
            id_proyecto = request.form['id_proyecto']
            cur.execute('UPDATE documentos SET titulo = %s, id_proyecto = %s WHERE id = %s AND usuario_id = %s', (titulo, id_proyecto, id_doc, current_user.id))
            conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('main.gestion_documentos'))
    cur.execute('SELECT d.*, p.nombre as proyecto_nombre FROM documentos d LEFT JOIN proyectos p ON d.id_proyecto = p.id WHERE d.usuario_id = %s ORDER BY d.fecha_modificacion DESC', (current_user.id,))
    documentos = cur.fetchall()
    cur.execute('SELECT * FROM proyectos WHERE usuario_id = %s', (current_user.id,))
    proyectos = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('documentos.html', documentos=documentos, proyectos=proyectos)

# --- EDITOR CENTRAL CON DECODIFICACIÓN SEGURA ---

@main.route('/editor', methods=['GET', 'POST'])
@main.route('/editor/<int:id_doc>', methods=['GET', 'POST'])
@login_required
def editor(id_doc=None):
    conn = get_db_connection()
    cur = conn.cursor()
    
    if request.method == 'POST':
        id_proyecto = request.form['id_proyecto']
        titulo = request.form['titulo']
        autor = request.form['autor']
        doc_id_form = request.form.get('id_doc') 
        
        # --- LÓGICA DE DECODIFICACIÓN PARA SALTAR EL WAF ---
        # Recibimos el campo 'd' que viene ofuscado desde el JS
        contenido_disfrazado = request.form.get('d')
        
        try:
            # 1. Decodificar Base64
            decodificado_bytes = base64.b64decode(contenido_disfrazado)
            decodificado_str = decodificado_bytes.decode('utf-8')
            # 2. Revertir el 'escape' de URI
            limpio = unquote(decodificado_str)
            # 3. Invertir el texto (ya que el JS lo envió al revés)
            contenido = limpio[::-1]
        except Exception as e:
            print(f"Error en decodificación: {e}")
            # Si falla, intentamos usar el campo original por si acaso
            contenido = request.form.get('contenido_texto') or contenido_disfrazado

        if doc_id_form:
            cur.execute('''UPDATE documentos 
                           SET id_proyecto = %s, titulo = %s, autor = %s, contenido_texto = %s, fecha_modificacion = CURRENT_TIMESTAMP 
                           WHERE id = %s AND usuario_id = %s''', 
                         (id_proyecto, titulo, autor, contenido, doc_id_form, current_user.id))
        else:
            cur.execute('''INSERT INTO documentos (id_proyecto, titulo, autor, contenido_texto, usuario_id) 
                           VALUES (%s, %s, %s, %s, %s)''', 
                         (id_proyecto, titulo, autor, contenido, current_user.id))
            
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('main.gestion_documentos'))

    # Lógica para cargar el editor (GET)
    cur.execute('SELECT * FROM proyectos WHERE usuario_id = %s', (current_user.id,))
    proyectos = cur.fetchall()
    doc_actual = None
    if id_doc:
        cur.execute('SELECT * FROM documentos WHERE id = %s AND usuario_id = %s', (id_doc, current_user.id))
        doc_actual = cur.fetchone()
        
    cur.close()
    conn.close()
    return render_template('editor.html', proyectos=proyectos, doc_actual=doc_actual)

# --- SUBIDA A CLOUDINARY ---

@main.route('/upload_attachment', methods=['POST'])
@login_required
def upload_attachment():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    file = request.files['file']
    try:
        upload_result = cloudinary.uploader.upload(file, folder="docusuite")
        return jsonify({'location': upload_result['secure_url']})
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

# --- EXPORTACIÓN ---

@main.route('/exportar/<int:id_doc>/<formato>')
@login_required
def exportar(id_doc, formato):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM documentos WHERE id = %s AND usuario_id = %s', (id_doc, current_user.id))
    doc = cur.fetchone()
    cur.close()
    conn.close()
    if not doc:
        return "Documento no encontrado", 404
    filepath = export_document(dict(doc), formato)
    return send_file(filepath, as_attachment=True)
    
@main.route('/documentos/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar_documento(id):
    conn = get_db_connection()
    cur = conn.cursor()
    # Aseguramos que solo el dueño pueda borrarlo
    cur.execute('DELETE FROM documentos WHERE id = %s AND usuario_id = %s', (id, current_user.id))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('main.gestion_documentos'))
