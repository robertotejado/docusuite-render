# 📚 DocuSuite IT/OT

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![Flask](https://img.shields.io/badge/flask-3.x-green.svg)
![Docker](https://img.shields.io/badge/docker-ready-blue.svg)
![SQLite](https://img.shields.io/badge/sqlite-integrated-lightgrey.svg)

**DocuSuite IT/OT** es una aplicación web profesional diseñada para la creación, gestión y exportación de documentación técnica orientada a proyectos de Informática (IT) y Tecnología Operativa (OT). 

Construida sobre una arquitectura ligera con **Flask** y **SQLite**, esta suite permite redactar documentos ricos en formato, adjuntar imágenes directamente desde el portapapeles y exportar el resultado final a formatos listos para producción (PDF con formato de paper académico, DOCX para Microsoft Word, y Markdown nativo).

---

## ✨ Características Principales

* **Gestión Centralizada (CRUD):** Creación, edición y borrado en cascada de Proyectos y Documentos.
* **Editor Avanzado:** Integración con **TinyMCE** para redacción WYSIWYG. Soporta pegado de imágenes desde el portapapeles (`Ctrl+V`) con guardado automático en el servidor.
* **Metadatos y Autoría:** Seguimiento de fechas de modificación y asignación de autoría a cada documento.
* **Exportación Multiformato:**
    * 📄 **PDF:** Generado mediante `xhtml2pdf` conservando tablas, imágenes y estilos.
    * 📝 **DOCX:** Exportación nativa a Microsoft Word preservando la semántica HTML mediante `htmldocx`.
    * 💻 **Markdown / TXT:** Conversión limpia para repositorios de código usando `markdownify`.
* **Interfaz Moderna:** Panel lateral colapsable, diseño responsivo y soporte nativo para **Modo Claro / Oscuro**.
* **DevOps Ready:** Contenedorizado con Docker, optimizado con librerías `C++` para renderizado gráfico.

---

## 🛠️ Stack Tecnológico

* **Backend:** Python 3.11+, Flask, SQLite3
* **Frontend:** HTML5, CSS3 (Variables nativas), JS Vainilla, Jinja2
* **Editor:** TinyMCE 6 (Vía CDN)
* **Motores de Exportación:** `xhtml2pdf` (PDF), `python-docx` + `htmldocx` (Word), `markdownify` (MD/TXT)

---

## 🚀 Instalación y Uso (Entorno Local)

### Requisitos previos
* Python 3.10 o superior.
* Una API Key gratuita de [TinyMCE](https://www.tiny.cloud/) (Añádela en `templates/editor.html`).

### Pasos de instalación

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/TU_USUARIO/docusuite_it_ot_flask.git](https://github.com/robertotejado/docusuite_it_ot_flask.git)
   cd docusuite_it_ot_flask
   ```

2. **Crear y activar un entorno virtual:**
   ```bash
   python -m venv venv
   # En Windows:
   venv\Scripts\activate
   # En Linux/Mac:
   source venv/bin/activate
   ```

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Ejecutar la aplicación:**
   ```bash
   python app.py
   ```
   *La base de datos SQLite y las carpetas de almacenamiento se crearán automáticamente al iniciar.*

5. **Acceder:** Abre tu navegador web en `http://127.0.0.1:5000`

---

## 🐳 Despliegue con Docker (Producción)

El proyecto incluye un `Dockerfile` optimizado que instala todas las dependencias del sistema operativo (C headers, Cairo, etc.) necesarias para procesar PDFs de forma robusta.

1. **Construir la imagen:**
   ```bash
   docker build -t docusuite-app .
   ```

2. **Ejecutar con volúmenes persistentes:**
   Para asegurar que la base de datos y las imágenes no se pierdan al reiniciar el contenedor, usa este comando:
   ```bash
   # Crear archivos preventivos
   touch docusuite.db
   mkdir -p attachments

   # Lanzar contenedor
   docker run -d \
     -p 5000:5000 \
     -v $(pwd)/docusuite.db:/app/docusuite.db \
     -v $(pwd)/attachments:/app/static/attachments \
     --name docusuite_server \
     docusuite-app
   ```

---

## 📂 Estructura del Proyecto

```text
docusuite_it_ot_flask/
├── app.py                  # Punto de entrada de la aplicación
├── requirements.txt        # Dependencias de Python
├── Dockerfile              # Configuración de contenedorización
├── .dockerignore           # Exclusiones de Docker
├── src/
│   ├── db/
│   │   └── database.py     # Lógica de SQLite e inicialización
│   ├── routes/
│   │   └── main_routes.py  # Controladores (Dashboard, CRUDs, Exportación)
│   └── utils/
│       └── exporters.py    # Motores de conversión (PDF, DOCX, MD)
├── static/
│   └── attachments/        # Almacenamiento local de imágenes
└── templates/              # Vistas HTML (Jinja2)
    ├── base.html           # Layout principal y menú lateral
    ├── splash.html         # Pantalla de carga
    ├── dashboard.html      # Panel principal
    ├── proyectos.html      # Gestión de proyectos
    ├── documentos.html     # Gestión de documentos
    └── editor.html         # Integración TinyMCE
```

---

## ☁️ Notas sobre despliegue en la Nube (Render, Heroku, etc.)
Si vas a desplegar esta aplicación en plataformas PaaS con sistemas de archivos efímeros (como el plan gratuito de Render.com):
* Deberás configurar un **Persistent Disk** para montar la ruta `/app/data`.
* Asegúrate de configurar tu comando de inicio (`Start Command`) para usar Gunicorn: `gunicorn app:app`.


render.com 
puedes ver la demo aquí: https://docusuite-it-ot.onrender.com/
---

## 👤 Autor

**Roberto Tejado** [[Enlace a LinkedIn](https://www.linkedin.com/in/roberto-tejado/)]

© 2006-Presente. Todos los derechos reservados.
```
# docusuite-render
# docusuite-render
