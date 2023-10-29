import tkinter as tk
from tkinter import *
from tkinter import ttk
import threading
import subprocess

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
        self.dashApp.attInformacoes(self.dados)
        self.dashboard.after(5000, self.buscarDados)


#Model
class BuscaDados:
    def __init__(self):
        self.informacoesCPU = None
        self.quantidadeCPU = None
        self.infoHardware = None
        self.infoMemoria = None
        self.memoriaResumo = None
        self.processos = None
        self.particoes = None
        self.infoSO = None
        self.infoSO2 = None

    def buscaInformacoesCPU(self):
        self.informacoesCPU = subprocess.run(['car', '/proc/cpuinfo'], stdout=subprocess.PIPE)

    def buscaInfoMemoria(self):
        self.memoriaResumo = subprocess.run(['free'], stdout=subprocess.PIPE)
        self.infoMemoria = subprocess.run(['cat', '/proc/meminfo'], stdout=subprocess.PIPE)

    def buscaQuantidadeCPU(self):
        self.quantidadeCPU = subprocess.run(['nproc'], stdout = subprocess.PIPE)

    def buscaInfoHardware(self):
        self.infoHardware = subprocess.run(['lscpu'], stdout = subprocess.PIPE)

    def buscaProcessos(self):
        self.processos = subprocess.run(['ps', 'aux'], stdout = subprocess.PIPE)

    def buscaParticoes(self):
        self.particoes = subprocess.run(['cat', '/proc/partitions'], stdout = subprocess.PIPE)

    def buscaInfoSO(self):
        self.infoSO = subprocess.run(["uname", '-a'], stdout=subprocess.PIPE)
        self.infoSO2 = subprocess.run(['cat', '/proc/version'], stdout=subprocess.PIPE)

#View
class DashboardApp:
    def __init__(self, dashboard):
        self.dashboard = dashboard
        self.dashboard.title("Dashboard Sistemas Operacionais")
        self.dashboard.geometry("960x540")
        self.dashboard.config(background="#eff5f6")

        self.frame1 = Frame(self.dashboard, bg='#eff5f6')
        self.frame1.place(x=0, y=0, width=960, height=540)

        nb = ttk.Notebook(self.dashboard)
        nb.place(x=0, y=0)
        nb.add(self.frame1, text="Aba 1")

        self.frame2 = Frame(dashboard, width=960, height=530, bg='#eff5f6')
        nb.add(self.frame2, text="Aba 2")

        self.frame3 = Frame(dashboard, width=960, height=530, bg='#eff5f6')
        nb.add(self.frame3, text="Aba 3")

        self.frame4 = Frame(dashboard, width=960, height=530, bg='#eff5f6')
        nb.add(self.frame4, text="Aba 4")


    def attInformacoes(self, dados):
        print(dados.infoSO)


if __name__ == "__main__":
    dash = DashboardController()
