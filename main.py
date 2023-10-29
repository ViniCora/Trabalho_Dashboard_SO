import tkinter as tk
from tkinter import *
import threading

class DashboardController:
    def __init__(self):
        self.dashboard = tk.Tk()
        self.dashApp = DashboardApp(self.dashboard)
        self.dados = BuscaDados()
        self.buscarDados()
        self.dashboard.mainloop()

    def buscarDados(self):
        thread1 = threading.Thread(target=self.dados.buscaProcessos)
        thread2 = threading.Thread(target=self.dados.buscaInfoSO)
        thread3 = threading.Thread(target=self.dados.buscaParticoes)
        thread4 = threading.Thread(target=self.dados.buscaInfoHardware)
        thread5 = threading.Thread(target=self.dados.buscaInfoMemoria)
        thread6 = threading.Thread(target=self.dados.buscaInformacoesCPU)
        thread7 = threading.Thread(target=self.dados.buscaQuantidadeCPU)

        thread1.start()
        thread2.start()
        thread3.start()
        thread4.start()
        thread5.start()
        thread6.start()
        thread7.start()
        thread1.join()
        thread2.join()
        thread3.join()
        thread4.join()
        thread5.join()
        thread6.join()
        thread7.join()
        self.dashboard.after(5000, self.buscarDados)


#Model
class BuscaDados:
    def __init__(self):
        self.informacoesCPU = None
        self.quantidadeCPU = None
        self.infoHardware = None
        self.infoMemoria = None
        self.processos = None
        self.particoes = None
        self.infoSO = None

    def buscaInformacoesCPU(self):
        print('informacoesCPU')

    def buscaInfoMemoria(self):
        print('Memoria')

    def buscaQuantidadeCPU(self):
        print('quantidadeCPU')

    def buscaInfoHardware(self):
        print('infoHardware')

    def buscaProcessos(self):
        print('processos')

    def buscaParticoes(self):
        print('particoes')

    def buscaInfoSO(self):
        print('Info SO')

#View
class DashboardApp:
    def __init__(self, dashboard):
        self.dashboard = dashboard
        self.dashboard.title("Dashboard Sistemas Operacionais")
        self.dashboard.geometry("960x540")
        self.dashboard.config(background="#eff5f6")

        self.header = Frame(self.dashboard, bg='#333333')
        self.header.place(x=0, y=0, width=960, height=60)
        #self.iniciaTela()


if __name__ == "__main__":
    dash = DashboardController()
