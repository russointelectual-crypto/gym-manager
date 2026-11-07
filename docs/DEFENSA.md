# Guion de defensa y evidencias

## 1. Modelo de datos

- `Client` es el centro del negocio y se relaciona con `Membership`, `Enrollment` y `Sale`.
- `Trainer` administra las disciplinas que imparte.
- `Discipline` se relaciona con `Trainer` y `Enrollment`.
- `Membership` pertenece a un cliente y puede asociarse a ventas.
- `Enrollment` resuelve la relación entre clientes y disciplinas.
- `Sale` registra el ingreso de un cliente y, opcionalmente, la membresía pagada.

## 2. Operaciones CRUD

Desde el menú Gestión se puede listar, crear, consultar, editar y eliminar cada entidad. Las vistas generan permisos de Flask-AppBuilder y requieren sesión autenticada.

## 3. Inteligencia artificial

El cliente tiene un objetivo escrito. El sistema transforma ese texto y la información de cada disciplina en vectores TF-IDF. La similitud coseno ordena las disciplinas y presenta las tres con mayor coincidencia. El modelo corre localmente con scikit-learn.

## 4. Reportes verificables

- Ventas por período y método de pago, con total calculado.
- Membresías agrupadas por plan y estado, con ingreso mensual estimado.
- Ocupación por disciplina comparando inscripciones activas con capacidad.

## 5. Evidencias que se deben capturar

1. Inicio de sesión y menú protegido.
2. Vista de seis tablas y formularios CRUD.
3. Recomendación IA para `Ana Flores` o `Diego Mamani`.
4. Cada reporte con filtros y resultados.
5. `git branch -a`.
6. `git log --oneline --graph --all`.
7. Repositorio remoto y ramas publicadas.
8. Resultado de `pytest -q`.

## 6. Comandos de evidencia

```bash
git status
git branch -a
git log --oneline --decorate --graph --all
pytest -q
```
