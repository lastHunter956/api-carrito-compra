from flask import Flask, redirect, url_for, request,jsonify, session
from flask_mysqldb import MySQL


app = Flask(__name__)

#Conexion de la base de datos

app.config ['MYSQL_HOST'] = 'us-cdbr-east-06.cleardb.net'
app.config ['MYSQL_USER'] = 'bbd292aa23aeaf'
app.config ['MYSQL_PASSWORD'] = 'ece55924'
app.config ['MYSQL_DB'] = 'heroku_978ea61906c2949'

mysql = MySQL(app)

# Se define la direccion / en este caso para comprobar el funcionamiento

@app.route('/')
def index():
    return 'Hello word, Its an API'

# Se define la direccion de /add que seria cuando el usuario agrega un producto en el carrito de compras
@app.route("/add", methods=['POST'])
def add_product():
    cursor = None
    try:
        # Aca se edita para cantidad del pedido del producto
        _quantity = int(request.form['quantify'])
        _code = request.form('code')
        # Se ingresa la cantidad del pedido y se hace la conexion con la base de datos
        if _quantity and _code and request.method == 'POST':
            cursor= mysql.connection.cursor()
            sql= "SELECT Id_vehiculo, Nombre FROM heroku_978ea61906c2949.vehiculos WHERE Id_vehiculo ={0}".format(_code)
            cursor.execute(sql)
            datos = cursor.fetchone()
            itemarray={datos['Id_vehiculo']:{'Nombre': datos['Nombre'],'ID':datos['Id_vehiculo'], 'Cantidad':_quantity, 'Precio':datos['Precio'], 'Precio_total': _quantity * datos['Precio']}}
            all_total_price = 0
            all_total_quantity = 0
            session.modified = True
            # Para determinar si esta en seccion
            if 'cart_item' in session:
                #Se valida la conexion de la base de datos en la seccion
                if datos['Id_vehiculo'] in session['cart-item']:
                    for key, value in session['cart_item'].items():
                        if datos['Id_vehiculo']==key:
                            old_quantity = session['cart_item'][key]['quantity']
                            total_quantity = old_quantity+_quantity
                            session['cart_item'][key]['quantity'] = total_quantity
                            session['cart_item'][key]['total_price'] = total_quantity*datos['Precio']
                        # en est caso de que no
                        else:
                            session['cart_item'] =array_merge(session['cart_item'],itemarray)
                        for key, value in session['cart_item'].item():
                            individual_quantity = int(session['cart_item']['key']['quantity'])
                            individual_price = int(session['cart_item']['key']['total_price'])
                            all_total_quantity = all_total_quantity + individual_quantity
                            all_total_price = all_total_price + individual_price
            else:
                session['cart_item'] = itemarray
                all_total_quantity += _quantity
                all_total_price+= _quantity*datos['Precio']
            return redirect(url_for('.product'))
        #  En el caso de que no se conecta con data.
        else:
            return 'ERROR WHILE ADDING ITEM TO CART'
     # En el caso de que no se conecta con data.
    except Exception as e:
        return jsonify({'message': 'ERROR'})

# Se define el /stock para visualizar el stock de los productos
@app.route("/stock")
def product():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM  heroku_978ea61906c2949.vehiculos')
        datos = cursor.fetchall()
        vehiculos = []
        for fila in datos:
            dato = {'Id_vehiculo': fila[0], 'Nombre': fila[1], 'Modelo': fila[2] , 'Tipo': fila[3], 'Caracteristica': fila[4], 'Cantidad': fila[5] , 'Precio': fila[6]}
            vehiculos.append(dato)
        return jsonify({'vehiculos': vehiculos, 'message': 'OK'})
    except Exception as e:
        return jsonify({'message':'ERROR'})

# Se define el /empty para saber si esta conectado a una seccion de
@app.route('/empty')
def empty_cart():
    try:
        session.clear()
        return redirect(url_for('.product'))
    except Exception as e:
        return jsonify({'message': 'ERROR'})


# Se define /delete de un producto en especifico para quitar este producto del carrito de compras
@app.route('/delete/<string:code>')
def delete_product(code):
    try:
        all_total_price = 0
        all_total_quantity = 0
        session.modified = True
        for item in session['cart_item'].items():
            if item[0] == code:
                session['cart_item'].pop(item[0], None)
                if 'cart_item' in session:
                    for key, value in session['cart_item'].items():
                        individual_quantity= int(session['cart_item'] [key]['quantity'])
                        individual_price= float (session['cart_item'] [key] ['total_price'])
                        all_total_quantity = all_total_quantity + individual_quantity
                        all_total_price = all_total_price + individual_price
                        break
        if all_total_quantity == 0:
            session.clear()
        else:
            session['all_total_quantity'] = all_total_quantity
            session['all_total_price'] = all_total_price
        return redirect (url_for('.products'))
    except Exception as e:
        return jsonify({'message': 'ERROR'})




def array_merge( first_array, second_array):
    if isinstance( first_array, list) and isinstance( second_array, list):
        return first_array + second_array
    elif isinstance ( first_array, dict) and isinstance (second_array, dict ):
        return dict(list (first_array.items()) + list (second_array.items() ) )
    elif isinstance( first_array, set) and isinstance (second_array, set):
        return first_array.union (second_array)
    return False


if __name__=="__main__":
    app.run(debug=True, port=4000)