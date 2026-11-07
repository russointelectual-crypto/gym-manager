# Gym Manager

Sistema integral de gestión de clientes, disciplinas y ventas para gimnasios. Proyecto individual de **Taller de Aplicación en Internet** con Python, Flask-AppBuilder, MySQL y Git/GitHub.

## Qué cumple

- Seis tablas relacionadas: `clients`, `trainers`, `disciplines`, `memberships`, `enrollments` y `sales`.
- CRUD protegido por autenticación de Flask-AppBuilder.
- Reglas de negocio para correos, capacidad, duplicidad de inscripciones, fechas y montos.
- IA local gratuita con TF-IDF y similitud coseno para recomendar disciplinas según el objetivo del cliente.
- Tres reportes con consultas y filtros reales: ventas por período, membresías y ocupación.
- MySQL 8 mediante Docker Compose, con SQLite como modo rápido de demostración.
- Historial Git con ramas de funcionalidades.

## Instalación rápida

```bash
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
cp .env.example .env
python scripts/init_db.py
python scripts/seed_data.py
python scripts/create_admin.py
python run.py
```

Abre `http://127.0.0.1:5000` e inicia sesión con las credenciales de `.env`.

## Con MySQL

```bash
docker compose up -d mysql
cp .env.example .env
# DATABASE_URL del .env ya apunta al contenedor MySQL
python scripts/init_db.py
python scripts/seed_data.py
python scripts/create_admin.py
python run.py
```

## Rutas para la defensa

- CRUD: menú **Gestión**.
- IA: **Inteligencia Artificial > Recomendador IA** o `/ai/recommendations?client_id=1`.
- Reporte de ventas: `/reports/sales`.
- Reporte de membresías: `/reports/memberships`.
- Reporte de ocupación: `/reports/occupancy`.
- API JSON de recomendación: `/api/ai/recommendations/1`.

## Git y GitHub

El historial local incluye ramas separadas para modelo, IA y reportes. Para conectar el repositorio remoto:

```bash
git remote add origin https://github.com/USUARIO/gym-manager.git
git push -u origin main
git push origin feature/modelos feature/ia-recomendador feature/reportes
```

Después de crear el repositorio remoto, presenta `git log --oneline --graph --all`, `git branch -a` y la URL del repositorio como evidencias.

## Pruebas

```bash
pytest -q
```
