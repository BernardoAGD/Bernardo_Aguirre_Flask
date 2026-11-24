# Ejercicios Flask — Bernardo Aguirre D.

Evaluación de Programación Web (IPLACEX 2026). Aplicación Flask con un menú principal y dos ejercicios con formularios.

- **Ejercicio 1:** recibe 3 notas (10 a 70) y la asistencia (0 a 100). Calcula el promedio y muestra APROBADO si el promedio es ≥ 40 y la asistencia es ≥ 75%; si no, REPROBADO.
- **Ejercicio 2:** recibe 3 nombres distintos y muestra el que tiene más caracteres (letras) y cuántos tiene.

## Estructura

```
Bernardo_Aguirre_Flask/
├── main.py
├── requirements.txt
├── static/css/styles.css
└── templates/
    ├── base.html
    ├── index.html
    ├── ejercicio1.html
    ├── ejercicio2.html
    └── 404.html
```

## Ejecución

```
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
python main.py
```

Abrir http://127.0.0.1:5000
