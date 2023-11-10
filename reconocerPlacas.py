from skimage import data, color, io, measure
from scipy import ndimage
from array import array
import numpy as np
import matplotlib.pyplot as plt
plt.close('all')
# --------------------------- Perfiles de numeros -------------------------------
ic = io.imread_collection('BaseDatos/*.jpg',conserve_memory=False)
dataBasePerfiles = []
for w in range(10):
    imaDB = (color.rgb2gray((ic[w]))*255<80).astype(int)
    # plt.figure ()
    # plt.imshow(imaDB,cmap='gray')
    perfilDB = []
    for i in range(imaDB.shape[0]):
        for j in range(imaDB.shape[1]):
            if (imaDB[i,j] == 1):
                perfilDB.append(j)
                break 
            
    for i in range(imaDB.shape[0]):
        for j in range(imaDB.shape[1]-1,0,-1):
            if (imaDB[i,j] == 1):
                perfilDB.append(j)
                break 
    # plt.figure()
    # plt.plot(perfilDB)  
    dataBasePerfiles.append(np.var(perfilDB))
# ------------------------------------------------------------------------------

dataBasePlaca = [[4,2,8,6],[6,8,2,9],[3,1,7,3],[9,3,3,2],[9,3,8,9]]

def distanciaEu (dato, centros, clases):
    vecEu = []
    for i in range(clases):
        D = np.sqrt((centros[i]-dato)**2)
        vecEu.append(D)
    solEu = [np.argmin(vecEu), vecEu[np.argmin(vecEu)]]
    return solEu

def detectarNumero (indicesCol, corte1n,Perfiles):

    corte2 = corte1[:,indicesCol[len(indicesCol)-1]:indicesCol[0]]
    plt.figure()
    plt.imshow(corte2,cmap='gray')
    # ------------- Perfil de un numero ----------
    perfil = []
    for i in range(corte2.shape[0]):
        for j in range(corte2.shape[1]):
            if (corte2[i,j] == 1):
                perfil.append(j)
                break 
                
    for i in range(corte2.shape[0]):
        for j in range(corte2.shape[1]-1,0,-1):
            if (corte2[i,j] == 1):
                perfil.append(j)
                break      
                  
    plt.figure()
    plt.plot(perfil)
    
    numPlaca=-1
    varPerfil = np.var(perfil)
    print('Distancia Euclidiana: %d'%varPerfil)
    posMinEu = distanciaEu(varPerfil,dataBasePerfiles,10)
    print('Número más cercano: %a'%posMinEu[0])
    acum = []    
    if (posMinEu[0] == 0):
        return 0
    elif(posMinEu[0] == 1):
        return 1
    elif(posMinEu[0] == 2):
        return 2
    elif(posMinEu[0] == 3):
        return 3
    elif(posMinEu[0] == 4):
        return 4
    elif(posMinEu[0] == 5):
        return 5
    elif(posMinEu[0] == 6 or posMinEu[0] == 9):
        for o in range(len(perfil)):
            if(perfil[o]<20):
                acum.append(perfil[o])
            elif(len(acum)>70):
                return 6    
            else:
                return 9
    elif(posMinEu[0] == 7):
        return 7
    elif(posMinEu[0] == 8):
        return 8

    
ima = color.rgb2gray(color.rgba2rgb(io.imread('Prueba2.png')))*255 # Transformar a gris
# plt.figure()
# plt.imshow(ima,cmap='gray')

ima2 = ((ima)<80).astype(int) # Binarizar a menores de 80
# plt.figure()
# plt.imshow(ima2,cmap='gray')

sumaFila = np.sum(ima2,axis=1)
# plt.figure()
# plt.plot(sumaFila)
intervInter = []
indices = []
temp = 0
Max = 0
bandera=2
# # ---------------------------------- Corte Filas ---------------------------------
for i in range(len(sumaFila)):
    if (sumaFila[i]>25):
        bandera = 1
    
    if (bandera == 0):
        temp = len(intervInter)
        if(temp>Max):
            Max = temp
            corteFinal = intervInter
            indicesFinal = indices
            intervInter = []
            indices = []
            
    if bandera == 1:
        intervInter.append(sumaFila[i]) 
        indices.append(i)
        bandera = 0
    
    if(i==len(sumaFila)-1):
        intervInter = []
        indices = []
        
# # ------------------------------------------------------------------------------    

corte1 = ima2[indicesFinal[0]:indicesFinal[len(indicesFinal)-1],:]
# plt.figure()
# plt.imshow(corte1,cmap='gray')

sumaColumna = np.sum(corte1,axis=0)
# plt.figure()
# plt.plot(sumaColumna)
# # ---------------------------------- Evaluación/clasificador ---------------------------------
start = 0
bandera = 2
indicesCol = []
vecColumnas = []
cont = 0
idPlaca = []
for j in range(len(sumaColumna)-1,0,-1):
    if sumaColumna[j] < 10 :
        start = 1
        
    if (sumaColumna[j]>10 and start == 1):
        bandera = 1
           
    if (bandera == 0):
        if(max(vecColumnas)>20):
            result = detectarNumero(indicesCol,corte1,dataBasePerfiles)
            print('Número identificado {%d}'%result)
            idPlaca.append(result)
        indicesCol = []
        cont += 1
        bandera = 2
        vecColumnas = []
        if cont == 6:
            break
            
    if bandera == 1:
        vecColumnas.append(sumaColumna[j])
        indicesCol.append(j)
        bandera = 0
# # ------------------------------------------------------------------------------
idPlaca.reverse()
print('El vehículo tiene placas con terminación: %a'%idPlaca)
noEntra=0
for k in range(len(dataBasePlaca)):
    cont=0
    for l in range(len(idPlaca)):
        if idPlaca[l] == dataBasePlaca[k][l]:
            cont +=1

    if idPlaca == dataBasePlaca[k]:
        print('Vehículo aceptado')
        k=len(dataBasePlaca)
        break
    elif (noEntra==1 and k==len(dataBasePlaca)-1):
        print('Vehículo no aceptado')
    else:
        print('Verificando placa...')
        noEntra=1
        
cont = cont/4*100
print('El desempeño del clasificador fue de: %d %%'%cont)
    


