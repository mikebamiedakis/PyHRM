
# coding: utf-8

# ## Introduction

# Please read a very nice introduction provided by self.figureNumberapa BioSystems to understand, prepare and troubleshoot
# 
# http://www.self.figureNumberapabiosystems.com/document/introduction-high-resolution-melt-analysis-guide/
# 

# ### Import Python modules for analysis


import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import addEventHandler
import sklearn.cluster as sc
# ### Read and Plot Melting Data


class PYHRM():

	def __init__(self):
		
		# Do not change this.
		self.figureNumber = 1

		# User Defined Variables.
		self.filename = 'test'
		self.referenceSample = 'J14'
		self.clusterNumber = 3
		self.minTemperature= 77
		self.maxTemperature = 85


	def linesPlot(self,df,eventHandler):

		for column in df:
			if column != "Temperature":
				eventHandler.generate(df["Temperature"].values,df[column].values,column)


	def generalPlot(self,title,df,eventHandler):

		self.linesPlot(df,eventHandler)
		plt.title(title)
		plt.savefig(self.filepath+title+'.png')


	def cluster(self, dfdif):

		mat = dfdif.T.as_matrix()
		hc = sc.KMeans(n_clusters= self.clusterNumber)
		hc.fit(mat)

		labels = hc.labels_
		results = pd.DataFrame([dfdif.T.index,labels])
		printResults = ""

		for i in range(0,self.clusterNumber):
			tempResult = results.ix[:0,results.ix[1]==i]
			tempPrint = ""

			for column in tempResult:
				tempPrint = tempPrint + tempResult[column][0] + " "

			printResults = printResults + "Cluster " + str(i+1) +": " + tempPrint +'\n\n'

		print printResults
		print "----------------------------------------"
		with open(self.filepath+'Results.txt','w') as f:
			f.write(printResults)


	def calculateDiff(self, df_norm, df_melt):

		fig4,ax4 = plt.subplots()

		dfdif = df_norm.sub(df_norm[self.referenceSample],axis=0)
		eventHandler4 = addEventHandler.eventHandler(fig4,ax4)
		dfdif = dfdif.assign(Temperature=pd.Series(df_melt.ix[:,0]))
		self.generalPlot("Difference Melt",dfdif,eventHandler4)
		del dfdif['Temperature']
		self.figureNumber += 1

		return dfdif, eventHandler4



	def normalization(self, df_data, df_melt):

		df_norm= (df_data - df_data.min()) / (df_data.max()-df_data.min())*100
		fig3,ax3 = plt.subplots()
		eventHandler3 = addEventHandler.eventHandler(fig3,ax3)
		df_norm = df_norm.assign(Temperature=pd.Series(df_melt.ix[:,0]))
		self.generalPlot("Normalized Melt",df_norm,eventHandler3)

		return df_norm, eventHandler3


	def showTemperatureMelt(self, df):

		df_melt=df.ix[(df.iloc[:,0]>self.minTemperature) & (df.iloc[:,0]< self.maxTemperature)]
		df_data=df_melt.ix[:,1:]
		fig2,ax2 = plt.subplots()
		eventHandler2 = addEventHandler.eventHandler(fig2,ax2)
		self.generalPlot("Temperature Melt",df_melt,eventHandler2)

		self.figureNumber += 1

		return df_melt, df_data, eventHandler2


	def showComponentMelt(self, df):

		fig,ax = plt.subplots()
		eventHandler1 = addEventHandler.eventHandler(fig,ax)
		self.generalPlot("Component Melt",df,eventHandler1)
		self.figureNumber += 1

		return eventHandler1


	def fileHandler(self):
		'''
			This method opens the file in question and generates a folder to store the output.
		'''
		df = pd.read_csv(self.filename+'.csv')
		self.filepath = self.filename + '/'
		if not os.path.exists(self.filepath[:-1]):
			os.makedirs(self.filepath[:-1])

		if 'Temperature' not in df:
			print "The first column of the imported file must be named Temperature."
			self.wait()
			exit(0)
		elif self.referenceSample not in df:
			print "There is not column named "+self.referenceSample+" in the imported file."
			self.wait()
			exit(0)

		return df


	def wait(self):
		raw_input("Press Enter to continue...")


	def run(self):
		'''
			This method calls all the other methods.
		'''
		df = self.fileHandler()

		eventHandler1 = self.showComponentMelt(df)

		[dfMelt, dfData, eventHandler2] = self.showTemperatureMelt(df)

		dfNorm, eventHandler3 = self.normalization( dfData, dfMelt)

		[dfDiff, eventHandler4] = self.calculateDiff(dfNorm, dfMelt)

		self.cluster(dfDiff)

		plt.show()




if __name__ == "__main__":
    pyHRM = PYHRM()
    pyHRM.run()