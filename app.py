from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'unaclavesecreta'

@app.route("/")
def carrito():
    # Verificar si 'lista' está en la sesión
    if 'lista' not in session:
        # Inicializar la lista como una lista vacía
        session['lista'] = []

    # Filtrar los elementos que tienen las claves 'precio' y 'cantidad'
    productos_validos = [item for item in session['lista'] if isinstance(item, dict) and 'precio' in item and 'cantidad' in item]
    
    # Calcular el total solo para los productos válidos
    total = sum(item['precio'] * item['cantidad'] for item in productos_validos)

    return render_template('index.html', lista=productos_validos, total=total)

@app.route("/proceso", methods=['POST'])
def procesa():
    producto = request.form.get("producto")
    try:
        precio = float(request.form.get("precio"))  # Convertir el precio a número
        cantidad = int(request.form.get("cantidad"))  # Convertir la cantidad a entero
    except ValueError:
        return redirect(url_for("carrito"))

    if 'lista' in session and producto and precio and cantidad:
        # Añadir el producto como un diccionario con su precio y cantidad
        session['lista'].append({'producto': producto, 'precio': precio, 'cantidad': cantidad})
        session.modified = True
    
    return redirect(url_for("carrito"))

@app.route("/vaciar", methods=["GET"])
def vaciar():
    # Eliminar la lista del carrito de la sesión
    session.pop("lista", None)
    return redirect(url_for("carrito"))

if __name__ == "__main__":
    app.run(debug=True)
