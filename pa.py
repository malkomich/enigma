#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import time 

def validarTexto(txt):	       
    correcto=True
    for j in range(len(txt)):
        if(txt[j]<'A' or txt[j]>'Z'):
            correcto=False
    return correcto

def validarCriba(criba):
    correcto=True
    for j in range(len(criba)):
        if(criba[j]<'A' or criba[j]>'Z'):
            correcto=False
    return correcto

# Traduce el texto a valores numéricos del rango 0-25
def convertirTexto(texto, clave, V): 
    dic={}
    for i in range(len(texto)):
        for j in range (len(clave)):
            if (texto[i]==clave[j]):
                dic[i]=j
        j=0    
    V=dic.values()
    return V

# Convierte los rotores generados en el rango 0-4
def convertirNumero(r,R): 
    dic={}
    for i in range(len(r)): 
        dic[i]=int(r[i])-1  
    R=dic.values()
    return R

def moverRotores(P,M,R):     
    if(int(P[0])==int(M[R[0]])):
        if(int(P[1])==int(M[R[1]])):
            P[2]=(P[2]+1)%26
	P[1]=(P[1]+1)%26			
    P[0]=(P[0]+1)%26
    return P

# Cifrado en el recorrido directo -de teclado hacia el espejo-
def recorridoDir(X,P,TD,R):     
    for k in (range(len(P))):		
        X=(X+P[k])%26
	X=TD[R[k]][X]
	X=((X-P[k])+26)%26
    return X

# Cifrado en el recorrido inverso -de espejo hacia el teclado-
def recorridoInv(X,P,TI,R):  
    for k in reversed(range(len(P))): 
        X=(X+P[k])%26
        X=TI[R[k]][X]
	X=((X-P[k])+26)%26
    return X

# Simula la Maquina Enigma
def maquinaEnigma(txt,pos_ini,r): 
    R=[]
    T=[]
    P=[]
    clave= 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    codigo={}
    A=[] 

    TD=[[4,10,12,5,11,6,3,16,21,25,13,19,14,22,24,7,23,20,18,15,0,8,1,17,2,9],
        [0,9,3,10,18,8,17,20,23,1,11,7,22,19,12,2,16,6,25,13,15,24,5,21,14,4],
        [1,3,5,7,9,11,2,15,17,19,23,21,25,13,24,4,8,22,6,0,10,12,20,18,16,14],
        [4,18,14,21,15,25,9,0,24,16,20,8,17,7,23,11,13,5,19,6,10,3,2,12,22,1],
        [21,25,1,17,6,8,19,24,20,15,18,3,13,7,11,23,0,22,12,9,16,14,5,4,2,10]]

    TE=[24,17,20,7,16,18,11,3,15,23,13,6,14,10,12,8,4,1,5,25,2,22,21,9,0,19]

    TI=[[20,22,24,6,0,3,5,15,21,25,1,4,2,10,12,19,7,23,18,11,17,8,13,16,14,9],
        [0,9,15,2,25,22,17,11,5,1,3,10,14,19,24,20,16,6,4,13,7,23,12,8,21,18],
        [19,0,6,1,15,2,18,3,16,4,20,5,21,13,25,7,24,8,23,9,22,11,17,10,14,12],
        [7,25,22,21,0,17,19,13,11,6,20,15,23,16,2,4,9,12,1,18,10,3,24,14,8,5],
        [16,2,24,11,23,22,4,13,5,19,25,14,18,12,21,9,20,3,10,6,8,0,17,15,7,1]]

    M=[16,4,21,9,25]

    T=convertirTexto(txt,clave,T)
    P=convertirTexto(pos_ini,clave,P)
    R=convertirNumero(r,R) 
    
    for i in range(len(T)): 
        P=moverRotores(P,M,R)
	X=T[i]
        X=recorridoDir(X,P,TD,R)
        X=TE[X] 
	X=recorridoInv(X,P,TI,R)	
	codigo[i]=X
    A=codigo.values()
    resultado=''
    # Conversion de los numeros al string codificado
    for i in range(len(T)): 
        resultado=resultado+clave[A[i]]
    return resultado

# Compara todos los mensajes decodificados con la criba e imprime a aquellos que la contengan
def encontrarCriba(resultado, criba):
    j=0
    coincide=0
    for i in range(len(resultado)):
        if(j<len(criba)):
            if(resultado[i]==criba[j]):  
                coincide=coincide+1
                j=j+1
            else:
                coincide=0
                j=0                              
                # Comprueba otra vez  con el primer caracter por si estaba comprobando otra letra de la criba y da fallo,
                # por ejemplo si criba HOLA y encuentra HOHOLA 
                if(resultado[i]==criba[j]): 
                    coincide=coincide+1
                    j=j+1
    return coincide
    
# Imprime el texto donde se haya encontrado la criba
def imprimirCriba(r,pos_ini,resultado):
    print "-------------"
    print r + "-" + pos_ini
    print resultado

# Descodifica la maquina por fuerza bruta 
def romperMaquina(txt,criba):
    r=''
    rotores='12345'
    clave= 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    pos_ini=''
    resultado=''
    coincide=0
    for i in range(len(rotores)):
        for j in range(len(rotores)):
            for k in range(len(rotores)):
                if(rotores[i]!=rotores[j]!=rotores[k]!=rotores[i]):
	            r=rotores[i]+rotores[j]+rotores[k]
                    for x in range(len(clave)):
                        for y in range(len(clave)):
        	            for z in range(len(clave)):
            		        pos_ini=clave[x]+clave[y]+clave[z]
			        resultado=maquinaEnigma(txt,pos_ini,r)
                                coincide=encontrarCriba(resultado,criba)
                                if(coincide==len(criba)):
		                    imprimirCriba(r,pos_ini,resultado)


# INICIO DEL PROGRAMA #

os.system("clear")

correcto=False
while(correcto==False):
    txt=raw_input ("Introduzca el mensaje a descodificar(LETRAS MAYUSCULAS):\n")
    correcto=validarTexto(txt)
    if(correcto==False):
        print "Mensaje incorrecto, introduzca de nuevo el mensaje."
correcto=False

while(correcto==False):
    criba=raw_input("Introduzca la criba que desea buscar en el mensaje:\n")
    correcto=validarCriba(criba)
    if(correcto==False):
        print "Criba incorrecta,introduzcala de nuevo."

t0=time.clock()
romperMaquina(txt,criba)
print "-------------"
print "%.2f seg." % (time.clock() - t0) 
