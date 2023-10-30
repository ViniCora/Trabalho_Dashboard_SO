import tkinter as tk
from tkinter import *
from tkinter import ttk
import threading
import subprocess
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import re

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
        self.mtotal = None
        self.mUsada = None
        self.mLivre = None
        self.mCompartilhada = None
        self.mBuff = None
        self.mDisponivel = None

    def buscaInformacoesCPU(self):
        self.informacoesCPU = subprocess.run(['cat', '/proc/cpuinfo'], stdout=subprocess.PIPE)
        cpuInfos = text=self.informacoesCPU.stdout
        cpuInfos.splitlines()


    def buscaInfoMemoria(self):
        self.memoriaResumo = subprocess.run(['free'], stdout=subprocess.PIPE)
        memoriaInfos = str(self.memoriaResumo.stdout)
        memoriaInfos.split()
        segunda_linha = memoriaInfos.split("\\n")[1]
        numbers = re.findall(r"\d+", segunda_linha)

        self.mtotal = numbers[0]
        self.mUsada = numbers[1]
        self.mLivre = numbers[2]
        self.mCompartilhada = numbers[3]
        self.mBuff = numbers[4]
        self.mDisponivel = numbers[5]

        self.infoMemoria = subprocess.run(['cat', '/proc/meminfo'], stdout=subprocess.PIPE)
        mDetalhada = text=self.infoMemoria.stdout


    def buscaQuantidadeCPU(self):
        cpu = subprocess.run(['nproc'], stdout = subprocess.PIPE)
        self.quantidadeCPU = cpu.stdout

    def buscaInfoHardware(self):
        hardwareInfo = subprocess.run(['lscpu'], stdout = subprocess.PIPE)
        hardwareInfoText = text=hardwareInfo.stdout
        self.infoHardware = hardwareInfoText.splitlines()

    def buscaProcessos(self):
        processosInfos = subprocess.run(['ps', 'aux'], stdout = subprocess.PIPE)
        processosInfosText = text=processosInfos.stdout
        self.processos = processosInfosText.splitlines()

    def buscaParticoes(self):
        particoesInfo = subprocess.run(['cat', '/proc/partitions'], stdout = subprocess.PIPE)
        particoesInfosText = text=particoesInfo.stdout
        self.particoes = particoesInfosText.splitlines()

    def buscaInfoSO(self):
        self.infoSO = subprocess.run(["uname", '-a'], stdout=subprocess.PIPE)

#View
class DashboardApp:
    def __init__(self, dashboard):
        self.dashboard = dashboard
        self.dashboard.title("Dashboard Sistemas Operacionais")
        self.dashboard.geometry("960x540")
        self.teste = False

        nb = ttk.Notebook(self.dashboard)
        nb.place(x=0, y=0)

        self.frame1 = Frame(dashboard, width=960, height=530, bg='#eff5f6')
        nb.add(self.frame1, text="Info. SO")

        self.frame2 = Frame(dashboard, width=960, height=530, bg='#eff5f6')
        nb.add(self.frame2, text="Info. CPU")

        self.frame3 = Frame(dashboard, width=960, height=530, bg='#eff5f6')
        nb.add(self.frame3, text="Info. Hardware")

        self.frame4 = Frame(dashboard, width=960, height=530, bg='#eff5f6')
        nb.add(self.frame4, text="Info. Memoria")

        nb2 = ttk.Notebook(self.frame4)
        nb2.place(x=0, y=0)
        self.frame4_1 = Frame(self.frame4, width=960, height=530, bg='#eff5f6')
        nb2.add(self.frame4_1, text="Valores totais memória")
        self.frame4_2 = Frame(self.frame4, width=960, height=530, bg='#eff5f6')
        nb2.add(self.frame4_2, text="Gráfico memória")

        self.frame5 = Frame(dashboard, width=960, height=530, bg='#eff5f6')
        nb.add(self.frame5, text="Info. processos")

        self.frame6 = Frame(dashboard, width=960, height=530, bg='#eff5f6')
        nb.add(self.frame6, text="Info. partições")

    def attTabelaMemoria(self, dados):
        for widget in self.frame4_1.winfo_children():
            widget.destroy()
        table = ttk.Treeview(self.frame4_1, columns=(1, 2), show="headings", height=10)
        table.pack()
        table.heading(1, text="Tipo")
        table.heading(2, text="Valor usado/disponivel (kb)")
        table.insert('', tk.END, values=['Memoria Total', dados.mtotal])
        table.insert('', tk.END, values=['Memoria Usado', dados.mUsada])
        table.insert('', tk.END, values=['Memoria Livre', dados.mLivre])
        table.insert('', tk.END, values=['Buff/Cache', dados.mBuff])
        table.insert('', tk.END, values=['Memoria Compartilhada', dados.mCompartilhada])
        table.insert('', tk.END, values=['Memoria Disponivel', dados.mDisponivel])


    def attInformacoes(self, dados):
        self.attGraficoMemoria(dados)
        self.attTabelaMemoria(dados)
        self.attInfoSO(dados)
        self.attInfoProcesso(dados)
        self.attInfoCPu(dados)
        self.attInfoHardware(dados)
        self.attInfoParticoes(dados)

    def attInfoProcesso(self, dados):
        for widget in self.frame5.winfo_children():
            widget.destroy()
        labelEXP = ttk.Label(self.frame5, text="Informações sobre os Processos:")
        infoProcessosLabel = ttk.Label(self.frame5, text=dados.infoHardware)
        labelEXP.pack()
        infoProcessosLabel.pack()

    def attInfoCPu(self, dados):
        for widget in self.frame2.winfo_children():
            widget.destroy()
        labelEXP = ttk.Label(self.frame2, text="Informações sobre a CPU:")
        infoCPULabel = ttk.Label(self.frame2, text=dados.infoHardware)
        labelEXP.pack()
        infoCPULabel.pack()

    def attInfoHardware(self, dados):
        for widget in self.frame3.winfo_children():
            widget.destroy()
        labelEXP = ttk.Label(self.frame3, text="Informações sobre o Hardware:")
        infoHardwareLabel = ttk.Label(self.frame3, text=dados.infoHardware)
        labelEXP.pack()
        infoHardwareLabel.pack()

    def attInfoParticoes(self, dados):
        for widget in self.frame6.winfo_children():
            widget.destroy()
        labelEXP = ttk.Label(self.frame6, text="Informações sobre as Partições:")
        infoParticoesLabel = ttk.Label(self.frame6, text=dados.particoes)
        labelEXP.pack()
        infoParticoesLabel.pack()

    def attInfoSO(self, dados):
        for widget in self.frame1.winfo_children():
            widget.destroy()
        labelEXP = ttk.Label(self.frame1, text="Informações sobre o SO:")
        infoSOLabel = ttk.Label(self.frame1, text=dados.infoSO)
        labelEXP.pack()
        infoSOLabel.pack()

    def attGraficoMemoria(self, dados):
        for widget in self.frame4_2.winfo_children():
            widget.destroy()
        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)
        labels = ['Usado', 'Livre', 'Buffer/Cache']
        sizes = [dados.mUsada, dados.mLivre, dados.mBuff]

        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        canvas = FigureCanvasTkAgg(fig, master=self.frame4_2)
        canvas.draw()
        canvas.get_tk_widget().pack()

if __name__ == "__main__":
    dash = DashboardController()