import matplotlib.pyplot as plt
import pandas as pd 
import numpy as np 

try:
    print('Obtendo dados...')
    ENDERECO_DADOS = "https://www.ispdados.rj.gov.br/Arquivos/BaseDPEvolucaoMensalCisp.csv"
    df_ocorrencia = pd.read_csv(ENDERECO_DADOS, sep=';', encoding='iso-8859-1')
    # print(df_ocorrencia.head(2))

    df_estelionato = df_ocorrencia.groupby('munic').sum(['estelionato']).reset_index()
    # print(df_estelionato[['munic', 'estelionato']])

except Exception as e:
    print(f"Erro: {e}")
    exit()

try:
    print('Obtendo iformações sobre padrões de estelionatos...')
    array_estelionato = np.array(df_estelionato['estelionato'])
    media_estelionato = np.mean(array_estelionato)
    mediana_estelionato = np.median(array_estelionato)
    distancia = abs((media_estelionato - mediana_estelionato) / mediana_estelionato)

    print(array_estelionato)
    print(80*"=")
    print("MEDIDAS DE TENDÊNCIA CENTRAL\n")
    print(f'Média de estelionatos {media_estelionato:.2f}')
    print(f'Mediana de estelionatos {mediana_estelionato:.2f}')
    print(f'A distância entre média e mediana {distancia:.2f}')
    print(80*"=")
    
    q1 = np.quantile(array_estelionato, 0.25, method='weibull')
    q2 = np.quantile(array_estelionato, 0.50, method='weibull')
    q3 = np.quantile(array_estelionato, 0.75, method='weibull')

    df_estelionato_menores = df_estelionato[df_estelionato['estelionato'] < q1]
    df_estelionato_maiores = df_estelionato[df_estelionato['estelionato'] > q3]

    print("\nMEDIDAS DE ESTELIONATOS POR CIDADE:")
    print(30*"=", "Cidades com menores índices de roubo: ", 30*"=")
    print(f"\n{df_estelionato_menores[['munic', 'estelionato']].sort_values('estelionato', ascending=True)}")
    print("\n", 30*"=", "Cidades com maiores índices de roubo: ", 30*"=")
    print(f"\n{df_estelionato_maiores[['munic', 'estelionato']].sort_values('estelionato', ascending=False)}")
    print(80*"=")

    iqr = q3-q1

    limite_superior = q3 + (1.5 * iqr)
    limite_inferior = q1 - (1.5 * iqr)
    maximo = np.max(array_estelionato)
    minimo = np.min(array_estelionato)
    amplitude_total = maximo - minimo

    variancia = np.var(array_estelionato)
    distancia_var_media = variancia / (media_estelionato ** 2)

    # O quanto os dados podem estar se distanciando da média 
    # É a raíz quadrada da variância
    desvio_padrao = np.std(array_estelionato)

    # Coeficiente de variação é a magnitude do desvio padrão
    coef_variacao = desvio_padrao / media_estelionato

    print('\nMEDIDAS DE DISPERSÃO:')
    print(f"Variancia: {variancia:.2f}")
    print(f"Distância média da variancia: {distancia_var_media:.2f}")
    print(f"Desvio padrão: {desvio_padrao:.2f}")
    print(f"Coeficiente de variação: {coef_variacao:.2f}")
    print(80*"=", "\n")

    df_estelionato_outliers_superiores = df_estelionato[df_estelionato['estelionato'] > limite_superior]
    df_estelionato_outliers_inferiores = df_estelionato[df_estelionato['estelionato'] < limite_inferior]

    print('Outliers inferiores:')
    if len(df_estelionato_outliers_inferiores) == 0:
        print('Não há outliers inferiores')
    else:
        print(f"\n{df_estelionato_outliers_inferiores.sort_values('estelionato', ascending=True)}")
        print(80*'=')

    print('\nOutliers superiores')
    if len(df_estelionato_outliers_superiores) == 0:
        print('Não há outliers superiores:')
    else:
        print(f"\n{df_estelionato_outliers_superiores.sort_values('estelionato', ascending=False)}")
        print(80*'=')

except Exception as e:
    print(f"Erro: {e}")
    exit()

# PLOTANDO GRÁFICO
# Matplotlib
try:
    # import matplotlib.pyplot as plt
    # fig, ax = plt.subplots(figsize=(10, 6))
    # ax.boxplot(array_roubo_veiculo, vert=False, showmeans=True)
    
    plt.subplots(2, 2, figsize=(16, 10))
    plt.suptitle('Análise de estelionatos no estado RJ') 

    # POSIÇÃO 01
    # BOXPLOT
    plt.subplot(2, 2, 1)  
    plt.boxplot(array_estelionato, vert=False, showmeans=True)
    plt.title("Boxplot dos Dados")

    # POSIÇÃO 02
    # MEDIDAS
    # Exibição de informações estatísticas
    plt.subplot(2, 2, 2)
    plt.title('Medidas Estatísticas')
    plt.text(0.1, 0.9, f'Limite inferior: {limite_inferior}', fontsize=10)
    plt.text(0.1, 0.8, f'Menor valor: {minimo}', fontsize=10) 
    plt.text(0.1, 0.7, f'Q1: {q1}', fontsize=10)
    plt.text(0.1, 0.6, f'Mediana: {mediana_estelionato}', fontsize=10)
    plt.text(0.1, 0.5, f'Q3: {q3}', fontsize=10)
    plt.text(0.1, 0.4, f'Média: {mediana_estelionato:.3f}', fontsize=10)
    plt.text(0.1, 0.3, f'Maior valor: {maximo}', fontsize=10)
    plt.text(0.1, 0.2, f'Limite superior: {limite_superior}', fontsize=10)

    plt.text(0.5, 0.9, f'Distância Média e Mediana: {distancia:.4f}', fontsize=10)
    plt.text(0.5, 0.8, f'IQR: {iqr}', fontsize=10)
    plt.text(0.5, 0.7, f'Amplitude Total: {amplitude_total}', fontsize=10)
    
    # POSIÇÃO 03
    # OUTLIERS INFERIORES
    plt.subplot(2, 2, 3)
    plt.title('Outliers Inferiores')
    # Se o DataFrame do outliers não estiver vazio
    if not df_estelionato_outliers_inferiores.empty:
        dados_inferiores = df_estelionato_outliers_inferiores.sort_values(by='estelionato', ascending=True) #crescente
        # Gráfico de Barras
        plt.barh(dados_inferiores['munic'], dados_inferiores['estelionato'])
    else:
        # Se não houver outliers
        plt.text(0.5, 0.5, 'Sem Outliers Inferiores', ha='center', va='center', fontsize=12)
        plt.title('Outilers Inferiores')
        plt.xticks([])
        plt.yticks([])
    
    # POSIÇÃO 04
    # OUTLIERS SUPERIORES
    plt.subplot(2, 2, 4)
    plt.title('Outliers Superiores')
    if not df_estelionato_outliers_superiores.empty:
        dados_superiores = df_estelionato_outliers_superiores.sort_values(by='estelionato', ascending=True)

        # Cria o gráfico e guarda as barras
        barras = plt.barh(dados_superiores['munic'], dados_superiores['estelionato'], color='black')
        # Adiciona rótulos nas barras
        plt.bar_label(barras, fmt='%.0f', label_type='edge', fontsize=8, padding=2)

        # Diminui o tamanho da fonte dos eixos
        plt.xticks(fontsize=8)
        plt.yticks(fontsize=8)

        plt.title('Outliers Superiores')
        plt.xlabel('Total de Estelionatos')    
    else:
        # Se não houver outliers superiores, exibe uma mensagem no lugar.
        plt.text(0.5, 0.5, 'Sem outliers superiores', ha='center', va='center', fontsize=12)
        plt.title('Outliers Superiores')
        plt.xticks([])
        plt.yticks([])

    # Ajusta os espaços do layout para que os gráficos não fiquem espremidos
    plt.tight_layout()
    # Mostra a figura com os dois gráficos
    plt.show()
    
except Exception as e:
    print(f'Erro ao plotar {e}')
    exit()
