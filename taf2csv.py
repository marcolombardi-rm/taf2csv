import tkinter as tk
from tkinter import *
from tkinter import filedialog, ttk, messagebox
import os

mainwindow = tk.Tk()
mainwindow.geometry("475x120")
mainwindow.title("taf2csv v0.1 - )c( Copyleft Marco LOMBARDI - 2020")
framewindow = tk.Frame()

def openTAF():
    fileTAF = filedialog.askopenfilename(initialdir=os.getcwd(),title="Selezione un file .taf",filetypes=[("TAF files", "*.taf")])
    TAFpath = str(os.path.split(fileTAF)[0])
    idProv = fileTAF.split('/')
    idProv = str(idProv[-1])
    idProv = idProv.rstrip('.taf')
    ultimoComune = ""
    listaComuni = []
    with open(fileTAF, 'r') as file:
        for line in file:
            codiceComune = line[0:4]
            if codiceComune != ultimoComune:
                listaComuni.append(codiceComune)
            ultimoComune = codiceComune
    #print(listaComuni)
    creaLista(TAFpath,idProv,listaComuni)

def creaLista(TAFpath,idProv,listaComuni):
    labelframe = LabelFrame(mainwindow, text="Scelta la TAF della Provincia di " + idProv, labelanchor="n")
    labelframe.pack(fill="both", expand="yes")
    empty1 = Label(labelframe, text=" ")
    empty1.grid(in_=labelframe, row=0, column=0, sticky=W)
    label1 = Label(labelframe, text="Seleziona il Comune interessato:")
    label1.grid(in_=labelframe, row=1, column=0, sticky=W)
    selCom_box = tk.StringVar()
    selCom_chosen = ttk.Combobox(labelframe, justify='center', width=10, state='readonly')
    selCom_chosen['values'] = tuple(listaComuni)
    selCom_chosen.grid(in_=labelframe, row=1, column=1, sticky=W)
    selCom_chosen.current(0)
    label2 = Label(labelframe, text="poi clicca sul pulsante 'Esporta in CSV'")
    label2.grid(in_=labelframe, row=1, column=2, sticky=W)
    empty2 = Label(labelframe, text=" ")
    empty2.grid(in_=labelframe, row=2, column=0, sticky=W)
    btn = Button(text="Esporta in CSV", command =(lambda: esportaCSV(TAFpath,idProv,selCom_chosen.get())))
    btn.place(relx=0.5, rely=0.5, anchor=CENTER)
    btn.grid(in_=labelframe, row=3, column=1, sticky=W)

def esportaCSV(TAFpath,idProv,idComune):
    fileTAF = TAFpath + "/" + idProv + ".taf"
    fileTAF = os.path.normpath(fileTAF)
    print(fileTAF)
    fileCSV = TAFpath + "/" + idProv + "_" + idComune + ".csv"
    fileCSV = os.path.normpath(fileCSV)
    stringaPF = "nome;est;nord;descrizione"
    with open(fileCSV, "w") as file:
                    file.write(stringaPF + "\n")
    stringaPF = ""                
    with open(fileTAF, 'r') as file:
        for data in file:
            if data[0:4] == idComune:
                comSez = data[4:5]
                if comSez == " ":
                    comSez = ""
                tmp = int(data[15:17])
                fgAll = data[11:12]
                fgCod = str(data[6:10])    
                if fgCod[0:2] == "10":
                    fgCod = "A" + fgCod[2:4]                            
                if fgCod[0:2] == "11":
                    fgCod = "B" + fgCod[2:4]
                if fgAll == " ":
                    fgAll = "0"
                pfDescr = data[30:100]
                y,x = data[102:114],data[115:127]
                if tmp < 10:
                    stringaPF = "PF0%1s/%3s%1s/" % (tmp,fgCod[-3:],fgAll) + idComune + comSez + ";" + x.strip() + ";" + y.strip() + ";" + pfDescr
                else:
                    stringaPF = "PF%2s/%3s%1s/" % (tmp,fgCod[-3:],fgAll) + idComune + comSez + ";" + x.strip() + ";" + y.strip() + ";" + pfDescr
                #print(stringaPF)    
                with open(fileCSV, "a") as file:
                    file.write(stringaPF + "\n")

    messagebox.showinfo("", "TAF selezionata esportata in " + fileCSV)
    
openTAF()
mainwindow.mainloop()
