#from configparser import Error
#from re import S
from flask import Flask, render_template as rt, request, redirect, url_for
#import requests
from pyt import BDsql as bd
from pyt import Recursos as R, Cobranza as C
#from pyt import GEThtml as G
from pyt import PDF_ as P
#import time

app = Flask(__name__)

#configuracion
app.secret_key = 'mysecretkey'


@app.route('/')
def Index():
    return rt('index.html')


@app.route('/FacturaEgreso')
def egr():
    return rt('Factura_Egreso.html')


@app.route('/Registrar_Egreso',methods=['POST'])
def egreso():
    
    if request.method == 'POST':
        nombre = request.form['Pagado_a']
        telefono =  request.form['Telefono']
        correo =  request.form['NIT']
        Valor = request.form['Valor']
        direccion  = request.form['Direccion']
        clave=request.form['Consepto']
        fecha = request.form['Fecha']
        Observaciones=request.form['Observaciones']
        ultimo =bd.Ultimo_Registro('caja','Codigo_Caja')
        if(len(ultimo)!=0):
            total = int(ultimo[0][2])-int(Valor)
        else:
            total=int(Valor)
        todo=[0,'egreso',total]
        bd.Registrar(todo,"caja")
        
        ultimo_registro=bd.Ultimo_Registro('caja','Codigo_Caja')
        if(len(ultimo_registro)!=0):
            bd.Registrar([ultimo_registro[0][1],ultimo_registro[0][0]],'facturas_ingresos')
        bd.Registrar(
            [clave,ultimo_registro[0][0],Valor,fecha],
            'egresos'
        )
        P.Comprovante_EgresoCaja(
            nombre,correo,telefono,
            fecha,direccion,Valor,ultimo[0][0],
            clave,Observaciones)

    return rt('Egreso_Exitoso.html')



@app.route('/Admin_Caja')
def caja():
    #valores en caja
    Caja = bd.Consulta('caja')
    #variables
    total=[]
    tota=[]
    ingresos = bd.Consulta('ingresos')
    egresos = bd.Consulta('egresos')
    facturas=bd.Consulta('facturas_ingresos')
    #clientes = bd.Consulta('usuarios')
    cont=False
    
    if(len(Caja)!=0):
        #se rrecorre la cantidad de veces que los registros en caja
        for i in range(0,len(Caja)):
            #se agrega el codigo de caja
            total.append(Caja[i][0])
            #se condiciona que ingresos o egresos no puede estar vacio
            if(len(ingresos)!=0 or len(egresos)!=0):
                #se condiciona a ver si es ingreso o egreso para obtener la fecha
                if(Caja[i][1] == 'ingreso'):
                    #si es un ingreso se agrega la fecha
                    var=bd.Consultar('ingresos',Caja[i][0],'Codigo_Caja')
                    total.append(var[0][3])
                    #se condiciona a ver si es ingreso o egreso para obtener el valor
                    total.append(var[0][2])

                    #se agrega el nombre de cliente 
                    codigo_cliente=bd.Consultar('facturas_ingresos',Caja[i][0],'Codigo_Caja')

                    codigo_cliente=codigo_cliente[0][0]
                    n =bd.Consultar('usuarios',codigo_cliente,'ID_Usuarios')
                    if(len(n)!=0):
                        total.append(n[0][1])
                    else:
                        total.append(bd.Consultar('usuarios_eliminados',codigo_cliente,'ID_Usuarios')[0][1])
            
                    
                elif(len(egresos)!=0):
                    #se agrega la fecha
                    var=bd.Consultar('egresos',Caja[i][0],'Codigo_Caja')
                    total.append(var[0][3])
                    #se agrega el valor
                    total.append(var[0][2])
                    #se agrega el nombre de usuario
                    total.append('Egreso registrado')

            
            #SE AGREGA EL VALOR TOTAL HASTA ESE MOVIMIENTO
            total.append(Caja[i][2])
            #se agrega el tipo de transaccion
            total.append(Caja[i][1])
            #se agrega a el arreglo de informacion todo el arreglo de una factura
            tota.append(total)
            #se limpia el arreglo utilizado
            total=[]

    else:
        cont=True

    disp=bd.Ultimo_Registro("caja","Codigo_Caja")
    if(len(disp)!=0):
        disp=disp[0][2]
    else:
        disp=00
    return rt('Admin_Caja.html',total=tota,contenido=cont,disponible=disp)

@app.route('/Admin_Fac')
def adminfac():
    #valores en caja
    Caja = bd.Consulta('caja')
    #variables
    total=[]
    tota=[]
    ingresos = bd.Consulta('ingresos')
    egresos = bd.Consulta('egresos')
    clientes = bd.Consulta('usuarios')
    facturas=bd.Consulta('facturas_ingresos')
    cont=False
    
    if(len(facturas)!=0):

        #se rrecorre la cantidad de veces que los registros en caja
        for i in range(0,len(facturas)):
            #se agrega el codigo de caja
            total.append(Caja[i][0])
            #se condiciona que ingresos o egresos no puede estar vacio
            if(len(ingresos)!=0 or len(egresos)!=0):
                #se condiciona a ver si es ingreso o egreso para obtener la fecha
                if(Caja[i][1] == 'ingreso'):
                    #si es un ingreso se agrega el valor
                    var=bd.Consultar('ingresos',Caja[i][0],'Codigo_Caja')
                    print('este es var en ingresos: ',var)
                    total.append(var[0][3])
                    #se agrega el valor
                    total.append(var[0][2])


                    #se agrega el nombre de cliente 
                    codigo_cliente=bd.Consultar('facturas_ingresos',Caja[i][0],'Codigo_Caja')

                    codigo_cliente=codigo_cliente[0][0]
                    n =bd.Consultar('usuarios',codigo_cliente,'ID_Usuarios')
                    if(len(n)!=0):
                        total.append(n[0][1])
                    else:
                        total.append(bd.Consultar('usuarios_eliminados',codigo_cliente,'ID_Usuarios')[0][1])
            
                          
                else:
                    #se agrega el valor del egreso
                
                    var=bd.Consultar('egresos',Caja[i][0],'Codigo_Caja')
                    print('este es var en egresos: ',var)
                    total.append(var[0][3])
                    #se agrega el valor
                    total.append(var[0][2])
                    #se agrega el nombre de usuario
                    total.append('Egreso registrado')

            
            #se agrega a el arreglo de informacion todo el arreglo de una factura
            tota.append(total)
            #se limpia el arreglo utilizado
            total=[]

    else:
        cont=True

    
    return rt('Admin_Facturas.html',total=tota,contenido=cont)

@app.route('/AbonoCredito')
def abono():
    dat = bd.Consulta('usuarios')
    return rt('Seleccion_usuario.html',datos = dat)

@app.route('/perfil/<id>')
def perfil(id):
    try:
        dat = bd.Consultar('usuarios',id,'ID_Usuarios')[0]
    except:
        dat=[]
        
    fac = bd.Consulta('facturas_ingresos')
    contenido=False
    arreglo=[]
    a=[]

    if(len(fac)!=0):
        print('este es fac: ',fac)
        for i in fac:
            
            if ((i[0])==str(id)):
                m = bd.Consultar('ingresos',i[1],'Codigo_Caja')
                arreglo.append(i[1])
                #se agrega el valor
                arreglo.append(m[0][2])
                #se agrega la fecha
                arreglo.append(m[0][3])
                #elif(i[2]=='egreso'):
                #    m = bd.Consultar('egresos',i[0],'Codigo_Caja')
                a.append(arreglo)
            arreglo=[] 
    else:
        contenido=True
    #print(a)
    return rt('Perfil_usuario.html',user = dat,contenido=contenido,total=a)




@app.route('/action',methods=['POST'])
def c():
    #variables
    info_product = []
    valor=0
    todo_ingreso=[]
    todo_caja = ['0']
    precios=[]
    cantidades=[]
    total = 0
    #validacion del metodo post
    if (request.method == 'POST'):
        #recibir datos del formulario
        pago = request.form['pago']
        id = request.form['identificador']
        codigos = request.form['codigos']
        observaciones = request.form['observaciones']
        #se consulta el usuario de la compra
        #usuario = bd.Consultar_Usuario('usuarios',id)[0]
        codigos_clientes = R.codigo_clientes(id+';')
        #cada cliente se genera una factura con el fin de enviarla
        for m in codigos_clientes:
            #se consulta el ultimo valor registrado en la caja
            ultimo = bd.Ultimo_Registro('caja','Codigo_Caja')
            #se obtiene los codigos en un arreglo
            codig = R.codigo(codigos+';')
            #se obtiene las cantidades en un arreglo
            cantidades =R.cantidad(codigos+';')
            
            #llenar los arreglos de las tablas
            i=0
            for e in codig:
                #la tabla solo tiene cuatro columnas
                for s in range(0,4):
                    #se crea un arreglo con el producto para luego cambiar el valor de cantidad
                    info_product.append(bd.Consultar('productos',e,'Codigo')[0][s])
                #en el valor de que representa las cantidades disponibles
                #se hace la resta de la cantidad existente menos la cantidad comprada
                info_product[3] =str(int(bd.Consultar('productos',e,'Codigo')[0][3])-int(cantidades[i]))
                #se envia la modificacion del producto y se limpia el arreglo
                bd.Modificar('productos',e,info_product,'Codigo')
                info_product=[]
                #se agrega el precio del producto al arreglo
                precios.append(bd.Consultar("productos",e,"Codigo")[0][2])
                
                i=i+1
            i=0


            #se condiciona el ultimo registro de la tabla
            if(len(ultimo) == 0):
                #si no tiene registros el total sera la cantidad comprada
                for e in range(0,len(codig)):
                    total = total+(int(precios[e])*int(cantidades[e]))
                #valor de la compra
                valor = total
            else:
                #si tiene registros, el total sera el total del ultimo registro mas el valor de la compra
                for e in range(0,len(codig)):
                    total = total+(int(precios[e])*int(cantidades[e]))
                #valor de la compra
                valor = total
                #valor de la compra mas el ultimo total
                total = int(ultimo[0][2])
                for e in range(0,len(codig)):
                    total = total+(int(precios[e])*int(cantidades[e]))

            #registro en la caja
            #se agregan datos al arreglo de la tabla caja
            
            todo_caja.append('ingreso')
            todo_caja.append(total)
            #print(todo_caja)
            bd.Registrar(todo_caja,'caja')

            #se registra el codigo de factura en la tabla 'facturas_ingresos
            ultimo_=bd.Ultimo_Registro('caja','Codigo_Caja')
            print('este es ultimo_: ',ultimo_)
            factura=[m,ultimo_[0][0]]
            print('este es factura: ',factura)
            bd.Registrar(factura,'facturas_ingresos')
            
            #llenado del arreglo para ingresos
            todo_ingreso.append(codigos)
            #suspende la ejecucion por segundos.
            #time.sleep(0.5)
            #obtener el ultimo registro de la caja
            #print(bd.Ultimo_Registro('caja','Codigo_Caja'))
            res = bd.Ultimo_Registro('caja','Codigo_Caja')
            #condicionar su contenido
            if (len(res)==0):
                #nunca deveria entrar aqui
                todo_ingreso.append('indefinido')
            else:
                #se agrega el valor del codigo de caja
                todo_ingreso.append(res[0][0])
            #valor de la compra
            todo_ingreso.append(str(valor))
            todo_ingreso.append(R.fecha_())
            #hacer el registro en ingresos
            bd.Registrar(todo_ingreso,'ingresos')

            #print(total)
            data=[pago]
            #print(usuario)
            #se crea la factura de esta venta
            usuario = bd.Consultar('usuarios',m,'ID_Usuarios')[0]
            #print(usuario)
            P.Factura_Venta(usuario,data, codigos,observaciones)
            todo_ingreso=[]
            todo_caja=['0']
            precios=[]
            total=0
    #disp=bd.Ultimo_Registro("caja","Codigo_Caja")[0][3]
    
    return redirect('Admin_Caja')


@app.route('/CrearFactura')
def Crear_factura():
    dat=bd.Consulta('usuarios')
    product=bd.Consulta('productos')
    return rt('CrearFactura.html',datos=dat,product=product)


@app.route('/Clientes')
def Clientes():
    dat=[]
    name_columnas = bd.Nombre_Columnas("usuarios")
    cli = bd.Consulta("usuarios")
    for i in range(len(name_columnas)):
        if i < len(name_columnas)-1:
            #append añade un elemento a la lista
            dat.append(format(name_columnas[i+1][0])) 
    sin_contenido = True
    if len(cli) !=0:
        sin_contenido = False
    return rt('Cliente.html', dat_colum=dat, Clientes=cli,contenido=sin_contenido)

@app.route('/Productos')
def Productos():
    dat=[]
    name_columnas = bd.Nombre_Columnas("productos")
    cli = bd.Consulta("productos")
    for i in range(len(name_columnas)):
        if i < len(name_columnas):
            #append añade un elemento a la lista
            dat.append(format(name_columnas[i][0])) 
    sin_contenido = True
    if len(cli) !=0:
        sin_contenido = False
    return rt('Productos.html', dat_colum=dat, Clientes=cli,contenido=sin_contenido)


@app.route('/Producto_Nuevo', methods=['POST'])
def Produt_new():
   
    if request.method == 'POST':
        nombre = request.form['Descripcion']
        #codigo =  request.form['Codigo']
        precio = request.form['Precio']
        cantidad= request.form['Existencia']
        #fecha = R.fecha_hora()
        

        todo = ['0',nombre,precio,cantidad]
        bd.Registrar(todo,'productos')
        return redirect("/Productos")
   


@app.route('/Cliente_Nuevo', methods=['POST'])
def client_new():
   
    if request.method == 'POST':
        nombre = request.form['Nombre_Completo']
        telefono =  request.form['Telefono']
        correo =  request.form['Correo']
        Cedula = request.form['Cedula']
        direccion  = request.form['Direccion']
        clave=request.form['ID']
        fecha = request.form['Fecha_Afiliacion']
        try:
            recurrente=request.form['Cobro_recurrente']
        except:
            recurrente=False
        #print(recurrente)
        
        todo = [0,nombre,telefono,correo,
        Cedula,direccion, clave,fecha]
        bd.Registrar(todo,'usuarios')
        if (recurrente!=False):
            user=bd.Ultimo_Registro('usuarios','ID_Usuarios')[0]
            valores=[]
            #for i in user:
            valores.append(user[0])
            valores.append('1008-1')
            valores.append(user[7])
            valores.append('')
            bd.Registrar(valores,'creditos')
        return redirect("Clientes")
   

@app.route('/Eliminar_usuario/<string:id>')
def delete(id):
    todo=[]
    print(id)
    usuario = (bd.Consultar('usuarios',id,'ID_Usuarios')[0])
    for i in range(0,len(usuario)):
        if(i==0):
            todo.append(str(usuario[i]))
        elif(i==(len(usuario)-1)):
            todo.append(R.fecha_())
        else:
            todo.append(usuario[i])
    bd.Registrar(todo,'usuarios_eliminados')

    bd.Consulta_elimina("usuarios", id)
    

    return redirect(url_for("Clientes"))


@app.route('/Eliminar_producto/<string:id>')
def delete_produt(id):

    print(id)
    bd.elimina("productos", id,'Codigo')
    

    return redirect(url_for("Productos"))

@app.route('/Editar/<id>')
def edit(id):
    respuesta = bd.Consultar_Usuario("usuarios",id)
    credit = bd.Consultar('creditos',id,'ID_Usuarios')
    if(len(credit) !=0):
        cobrar = 'checked'
    else:
        cobrar=''
    return rt("Editar_Cliente.html", dat=respuesta[0],cobra = cobrar)

@app.route('/Editar_producto/<id>')
def edit_produt(id):
    respuesta = bd.Consultar("productos",id,"Codigo")
    return rt("Editar_Producto.html", dat=respuesta[0])

@app.route('/Modificar_Producto/<id>', methods=['POST'])
def Modificar_produt(id):
    if request.method == 'POST':
        nombre = request.form['Descripcion']
        codigo =  request.form['Codigo']
        precio = request.form['Precio']
        cantidad= request.form['Existencia']
        #fecha = R.fecha_hora()

        todo = [codigo,nombre, precio,cantidad]
        
        bd.Modificar("productos",id,todo,"Codigo")
        return redirect(url_for("Productos"))
  

@app.route('/Modificar/<id>', methods=['POST'])
def Modificar(id):
    fec=R.fecha_()
    if request.method == 'POST':
        nombre = request.form['Nombre_Completo']
        telefono =  request.form['Telefono']
        correo =  request.form['Correo']
        Cedula = request.form['Cedula']
        direccion = request.form['Direccion']
        Clave = request.form['ID']
        fecha = request.form['Fecha_Afiliacion']

        todo = [nombre, telefono, correo, Cedula, direccion, Clave, fecha]
        
        try:
            recurrente=request.form['Cobro_recurrente']
        except:
            recurrente=False
        #print(recurrente,id)
        if (recurrente!=False):
            try:
                credit=bd.Consultar('creditos',id,'ID_Usuarios')
            except IndexError:
                credit=[]
            if(len(credit)!=0):
                credit=credit[0]
            
            valores=[]
            
            #print(fec)
            if(len(credit)==0):
                valores.append(str(id))
                valores.append('1008-1')
                
                valores.append(fec)
                valores.append('')
                bd.Registrar(valores,'creditos')

            else:
                valores.append(credit[0])
                valores.append('1008-1')
                #fec=R.fecha_
                valores.append(credit[2])
                valores.append(credit[3])
                bd.Modificar('creditos',id,valores,'ID_Usuario')
            print(valores)
        else:
            bd.elimina('creditos',id,'ID_Usuarios')
        bd.Modificar_Usuario("usuarios",id,todo)
        return redirect(url_for("Clientes"))
        

@app.route('/Vehiculos')
def Vehiculos():
    dat=[]
    name_columnas = bd.Nombre_Columnas("vehiculos")
    cli = bd.Consulta("vehiculos")
    for i in range(len(name_columnas)):
        if i < len(name_columnas)-1:
            #append añade un elemento a la lista
            dat.append(format(name_columnas[i+1][0])) 
    sin_contenido = True
    if len(cli) !=0:
        sin_contenido = False
    return rt('Vehiculos.html', dat_colum=dat, vehiculos=cli,contenido=sin_contenido)

@app.route('/Vehiculo_Nuevo', methods=['POST'])
def vehicle_new():
   
    if request.method == 'POST':
        placa = request.form['placa']
        gps =  request.form['Modelo_GPS']
        sim =  request.form['Numero_simcard']
        vehiculo = request.form['Descripcion_Vehiculo']
        dueño=request.form['Dueño_Vehiculo']
        fecha = request.form['Fecha_Instalacion']
        imei= request.form['Imei']
        tipo = request.form['Tipo_Instalacion']

        todo = [0,placa,gps,sim,vehiculo,dueño,imei,tipo,fecha]
        bd.Registrar(todo,'vehiculos')
        return redirect("Vehiculos")

@app.route('/Editar_Vehiculo/<id>')
def EditVehicle(id):
    respuesta = bd.Consultar_Usuario("vehiculos",id)
    return rt("Editar_Vehiculo.html", dat=respuesta[0])

@app.route('/Modificar_Vehiculo/<id>', methods=['POST'])
def Modificar_Vehiculo(id):
    placa = request.form['placa']
    gps =  request.form['Modelo_GPS']
    sim =  request.form['Numero_simcard']
    vehiculo = request.form['Descripcion_Vehiculo']
    dueño=request.form['Dueño_Vehiculo']
    fecha = request.form['Fecha_Instalacion']
    imei= request.form['Imei']
    tipo = request.form['Tipo_Instalacion']
    todo = [0,placa,gps,sim,vehiculo,dueño,imei,tipo,fecha]
    bd.Modificar_Usuario("vehiculos",id,todo)
    return redirect(url_for("Vehiculos"))




#consultar quien debe pagar
C.consulta_pagos_pendientes()
if __name__ == '__main__':
    app.run(port = 9000,debug= False)