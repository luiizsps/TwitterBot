import os
import pickle
import numpy as np
import pandas as pd

import sys
sys.path.append('../extracao/')
print(sys.path)
import listaProdutos

"Este arquivo gera rankings de score e os exibe em página html"

"______________________________________________________"

def gera_ranking(indice):
    estrutura_principal = '<!DOCTYPE html><html lang="pt-br"><head><meta charset="utf-8"/><meta content="width=device-width, initial-scale=1.0" name="viewport"/><title>Resultados</title><link href="style.css" rel="stylesheet"/></head><body><div class="container"><div class="barebone"><h2 class="title"></h2><div class="grid-container" id="grid-container"><!-- header --><div class="grid-row"><div class="grid-header">Junho</div><div class="grid-header">Julho</div><div class="grid-header">Agosto</div><div class="grid-header">Setembro</div><div class="grid-header">Outubro</div><div class="grid-empty"></div></div></div></div></body></html>'
    linha_item_top_um = '<div class="grid-row border-bottom"><div class="grid-empty">Top 1</div></div>'
    linha_item_top_cinco = '<div class="grid-row border-bottom"><div class="grid-empty">Top 5</div></div>'
    fim_grid_linha = '</div></div></body>'
    fim_linha_item = '<div class="grid-empty">'
    grid_name = '</p><p class="grid-score">'
    grid_score = '</p></a></div>'
    item_classe = '"><a class="grid-content"'

    caminho_dados = "../dados/"
    nome = "kfold_probas_0" + str(indice) + ".pkl"
    with open(caminho_dados+'kfold/'+nome, "rb") as arquivo:
        scores = pickle.load(arquivo)
    
    arquivo_nomes = "kfold_nomes_0" + str(indice) + ".pkl"
    print(arquivo_nomes)
    
    # carregando nome dos produtos
    with open(caminho_dados+'kfold/'+arquivo_nomes, "rb") as arquivo:
        lista_nomes = pickle.load(arquivo)
    
    # criando lista de barebones
    barebones = []
    for nome_comp in lista_nomes:
        partes_nome = nome_comp.split("__")
        partes_nome = partes_nome[4].split(".")
        barebone = partes_nome[0]
        barebones.append(barebone)
    
    barebone_referencia = barebones[0]
    num_linhas = scores.shape[0]
    
    # print(scores.shape)
    num_colunas = scores.shape[1]
    scores_resized = np.resize(scores, (num_linhas, 6))
    scores_str = scores.astype(str)
    matriz_scores = scores_resized.astype(str)
    
    # adicionando barebone à matriz de scores
    for i in range(num_linhas):
        matriz_scores[i] = np.insert(scores_str[i], 0, barebones[i])
    
    num_meses = matriz_scores.shape[1] - 1
    
    # separa a matriz original em novas matrizes para cada mês
    matriz_barebones_ordenados = []
    matriz_scores_ordenados = []
    for mes in range(num_meses):
        # cria nova matriz para o mês atual
        matriz_mes = matriz_scores[:, [0, mes + 1]].copy()
        scores_mes = matriz_mes[:, 1].astype(float)
        
        lista_nome_score = list(zip(barebones, scores_mes))
    
        lista_ordenada = sorted(lista_nome_score, key=lambda x: x[1], reverse=True)
        barebones_ordenados, scores_ordenados = zip(*lista_ordenada)
        barebones_ordenados = list(barebones_ordenados)
        scores_ordenados = list(scores_ordenados)
    
        matriz_barebones_ordenados.append(barebones_ordenados)
        matriz_scores_ordenados.append(scores_ordenados)
    
    print(matriz_barebones_ordenados, matriz_scores_ordenados)
    
    for i in range(num_linhas):
        linha_item = '<div class="grid-row"><div class="grid-empty"></div></div>'
        # cria lista de barebones e scores ordenados por linha do grid
        barebones_linha = [linha[i] for linha in matriz_barebones_ordenados]
        scores_linha = [linha[i] for linha in matriz_scores_ordenados]

        for score, barebone in zip(scores_linha, barebones_linha):
            estrutura_grid_item = '<div class="grid-item"><a class="grid-content" href=""><p class="grid-name"></p><p class="grid-score"></p></a></div>'
            # insere nome no item
            posicao_nome = estrutura_grid_item.find(grid_name)
            estrutura_grid_item = estrutura_grid_item[:posicao_nome] + barebone + estrutura_grid_item[posicao_nome:]

            # insere score no item
            posicao_score = estrutura_grid_item.find(grid_score)
            estrutura_grid_item = estrutura_grid_item[:posicao_score] + str(round(score, 2)) + estrutura_grid_item[posicao_score:]

            # insere item com nome e score na linha
            posicao_item = linha_item.find(fim_linha_item)
            linha_item = linha_item[:posicao_item] + estrutura_grid_item + linha_item[posicao_item:]

            if(barebone == barebone_referencia):
                posicao_classe = linha_item.find(item_classe)
                linha_item = linha_item[:posicao_classe] + ' referencia' + linha_item[posicao_classe:]
            print(linha_item)
        # insere linha no grid
        posicao_grid_linha = estrutura_principal.find(fim_grid_linha)
        estrutura_principal = estrutura_principal[:posicao_grid_linha] + linha_item + estrutura_principal[posicao_grid_linha:]

        #if(i==0):
            
        #for barebone, score in zip(barebones_linha, scores_linha):





    '''
    caminho_treinamento = "../treinamento/"
    nome = "base_ranking.html"
    with open(caminho_treinamento+nome, 'r') as arquivo:
        conteudo_html = arquivo.read()
    
    caminho_rankings = "../dados/ranking/"
    num_linhas_base = 6
    if(num_linhas > num_linhas_base):
        for i in range(num_linhas - num_linhas_base):
            insere_linha_grid()
    else:
        with open(caminho_rankings+"temp.html", "w") as arquivo:
            arquivo.write(conteudo_html)

    with open(caminho_rankings+"temp.html", "r") as arquivo:
        novo_conteudo_html = arquivo.read()
    
    soup_principal = BeautifulSoup(novo_conteudo_html, 'html.parser')
    soup_barebone = soup_principal.select_one('.barebone')
    grid_contents = soup_barebone.select('.grid-content')
    grid_items = soup_barebone.select('.grid-item')
    grid_names = soup_barebone.select('.grid-name')
    grid_scores = soup_barebone.select('.grid-score')
    
    linha=0
    coluna=0
    barebones_mes = [column[linha] for column in matriz_barebones_ordenados]
    for grid_name, grid_score, grid_item, grid_content in zip(grid_names, grid_scores, grid_items, grid_contents):
        barebone = barebones_mes[coluna]
        grid_name.string = str(barebone)
        grid_score.string = str(round(matriz_scores_ordenados[coluna][linha], 4))
        
        # adciona link de exemplo provisório como nome do barebone
        grid_content['href'] = f'../casos/{barebone}/index.html'
    
        if 'referencia' in grid_item.get('class', []):
            grid_item['class'].remove('referencia')
    
        if(barebone == barebone_referencia):
            grid_item["class"].append("referencia")  
        
        coluna+=1
    
        if(coluna >= num_colunas):
            coluna = 0
            linha += 1
    
            if(linha >= num_linhas):
                break
    
            barebones_mes = [column[linha] for column in matriz_barebones_ordenados]
    
    barebone_grid = soup_barebone.select('.grid-item')
    if 'hidden' in barebone_grid[0].get('class', []):
        barebone_grid[0]['class'].remove('hidden')
    
    titulo = soup_barebone.select('.title')
    titulo[0].string = "# "+str(barebone_referencia)
    
    print(matriz_barebones_ordenados)
    '''
    
    # encontra os scores top 1 e top 5
    score_top1 = []
    score_top5 = []
    for linha in matriz_barebones_ordenados:
        posicao = linha.index(barebone_referencia)
    
        if(posicao == 0):
            score_top1.append(1)
            score_top5.append(1)
        elif(posicao < 5):
            score_top1.append(0)
            score_top5.append(1)
        else:
            score_top1.append(0)
            score_top5.append(0)
    
    # calcula as médias dos top 1 e top 5
    media_top1 = sum(score_top1)/len(score_top1)
    media_top5 = sum(score_top5)/len(score_top5)
    score_top1.append(media_top1)
    score_top5.append(media_top5)

    '''
    print(score_top1, score_top5)
    data = {
        '': ['Media'],
        'Score TOP 1': score_top1[5],
        'Score TOP 5': score_top5[5]
    }
    
    df = pd.DataFrame(data)
    tabela_html = df.to_html(index=False)
    
    table = soup_barebone.select_one('.dataframe')
    df_soup = BeautifulSoup(tabela_html, 'html.parser')
    table.replace_with(df_soup.table)
    '''

    div_pai = soup_principal.select('.container')[0]
    div_pai.append(soup_barebone)
    
    html_modificado = soup_principal.prettify()
    
    nome = f"ranking_{barebone_referencia}.html"
    with open(caminho_rankings+nome, 'w') as arquivo:
        arquivo.write(html_modificado)
    
    # deleta arquivo html temporário
    arquivo_a_deletar = caminho_rankings+"temp.html"
    if os.path.exists(arquivo_a_deletar):
        os.remove(arquivo_a_deletar)

def gera_menu():
    caminho_arquivo_menu = "../treinamento/"
    caminho_arquivos_rankings = "../dados/ranking/"
    caminho_salvar_menu = "ranking/"
    nome_menu = "menu_ranking.html"

    with open(caminho_arquivo_menu+nome_menu, "r") as arquivo:
        conteudo_menu = arquivo.read()

    # Lista para armazenar os nomes dos arquivos encontrados
    lista_nomes_arquivos = []

    for nome_arquivo in os.listdir(caminho_arquivos_rankings):
        caminho_completo = os.path.join(caminho_arquivos_rankings, nome_arquivo)
        if os.path.isfile(caminho_completo):
            nome_arquivo_simples = os.path.basename(nome_arquivo)
            lista_nomes_arquivos.append(nome_arquivo_simples)

    print(lista_nomes_arquivos)
    """ soup_menu = BeautifulSoup(conteudo_menu, 'html.parser')
    link_places = soup_menu.select(".link")
    
    for place in link_places:
        place["href"] = link_ """
    
def insere_linha_grid():
    linha_html = '<div class="grid-row"><div class="grid-item 6-1"><a class="grid-content" href="#"><p class="grid-name">POS_RIB360EE</p><p class="grid-score">0</p></a></div><div class="grid-item 6-2 referencia"><a class="grid-content" href="#"><p class="grid-name">POS_RIB360EE</p><p class="grid-score">0</p></a></div><div class="grid-item 6-3"><a class="grid-content" href="#"><p class="grid-name">POS_RIB360EE</p><p class="grid-score">0</p></a></div><div class="grid-item 6-4"><a class="grid-content" href="#"><p class="grid-name">POS_RIB360EE</p><p class="grid-score">0</p></a></div><div class="grid-item 6-5"><a class="grid-content" href="#"><p class="grid-name">POS_RIB360EE</p><p class="grid-score">0</p></a></div><div class="grid-empty 6-6"></div></div>'

    caminho_treinamento = "../treinamento/"
    nome = "base_ranking.html"
    with open(caminho_treinamento+nome, 'r') as arquivo:
        conteudo_html = arquivo.read()

    soup = BeautifulSoup(conteudo_html, "html.parser")
    soup_linha = BeautifulSoup(linha_html, "html.parser")

    estrutura_principal = soup.find('div', {'id': 'grid-container'})
    
    estrutura_principal.append(soup_linha.div)

    html_final = str(soup)

    caminho_ranking = "../dados/ranking/"
    with open(caminho_ranking+"temp.html", "w") as arquivo:
        arquivo.write(html_final)

if __name__ == "__main__":

    for i in range(7):
        gera_ranking(i)

