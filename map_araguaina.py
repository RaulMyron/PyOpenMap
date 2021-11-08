#import osmapi
### Doc API http://osmapi.metaodi.ch/#osmapi.OsmApi.OsmApi.Map
### instalar a extensão portugues
### instalar a extensão python
### para import acima funcionar
### executar Crtl + F5
# pip3 install osmapi

import pickle
import datetime
import json

#api = osmapi.OsmApi()

#$print(api.NodeGet(13305118))

#print(api.WayGet(816360282))

#min_lat = -7.2719
#max_lat = -7.1200
#min_lon = -48.2581
#max_lon = -48.1407

#list_dict_data = api.Map(min_lon,min_lat,max_lon,max_lat)
#print(list_dict_data)

#with open('map.dictionary','wb') as map_file:
#    pickle.dump(list_dict_data,map_file)

#https://www.techcoil.com/blog/how-to-save-and-load-objects-to-and-from-file-in-python-via-facilities-from-the-pickle-module/

with open('map.dictionary','rb') as map_file:
    list_dict_data = pickle.load(map_file)

#type(list_dict_data) ## Lista e não um dicionario

#criação de 4 dicionários que armazenam apenas [clinicas, hospitais e escolas] e um que armazena todos juntos

dicionario_clinicas = {} #para ubs
dicionario_hospitais = {} #hospitais e upas
dicionario_escolas = {}
dicionario_geral = {} #com tudo


#aqui é criado um loop for do tamanho do dicionario data, nele é verificado cada um dos elementos dentro da list_dict_data
for contador in range(len(list_dict_data)):
    
    try: #aqui ele vai tentar achar os que tem hospital e filtrar para um só dicionario, mesma coisa com os demais para usas tags
        if(list_dict_data[contador]["data"]["tag"]["amenity"]=="hospital")
            
            #1 - se quiser que o id seja o id no openmap //tbm pode ser o uid
            #dicionario_hospitais[list_dict_data[contador]["data"]["id"]] = list_dict_data[contador]["data"]
            
            #2 - se quiser que o id seja o numero por entrada começando de 0, tipo uma lista (foi esse que adotei)
            dicionario_hospitais[(len(dicionario_hospitais))] = list_dict_data[contador]["data"]
            
            #inserindo no dicionario geral
            dicionario_geral[(len(dicionario_geral))] = list_dict_data[contador]["data"]
        
        elif(list_dict_data[contador]["data"]["tag"]["amenity"]=="clinic"): 
            dicionario_clinicas[(len(dicionario_clinicas))] = list_dict_data[contador]["data"]
            
            dicionario_geral[(len(dicionario_geral))] = list_dict_data[contador]["data"]
        
        elif(list_dict_data[contador]["data"]["tag"]["amenity"]=="school"):
            
            dicionario_escolas[(len(dicionario_escolas))] = list_dict_data[contador]["data"]
            
            dicionario_geral[(len(dicionario_geral))] = list_dict_data[contador]["data"] 
    
    except KeyError: #se a tag não existir ou ele não ter a tag, simplesmenhte não faz nada
        pass
    
'''
#print(dicionario_clinicas)
#print(dicionario_escolas)
#print(dicionario_clinicas)
#agora que temos todos os elementos filtrados, pesquisar pelo elemento individual
#print("Olá, bom dia.\nO que você está buscando?")
#print("Hospitais? Pressione 1")
#print("Clínicas? Pressione 2") #tem que pressionar e dar enter, tá?
#print("Escolas? Pressione 3")

#ou podemos só pesquisar normalmente, e não por tags'''
    
#aqui temos um loop while para verificar sempre que o usuario quiser sem encerrar o programa
while True:
#primeiro checar por qualquer elemento da palavra
    string_pesquisada = input("Insira o nome do lugar que deseja pesquisar: ")
    print("## Resultado ##\n")
    qtd_resultados = 0
    lista_baixar = []
    
    #aqui vamos percorrer todos os elementos do dicionario geral
    for contador in range(len(dicionario_geral)):
        try: #o programa vai tentar achar a string que procuramos no nome que está salvo
            #aqui ele vai comparar, ambos em minusculo, pois se Escola != escolas
            if(string_pesquisada.lower() in dicionario_geral[contador]["tag"]["name"].lower()): # // detalhe caso queira que seja por tag, mudar aqui, posteriormente
                print("#########\n") #só pra ser legivel embaixo
                
                #aqui é bem imporntatnte, estamos pegando as ou elementos tags do dicionario, já achado
                # e separando por nome, id, telefone, etc...
                #tem que ser dentro do try pois individualmente o banco de dados do openmap tem alguns elemtnos que tem valores
                #que estão inválidos ou faltando informação, exemplo aqui é o numero de telefone onde tem varios invalidos, se for
                #sem o try ele não vai resgatar esses lugares com valores invalidos, ficando 52 escolas ao inves de 57, por ex
                
                try: 
                    id_ = dicionario_geral[contador]["id"]
                except:
                    id_ = "invalido"
                try:
                    nome = dicionario_geral[contador]["tag"]["name"]
                except:
                    nome = "invalido"
                try:
                    rua = dicionario_geral[contador]["tag"]["addr:street"]
                except:
                    rua = "invalido"
                try:
                    cep = dicionario_geral[contador]["tag"]["addr:postcode"]
                except:
                    cep = "invalido"
                try:
                    numero = dicionario_geral[contador]["tag"]["addr:housenumber"] #varios invalidos
                except:
                    numero = "invalido"
                try:
                    setor = dicionario_geral[contador]["tag"]["addr:suburb"] #alguns invaldios
                except:
                    setor = "invalido"
                try:
                    cel = dicionario_geral[contador]["tag"]["phone"]
                except:
                    cel = "invalido"

                #a lista que o usuario vai baixar no final
                lista_baixar.append({
                    'id': id_,
                    'nome': nome,
                    'rua': rua,
                    'cep': cep,
                    'numero': numero,
                    'setor': setor,
                    'cel': cel
                    })
                
                #print exibindo no console
                print(f'Resultado {qtd_resultados+1} - {nome}')
                print(f'Endereço: {rua}, numero: {numero}, {cep}, {setor}')
                print(f'Numero: {cel}')
                
                qtd_resultados+=1
                
                print()
            else: #se não achar não faz nada
                pass
        except: #se não achar não faz nada novamente
            pass
    
    baixar = input('Deseja baixar como arquivos de texto?\n1 - SIM\n2 - NÃO\n')
    
    if(baixar == "2"):
        pass
    elif(baixar == "1"): #aqui ele gera um arquivo de texto com a pesquisa do usuario
        with open('pesquisa.txt', 'w', encoding='utf-8') as arquivo:
            contando = 0
            for elemento in lista_baixar:
                arquivo.write(f'{contando} :')
                arquivo.write(str(elemento))
                arquivo.write('\n\n')
                contando+=1
    else:
        print("CÓDIGO INVÁLIDO, O PROGRAMA IRÁ SE ENCERRAR")
        break
    

    
    continuar = input("\nDeseja continuar pesquisando? \n1 - SIM\n2 - NÃO\n")
    
    if(continuar == "2"):
        print("Obrigado por sua pesquisa, volte sempre!")
        break
    elif(continuar == "1"):
        pass
    else:
        print("CÓDIGO INVÁLIDO, O PROGRAMA IRÁ SE ENCERRAR")
        break

### Doc de Listas: https://pense-python.caravela.club/10-listas/00-listas.html

#aqui é um arquivo geral contendo hospitais, escolas e clinicas
with open('dicionario_escolashospitais.txt', 'w', encoding='utf-8') as f:
     for contador in range(len(dicionario_geral)):
         #print(str(dicionario_geral[contador]))
         f.write(f'{contador} :')
         f.write(str(dicionario_geral[contador]))
         f.write('\n\n')

#aqui é só um arquivo com escolas, caso queira só de clinica ou hospital, mudar os nomes
'''with open('dicionario_escolas.txt', 'w', encoding='utf-8') as f:
     for contador in range(len(dicionario_escolas)):
         #print(str(dicionario_geral[contador]))
         f.write(f'{contador} :')
         f.write(str(dicionario_escolas[contador]))
         f.write('\n\n')'''

#aqui é a lista com TODOS os objetos do mapa
with open('listas_objetos.txt', 'w', encoding='utf-8') as f:
     for element in list_dict_data:
         f.write(str(element))
         f.write('\n\n')

