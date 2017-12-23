import matplotlib.pyplot as plt
import numpy as np;

class eventHandler():

    def __init__ (self,fig,ax):
        self.line = []
        self.annot = []
        self.column = []
        self.fig = fig
        self.ax = ax
        self.text = ""

    def update_annot(self,ind, annot,i):
        x,y = self.line[i].get_data()
        annot.xy = (x[ind["ind"][0]], y[ind["ind"][0]])
        text = self.column[i]

        annot.set_text(text)
        flag = False
        if self.text != text:
            print text
            self.text = text
            flag = True
        annot.get_bbox_patch().set_alpha(0.4)

        return flag




    def hover(self,event):

        vis = []
        for annot in self.annot:
            vis.append(annot.get_visible())

        i = 0
        drawFlag = False
        if event.inaxes == self.ax:
            for line in self.line:
                cont, ind = line.contains(event)
                if cont:
                    drawFlag2 = self.update_annot(ind,annot,i)
                    j = 0
                    for v in vis:
                        if v and i != j:
                            self.annot[j].set_visible(False)
                    annot.set_visible(True)
                    drawFlag = True
                   
                i+=1
            if drawFlag :
                self.fig.canvas.draw_idle()



            


    def generate(self,x,y,column):
        self.column.append(column)


        norm = plt.Normalize(1,4)
        cmap = plt.cm.RdYlGn

        myline, = plt.plot(x,y)
        self.line.append(myline)

        annot = self.ax.annotate("", xy=(0,0), xytext=(-20,20),textcoords="offset points",
                        bbox=dict(boxstyle="round", fc="w"),
                        arrowprops=dict(arrowstyle="->"))
        self.annot.append(annot)

        self.annot[-1].set_visible(False)
        self.fig.canvas.mpl_connect("motion_notify_event", self.hover)
