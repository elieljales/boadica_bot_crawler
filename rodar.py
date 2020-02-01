import csv
import os
from scrapy.cmdline import execute
from operator import itemgetter, attrgetter
os.chdir(os.path.dirname(os.path.realpath(__file__)))



def rodar_robo():
    try:
        execute(
        [ 
            'scrapy',
            'crawl',
            'busca_preco', 
        ]
        )

    except SystemExit:
        pass

def main():
    rodar_robo()
    os.system('cls')
    cpu_proc = 'Ryzen 7 2700'
    cpu_plmae = 'B450'
    mem_cpu = '4G'
    
     #Buscar o processador 
    cpu_lista = ordenar_csv_beta('cpu_proc')
    cpu_preco = buscar_preco(cpu_proc,cpu_lista)
    
        #Buscar a placa mae
    plmae_lista = ordenar_csv_beta('cpu_plmae')
    plmae_preco = buscar_preco(cpu_plmae,plmae_lista)    

    #Buscar a memoria
    mem_lista = ordenar_csv_beta('mem_cpu')
    mem_preco = buscar_preco(mem_cpu,mem_lista)    

    
    
    return cpu_preco,plmae_preco,mem_preco
   
def ordenar_csv_beta(tipo_peca):
    with open (tipo_peca + ".csv", "r") as f:
        dados = csv.reader(f, delimiter=";")
        lista = list(dados)
        lista_ordenada = sorted (lista, key = lambda dado: int(dado[1]), reverse = False)
    return lista_ordenada

def buscar_preco(peca, lista_ordenada):
    for item in range(len(lista_ordenada)):
        if peca in str(lista_ordenada[item]):
            print(lista_ordenada[item])
            return lista_ordenada[item]
    return 0



if __name__ == "__main__":
    main()