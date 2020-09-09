#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#Validacion del campo Titulo con funcion validar
#patron="^[A-Za-z]+(?:[ _-][A-Za-z]+)*$"
import re
import sys

def validar (titulo):
    dato=titulo
    patron="^[A-Za-z]+(?i:[ _-][A-Za-z]+)*$"
    if(re.match(patron,dato)):
        return True
    else:
        return False

