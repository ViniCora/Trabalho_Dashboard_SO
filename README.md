def buscaInfoMemoria(self):
        self.memoriaResumo = subprocess.run(['free'], stdout=subprocess.PIPE)
        memoriaInfos = str(self.memoriaResumo.stdout)
        memoriaInfos.split()
        segunda_linha = memoriaInfos.split("\\n")[1]
        numbers = re.findall(r"\d+", segunda_linha)

        mtotal = numbers[0]
        mUsada = numbers[1]
        mLivre = numbers[2]
        mCompartilhada = numbers[3]
        mBuff = numbers[4]
        mDisponivel = numbers[5]

        self.infoMemoria = subprocess.run(['cat', '/proc/meminfo'], stdout=subprocess.PIPE)
        mDetalhada = text=self.infoMemoria.stdout



### Como Rodar
```
python3 main.py
```

###Libs utilizadas
*is mathplotlib 




### Comandos
```
Informações detalhadas sobre todos os cpu
cat /proc/cpuinfo

Quantidade de cpu
nproc

Informações de hardware
lscpu

Informações sobre memória (free é resumido)
cat /proc/meminfo
free

Processos e porcentagens de uso de cpu e memoria
ps aux

Partições
cat /proc/partitions

Informações do sistema operacional
uname -a 
```
