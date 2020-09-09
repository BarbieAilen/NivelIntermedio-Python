#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import mysql.connector
import sys
from tkinter import *
from tkinter import messagebox
import validations

class My_SQL():
    
        def __init__(self,):
                pass

        def conexion(self,):
        
                mi_db = mysql.connector.connect(host="localhost", user="root", passwd="", database="Nivel_Intermedio")
                return mi_db
        def create_db(self,):
                try:
                        mi_db= mysql.connector.connect(host="localhost", user="root", passwd="")
                        micursor = mi_db.cursor()
                        micursor.execute("CREATE DATABASE Nivel_Intermedio")
                        messagebox.showinfo(message="Base de Datos creada exitosamente", title="Alta de DB")
        
                except:
                        print("La Base de Datos ya fue creada")


        
        def crear_table(self,):
                try:
                    mi_db = self.conexion() 
                    micursor = mi_db.cursor()
                    micursor.execute("CREATE TABLE producto(id int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT, titulo VARCHAR(128) COLLATE utf8_spanish2_ci NOT NULL, descripcion text COLLATE utf8_spanish2_ci NOT NULL )")
                
                except:
                    print("La Tabla ya existe")
        
        def add_record (self,reg):

            self.add = reg
            sql = "INSERT INTO Nivel_Intermedio.producto (titulo, descripcion) VALUES (%s, %s)"
            mi_db = self.conexion()
            micursor = mi_db.cursor()
            micursor.execute(sql, self.add)
            mi_db.commit()


        def delete_reg(self,id):
            
            mi_db = self.conexion()
            micursor = mi_db.cursor()
            sql = "DELETE FROM producto WHERE ID="+str(id)
            micursor.execute(sql)
            mi_db.commit()

base = My_SQL()
