import numpy as np
import time
from gurobipy import *
import matplotlib.pyplot as plt
#x=1為在主場 0為客場
#輸入n
print("please enter number n : ")
n = int(input())
i = n
j = n
t = n-1 
cons = []
for z in range(30):
    cons.append(0)
try:
  M=Model("BREAK")
  
  x=M.addVars(i,j,t,vtype=GRB.BINARY,name="x")
  y=M.addVars(i,t,vtype=GRB.BINARY,name="y")
  M.update()
## i => k
## j => l
## t => m
  #set obj
  Obj = LinExpr()           
  for k in range(0,n):
     for m in range(0,n-1):
         Obj+=y[k,m]    
  M.setObjective(Obj*2,GRB.MINIMIZE) #主客 *2  
  
  #set constraint 可能牴觸下面限制式 有下面cons[0]即足夠
  for m in range(0,n-1):
      for l in range(0,n):
          cons[0] = LinExpr()
          for k in range(0,n): 
              cons[0].addTerms([1,1],[x[k,l,m],x[l,k,m]])
          M.addConstr(cons[0]==1)
    
  for k in range(0,n): 
      for l in range(0,n):
          if(k!=l):
              cons[1] = LinExpr()
              for m in range(0,n-1): 
                  cons[1].addTerms([1,1],[x[k,l,m],x[l,k,m]])
              M.addConstr(cons[1]==1)        
  
  for m in range(0,n-2):
      for k in range(0,n):
          cons[2] = LinExpr()
          for l in range(0,n): 
              cons[2].addTerms([1,1], [x[k,l,m],x[k,l,m+1]])
          M.addConstr(cons[2]<=y[k,m]+1)  
    
  starttime = time.time()     
  M.optimize()
  endtime = time.time()     
  
  for v in M.getVars():
      print('%s %g'%(v.varName,v.x))
      
  print('Obj:%g'%M.objVal)
  
except GurobiError:
    print('Encountered an gurobi error')
    
except AttributeError:
    print('Encountered an attribute error')
    
print('Total:',endtime-starttime)

#plot
teamnum = [4,6,8,10]

time = [ 0.087,0.16,1.27,2061]


plt.xlabel("team number")
plt.ylabel("time")
plt.plot(teamnum,time)

