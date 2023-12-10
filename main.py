import tkinter as tk
from tkinter import *
from tkinter import ttk
import threading
import subprocess
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import re

class DashboardController:
    # Classe para controlar as chamadas do dashboard via thread
    def __init__(self):
        self.dashboard = tk.Tk()
        self.dashApp = DashboardApp(self.dashboard)
        self.dados = BuscaDados()
        self.buscarDados()
        self.dashboard.mainloop()

    def buscarDados(self):
        #Codigo que irá buscar a cada 5 segundos os dados do linux via threads, utilizamos uma thread para cada função de busca
        thread1 = threading.Thread(target=self.dados.buscaProcessos)
        thread2 = threading.Thread(target=self.dados.buscaInfoSO)
        thread3 = threading.Thread(target=self.dados.buscaParticoes)
        thread4 = threading.Thread(target=self.dados.buscaInfoHardware)
        thread5 = threading.Thread(target=self.dados.buscaInfoMemoria)
        thread6 = threading.Thread(target=self.dados.buscaInformacoesCPU)
        thread7 = threading.Thread(target=self.dados.buscaQuantidadeCPU)
        thread8 = threading.Thread(target=self.dados.buscaInfoParticoesDir)


        thread1.start()
        thread2.start()
        thread3.start()
        thread4.start()
        thread5.start()
        thread6.start()
        thread7.start()
        thread8.start()
        thread1.join()
        thread2.join()
        thread3.join()
        thread4.join()
        thread5.join()
        thread6.join()
        thread7.join()
        thread8.join()
        #Depois de buscar as informações o dashboard é atualizado com os dados
        self.dashApp.attInformacoes(self.dados)
        self.dashboard.after(5000, self.buscarDados)


#Model
class BuscaDados:
    #Classe que possue os valores mostrados em tela e que faz a busca desses valores
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
        self.infoParticoesDir = None

    #Busca das informações do CPU
    def buscaInformacoesCPU(self):
        cpuInfos = subprocess.run(['cat', '/proc/cpuinfo'], stdout=subprocess.PIPE)
        cpuInfosText = text=cpuInfos.stdout
        self.informacoesCPU = cpuInfosText.splitlines()

    #Busca informações da memoria
    def buscaInfoMemoria(self):
        self.memoriaResumo = subprocess.run(['free'], stdout=subprocess.PIPE)
        memoriaInfos = str(self.memoriaResumo.stdout)
        memoriaInfos.split()

        #Aqui estamos separando cada valor de uso de cada tipo da memoria, entre total, usada, livre, compartilhada, buff/cache e disponivel
        segunda_linha = memoriaInfos.split("\\n")[1]
        numbers = re.findall(r"\d+", segunda_linha)

        self.mtotal = numbers[0]
        self.mUsada = numbers[1]
        self.mLivre = numbers[2]
        self.mCompartilhada = numbers[3]
        self.mBuff = numbers[4]
        self.mDisponivel = numbers[5]

        self.infoMemoria = subprocess.run(['cat', '/proc/meminfo'], stdout=subprocess.PIPE)

    #Busca de quantidade de CPUs, esse valor não está sendo usado, mas foi mantido para mostrar o desenvolvimento do raciocinio
    def buscaQuantidadeCPU(self):
        cpu = subprocess.run(['nproc'], stdout = subprocess.PIPE)
        self.quantidadeCPU = cpu.stdout

    #Busca das informações de hardware
    def buscaInfoHardware(self):
        hardwareInfo = subprocess.run(['lscpu'], stdout = subprocess.PIPE)
        hardwareInfoText = text=hardwareInfo.stdout
        self.infoHardware = hardwareInfoText.splitlines()

    #Busca dos processos, utilizando n1 para atualizar apenas uma vez
    def buscaProcessos(self):
        processosInfos = subprocess.run(['top', '-b', '-n1'], stdout = subprocess.PIPE)
        processosInfosText = text=processosInfos.stdout
        self.processos = processosInfosText.splitlines()

    #Busca das partições
    def buscaParticoes(self):
        particoesInfo = subprocess.run(['cat', '/proc/partitions'], stdout = subprocess.PIPE)
        particoesInfosText = text=particoesInfo.stdout
        self.particoes = particoesInfosText.splitlines()

    #Busca das informações do Sistema Operacional
    def buscaInfoSO(self):
        self.infoSO = subprocess.run(["uname", '-a'], stdout=subprocess.PIPE).stdout

    def buscaInfoParticoesDir(self):
        self.infoParticoesDir = subprocess.run(["df", '-h'], stdout=subprocess.PIPE).stdout

#View
class DashboardApp:
    #Essa classe manipula especificamente a parte visual do codigo, pegando os dados da classe de BuscaDados
    def __init__(self, dashboard):
        #Criação dos Frames, Notebooks e ListBox
        self.dashboard = dashboard
        self.dashboard.title("Dashboard Sistemas Operacionais")
        self.dashboard.geometry("960x540")

        nb = ttk.Notebook(self.dashboard)
        nb.place(x=0, y=0)

        self.frame1 = Frame(dashboard, width=960, height=530, bg='#eff5f6')
        nb.add(self.frame1, text="Info. SO")

        self.frame2 = tk.Listbox(dashboard, width=960, height=530, bg='#eff5f6')
        nb.add(self.frame2, text="Info. CPU")

        self.frame3 = tk.Listbox(dashboard, width=960, height=530, bg='#eff5f6')
        nb.add(self.frame3, text="Info. Hardware")

        self.frame4 = Frame(dashboard, width=960, height=530, bg='#eff5f6')
        nb.add(self.frame4, text="Info. Memoria")

        nb2 = ttk.Notebook(self.frame4)
        nb2.place(x=0, y=0)
        self.frame4_1 = Frame(self.frame4, width=960, height=530, bg='#eff5f6')
        nb2.add(self.frame4_1, text="Valores totais memória")
        self.frame4_2 = Frame(self.frame4, width=960, height=530, bg='#eff5f6')
        nb2.add(self.frame4_2, text="Gráfico memória")

        self.frame5 = tk.Listbox(dashboard, width=960, height=530, bg='#eff5f6')
        nb.add(self.frame5, text="Info. processos")
        scroll = tk.Scrollbar( self.frame5)
        scroll.pack(side="right", fill="both")

        self.frame5.config(yscrollcommand=scroll.set)
        scroll.config(command= self.frame5.yview)

        self.frame6 = tk.Listbox(dashboard, width=960, height=530, bg='#eff5f6')
        nb.add(self.frame6, text="Info. partições")

        self.frame7 = tk.Listbox(dashboard, width=960, height=530, bg='#eff5f6')
        nb.add(self.frame7, text="Info. Arquivos")

        nb3 = ttk.Notebook(self.frame7)
        nb3.place(x=0, y=0)
        self.frame7_1 = tk.Listbox(self.frame7, width=960, height=530, bg='#eff5f6')
        nb3.add(self.frame7_1, text="Info. Partições")
        self.frame7_2 = tk.Listbox(self.frame7, width=960, height=530, bg='#eff5f6')
        nb3.add(self.frame7_2, text="Navegação Diretórios")

        self.frame8 = tk.Listbox(dashboard, width=960, height=530, bg='#eff5f6')
        nb.add(self.frame8, text="Entrada/Saída")

    #Função que atualiza todas as abas de informações
    def attInformacoes(self, dados):
        # self.attGraficoMemoria(dados)
        # self.attTabelaMemoria(dados)
        # self.attInfoSO(dados)
        # self.attInfoProcesso(dados)
        # self.attInfoCPU(dados)
        # self.attInfoHardware(dados)
        # self.attInfoParticoes(dados)
        # self.attInfoParticoesDir(dados)
        print()

    # Atualiza a tabela de dados da memoria usando Treeview
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

    #Adiciona linha por linha dos dados de processos
    def attInfoProcesso(self, dados):
        #Deleta as informações antigas
        for widget in self.frame5.winfo_children():
            widget.destroy()
        self.frame5.delete(0, END)
        i = 1
        #Insere uma linha vazia para identação
        self.frame5.insert(0, '')
        #Adiciona as linhas de informações
        for linha in dados.processos:
            self.frame5.insert(i, linha)
            i+=1
        labelEXP = ttk.Label(self.frame5, text="Informações sobre os Processos:")
        labelEXP.pack()

    # Adiciona linha por linha dos dados da CPU
    def attInfoCPU(self, dados):
        # Deleta as informações antigas
        for widget in self.frame2.winfo_children():
            widget.destroy()
        self.frame2.delete(0, END)
        labelEXP = ttk.Label(self.frame2, text="Informações sobre a CPU:")
        i = 1
        # Insere uma linha vazia para identação
        self.frame2.insert(0, '')
        # Adiciona as linhas de informações
        for linha in dados.informacoesCPU:
            self.frame2.insert(i, linha)
            i += 1
        labelEXP.pack()

    # Adiciona linha por linha dos dados do hardware
    def attInfoHardware(self, dados):
        # Deleta as informações antigas
        for widget in self.frame3.winfo_children():
            widget.destroy()
        self.frame3.delete(0, END)
        labelEXP = ttk.Label(self.frame3, text="Informações sobre o Hardware:")
        i = 1
        # Insere uma linha vazia para identação
        self.frame3.insert(0, '')
        # Adiciona as linhas de informações
        for linha in dados.infoHardware:
            self.frame3.insert(i, linha)
            i += 1
        labelEXP.pack()

    # Adiciona linha por linha dos dados das partições
    def attInfoParticoes(self, dados):
        # Deleta as informações antigas
        for widget in self.frame6.winfo_children():
            widget.destroy()
        self.frame6.delete(0, END)
        labelEXP = ttk.Label(self.frame6, text="Informações sobre as Partições:")
        i = 1
        # Insere uma linha vazia para identação
        self.frame6.insert(0, '')
        # Adiciona as linhas de informações
        for linha in dados.particoes:
            self.frame6.insert(i, linha)
            i += 1
        labelEXP.grid()

    # Adiciona os dados do Sistema Operacional
    def attInfoSO(self, dados):
        # Deleta as informações antigas
        for widget in self.frame1.winfo_children():
            widget.destroy()
        labelEXP = ttk.Label(self.frame1, text="Informações sobre o SO:")
        infoSOLabel = ttk.Label(self.frame1, text=dados.infoSO, background='#eff5f6')
        labelEXP.grid()
        infoSOLabel.grid()

    #Cria um grafico para o uso de memória e insere a imagem na tela
    def attGraficoMemoria(self, dados):
        # Deleta o grafico antigo
        for widget in self.frame4_2.winfo_children():
            widget.destroy()
        #Tamanho
        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)
        #Labels e dados
        labels = ['Usado', 'Livre', 'Buffer/Cache']
        sizes = [dados.mUsada, dados.mLivre, dados.mBuff]

        #Angulos
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        canvas = FigureCanvasTkAgg(fig, master=self.frame4_2)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def attInfoParticoesDir(self, dados):
        # Deleta as informações antigas
        for widget in self.frame7_1.winfo_children():
            widget.destroy()
        self.frame7_1.delete(0, END)
        labelEXP = ttk.Label(self.frame7_1, text="Informações sobre as Partições do Sistema de arquivos:")
        i = 1
        # Insere uma linha vazia para identação
        self.frame7_1.insert(0, '')
        # Adiciona as linhas de informações
        for linha in dados.infoParticoesDir:
            self.frame7_1.insert(i, linha)
            i += 1
        labelEXP.grid()

if __name__ == "__main__":
    dash = DashboardController()