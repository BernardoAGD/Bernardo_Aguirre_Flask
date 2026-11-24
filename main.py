"""
Evaluación Unidad III - Programación Web
Aplicación Flask con menú principal y dos ejercicios con formularios.
Autor: Bernardo Aguirre D. - IPLACEX 2026
"""
from flask import Flask, render_template, request, redirect, url_for, abort

app = Flask(__name__)

# Rangos válidos del ejercicio 1
NOTA_MIN, NOTA_MAX = 10, 70
ASISTENCIA_MIN, ASISTENCIA_MAX = 0, 100
PROMEDIO_APROBACION = 40
ASISTENCIA_APROBACION = 75

# Registros almacenados en memoria (se pierden al reiniciar el servidor)
historial_notas = []
historial_nombres = []


# --------------------------------------------------------------------
# Funciones de lógica
# --------------------------------------------------------------------
def calcular_promedio(notas):
    """Retorna el promedio de una lista de notas redondeado a 1 decimal."""
    return round(sum(notas) / len(notas), 1)


def obtener_estado(promedio, asistencia):
    """Aprobado solo si el promedio es >= 40 Y la asistencia es >= 75%."""
    if promedio >= PROMEDIO_APROBACION and asistencia >= ASISTENCIA_APROBACION:
        return "APROBADO"
    return "REPROBADO"


def contar_letras(nombre):
    """Cuenta solo las letras del nombre (ignora espacios y otros símbolos)."""
    return sum(1 for caracter in nombre if caracter.isalpha())


def nombre_mas_largo(nombres):
    """Retorna la lista de nombres con más letras (más de uno si hay empate) y su cantidad."""
    maximo = max(contar_letras(n) for n in nombres)
    ganadores = [n for n in nombres if contar_letras(n) == maximo]
    return ganadores, maximo


# --------------------------------------------------------------------
# Rutas
# --------------------------------------------------------------------
@app.route("/")
def index():
    """Menú principal con los dos botones."""
    total_registros = len(historial_notas) + len(historial_nombres)
    return render_template("index.html", total_registros=total_registros)


@app.route("/ejercicio1", methods=["GET", "POST"])
def ejercicio1():
    """Formulario de notas: promedio y estado de aprobación."""
    resultado = None
    error = None
    datos = {"nota1": "", "nota2": "", "nota3": "", "asistencia": ""}

    if request.method == "POST":
        datos = {campo: request.form.get(campo, "").strip() for campo in datos}
        try:
            notas = [float(datos["nota1"]), float(datos["nota2"]), float(datos["nota3"])]
            asistencia = float(datos["asistencia"])

            if any(n < NOTA_MIN or n > NOTA_MAX for n in notas):
                error = f"Las notas deben estar entre {NOTA_MIN} y {NOTA_MAX}."
            elif asistencia < ASISTENCIA_MIN or asistencia > ASISTENCIA_MAX:
                error = f"La asistencia debe estar entre {ASISTENCIA_MIN} y {ASISTENCIA_MAX}."
            else:
                promedio = calcular_promedio(notas)
                estado = obtener_estado(promedio, asistencia)
                resultado = {"promedio": promedio, "estado": estado}
                historial_notas.append({"notas": notas, "asistencia": asistencia, **resultado})
        except ValueError:
            error = "Debes ingresar valores numéricos en todos los campos."

    return render_template("ejercicio1.html", resultado=resultado, error=error,
                           datos=datos, historial=historial_notas)


@app.route("/ejercicio2", methods=["GET", "POST"])
def ejercicio2():
    """Formulario de nombres: nombre con más caracteres y su cantidad."""
    resultado = None
    error = None
    datos = {"nombre1": "", "nombre2": "", "nombre3": ""}

    if request.method == "POST":
        datos = {campo: request.form.get(campo, "").strip() for campo in datos}
        nombres = list(datos.values())

        if any(contar_letras(n) == 0 for n in nombres):
            error = "Debes ingresar los 3 nombres."
        elif len({n.lower() for n in nombres}) < 3:
            error = "Los 3 nombres deben ser diferentes."
        else:
            ganadores, cantidad = nombre_mas_largo(nombres)
            resultado = {"ganadores": ganadores, "cantidad": cantidad}
            historial_nombres.append({"nombres": nombres, **resultado})

    return render_template("ejercicio2.html", resultado=resultado, error=error,
                           datos=datos, historial=historial_nombres)


@app.route("/ejercicio/<int:numero>")
def ejercicio(numero):
    """Ruta con parámetro por URL: redirige al ejercicio indicado o aborta si no existe."""
    if numero == 1:
        return redirect(url_for("ejercicio1"))
    if numero == 2:
        return redirect(url_for("ejercicio2"))
    abort(404)


@app.route("/historial/limpiar", methods=["POST"])
def limpiar_historial():
    """Borra los registros en memoria y vuelve al menú principal."""
    historial_notas.clear()
    historial_nombres.clear()
    return redirect(url_for("index"))


@app.errorhandler(404)
def pagina_no_encontrada(e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)
