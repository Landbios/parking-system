﻿from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import tkinter as tk
import array as ar
import sqlite3




def query_database():

    global count

    count = 0
    
    conne = sqlite3.connect('parkingdatabase.db')

    c = conne.cursor()

    c.execute("SELECT * FROM Reserves")

    records = c.fetchall()

    for record in records:
        info.insert(parent='',index='end', iid=count, text="", values=(record[0], record[1], record[2], record[3], record[4],record[5],record[6],record[7],record[8]))

        count += 1

        

    conne.commit()

    conne.close()

def InfoAdicional():
    messagebox.showinfo("Acerca de nuestro proyecto","Nuestro proyecto esta desarrollado mediante software libre, no infrige derechos de autor ni copyright")

def InfoEquipo():
    messagebox.showwarning("Nosotros", "Este programa fue hecho en equipo")

def salirdelapp():
    valor=messagebox.askquestion("Salir", "¿Desea salir de la aplicacion?") 
    if valor=="yes":
       root.destroy()


def Abrirarchivo():
    archivo=filedialog.askopenfilename(filetypes=(
        ("Ficheros en PDF","*.PDF"),
        ("Todos los ficheros","*.*")
    ), 
    title = "Abrir documento"
)     
    print(archivo)

def abrirform():
    
    regiForm.deiconify()


def salirdelform():
    revalor=messagebox.askquestion("Salir", "¿Desea salir de la aplicacion?") 
    if revalor=="yes":
       regiForm.withdraw()
    else:
        regiForm.deiconify()



def validarposicion():
    

    tempost = positBox.get()

    posvalid = False
    
    for child in info.get_children():
        if tempost in info.item(child)['values']:

            messagebox.showinfo(message="Puesto ocupado, Porfavor seleccione otro puesto o espere su liberacion.", title="Error")
            posvalid = True

            

    if posvalid == True:

        regiForm.deiconify()

    else:

        
        AgregarReserva()
            

        

            
    

def AgregarReserva():
       
        conne = sqlite3.connect('parkingdatabase.db')

        c = conne.cursor()

        
        if nameE.get() == "" or ModelE.get() == "" or idE.get() == "" or mailE.get() == "" or BrandBox.get() == "" or ColorBox.get() == "" or yearE.get() == "" or caridE.get() == "" or positBox.get() == "":
    
            messagebox.showinfo(message="Por favor rellene todos los campos", title="Error")
            regiForm.deiconify()
            
        elif int(yearE.get()) < 1884 or int(yearE.get()) > 2022 :

             messagebox.showinfo(message="Usted ha introducido un año invalido", title="Error")
             regiForm.deiconify()


            
        else:

            c.execute("INSERT INTO Reserves VALUES(:id, :name, :mail, :brand, :model, :color, :year, :carid, :posit)",
                      {
                          'id': idE.get(),
                          'name': nameE.get(),
                          'mail': mailE.get(),
                          'brand': BrandBox.get(),
                          'model': ModelE.get(),
                          'color': ColorBox.get(),
                          'year': yearE.get(),
                          'carid': caridE.get(),
                          'posit': positBox.get(),
                        

                      })
             
        
            conne.commit()

            conne.close()
            
            nameE.delete(0,END)
            mailE.delete(0,END)
            ModelE.delete(0,END)
            idE.delete(0,END)
            BrandBox.set('')
            ColorBox.set('')
            yearE.delete(0,END)
            caridE.delete(0,END)
            positBox.set('')
            

            #Refresscar lista

            info.delete(*info.get_children())

            query_database()

            regiForm.withdraw()


def validateints():
    try:
        int(idE.get())
        int(yearE.get())
        
        validarposicion()
        
    except ValueError:
        messagebox.showinfo(message="Solo debe ingresar numeros en año y cedula", title="Error")
        regiForm.deiconify()
        

def eliminarreserva():

    conne = sqlite3.connect('parkingdatabase.db')

    c = conne.cursor()

    
    selected = info.focus()
    
    values = info.item(selected, 'values')

    delid = values[0]

    c.execute("DELETE from Reserves WHERE oid=" + values[0])

    conne.commit()

    conne.close()

    messagebox.showinfo(message="Ha eliminado la reserva de la persona con C.I" + values[0] , title="Error")

    info.delete(*info.get_children())
    
    query_database()
    
    

        
    
root = Tk()

root.geometry("800x800")

root.iconbitmap("volante.ico")

root.config(bg="silver")

root.title("Parking System")

root.attributes('-fullscreen', True)

menubar = Menu(root)
root.config(menu=menubar)




filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Salir", command=salirdelapp)



helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Nosotros", command=InfoEquipo)
helpmenu.add_separator()
helpmenu.add_command(label="Acerca de...", command=InfoAdicional)

resmenu = Menu(menubar, tearoff=0)
resmenu.add_command(label="Añadir Reserva", command=abrirform)
resmenu.add_command(label="Eliminar Reserva", command=eliminarreserva)


menubar.add_cascade(label="Archivo", menu=filemenu)
menubar.add_cascade(label="Ayuda", menu=helpmenu)
menubar.add_cascade(label="Reservas", menu=resmenu)



info = ttk.Treeview(root,show='headings', height=20)
info["columns"]=("Cedula","Nombre y Apellido","Correo Electronico","Marca","Modelo","Color","Año","Placa","Puesto")
info.column("#0", width=0, stretch=NO)
info.column("Cedula", anchor=CENTER, width=80)
info.column("Nombre y Apellido", anchor=CENTER, width=180)
info.column("Correo Electronico", anchor=CENTER, width=180)
info.column("Marca", anchor=CENTER, width=80)
info.column("Modelo", anchor=CENTER, width=80)
info.column("Color", anchor=CENTER, width=80)
info.column("Año", anchor=CENTER, width=80)
info.column("Placa", anchor=CENTER, width=80)
info.column("Puesto", anchor=CENTER, width=80)

info.heading("#0", text="", anchor=CENTER)
info.heading("Cedula", text="Cedula", anchor=CENTER)
info.heading("Nombre y Apellido", text="Nombre y Apellido", anchor=CENTER)
info.heading("Correo Electronico", text="Correo Electronico", anchor=CENTER)
info.heading("Marca", text="Marca", anchor=CENTER)
info.heading("Modelo", text="Modelo", anchor=CENTER)
info.heading("Color", text="Color", anchor=CENTER)
info.heading("Año", text="Año", anchor=CENTER)
info.heading("Placa", text="Placa", anchor=CENTER)
info.heading("Puesto", text="Puesto", anchor=CENTER)
info.pack()

regiForm = tk.Toplevel()
regiForm.geometry("500x500")
regiForm.attributes('-fullscreen', True)
regiForm.withdraw()

regimenubar = Menu(regiForm)
regiForm.config(menu=regimenubar)
regiForm.iconbitmap("volante.ico")

global rescount

rescount = 0

operamenu = Menu(regimenubar, tearoff=0)
operamenu.add_command(label="Limpiar")
operamenu.add_command(label="Salir", command=salirdelform)


regimenubar.add_cascade(label="Menu", menu=operamenu)

    
label_0 =Label(regiForm,text="Formulario de Reserva", width=25,font=("bold",20))
label_0.place(x=500,y=60)
    
Id = Label(regiForm ,text = "Cedula", width=20,font=("bold",10))
Id.place(x=240,y=137)

name = Label(regiForm ,text = "Nombre", width=20,font=("bold",10))
name.place(x= 490,y=137)
    
mail = Label(regiForm ,text = "Correo",  width=20,font=("bold",10))
mail.place(x=750,y=137)

model = Label(regiForm ,text = "Marca",  width=20,font=("bold",10))
model.place(x=240,y=197)

model = Label(regiForm ,text = "Modelo",  width=20,font=("bold",10))
model.place(x=490,y=197)

color = Label(regiForm ,text = "Color",  width=20,font=("bold",10))
color.place(x=750,y=197)

year = Label(regiForm ,text = "Año",  width=20,font=("bold",10))
year.place(x=240,y=257)

carid = Label(regiForm ,text = "Placa",  width=20,font=("bold",10))
carid.place(x=490,y=257)

carplace = Label(regiForm ,text = "Puesto",  width=20,font=("bold",10))
carplace.place(x=750,y=257)
   
   
idE = Entry(regiForm)
idE.place(x=390,y=140)
nameE = Entry(regiForm)
nameE.place(x=620,y=140)   
mailE = Entry(regiForm)
mailE.place(x=890,y=140)
BrandBox = ttk.Combobox(regiForm,
                        state="readonly",
                        values=["Ford","Toyota","Chevrolet","Jeep","Mercedes-Benz","Ferrari","BMW","Lamborghini","Volkswagen","Nissan"])
BrandBox.place(x=390, y=197)

ModelE = Entry(regiForm)
ModelE.place(x=620,y=197)

ColorBox = ttk.Combobox(regiForm,
                        state="readonly",
                        values=["Rojo","Beige","Gris","Azul","Verde","Morado","Rosado","Blanco","Negro","Marron","Celeste","Amarillo","Naranja","Plateado","Dorado"])
ColorBox.place(x=890, y=197)

yearE = Entry(regiForm)
yearE.place(x=390,y=257)
caridE = Entry(regiForm)
caridE.place(x=620,y=257)

positBox = ttk.Combobox(regiForm,
                        state="readonly",
                        values=["A1","A2","A3","A4","A5","A6","B1","B2","B3","B4","B5","B6","C1","C2","C3"])
positBox.place(x=890, y=257)


btnReserva = Button(regiForm, text='Reservar' ,width=20,bg="dark blue",fg='white', command=validateints)
btnReserva.place(x=580,y=380)

query_database()

root.mainloop()
