#!/usr/bin/env python
# coding: utf-8

# In[19]:


from tkinter import *
from tkinter.ttk import *
from tkinter import ttk
from tkinter import messagebox
from sklearn import tree
import random
import mysql.connector
import validations
import saveRecords
import themes
import info
from themes import *
import sklearn
import sys


class Admin():

    def __init__(self, ini):
            
        self.root = ini
        self.val1 = StringVar()
        self.val2 = StringVar()
        saveRecords.base.create_db()
        saveRecords.base.crear_table()
        self.screen()
        self.entries()
        self.tree()
        self.botones()
        

    def screen(self,):
        self.root.title('Entrega Final')
        self.root.resizable(True, True)
        self.cabecera = Label(self.root, text="Ingrese sus datos", background="DarkOrchid3", foreground="thistle1", width=100)
        self.title = Label(self.root, text="Título")
        self.descrip = Label(self.root, text="Descripción")
        self.tema = Label(self.root, text="Temas disponibles")
        self.cabecera.grid(row=0, columnspan=4, padx=1, pady=1, sticky=W+S+N+E)
        self.title.grid(padx=0, pady=0, row=1, column=0,sticky=W)
        self.descrip.grid(padx=0,pady=0, row=2, column=0,sticky=W)
        
        self.tema.grid(row=18, column=0, columnspan=3, sticky=W)

    def crear_entry (self,valor, ancho, fila, columna = 1):
        self.valor=valor
        self.ancho=ancho
        self.fila=fila
        self.columna=columna
        self.entrada= Entry(self.root, textvariable = valor , width=25)
        self.entrada.grid(padx=65, row=fila)
        return self.entrada

    def entries(self,):
        self.entry_t = self.crear_entry(self.val1, 100, 1, 1)
        self.entry_d = self.crear_entry(self.val2, 100, 2, 1)
   

    def tree(self,):
        
        self.tree = ttk.Treeview(self.root, height = 10, column=(0,1,2),  show="headings", selectmode ="browse")
        self.tree.grid(row=4, column=0, columnspan=3, rowspan=10, sticky=NSEW)
        self.tree.heading(0, text="ID")
        self.tree.heading(1, text="Título")
        self.tree.heading(2, text="Descripción")
        self.tree.column(0, width=150, minwidth=150, stretch=YES)
        self.tree.column(1, width=150, minwidth=150, stretch=YES)
        self.tree.column(2, width=150, minwidth=150, stretch=YES)
       
        self.root.grid_rowconfigure(5, weight=1)
        self.barra = ttk.Scrollbar(self.root, orient ="vertical", command = self.tree.yview)
        self.barra.grid(row=5, column=4, rowspan=5, sticky=NSEW)
        self.tree.configure(yscrollcommand = self.barra.set)

    def botones(self,):
         
        self.add= Button(self.root, text="Alta", command=lambda: self.alta(self.val1.get(), self.val2.get()))
        self.delete = Button(self.root, text='Borrar', command= lambda: self.borrar())
        self.reg_e= Button(self.root, text="Mostrar registros existentes", command=lambda: self.obtener_reg())
        self.info= Button(self.root, text="About this APP - Bárbara Almaraz", command=lambda: self.information())
        self.add.grid(row=17, column=0)
        self.delete.grid(row=17, column=1)
        self.reg_e.grid(row=3, columnspan=3, sticky=W+E)
        self.info.grid(row=23, columnspan=3, sticky=W+E)

        self.radio = IntVar()
        self.radio.set(0)
        
        self.RadioB1 = Radiobutton(self.root, text="Default", variable=self.radio, value=0, command=lambda: self.choice_themes(self.radio.get()))
        self.RadioB1.grid(row=19, column=0)
        self.RadioB2 = Radiobutton(self.root, text="Elegir tema 1", variable=self.radio, value=1, command=lambda: self.choice_themes(self.radio.get()))
        self.RadioB2.grid(row=20, column=0)
        self.RadioB3 = Radiobutton(self.root, text="Elegir tema 2", variable=self.radio, value=2, command=lambda: self.choice_themes(self.radio.get()))
        self.RadioB3.grid(row=21, column=0)
        self.RadioB4 = Radiobutton(self.root, text="Elegir tema 3", variable=self.radio, value=3, command=lambda: self.choice_themes(self.radio.get()))
        self.RadioB4.grid(row=22, column=0)

    def information(self,):

        messagebox.showinfo("Entrega Final","Desarrollado por Bárbara Almaraz")
        print ('DESCRIPCION GENERAL DEL PROGRAMA: El programa consiste de cinco módulos: main, temas, validaciones, el registro en la base de Datos y modulo info con la descripcion de la Entrega Final')
        info.mostrar()
        
        

   
    def borrar_tree(self,):
        arbol= self.tree.get_children()
        for elementos in arbol:
            self.tree.delete(elementos)
    
    def clear_entries(self,):
        self.entry_t.delete(0, "end")
        self.entry_d.delete(0, "end")  

    def obtener_reg(self):
        try:
            self.borrar_tree()
            sql = 'SELECT * FROM producto ORDER BY id ASC'
            mi_db = saveRecords.base.conexion()
            micursor = mi_db.cursor()
            micursor.execute(sql)
            base = micursor.fetchall()
            for row in base:
                self.tree.insert("", "end", values=(row[0], row[1], row[2]))
            return
        except:
            return None
        

    def borrar(self,): 
        id = self.tree.focus()
        item_id= self.tree.item(id)
        values = (item_id['values'])
        i=values[0]
        saveRecords.base.delete_reg(i)
        self.tree.delete(id)    

      
    def alta(self, dato1, dato2):
        self.titulo = dato1
        self.descripcion = dato2
        cadena = self.titulo
        datos = (self.titulo, self.descripcion)
        resultado = validations.validar(cadena)
        
        try:
            mi_db = saveRecords.base.conexion()
            micursor = mi_db.cursor()
            if not self.val1.get() or not self.val2.get(): 
                messagebox.showinfo("Error","Complete todos los campos")
                micursor.close()
                return None
            if resultado == False:  #se ingreso en titulo un valor no permitido
                self.clear_entries()
                messagebox.showinfo("Error","Titulo debe ser un caracter alfanumerico")
                return None 
            elif resultado: #titulo valido
                saveRecords.base.add_record(datos)
                micursor.close()
            else:
                return None
        except:
            messagebox.showerror("Error", "Error al procesar alta")
        
        try:
            self.clear_entries()
            self.obtener_reg()
        except:
            messagebox.showinfo("Error", "No se ha podido cargar el arbol.")



    def choice_themes(self, radio):
        self.root.configure(background=themes.back[radio])
        self.descrip.configure(background=themes.botton[radio])
        self.title.configure(background=themes.botton[radio])
        self.tema.configure(background=themes.botton[radio])
        self.RadioB1.configure(foreground=themes.fore[radio])
        self.RadioB2.configure(background=themes.botton[radio], foreground=themes.fore[radio])
        self.RadioB3.configure(background=themes.botton[radio], foreground=themes.fore[radio])
        self.RadioB4.configure(background=themes.botton[radio], foreground=themes.fore[radio])
        self.cabecera.configure(foreground=themes.titlefore[radio], background=themes.botton[radio])
        self.reg_e.configure( background=themes.reg[radio])
        self.add.configure(background=themes.botton[radio], foreground=themes.fore[radio])
        self.delete.configure(background=themes.botton[radio], foreground=themes.fore[radio])
          
        return


if __name__ == '__main__':
    root = Tk()
    adm = Admin(root)
    root.mainloop()


# In[ ]:




