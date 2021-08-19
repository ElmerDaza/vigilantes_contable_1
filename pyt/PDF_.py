from pyt import BDsql as bd,Recursos as R

#libreria para generar pdf
from fpdf import FPDF
import time
#numeos aleatorios
import random
#fecha
from datetime import datetime as dt

#Comprovante de egreso________________
def Comprovante_EgresoCaja(Nombre,NIT,Telefono,fech,direct,valor,Codigo_Caja,Consept,observaciones):
    #variables de contenido
    w=30#width
    w2=105
    h=5#height
    #tamaño de letra
    fz=9#font zise
    font='arial'


    nombre = Nombre
    cedula = NIT
    telefono=Telefono
    fecha=fech
    fpago='efectivo'
    direccion=direct
    total=valor
    total_letra=R.numero_a_moneda(int(valor))
    NumRecibo = Codigo_Caja
    consepto=Consept

    #clase para encabezado
    titulo_header = "GPS VIGILANTES 24/7"
    #datos del encabezado
    meta_dat = 'NIT: 1041610630-8 Carrera 7H #34-45 Tel: 3104279136 Riohacha - Colombia'
    class PDF(FPDF):
        def header(self):
            #logo o imagen
            self.image('static/img/logo.jpg',25,10,30)
            self.set_font(font,'B', 13)
            #padding
            self.cell(10)
            #texto de encavezado
            self.cell(0,10,titulo_header, border=False, ln=1, align='C')
            #self.cell(0,25, meta_dat,ln=1,align='C')
            self.cell(85)
            self.set_font(font,'', 9)
            self.multi_cell(32,3,meta_dat,border=False,align='C')
            self.set_font(font,'B', 10)
            self.cell(0,10,"Recibo N° "+format(NumRecibo),align='R',ln=1)
            self.cell(0,30)
            #espacio adicional
            self.ln(2)

        #pie de pagina
        def footer(self):
            #posicion de texto
            self.set_y(-20)
            # agregar tipografia
            self.set_font('courier', 'I', 7)
            #agregar paginacion
            self.cell(0, 20, f'pagina {self.page_no()}/{{nb}}', align='C')

    #objeto pdf:
    #('layaut', 'unidades', 'tamaño de papel')
    pdf = PDF('P','mm','Letter')
    #get total pages nunbers
    pdf.alias_nb_pages()
    #agregar pagina
    pdf.add_page()
    #especificar tipografia
    #tipografia disponible: times, courier, helvetica, symbol, zpdfdingbats,DroidSans(arial)
    #'B' negrita, 'U' subrallado, 'I' cursiva,'' regular
    pdf.set_font(font,'B',fz)


    #agregar texto
    #('with', 'height', 'String')
    pdf.cell(w-10, h, 'Pagado a ', border=True)
    pdf.set_font(font,'',fz)
    pdf.cell(w2, h, nombre, border=True)
    pdf.set_font(font,'B', fz)
    pdf.cell(5, h, '')
    pdf.cell(w, h, 'Fecha de pago', border=True)
    pdf.cell(w+5, h, 'Forma de pago',ln=1, border=True)


    pdf.cell(w-10, h, 'NIT', border=True)
    pdf.set_font(font,'', fz)
    pdf.cell(w, h, cedula, border=True)
    pdf.set_font(font,'B', fz)
    pdf.cell(w-10, h, 'Teléfono', border=True)
    pdf.set_font(font,'', fz)
    pdf.cell(w+25, h, telefono, border=True)
    pdf.cell(5, h, '')
    pdf.cell(w, h*2, fecha, border=True)
    pdf.cell(w+5,h*2,fpago, border=True)
    pdf.set_font(font,'B', fz)
    pdf.cell(0, h, '',ln=1)


    pdf.cell(w-10, h, 'Direccion', border=True)
    pdf.set_font(font,'', fz)
    pdf.cell(w, h, direccion, border=True)
    pdf.set_font(font,'B', fz)
    pdf.cell(w-10, h, 'Ciudad', border=True)
    pdf.set_font(font,'', fz)
    pdf.cell(w+25, h, 'Riohacha - Colombia',ln=1, border=True)



    pdf.cell(w,h,'',ln=1)
    pdf.cell(w,h,'El valor de ',border=True)
    pdf.cell(135,h,total_letra,border=True)
    pdf.cell(w,h,format(total),border=True,align='R',ln=1)
    pdf.cell(w,h,ln=1)

    pdf.set_font(font,'B',fz)
    pdf.cell(165,h,'Consepto',border=True,align='C')
    pdf.cell(w,h,'Valor',border=True,ln=1)

    pdf.set_font(font,'',fz)
    pdf.cell(165,h,consepto,border=True)
    pdf.cell(w,h,format(total),ln=1,border=True,align='R')


    pdf.cell(135,h)
    pdf.cell(w,h,'Total COP')
    pdf.cell(w,h,format(total),ln=1,align='R')


    pdf.cell(0,4,ln=1)
    pdf.cell(0,h,'Observaciones:',border='LTR',ln=1)
    pdf.cell(0,h*5,observaciones,border='LBR')
    pdf.cell(w*3.25,h*4,'')
    pdf.cell(w*3.25,h*2,'',ln=1)
    pdf.cell(0,h,ln=1)
    pdf.cell(w*3.25,h,'_________________________', align='C')
    pdf.cell(w*3.25,h,'_________________________',align='C',ln=1)
    pdf.cell(w*3.25,h,'Firma elaborado', align='C')
    pdf.cell(w*3.25,h,'Firma recibido',align='C',ln=1)
    pdf.cell(w,h,'')

    filename=f'Factura_Egreso_{NumRecibo}.pdf'

    pdf.output('pdf/egreso/'+filename,'F')



#Recibo de caja_____________
def Recibo_caja(id,consepto,valor,forma_pago):

    #variables de contenido
    w=30#width
    w2=105
    h=7#height
    #tamaño de letra
    fz=11#font zise
    font='arial'


    nombre = ''
    cedula = ''
    telefono=''
    fecha=''
    fpago=''
    direccion=''
    total=0
    total_letra=''

    #clase para encabezado
    titulo_header = "GPS VIGILANTES 24/7"
    #datos del encabezado
    meta_dat = 'NIT: 1041610630-8 Carrera 7H #34-45 Tel: 3104279136 Riohacha - Colombia'
    class PDF(FPDF):
        def header(self):
            #logo o imagen
            self.image('static/img/logo.jpg',10,8,45)
            self.set_font(font,'B', 13)
            #padding
            self.cell(10)
            #texto de encavezado
            self.cell(0,10,titulo_header, border=False, ln=1, align='C')
            #self.cell(0,25, meta_dat,ln=1,align='C')
            self.cell(85)
            self.set_font(font,'', 9)
            self.multi_cell(32,3,meta_dat,border=False,align='C')
            self.set_font(font,'B', 10)
            self.cell(0,10,"Recibo N° 1221",align='R',ln=1)
            self.cell(0,30)
            #espacio adicional
            self.ln(2)
        
        #pie de pagina
        def footer(self):
            #posicion de texto
            self.set_y(-20)
            # agregar tipografia
            self.set_font('courier', 'I', 13)
            #agregar paginacion
            self.cell(0, 20, f'pagina {self.page_no()}/{{nb}}', align='C')

    #objeto pdf:
    #('layaut', 'unidades', 'tamaño de papel')
    pdf = PDF('P','mm','Letter')
    #get total pages nunbers
    pdf.alias_nb_pages()
    #agregar pagina
    pdf.add_page()
    #especificar tipografia
    #tipografia disponible: times, courier, helvetica, symbol, zpdfdingbats,DroidSans(arial)
    #'B' negrita, 'U' subrallado, 'I' cursiva,'' regular
    pdf.set_font('arial','B',12)

    #agregar texto
    #('with', 'height', 'String')
    
    pdf.cell(w, h, 'Recibimos de ', border=True)
    pdf.set_font(font,'',fz)
    pdf.cell(w2, h, nombre, border=True)
    pdf.set_font(font,'B', fz)
    pdf.cell(w, h, 'Fecha recibo', border=True)
    pdf.cell(w, h, 'Forma de pago',ln=1, border=True)


    pdf.cell(w, h, 'NIT', border=True)
    pdf.set_font(font,'', fz)
    pdf.cell(w+15, h, cedula, border=True)
    pdf.set_font(font,'B', fz)
    pdf.cell(w, h, 'Teléfono', border=True)
    pdf.set_font(font,'', fz)
    pdf.cell(w, h, telefono, border=True)
    pdf.cell(w, h, fecha, border=True)
    pdf.cell(w,h,fpago,ln=1, border=True)
    pdf.set_font(font,'B', fz)


    pdf.cell(w, h, 'Direccion', border=True)
    pdf.set_font(font,'', fz)
    pdf.cell(w+15, h, direccion, border=True)
    pdf.set_font(font,'B', fz)
    pdf.cell(w, h, 'Ciudad', border=True)
    pdf.set_font(font,'', fz)
    pdf.cell(w*3, h, 'Riohacha - Colombia',ln=1, border=True)
    pdf.cell(0,h/2,ln=1)

    pdf.set_font(font,'B', fz)
    pdf.cell((w*5)+15,h,'El valor de '+total_letra+' m/cte',border=True)
    pdf.set_font(font,'', fz)
    pdf.cell(w,h,format(total),border=True,align='R',ln=1)
    pdf.cell(0,4,ln=1)


    pdf.set_font(font,'B', fz)
    pdf.cell((w*5)+15,h,'Consepto', align='C')
    pdf.cell(w,h,'Valor',align='C',ln=1)
    for i in range(0,len(consepto)):
        pdf.cell(w,h)
    pdf.set_font(font,'B',fz)
    pdf.cell((w*5)+15,h,align='R')
    pdf.cell(w,h,format(total),align='C',ln=1)
    pdf.cell(0,4,ln=1)
    pdf.cell(0,h,'Observaciones:',border='LTR',ln=1)
    pdf.cell(0,h*5,'',border='LBR')
    pdf.cell(w*3.25,h*4,'')
    pdf.cell(w*3.25,h*2,'',ln=1)
    pdf.cell(0,h,ln=1)
    pdf.cell(w*3.25,h,'_________________________', align='C')
    pdf.cell(w*3.25,h,'_________________________',align='C',ln=1)
    pdf.cell(w*3.25,h,'Firma elaborado', align='C')
    pdf.cell(w*3.25,h,'Firma recibido',align='C',ln=1)
    #guardar pdf
    pdf.output('pdf_prueva_Caja.pdf')

#Recibo_caja('','','','')
#factura de venta_____________________
def Factura_Venta(usuario,datos,codigos,observaciones):

    #contenido de codigos producto
    A = codigos+';'
    codigos=R.codigo(A)
    cantidades=R.cantidad(A)
    productos=[]
    precios=[]
    cadena=''
    contador=0
    
    #variables de contenido
    w=30#width
    w2=105
    h=5#height
    #tamaño de letra
    fz=9#font zise
    font='arial'


    nombre = usuario[1]
    cedula = usuario[4]
    telefono=usuario[2]
    fecha=R.fecha_()
    fpago=datos[0]
    direccion = usuario[5]
    total=0
    NumRecibo =bd.Ultimo_Registro('caja','Codigo_Caja')[0][0]
    
    
    

    for e in codigos:
        productos.append(bd.Consultar("productos",e,"Codigo")[0][1])
        precios.append(bd.Consultar("productos",e,"Codigo")[0][2])

    for e in range(0,len(productos)):
        total = total+(int(precios[e])*int(cantidades[e]))
    total_letra= R.numero_a_letras(total)
    #clase para encabezado
    titulo_header = "GPS VIGILANTES 24/7"
    #datos del encabezado
    meta_dat = 'NIT: 1041610630-8 Carrera 7H #34-45 Tel: 3104279136 Riohacha - Colombia'
    class PDF(FPDF):
        def header(self):
            #logo o imagen
            self.image('static/img/logo.jpg',25,10,30)
            self.set_font(font,'B', 13)
            #padding
            self.cell(10)
            #texto de encavezado
            self.cell(0,10,titulo_header, border=False, ln=1, align='C')
            #self.cell(0,25, meta_dat,ln=1,align='C')
            self.cell(85)
            self.set_font(font,'', 9)
            self.multi_cell(32,3,meta_dat,border=False,align='C')
            self.set_font(font,'B', 10)
            self.cell(0,10,"Recibo N° "+format(NumRecibo),align='R',ln=1)
            self.cell(0,30)
            #espacio adicional
            self.ln(2)

        #pie de pagina
        def footer(self):
            #posicion de texto
            self.set_y(-20)
            # agregar tipografia
            self.set_font('courier', 'I', 7)
            #agregar paginacion
            self.cell(0, 20, f'pagina {self.page_no()}/{{nb}}', align='C')

    #objeto pdf:
    #('layaut', 'unidades', 'tamaño de papel')
    pdf = PDF('P','mm','Letter')
    #get total pages nunbers
    pdf.alias_nb_pages()
    #agregar pagina
    pdf.add_page()
    #especificar tipografia
    #tipografia disponible: times, courier, helvetica, symbol, zpdfdingbats,DroidSans(arial)
    #'B' negrita, 'U' subrallado, 'I' cursiva,'' regular
    pdf.set_font(font,'B',fz)

    #agregar texto
    #('with', 'height', 'String')
    
    pdf.cell(w-10, h, 'Señores ', border=True)
    pdf.set_font(font,'',fz)
    pdf.cell(w2+25, h, nombre, border=True)
    pdf.set_font(font,'B', fz)
    pdf.cell(15, h, '')
    pdf.cell(w, h, 'Fecha de factura', border=True,ln=1)
    #pdf.cell(w+5, h, 'Fecha de vencimiento',ln=1, border=True)


    pdf.cell(w-10, h, 'NIT', border=True)
    pdf.set_font(font,'', fz)
    pdf.cell(w, h, cedula, border=True)
    pdf.set_font(font,'B', fz)
    pdf.cell(w-10, h, 'Teléfono', border=True)
    pdf.set_font(font,'', fz)
    pdf.cell(w+50, h, telefono, border=True)
    pdf.cell(15, h, '')
    pdf.cell(w, h*2, fecha, border=True)
    #pdf.cell(w+5,h*2,'', border=True)
    pdf.set_font(font,'B', fz)
    pdf.cell(0, h, '',ln=1)


    pdf.cell(w-10, h, 'Direccion', border=True)
    pdf.set_font(font,'', fz)
    pdf.cell(w, h, direccion, border=True)
    pdf.set_font(font,'B', fz)
    pdf.cell(w-10, h, 'Ciudad', border=True)
    pdf.set_font(font,'', fz)
    pdf.cell(w+50, h, 'Riohacha - Colombia',ln=1, border=True)
    pdf.cell(5, h, '')
    pdf.cell(0,h,ln=1)


    pdf.set_font(font,'B', fz)
    pdf.cell(w, h, 'Ítem', border='LT')
    pdf.cell(w+25, h, 'Descripcion', border='T')
    pdf.cell(w+25, h, 'Cantidad', border='T')
    pdf.cell(w+25, h, 'Vr. Unidad',ln=1, border='RT',align='R')


    for i in range(0,len(productos)):
        pdf.set_font(font,'', fz)
        pdf.cell(w, h, str(i+1),border='L')
        pdf.cell(w+25, h, productos[i])
        pdf.cell(w+25, h, cantidades[i])
        pdf.cell(w+25, h, precios[i],ln=1,border='R',align='R')

    #    pdf.cell(w,h)
    #----------------------
    pdf.cell(((w+25)*3)+w,h*len(productos)+20,ln=1,border='BLR')
    #----------------------

    pdf.cell(135,h,'Total ítems: '+str(len(productos)))
    pdf.cell(w,h,'Total Bruto')
    pdf.set_font(font,'', fz)
    pdf.cell(w,h,format(total), ln=1,align='R')


    pdf.set_font(font,'B', fz)
    pdf.cell(135,h,'Valor en letras:')
    pdf.cell(w,h,'Total a pagar')
    pdf.set_font(font,'', fz)
    pdf.cell(w,h,format(total),ln=1,align='R')

    
    pdf.cell(135,h,total_letra+" pesos.",ln=1)
    pdf.cell(w,h,ln=1)
    

    pdf.set_font(font,'B', fz)
    pdf.cell(140,h,'Condiciones de pago:',ln=1)
    pdf.set_font(font,'', fz)
    pdf.cell(110,h,'Pago de factura No: '+format(NumRecibo))
    pdf.cell(w,h,'$ '+format(total),ln=1)

    pdf.set_font(font,'B', fz)
    pdf.cell(0,h,'Observaciones:   ',ln=1)
    pdf.set_font(font,'', fz)
    pdf.cell(0,h*3,observaciones,align='J',ln=1)

    filename=f'Factura_venta_{NumRecibo}.pdf'

    pdf.output('pdf/'+filename,'F')
    #time.sleep(1)
    R.email(usuario[3],filename,usuario[1])

def Factura_Pago_Recurrente(usuario,datos,codigos,observaciones,enviar_correo=True):

    #contenido de codigos producto
    A = codigos+';'
    codigos=R.codigo(A)
    cantidades=R.cantidad(A)
    productos=[]
    precios=[]
    cadena=''
    contador=0
    
    #variables de contenido
    w=30#width
    w2=105
    h=5#height
    #tamaño de letra
    fz=9#font zise
    font='arial'


    nombre = usuario[1]
    cedula = usuario[4]
    telefono=usuario[2]
    print(usuario[0])
    fe=bd.Consultar('creditos',usuario[0],'ID_Usuarios')
    fecha=fe[0][2]
    fpago=datos
    direccion = usuario[5]
    total=0
    mes=dt.now()
    mes=mes.month
    NumRecibo = format(random.randrange(10000,19999,3))+'-u'+format(usuario[0])+'-m'+format(mes)#bd.Ultimo_Registro('caja','Codigo_Caja')[0][0]
    
    
    

    for e in codigos:
        productos.append(bd.Consultar("productos",e,"Codigo")[0][1])
        precios.append(bd.Consultar("productos",e,"Codigo")[0][2])

    for e in range(0,len(productos)):
        total = total+(int(precios[e])*int(cantidades[e]))
    total_letra= R.numero_a_letras(total)
    #clase para encabezado
    titulo_header = "GPS VIGILANTES 24/7"
    #datos del encabezado
    meta_dat = 'NIT: 1041610630-8 Carrera 7H #34-45 Tel: 3104279136 Riohacha - Colombia'
    class PDF(FPDF):
        def header(self):
            #logo o imagen
            self.image('static/img/logo.jpg',25,10,30)
            self.set_font(font,'B', 13)
            #padding
            self.cell(10)
            #texto de encavezado
            self.cell(0,10,titulo_header, border=False, ln=1, align='C')
            #self.cell(0,25, meta_dat,ln=1,align='C')
            self.cell(85)
            self.set_font(font,'', 9)
            self.multi_cell(32,3,meta_dat,border=False,align='C')
            self.set_font(font,'B', 10)
            self.cell(0,10,"Recibo N° "+format(NumRecibo),align='R',ln=1)
            self.cell(0,30)
            #espacio adicional
            self.ln(2)

        #pie de pagina
        def footer(self):
            #posicion de texto
            self.set_y(-20)
            # agregar tipografia
            self.set_font('courier', 'I', 7)
            #agregar paginacion
            self.cell(0, 20, f'pagina {self.page_no()}/{{nb}}', align='C')

    #objeto pdf:
    #('layaut', 'unidades', 'tamaño de papel')
    pdf = PDF('P','mm','Letter')
    #get total pages nunbers
    pdf.alias_nb_pages()
    #agregar pagina
    pdf.add_page()
    #especificar tipografia
    #tipografia disponible: times, courier, helvetica, symbol, zpdfdingbats,DroidSans(arial)
    #'B' negrita, 'U' subrallado, 'I' cursiva,'' regular
    pdf.set_font(font,'B',fz)

    #agregar texto
    #('with', 'height', 'String')
    
    pdf.cell(w-10, h, 'Señores ', border=True)
    pdf.set_font(font,'',fz)
    pdf.cell(w2, h, nombre, border=True)
    pdf.set_font(font,'B', fz)
    pdf.cell(5, h, '')
    pdf.cell(w, h, 'Fecha de factura', border=True)
    pdf.cell(w+5, h, 'Fecha de vencimiento',ln=1, border=True)


    pdf.cell(w-10, h, 'NIT', border=True)
    pdf.set_font(font,'', fz)
    pdf.cell(w, h, cedula, border=True)
    pdf.set_font(font,'B', fz)
    pdf.cell(w-10, h, 'Teléfono', border=True)
    pdf.set_font(font,'', fz)
    pdf.cell(w+25, h, telefono, border=True)
    pdf.cell(5, h, '')
    pdf.cell(w, h*2, fecha, border=True)
    pdf.cell(w+5,h*2,R.FVencimiento(fecha), border=True)
    pdf.set_font(font,'B', fz)
    pdf.cell(0, h, '',ln=1)


    pdf.cell(w-10, h, 'Direccion', border=True)
    pdf.set_font(font,'', fz)
    pdf.cell(w, h, direccion, border=True)
    pdf.set_font(font,'B', fz)
    pdf.cell(w-10, h, 'Ciudad', border=True)
    pdf.set_font(font,'', fz)
    pdf.cell(w+25, h, 'Riohacha - Colombia',ln=1, border=True)
    pdf.cell(5, h, '')
    pdf.cell(0,h,ln=1)


    pdf.set_font(font,'B', fz)
    pdf.cell(w, h, 'Ítem', border='LT')
    pdf.cell(w+25, h, 'Descripcion', border='T')
    pdf.cell(w+25, h, 'Cantidad', border='T')
    pdf.cell(w+25, h, 'Vr. Unidad',ln=1, border='RT',align='R')


    for i in range(0,len(productos)):
        pdf.set_font(font,'', fz)
        pdf.cell(w, h, str(i+1),border='L')
        pdf.cell(w+25, h, productos[i])
        pdf.cell(w+25, h, cantidades[i])
        pdf.cell(w+25, h, precios[i],ln=1,border='R',align='R')

    #    pdf.cell(w,h)
    #----------------------
    pdf.cell(((w+25)*3)+w,h*len(productos)+20,ln=1,border='BLR')
    #----------------------

    pdf.cell(135,h,'Total ítems: '+str(len(productos)))
    pdf.cell(w,h,'Total Bruto')
    pdf.set_font(font,'', fz)
    pdf.cell(w,h,format(total), ln=1,align='R')


    pdf.set_font(font,'B', fz)
    pdf.cell(135,h,'Valor en letras:')
    pdf.cell(w,h,'Total a pagar')
    pdf.set_font(font,'', fz)
    pdf.cell(w,h,format(total),ln=1,align='R')

    
    pdf.cell(135,h,total_letra+" pesos.",ln=1)
    pdf.cell(w,h,ln=1)
    

    pdf.set_font(font,'B', fz)
    pdf.cell(140,h,'Condiciones de pago:',ln=1)
    pdf.set_font(font,'', fz)
    pdf.cell(110,h,'servicio recurrente vence el '+R.FVencimiento(fecha))
    pdf.cell(w,h,'$ '+format(total),ln=1)

    pdf.set_font(font,'B', fz)
    pdf.cell(0,h,'Observaciones:   ',ln=1)
    pdf.set_font(font,'', fz)
    pdf.cell(0,h*3,observaciones,align='J',ln=1)

    filename=f'Factura_venta_{NumRecibo}.pdf'

    pdf.output('pdf/'+filename,'F')
    #time.sleep(1)
    if(enviar_correo):
        R.email(usuario[3],filename,usuario[1],contexto='Recurrente')



 
#Comprovante_EgresoCaja('')

#factura de compra______________
def Factura_Compra(consepto):
    #variables de contenido
    w=30#width
    w2=105
    h=5#height
    #tamaño de letra
    fz=9#font zise
    font='arial'


    nombre = ''
    cedula = ''
    telefono=''
    fecha=''
    fpago=''
    direccion=''
    total=0
    total_letra=''

    #clase para encabezado
    titulo_header = "GPS VIGILANTES 24/7"
    #datos del encabezado
    meta_dat = 'NIT: 1041610630-8 Carrera 7H #34-45 Tel: 3104279136 Riohacha - Colombia'
    class PDF(FPDF):
        def header(self):
            #logo o imagen
            self.image('static/img/logo.jpg',10,8,45)
            self.set_font(font,'B', 13)
            #padding
            self.cell(10)
            #texto de encavezado
            self.cell(0,10,titulo_header, border=False, ln=1, align='C')
            #self.cell(0,25, meta_dat,ln=1,align='C')
            self.cell(85)
            self.set_font(font,'', 9)
            self.multi_cell(32,3,meta_dat,border=False,align='C')
            self.set_font(font,'B', 10)
            self.cell(0,10,"Factura N° 1221",align='R',ln=1)
            self.cell(0,30)
            #espacio adicional
            self.ln(2)
        
        #pie de pagina
        def footer(self):
            #posicion de texto
            self.set_y(-20)
            # agregar tipografia
            self.set_font('courier', 'I', 13)
            #agregar paginacion
            self.cell(0, 20, f'pagina {self.page_no()}/{{nb}}', align='C')

    #objeto pdf:
    #('layaut', 'unidades', 'tamaño de papel')
    pdf = PDF('P','mm','Letter')
    #get total pages nunbers
    pdf.alias_nb_pages()
    #agregar pagina
    pdf.add_page()
    #especificar tipografia
    #tipografia disponible: times, courier, helvetica, symbol, zpdfdingbats,DroidSans(arial)
    #'B' negrita, 'U' subrallado, 'I' cursiva,'' regular
    pdf.set_font(font,'B',fz)


    #agregar texto
    #('with', 'height', 'String')
    pdf.cell(w-10, h, 'Proveedor ', border=True)
    pdf.set_font(font,'',fz)
    pdf.cell(w2, h, nombre, border=True)
    pdf.set_font(font,'B', fz)
    pdf.cell(5, h, '')
    pdf.cell(w, h, 'Fecha de compra', border=True)
    pdf.cell(w+5, h, '',ln=1, border=True)


    pdf.cell(w-10, h, 'NIT', border=True)
    pdf.set_font(font,'', fz)
    pdf.cell(w, h, cedula, border=True)
    pdf.set_font(font,'B', fz)
    pdf.cell(w-10, h, 'Teléfono', border=True)
    pdf.set_font(font,'', fz)
    pdf.cell(w+25, h, telefono, border=True)
    pdf.cell(5, h, '')
    pdf.cell(w, h, 'Fecha de vencimiento', border=True)
    pdf.cell(w+5,h,'', border=True,ln=1)
    pdf.set_font(font,'B', fz)


    pdf.cell(w-10, h, 'Direccion', border=True)
    pdf.set_font(font,'', fz)
    pdf.cell(w, h, direccion, border=True)
    pdf.set_font(font,'B', fz)
    pdf.cell(w-10, h, 'Ciudad', border=True)
    pdf.set_font(font,'', fz)
    pdf.cell(w+25, h, 'Riohacha - Colombia', border=True)
    pdf.cell(5,h,'')
    pdf.set_font(font,'B', fz)
    pdf.cell(w,h,'Factura del proveedor', border=True)
    pdf.cell(w+5,h,'', border=True,ln=1)






    pdf.cell(w,h,'',ln=1)
    pdf.cell(w,h,'El valor de ',border='LTB')
    pdf.cell(135,h,'este es el valor en letras',border='TBR')
    pdf.cell(w,h,format(total),border=True,align='R',ln=1)
    pdf.cell(w,h,ln=1)

    pdf.set_font(font,'B',fz)
    pdf.cell(165,h,'Consepto',border=True,align='C')
    pdf.cell(w,h,'Valor',border=True,ln=1)

    pdf.set_font(font,'',fz)
    pdf.cell(165,h,'este es el consepto',border=True)
    pdf.cell(w,h,format(total),ln=1,border=True,align='R')


    pdf.cell(135,h)
    pdf.cell(w,h,'Total COP')
    pdf.cell(w,h,format(total),ln=1,align='R')


    pdf.cell(0,4,ln=1)
    pdf.cell(0,h,'Observaciones:',border='LTR',ln=1)
    pdf.cell(0,h*5,'',border='LBR')
    pdf.cell(w*3.25,h*4,'')
    pdf.cell(w*3.25,h*2,'',ln=1)
    pdf.cell(0,h,ln=1)
    pdf.cell(w*3.25,h,'_________________________', align='C')
    pdf.cell(w*3.25,h,'_________________________',align='C',ln=1)
    pdf.cell(w*3.25,h,'Firma elaborado', align='C')
    pdf.cell(w*3.25,h,'Firma recibido',align='C',ln=1)
    pdf.cell(w,h,'')

    pdf.output('Factura_Compra_Prueva.pdf')




def create_pdf_prueva():
    fp= 'provando la cadena f a ver que'
    class PDF(FPDF):
        def header(self):
            #logo o imagen
            self.image('LOTE.jpg',10,8,25)
            self.set_font('courier','', 40)
            #padding
            self.cell(80)
            #texto de encavezado
            self.cell(0,10,fp, border=False, ln=1, align='C')
            #espacio adicional
            self.ln(20)
        
        #pie de pagina
        def footer(self):
            #posicion de texto
            self.set_y(-20)
            # agregar tipografia
            self.set_font('courier', 'I', 13)
            #agregar paginacion
            self.cell(0, 20, f'pagina {self.page_no()}/{{nb}}',border=True, align='C')

    #objeto pdf:
    #('layaut'(orientacion), 'unidades', 'tamaño de papel')
    pdf = PDF('P','mm','Letter')
    #get total pages nunbers
    pdf.alias_nb_pages()
    #añadir pagina auto al terminar
    #incluido un margen
    pdf.set_auto_page_break(auto=True, margin=100)
    #agregar pagina
    pdf.add_page()
    #especificar tipografia
    #tipografia disponible: times, courier, helvetica, symbol, zpdfdingbats,DroidSans(arial)
    #'B' negrita, 'U' subrallado, 'I' cursiva,'' regular
    pdf.set_font('courier','U',17)
    #agregar texto
    #('with', 'height', 'String')
    pdf.cell(40, 10, 'hello world')
    pdf.cell(40, 10, 'bye world',ln=True)
    #('with', 'height', 'String', 'ln=True'salto de linea,)
    pdf.cell(0,10, f'aqui estoy {fp}',ln=True, border=True)
    pdf.set_font('courier','',7)
    for i in range(1, 16):
        pdf.cell(40,5, f'YO SOY LA LINEA {i}',ln=True, border=True, align='C')
    #guardar pdf
    pdf.output('pdf_prueva_6.pdf')
