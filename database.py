import miniScrapper as sc
import sqlite3
import time

# - - - - - STOCK - - - - -
def agregarProductoStock(producto):
    if producto:
        print('Producto N°: ' + str(producto[0]))
        conn = sqlite3.connect("data/natura_v2.db")
        cursor = conn.cursor()
        precio_compra = float(input('Cuanto lo pagaste? '))
        fecha = time.localtime()
        fechaNum = str(fecha.tm_mday) + '/' + str(fecha.tm_mon) + '/' + str(fecha.tm_year)
        try:
            cursor.execute('''INSERT INTO stock (id_producto,precio_compra,fecha) VALUES(?,?,?)''',(producto[0],precio_compra,fechaNum))
            print(f'Producto: {producto[0]} cargado con exito.')
        except Exception as e:
            print(e)
            print(f'Error al cargar el producto {producto[0]}.')
        conn.commit()
        conn.close()
    else: print('No existe el producto.')

def eliminarProductoStock(productoStock):
    if productoStock:
        #print('Producto N°: ' + str(id_stock[0]))
        conn = sqlite3.connect("data/natura_v2.db")
        cursor = conn.cursor()
        try:
            cursor.execute('''DELETE FROM stock WHERE id = ?''',(productoStock[0],))
            print(f'Producto: {productoStock[1]} eliminado con exito.')
        except Exception as e:
            print(e)
            print(f'Error al eliminar el producto {productoStock[1]}.')
        conn.commit()
        conn.close()
    else: print('No existe el producto.')

def mostrarStock():
    conn = sqlite3.connect("data/natura_v2.db")
    cursor = conn.cursor()
    cursor.execute('''SELECT p.nombre, s.precio_compra, s.fecha
                    FROM stock s
                    JOIN productos p ON s.id_producto = p.id
                    ORDER BY p.nombre
                ''')
    productos = cursor.fetchall()
    i = 1
    for producto in productos:
        print(f'{i-1}. {producto}')
        i = i+1

def buscarProductoStock(producto):
    if producto:
        conn = sqlite3.connect("data/natura_v2.db")
        cursor = conn.cursor()
        cursor.execute('''SELECT s.id,p.nombre, s.precio_compra, s.fecha
                    FROM stock s
                    JOIN productos p ON s.id_producto = p.id
                    WHERE s.id_producto = ?''',(producto[0],))
        productos = cursor.fetchall()
        if len(productos) > 1:
            i = 1
            for producto in productos:
                print(f'{i-1}. {producto[1]} ${producto[2]}.')
                i = i+1
            productoStock = productos[int(input('Cual eliges? '))]
        elif len(productos) == 1: 
            print('Producto stock: '  + str(productos))
            productoStock = productos[0]
        else: 
            print('No existe el producto.')
            productoStock = None
        conn.commit()
        conn.close()
        return productoStock

def buscarProductoStockId(id):
    conn = sqlite3.connect("data/natura_v2.db")
    cursor = conn.cursor()
    cursor.execute('''SELECT s.id,p.nombre, s.precio_compra, s.fecha
                FROM stock s
                JOIN productos p ON s.id_producto = p.id
                WHERE s.id_producto = ?''',(id,))
    producto = cursor.fetchall()
    if producto:
        productoStock = producto[0]
    else: 
        print('No existe el producto.')
        productoStock = None
    conn.commit()
    conn.close()
    return productoStock          

# - - - - -  PRODUCTOS - - - - -
def buscarProducto():
    conn = sqlite3.connect("data/natura_v2.db")
    cursor = conn.cursor()
    nombre = '%' + input('Nombre del producto: ').lower() + '%'
    cursor.execute('''SELECT id, nombre FROM productos WHERE LOWER(nombre) LIKE ? ORDER BY nombre LIMIT 15 ''',(nombre,))
    productos = cursor.fetchall()
    if len(productos) > 1:
        i = 1
        for producto in productos:
            print(f'{i-1}. {producto[1]}')
            i = i+1
        producto = productos[int(input('Cual eliges? '))]
    elif len(productos) == 1: 
        print('Producto: '  + str(productos))
        producto = productos[0]
    else: 
        print('No existe el producto.')
        producto = None
    conn.commit()
    conn.close()
    return producto

def buscarProductoPorNombre(nombre):
    conn = sqlite3.connect("data/natura_v2.db")
    cursor = conn.cursor()
    cursor.execute('''SELECT id, nombre, marca FROM productos WHERE nombre LIKE ? ORDER BY nombre LIMIT 15 ''',(nombre,))
    producto = cursor.fetchone()
    conn.commit()
    conn.close()
    return producto

def buscarProductoIdPorNombre(nombre):
    conn = sqlite3.connect("data/natura_v2.db")
    cursor = conn.cursor()
    cursor.execute('''SELECT id FROM productos WHERE nombre LIKE ? ORDER BY nombre LIMIT 15 ''',(nombre,))
    producto = cursor.fetchone()
    conn.commit()
    conn.close()
    return producto[0]

def buscarProductoPorId(id):
    conn = sqlite3.connect("data/natura_v2.db")
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM productos WHERE id = ? ''',(id,))
    datos = cursor.fetchone()
    producto = {
        'id': datos[0],
        'nombre': datos[1],
        'marca': datos[2],
        'imagen': datos[3],
        'link': datos[4],
        'categoria': datos[5]
    }
    conn.commit()
    conn.close()
    return producto

def buscarProductos(nombre):
    conn = sqlite3.connect("data/natura_v2.db")
    cursor = conn.cursor()
    cursor.execute('''SELECT id, nombre, marca FROM productos WHERE LOWER(nombre) LIKE ? ORDER BY nombre ''',(f'%{nombre}%',))
    productos = cursor.fetchall()
    conn.commit()
    conn.close()
    return productos

# - - - - -  CLIENTES - - - - -
def agregarCliente(nombre,telefono,notas):
    cliente = {
        'nombre': nombre,
        'telefono': telefono,
        'notas': notas
    }
    conn = sqlite3.connect("data/natura_v2.db")
    cursor = conn.cursor()
    try:
        cursor.execute('''INSERT INTO clientes (nombre,telefono,notas) VALUES(?,?,?)''',(nombre,telefono,notas))
        print(f'Cliente: {nombre} cargado con exito.')
    except Exception as e:
        print(e)
        print(f'Error al cargar el cliente {nombre}.')
    conn.commit()
    conn.close()
    return buscarCliente(cliente['nombre'])

def eliminarCliente(id_cliente):
    conn = sqlite3.connect("data/natura_v2.db")
    cursor = conn.cursor()
    try:
        cursor.execute('''DELETE FROM clientes WHERE id = ?''',(id_cliente,))
        print(f'Cliente: {id_cliente} eliminado con exito.')
    except Exception as e:
        print(e)
        print(f'Error al eliminar el cliente {cliente[1]}.')
    conn.commit()
    conn.close()

def buscarCliente(nombre = None):
    conn = sqlite3.connect("data/natura_v2.db")
    cursor = conn.cursor()
    if nombre == None:
        nombre = '%' + input('Nombre del cliente: ').lower() + '%'
    cursor.execute('''SELECT id, nombre FROM clientes WHERE LOWER(nombre) LIKE ? LIMIT 15''',(nombre,))
    clientes = cursor.fetchall()
    if len(clientes) > 1:
        i = 1
        for cliente in clientes:
            print(f'{i-1}. {cliente[1]}')
            i = i+1
        cliente = clientes[int(input('Cual eliges? '))]
    elif len(clientes) == 1: 
        print('Cliente: '  + str(clientes))
        cliente = clientes[0]
    else: 
        print('No existe el cliente.')
        cliente = agregarCliente()
    conn.commit()
    conn.close()

    clientea = {
        'id': cliente[0],
        'nombre': cliente[1]
    }
    return clientea

def mostrarClientes():
    conn = sqlite3.connect("data/natura_v2.db")
    cursor = conn.cursor()
    cursor.execute('''SELECT id, nombre, telefono,notas FROM clientes''')
    clientes = [{"id": row[0], "nombre": row[1], "telefono": row[2], "notas": row[3]} for row in cursor.fetchall()]
    return clientes

def mostrarDatosCliente(cliente):
    conn = sqlite3.connect("data/natura_v2.db")
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM clientes WHERE id = ?''',(cliente[0],))
    datos = cursor.fetchall()
    print(datos)

def editarCliente(id,nombre,telefono,nota):
    conn = sqlite3.connect("data/natura_v2.db")
    cursor = conn.cursor()
    cursor.execute('''UPDATE clientes SET nombre = ?, telefono = ?, notas = ? WHERE id = ?''',(nombre,telefono,nota,id))
    conn.commit()
    conn.close()

def cargarPedido(datos):
    cliente = datos[0]
    productos = datos[1]
    if cliente == None:
        cliente = agregarCliente()
        
    fecha = time.localtime()
    fechaNum = str(fecha.tm_mday) + '/' + str(fecha.tm_mon) + '/' + str(fecha.tm_year)

    conn = sqlite3.connect("data/natura_v2.db")
    cursor = conn.cursor()

    precio_total = sum([p['precio'] * p['cantidad'] for p in productos])

    cursor.execute('''INSERT INTO pedidos (id_cliente,fecha,precio) VALUES(?,?,?)''',(cliente['id'], fechaNum, precio_total))
    cursor.execute('''SELECT id FROM pedidos WHERE id_cliente = ? AND fecha = ? AND precio = ? ORDER BY id DESC''',(cliente['id'], fechaNum, precio_total))
    idPedido = cursor.fetchone()[0]
    for producto in productos:
            id_producto = producto['id']
            precio_venta = producto['precio']
            origen = producto['origen']

            # Buscar costo según origen
            if origen == 'stock':
                cursor.execute('''
                    SELECT precio_compra FROM stock 
                    WHERE id_producto = ? 
                    ORDER BY id DESC LIMIT 1
                ''', (id_producto,))
                precio_compra = cursor.fetchone()[0]
                if precio_compra:
                    # Actualizar stock
                    #cursor.execute('''
                    #    DELETE FROM stock 
                    #    WHERE id_producto = ? AND precio_compra = ?
                    #    LIMIT 1 
                    #''', (id_producto, precio_compra))
                    print(f'Producto N: {producto['id']} eliminado de stock')

            elif origen == 'consultoria':
                precio_compra = float(input('Precio revista: '))
                print(f'Producto N: {producto['id']} añadido al pedido consultora')

            elif origen == 'web':
                precio_compra = obtenerPrecioWeb(producto)
                
            else:
                precio_compra = 0  # Por si viene algo inesperado

            if not precio_compra:
                print(f'Producto N: {producto['id']} no disponible, intenta por otro medio.')
                pass
            else:
                ganancia = (precio_venta - precio_compra)

                cursor.execute('''
                    INSERT INTO detalle_pedido 
                    (id_pedido, id_producto, precio_compra, precio_venta, ganancia, fecha, origen)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    idPedido, id_producto, precio_compra, precio_venta,
                    ganancia, fechaNum, origen
                ))
                print(f'Producto {producto['id']} agregado correctamente.')

    conn.commit()
    conn.close()
    print(f'Pedido: {idPedido} creado con exito.')

def obtenerPrecioWeb(id_producto):
    conn = sqlite3.connect("data/natura_v2.db")
    cursor = conn.cursor()
    cursor.execute('''SELECT link FROM productos WHERE id = ?''',(id_producto,))
    url = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    print(url)
    datos = sc.scrapear(url)
    if datos:
        if datos['precio_descuento']:  return (datos['precio_descuento'],datos['descuento'])
        elif datos['precio_original']: return (datos['precio_original'],datos['descuento'])
    else: return None

def crearPedido():
    cargar = True
    productos = []
    while cargar:
        producto = buscarProducto()
        if producto:
            origen = input('Origen: ')
            productos.append({
                'id': producto[0],
                'nombre':producto[1],
                'precio':float(input('Precio de venta: ')),
                'origen':origen,
                'cantidad':float(input('Cantidad: ')),
            })
        else:print('producto agotado')
        print('seguir cargando \n1. listo')
        if input() == '':
            pass
        else: cargar = False
    cliente = buscarCliente()
    print(cliente, productos)
    return (cliente, productos)

def agregarPedidoYDevolverId(cliente):
    conn = sqlite3.connect("data/natura_v2.db")
    cursor = conn.cursor()
    fecha = time.localtime()
    fechaNum = str(fecha.tm_mday) + '/' + str(fecha.tm_mon) + '/' + str(fecha.tm_year)
    cursor.execute('''INSERT INTO pedidos (id_cliente,fecha,precio) VALUES(?,?,?)''',(cliente, fechaNum, 0))
    cursor.execute('''SELECT id FROM pedidos WHERE id_cliente = ? AND fecha = ? AND precio = ? ORDER BY id DESC''',(cliente, fechaNum, 0))
    idPedido = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return idPedido

def agregarDetallePedido(id_pedido, id_producto, modo_venta, precio,precio_compra):
    conn = sqlite3.connect("data/natura_v2.db")
    cursor = conn.cursor()

    if modo_venta == 'stock':
        cursor.execute('''SELECT precio_compra FROM stock WHERE id_producto = ? ORDER BY id ASC ''',(id_producto,))
        precio_compra = cursor.fetchone()
        if precio_compra:
            precio_compra = precio_compra[0]
            cursor.execute('''INSERT INTO detalle_pedido (id_pedido,id_producto,precio_compra,precio_venta,origen) VALUES(?,?,?,?,?)''',(id_pedido, id_producto, precio_compra,precio, modo_venta))
            print('producto por stock')
        else: 
            return 'agotado'
    elif modo_venta == 'consultoria':
        cursor.execute('''INSERT INTO detalle_pedido (id_pedido,id_producto,precio_compra,precio_venta,origen) VALUES(?,?,?,?,?)''',(id_pedido, id_producto, precio_compra,precio, modo_venta))
        print('producto por consultoria')
    elif modo_venta == 'web':
        precio_compra = obtenerPrecioWeb(id_producto)
        if precio_compra:
            cursor.execute('''INSERT INTO detalle_pedido (id_pedido,id_producto,precio_compra,precio_venta,origen) VALUES(?,?,?,?,?)''',(id_pedido, id_producto, precio_compra,precio, modo_venta))
            print('producto por web')
        else: return 'agotado'
    conn.commit()
    conn.close()

def obtenerDetallePedido(id_pedido):
    conn = sqlite3.connect("data/natura_v2.db")
    cursor = conn.cursor()
    cursor.execute('''SELECT 
                  dp.id,
                  p.nombre,
                  dp.precio_compra,
                  dp.precio_venta,
                  dp.precio_venta - dp.precio_compra AS ganancia,
                  dp.origen
                FROM detalle_pedido dp
                JOIN productos p ON dp.id_producto = p.id
                WHERE dp.id_pedido = ?
                ''',(id_pedido,))
    datos = cursor.fetchall()
    conn.commit()
    conn.close()
    detalles = []
    for detalle in datos:
        detalle_producto = {
        'id': detalle[0],
        'producto':detalle[1],
        'precio_compra':detalle[2],
        'precio_venta':detalle[3],
        'ganancia':detalle[4],
        'origen':detalle[5]
        }
        detalles.append(detalle_producto)
    
    return detalles

def obtenerPedidos():
    conn = sqlite3.connect("data/natura_v2.db")
    cursor = conn.cursor()
    cursor.execute('''SELECT p.id,c.nombre,p.precio,p.fecha
                    FROM pedidos p
                    JOIN clientes c ON p.id_cliente = c.id
                   ORDER BY p.id DESC''')
    pedidos = cursor.fetchall()
    conn.commit()
    conn.close()
    return pedidos

def guardarPedido(id,precio):
    conn = sqlite3.connect("data/natura_v2.db")
    cursor = conn.cursor()
    cursor.execute('''UPDATE pedidos
                   SET precio = ?
                   WHERE id = ?''',(precio,id))
    conn.commit()
    conn.close()
    return

def borrarPedido(id):
    conn = sqlite3.connect("data/natura_v2.db")
    cursor = conn.cursor()
    cursor.execute('''DELETE FROM pedidos
                   WHERE id = ?''',(id,))
    conn.commit()
    conn.close()
    return
# ----- FUNCIONES STOCK -----
#   agregarProductoStock(buscarProducto())
#   mostrarStock()
#   buscarProductoStock(buscarProducto())
#   eliminarProductoStock(buscarProductoStock(buscarProducto()))
#   buscarProductoStockId(id)

# ----- FUNCIONES PRODUCTOS -----
#   buscarProducto()

# ----- FUNCIONES CLIENTES -----   
#   agregarCliente()
#   eliminarCliente(buscarCliente())
#   buscarCliente()
#   mostrarClientes()
#   mostrarDatosCliente(buscarCliente())

#cargarPedido((cliente,productos))

print(buscarProductoPorNombre('Kaiak Vital Femenino'))