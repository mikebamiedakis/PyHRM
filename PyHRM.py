
# coding: utf-8

# ## Introduction

# Please read a very nice introduction provided by Kapa BioSystems to understand, prepare and troubleshoot
# 
# http://www.kapabiosystems.com/document/introduction-high-resolution-melt-analysis-guide/
# 

# ### Import Python modules for analysis


import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import addEventHandler
import sklearn.cluster as sc
# ### Read and Plot Melting Data

# In[ ]:
#get_ipython().magic(u'matplotlib inline')
filename = 'test'
referenceSample = 'C5'
clusterNumber = 3
minTemperature= 75
maxTemperature = 81

def linesPlot(df,eventHandler):
	for column in df:
		if column != "Temperature":
			eventHandler.generate(df["Temperature"].values,df[column].values,column)


def generalPlot(filepath,title,df,eventHandler):

	linesPlot(df,eventHandler)
	plt.title(title)
	plt.savefig(filepath+title+'.png')


j = 1
df = pd.read_csv(filename+'.csv')
filepath = filename + '/'
if not os.path.exists(filepath[:-1]):
    os.makedirs(filepath[:-1])


fig,ax = plt.subplots()
eventHandler1 = addEventHandler.eventHandler(fig,ax)
generalPlot(filepath,"Component Melt",df,eventHandler1)
j+=1


# ### Select melting range

# In[ ]:

df_melt=df.ix[(df.iloc[:,0]>minTemperature) & (df.iloc[:,0]< maxTemperature)]
df_data=df_melt.ix[:,1:]
fig2,ax2 = plt.subplots()
eventHandler2 = addEventHandler.eventHandler(fig2,ax2)
generalPlot(filepath,"Temperature Melt",df_melt,eventHandler2)

j+=1




# ### Normalizing 

# In[ ]:

df_norm= (df_data - df_data.min()) / (df_data.max()-df_data.min())*100


fig3,ax3 = plt.subplots()
eventHandler3 = addEventHandler.eventHandler(fig3,ax3)
df_norm = df_norm.assign(Temperature=pd.Series(df_melt.ix[:,0]))
generalPlot(filepath,"Normalized Melt",df_norm,eventHandler3)

# ### Calculate and Show Diff Plot 

fig4,ax4 = plt.subplots()
dfdif = df_norm.sub(df_norm[referenceSample],axis=0)
eventHandler4 = addEventHandler.eventHandler(fig4,ax4)
dfdif = dfdif.assign(Temperature=pd.Series(df_melt.ix[:,0]))
generalPlot(filepath,"Difference Melt",dfdif,eventHandler4)
del dfdif['Temperature']
j+=1


# ### Clustering

# Use KMeans module from SciKit-Learn to cluster your sample into three groups (WT, KO, HET). Be careful, your samples may have less than three groups. So always check the diff plots first.

# In[ ]:




# In[ ]:

mat = dfdif.T.as_matrix()
hc = sc.KMeans(n_clusters=clusterNumber)
hc.fit(mat)

labels = hc.labels_
results = pd.DataFrame([dfdif.T.index,labels])
printResults = ""
for i in range(0,clusterNumber):
	printResults = printResults + str(results.ix[:0,results.ix[1]==i])+'\n'
print printResults
print "----------------------------------------"
with open(filepath+'Results.txt','w') as f:
	f.write(printResults)


plt.show()