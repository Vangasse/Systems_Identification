# -*- coding: utf-8 -*-
"""
ARX algorithm
1- Start defining order(n);
2- Program will read from file "dados_1.csv";
3- Number of Samples is set by data;
4- Function arx is called at bottom.
"""
###################### Order and Samples ######################
N=10
n=3
DEBUG = True

import numpy as np
import pandas as pd

def genRegMatrix(u, y, n):
    N = len(y)
    ###################### Phi Construction ######################
    # Inicialização da matriz phi
    phi = np.empty((N-n,0))
    """
    Neste algoritmo, as colunas da matriz phi são geradas incrementalmente
    de acordo com seus limites e adicionadas à mesma através da função
    hstack(numpy).
    """
    # colunas de y:
    for j in range(n):
        y_column = np.array([])
        for k in range(n - (j + 1), N - (j + 1)):
            y_column= np.append(y_column, y[k])
        y_column = y_column.reshape(len(y_column), 1)   # Transforma o array linha em coluna
        phi = np.hstack((phi, y_column))                # Adiciona o array coluna na matriz phi
    
    # colunas de u
    for j in range(n):
        u_column = np.array([])
        for k in range(n - (j + 1), N - (j + 1)):
            u_column = np.append(u_column, u[k])
        u_column = u_column.reshape(len(u_column), 1)   # Transforma o array linha em coluna
        phi = np.hstack((phi, u_column))                # Adiciona o array coluna na matriz phi
    
    return phi
    


def recursive_arx(u, y, n, l):
    N = len(y)
    ###################### Setting Parameters ######################
    #Regressor Matrix
    phi = genRegMatrix(u, y, n)
    #Covariance Matrix
    P = np.identity(n*2)*10000
    #System Parameters
    theta = np.random.uniform(low=-1, high=1, size=(n*2, 1))
    ###################### Recursive Procedure ######################
    for i in range(N-n):
        K = P.dot(phi[i,:].transpose())/(phi[i,:].dot(P)).dot(phi[i,:].transpose()) + l
        theta = theta + K*(y[i+n] - phi[i,:].dot(theta))
        #P = (1/l)*(P - ((P.dot(phi[i,:].transpose()).dot(phi[i,:])).dot(P))/((phi[i,:].dot(P)).dot(phi[i,:].transpose())))
        print(K.shape, theta.shape)
    """phi_t = phi.transpose()
    phi_pseudo_inverse = (np.linalg.inv(phi_t.dot(phi))).dot(phi_t)
    theta_est = phi_pseudo_inverse.dot(y[n:])
    
    ###################### Model Evaluation ######################
    y_est = phi.dot(theta_est)
    y_est = np.append(y[0:n], y_est, axis=0)
    
    y_mean = np.mean(y_est)
    erro = y - y_est
    
    MSE=0
    for i in range(len(erro)):
        MSE += erro[i] ** 2
    C=0
    for k in range(len(y)):
        C += (y[k] - y_mean) ** 2
    COEEF = 1 - MSE/C
    
    print("MSE: "+str(MSE))
    print("COEEF: "+str(COEEF))
    
    return theta_est"""


###################### File Reading ######################
data = pd.read_csv('dados_1.csv')
data_matrix = data.to_numpy()
if not DEBUG:
    y = data_matrix[:,0]
u = data_matrix[:,1]

###################### Known Model Testing ######################
if DEBUG:
    y = np.empty((0,1))
    y = np.append(y, n*[0])
    for k in range(n, N):
        y = np.append(y, -0.5*y[k-1] - 0.3*y[k-2] + 0.09*y[k-3] + 8.3*u[k-1] + 1.7*u[k-2] - 5.2*u[k-3])

###################### Resulting Array of Parameters ######################
#lambda = 0.97
theta = recursive_arx(u,y,n, 0.97)
print(theta)