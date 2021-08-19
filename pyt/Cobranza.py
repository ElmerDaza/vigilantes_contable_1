import time
from datetime import datetime
from pyt import BDsql as bd, Recursos as R,PDF_ as P
#import para manejo de hilos
import threading


#___________________________________________
def ultima_fecha(String_fechas):
    #contador=len(String_meses)
    cadena=''
    for i in String_fechas:
        if(i!=','):
            cadena+=i
        else:
            cadena=''
    return cadena

def recordatorio_pago():
    #
    contador=1
    usuarios=bd.Consulta('creditos')

    if(len(usuarios)!=0):
        while contador !=0:
            usuarios=bd.Consulta('creditos')
            now = datetime.now()
            #Mesactual= now.month
            #print(now.hour,' entre en el bucle')
            #si son las 9 de la mañana enviará a cada usuario el recordatorio
            #de lo contrario esperara una hora mas
            if now.hour >= 8 and now.hour <=18:
                
                #se recorre cada suario
                for i in usuarios:
                    if(i[3]==''):
                        cantidad_meses_registro=R.cantidad_meses(i[2])
                        año,mes,dia_cobro=R.Seleccion_año_mes_dia(i[2])
                        if(cantidad_meses_registro>0 and int(dia_cobro)==now.day):
                            #se consulta el usuario
                            user = bd.Consultar('usuarios',i[0],'ID_Usuarios')
                            #se crea y envia la factura
                            P.Factura_Pago_Recurrente(user[0],'',i[1],'Recordatorio de compromiso')
                            #guardar los cambios en la tabla creditos
                            datos=[]
                            #se recorre el registro para recuperar los datos
                            for a in range(0,len(i)-1):
                                datos.append(i[a])
                            # se modifica las fechas de pago
                            datos.append(R.fecha_(Hora=False))
                            #se modifica el registro en la tabla creditos
                            bd.Modificar('creditos',i[0],datos,'ID_Usuarios')
                            print('primer cobro.',user[0])
                        else:
                            print('aun no es momento de cobrar. ',i)
                    else:
                        #cantidad_meses_registro=R.cantidad_meses(i[2])
                        u_fecha=ultima_fecha(i[3])
                        cantidad_meses_registro=R.cantidad_meses(u_fecha)
                        año,mes,dia_cobro=R.Seleccion_año_mes_dia(i[2])
                        if(cantidad_meses_registro>0 and int(dia_cobro)==now.day):
                            #se consulta el usuario
                            user = bd.Consultar('usuarios',i[0],'ID_Usuarios')
                            #se crea y envia la factura
                            P.Factura_Pago_Recurrente(user[0],'',i[1],'Recordatorio de compromiso')
                            #guardar los cambios en la tabla creditos
                            datos=[]
                            #se recorre el registro para recuperar los datos
                            for a in range(0,len(i)-1):
                                datos.append(i[a])
                            # se modifica las fechas de pago
                            fechas_cobro=i[3]+','+R.fecha_()
                            datos.append(fechas_cobro)
                            #se modifica el registro en la tabla creditos
                            bd.Modificar('creditos',i[0],datos,'ID_Usuarios')
                            print('otro cobro mas.', user[0])
                        else:
                            print('aun no es momento de cobrar. ',i)
                time.sleep(60)

                
            else:
                #suspende la ejecucion por 1 hora
                time.sleep(3600)
    else:
        print('no hay registros en la tabla creditos.')
        time.sleep(3600)
        recordatorio_pago()

def consulta_pagos_pendientes():
    hilo1=threading.Thread(target=recordatorio_pago)
    hilo1.start()