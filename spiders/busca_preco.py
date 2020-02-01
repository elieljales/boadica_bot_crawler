# -*- coding: utf-8 -*-
import scrapy
import csv

class CpuSpider(scrapy.Spider):
    name = 'busca_preco'

    def start_requests(self):
        urls = [
            'https://www.boadica.com.br/pesquisa/cpu_proc/precos?ClasseProdutoX=5&CodCategoriaX=27&XT=13',
            'https://www.boadica.com.br/pesquisa/cpu_plmae/precos?ClasseProdutoX=5&CodCategoriaX=13&XT=2&XE=2&XG=4',
            'https://www.boadica.com.br/pesquisa/mem_cpu/precos?ClasseProdutoX=3&CodCategoriaX=14&XT=8&XK=10',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse,meta={'dont_redirect': True,"handle_httpstatus_list": [302]})

    def parse(self, response):
        try:
            ultima_pagina = response.xpath('//div[@class="no-mobile-inline"]/a[@title= "Última"]/@href').get()
            ultima_pagina = ultima_pagina.split('curpage=')
            int(ultima_pagina[1])
            link = response.url+'&curpage='
            for pagina in range(1,int(ultima_pagina[1])):
                yield scrapy.Request(url=link+str(pagina), callback=self.item_pagina,meta={'dont_redirect': True,"handle_httpstatus_list": [302]})
        except Exception as erro:
            self.salvar_log("parse : " + str(erro))
        
    def item_pagina(self, response):
        itens = response.xpath('//div[@class="pull-left"]/a/span/text()').getall()
        precos = response.xpath('//div[@class="col-md-1 preco"]//text()').getall()
        lojas = response.xpath('//div[@class="mobile loja-mobile"]/a[2]/text()').getall()
        tipo_peca = response.url.split('/')[4]
        self.salvar_itens(self.limpar_lista(itens), precos, lojas, tipo_peca)  
        pass    
        
    def limpar_lista(self, itens):
        while '- BOX' in itens:
            itens.remove("- BOX")
        while '- OEM' in itens:
            itens.remove("- OEM")
        return itens
        
    def tratar_preco(self, preco):
        preco = preco.split(' ')[1]
        preco = preco.replace('.','')
        preco = preco.replace(',' , '.')
        try:
            preco = int(float(preco))
        except Exception as erro:
            self.salvar_log("tratar_preco : " + "dado : "+ preco + str(erro))
            preco = preco 
        return preco

    def buscar_item(self):
        entrada_usuario = getattr(self,'busca','')
        itens_buscados = entrada_usuario.split(',')
        cpu = itens_buscados[0]
        plmae = itens_buscados[1]
        mem = itens_buscados[2]
        
#    def separar_pecas(self,itens, precos, lojas, tipo_peca):
#        if tipo_peca == 'cpu_proc'
#        elif tipo_peca == 'cpu_plmae'
#        elif tipo_peca == 'cpu_mem'
    
    def salvar_itens(self,itens, precos, lojas, tipo_peca):
        with open(tipo_peca+'.csv','a', newline='') as arquivo_csv:
            writer = csv.writer(arquivo_csv, delimiter=';' )
            for item in range(len(itens)):
                writer.writerow((itens[item].strip() , self.tratar_preco(precos[item].strip()) , lojas[item].strip()))
                
    def ordenar_csv(self):
        reader = csv.reader(open("mem_cpu.csv"), delimiter=";")
        ordenado = sorted(reader, key=lambda row: row[1], reverse=True)
        writer = csv.writer(open("mem_cpu_ordenado.csv",'a', newline=''), delimiter=";")
        for row in ordenado:
            writer.writerow(row)
        
             
    def salvar_log(self, erro):
        log = open('log.txt','w')
        log.write(erro)

        
        