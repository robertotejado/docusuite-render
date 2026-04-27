# 📚 DocuSuite IT/OT

![Python](https://img.shields.io/badge/python-3.11-blue.svg)
![Flask](https://img.shields.io/badge/flask-3.x-green.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Supabase-336791.svg)
![Cloudinary](https://img.shields.io/badge/CDN-Cloudinary-blue.svg)
![Docker](https://img.shields.io/badge/docker-ready-2496ED.svg)
![Render](https://img.shields.io/badge/Deployed_on-Render-46E3B7.svg)

**DocuSuite IT/OT** es una plataforma web profesional de alto rendimiento diseñada para la creación, gestión y exportación de documentación técnica. 

Optimizado para entornos de IT y Tecnología Operativa, el sistema utiliza una arquitectura **Cloud Native** que garantiza la portabilidad y persistencia de los datos mediante el uso de contenedores y servicios gestionados.

🚀 **Demo en vivo:** [https://docusuite-v1.onrender.com/](https://docusuite-v1.onrender.com/)

---

## ✨ Características Principales

* **Arquitectura Stateless:** Diseñada para ser desplegada en contenedores sin pérdida de datos.
* **Gestión Avanzada (CRUD):** Control total sobre proyectos y documentos con **paginación optimizada** (10 docs/pág) para manejar grandes volúmenes de información.
* **Editor WYSIWYG Pro:** Integración con **TinyMCE** y sistema de ofuscación de datos para máxima seguridad en el transporte de información.
* **Almacenamiento en CDN:** Subida automática de imágenes a **Cloudinary**, liberando carga al servidor y mejorando la velocidad de respuesta.
* **Exportación Profesional:** Generación de archivos **PDF** (via xhtml2pdf/Cairo), **DOCX** y **Markdown**.
* **Modo Oscuro/Claro:** Interfaz moderna y adaptable para largas jornadas de redacción técnica.

---

## 🛠️ Stack Tecnológico

* **Backend:** Python 3.11 (Slim-Debian), Flask, Flask-Login.
* **Base de Datos:** PostgreSQL (Supabase) con conexión robusta vía `psycopg2`.
* **Media:** Cloudinary SDK para gestión de adjuntos.
* **Contenedores:** Docker Hub como registro privado de imágenes.
* **Despliegue:** Render.com con pipeline de CI/CD.

---

## 🚀 Instalación y Uso (Local)

### Requisitos previos
* Docker y Docker Desktop (recomendado).
* Archivo `.env` configurado con tus credenciales.

### Pasos rápidos con Docker Compose
1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/robertotejado/docusuite-render.git](https://github.com/robertotejado/docusuite-render.git)
   cd docusuite-render

Lanzar la aplicación:

Bash
docker-compose up -d --build
Acceder: Abre http://localhost:5000

🐳 Flujo de Despliegue (DevOps)
El proyecto utiliza un flujo de versiones etiquetadas para garantizar la estabilidad:

Construir: docker build -t robertroof/docusuite:v5 .

Publicar: docker push robertroof/docusuite:v5

Desplegar: Actualizar el tag en el panel de Render para iniciar el despliegue automático.

👤 Autor
Roberto Tejado [https://www.linkedin.com/in/roberto-tejado/]

© 2006-Presente. Todos los derechos reservados.
