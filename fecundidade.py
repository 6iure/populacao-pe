# %% 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import matplotlib.ticker as mticker
from matplotlib.lines import Line2D
# %%
df_all = pd.read_excel('data/data_geral/dinamica_populacional_pe.xlsx')
df_all.head()
# %%
pe = df_all[df_all['LOCAL'] == 'Pernambuco']
pe.head()

# %%
pe.rename(columns={'GRUPO ETÁRIO': 'grupo_etario', 'SEXO':'sexo', 'LOCAL':'local'}, inplace=True)
pe

# %%
pe = pe[pe['sexo'] != 'Ambos']
pe
# %%
# CALCULO DA TAXA DE CRESCIMENTO POPULACIONAL
cresc_pop = pe.groupby(['sexo', 'local'], as_index=False).sum(numeric_only=True)
cresc_pop

# %%
total_linha = cresc_pop.sum(numeric_only=True)
total_linha

# %%
total_df = pd.DataFrame([total_linha])
total_df

# %%
total_df['sexo'] = 'Ambos'
total_df['local'] = cresc_pop['local'].iloc[0]
total_df
# %%
cresc_pop_final = pd.concat([cresc_pop, total_df], ignore_index=True)
cresc_pop_final
# %%

#todo deixar isso mais bonitinho e adicionar no grafico

((cresc_pop_final[2024] - cresc_pop_final[2000]) / cresc_pop_final[2000]) * 100

# %%
total_df.drop(columns={'sexo', 'local'},inplace=True)

# %%
total_df = total_df.melt()
total_df

# %%
total_df.rename(columns={'variable': 'anos', 'value':'populacao'}, inplace=True)

# %%
total_df['anos'] = total_df['anos'].astype(int)  
# %% 
#todo melhorar GRAFICO PARA mostrar crescimento por sexo e colocar legenda com as taxas. 
#TODO OU FAZER COM UM HISTOGRAMA
fig, ax = plt.subplots(figsize=(13, 7))
fig.patch.set_facecolor('#F7F9FC')
ax.set_facecolor('#F7F9FC')

ax.fill_between(total_df['anos'], total_df['populacao'], alpha=0.25, color='#2166AC')
ax.plot(total_df['anos'], total_df['populacao'], color='#1a4f7a', linewidth=2.8, zorder=3)

for spine in ['top', 'right', 'left']:
    ax.spines[spine].set_visible(False)
ax.spines['bottom'].set_color('#cccccc')
ax.tick_params(length=0, labelcolor='#555555', labelsize=10)
ax.grid(axis='y', color='#dddddd', linewidth=0.8, linestyle='--', zorder=0)
ax.set_axisbelow(True)

ax.yaxis.set_major_formatter(
    mticker.FuncFormatter(lambda x, pos: f'{x/1_000_000:.1f} mi')
)
ax.set_xlim(1999.5, 2024.8)
ax.set_ylim(7_800_000, 10_100_000)
ax.set_xticks([2000, 2005, 2010, 2015, 2020, 2024])

plt.title('Crescimento Populacional - PE: 2000 - 2024', fontsize=14, pad=15, fontweight='bold', loc='left')
plt.xlabel('Ano', fontsize=10, fontweight='bold', color='#555555')
plt.ylabel('População (Milhões)', fontsize=10, fontweight='bold', color='#555555')
plt.tight_layout()
plt.show()

# %%
#CALCULO DA RAZAO DE DEPENDENCIA AO DECORRER DOS ANOS

# populacao dependente: soma dos indices 0, 1, 2, 13, 14, 15, 16, 17, 18.
# populacao com idade entre 15 ate 64 anos: soma dos indices 3 a 12.

#removendo espaco ' ' que vinha antes dos grupos etarios, pois estavam me causando problemas
print(pe['grupo_etario'].unique())
# %%
pe['grupo_etario'] = pe['grupo_etario'].str.strip()
print(pe['grupo_etario'].unique())

# %%
lista_jovens = ['00-04','05-09','10-14']
lista_idosos = ['65-69','70-74','75-79','80-84','85-89','90+']

condlist = [pe['grupo_etario'].isin(lista_idosos), pe['grupo_etario'].isin(lista_jovens)]
choicelist = ['dep_idoso', 'dep_jovem']
# %%
pe['dependencia'] = np.select(condlist, choicelist, 'independente')
pe

# %%
dependencia = pe.groupby(['dependencia']).sum(numeric_only=True)
dependencia
# %%
dependencia = dependencia.T
dependencia

# %%
dependencia.reset_index(inplace=True)
dependencia
# %%

dependencia.rename(columns={'index':'ano'}, inplace=True)
dependencia
# %% #CALCULO DA RAZAO DE DEPENDENCIA AO DECORRER DOS ANOS
dependencia['rdi'] = (dependencia['dep_idoso'] / dependencia['independente']) * 100
dependencia
# %%
dependencia['rdj'] = (dependencia['dep_jovem'] / dependencia['independente']) * 100
dependencia
# %%
dependencia['rdt'] = ((dependencia['dep_idoso'] + dependencia['dep_jovem']) / dependencia['independente']) * 100
dependencia

# %% 
#TODO GRAFICO DE LINHAS PARA MOSTRAR A RAZAO DE DEPENDENCIA
plt.figure(figsize=(12,6))

plt.plot(dependencia['ano'], dependencia['rdj'], color="#F60909", linestyle='-.', linewidth=2, label='Jovens (0-14)')
plt.plot(dependencia['ano'], dependencia['rdi'], color="#001AFF", linestyle='--', linewidth=2, label='Idosos (65+)')

plt.plot(dependencia['ano'], dependencia['rdt'], color="#04FD00", linestyle='-', linewidth=3, label='Razão de Dependência Total')

ax = plt.gca()
ax.spines['top'].set_visible(False)    # Remove a linha de cima
ax.spines['right'].set_visible(False)  # Remove a linha da direita
ax.spines['left'].set_color('#D1D5DB')  # Deixa o eixo Y sutil
ax.spines['bottom'].set_color('#D1D5DB')# Deixa o eixo X sutil

# 5. Títulos e Rótulos alinhados à esquerda (Padrão de leitura em Z)
plt.title('Evolução da Razão de Dependência em Pernambuco', fontsize=16, fontweight='bold', color='#1F2937', loc='left', pad=15)
# Subtítulo para dar contexto ao leitor antes de olhar o dado

plt.xlabel('Ano', fontsize=11, color='#4B5563', labelpad=10)
plt.ylabel('Dependentes para cada 100 ativos', fontsize=11, color='#4B5563', labelpad=10)

# 6. Configurar os anos no eixo X para ficarem limpos (ex: de 2 em 2 anos ou todos na horizontal)
plt.xticks(dependencia['ano'], rotation=0) 

# 7. Legenda posicionada de forma estratégica
plt.legend(frameon=False, loc='upper right', fontsize=10)

# Ajustar o espaçamento para não cortar textos
plt.tight_layout()

# Exibir o gráfico pronto para apresentação
plt.show()

# %% calculando o indice de envelhecimento da populacao

cond = pe['grupo_etario'].isin(lista_jovens), pe['grupo_etario'].isin(['60-64','65-69','70-74','75-79','80-84','85-89','90+'])
chce = ['jovem', 'idoso']
# %%
pe['fase_vida'] = np.select(cond, chce, 'adulto')
pe
# %%
ind_env = pe.groupby(['fase_vida', 'sexo']).sum(numeric_only=True)
ind_env

# %%
ind_env.reset_index(inplace=True)
ind_env

# %%
colunas_anos = ind_env.select_dtypes('number').columns.tolist()

# %%
tt = ind_env.melt(
    id_vars=['fase_vida', 'sexo'],
    value_vars=colunas_anos,
    var_name='ano',
    value_name='populacao'
)

#%%
tt.info()
# %%
tt['ano'] = tt['ano'].astype(int)
tt['populacao'] = tt['populacao'].astype(float)

# %%
tt.sort_values(['fase_vida', 'sexo', 'ano']).reset_index(drop=True)
tt

# %%
#TODO Mlehorar grafico de indice de envelhecimento da populacao
CORES   = {'jovem': '#2166AC', 'adulto': '#1A9641', 'idoso': '#D73027'}
ESTILOS = {'Homens': '-',  'Mulheres': '--'}

fig, ax = plt.subplots(figsize=(13, 7))
fig.patch.set_facecolor('#F7F9FC')
ax.set_facecolor('#F7F9FC')

for (fase, sexo), grupo in tt.groupby(['fase_vida', 'sexo']):
    x = grupo['ano'].values
    y = grupo['populacao'].values

    ax.plot(x, y,
            color=CORES[fase], linestyle=ESTILOS[sexo], linewidth=2.2)

    # Anotação no valor final (2024)
    pop_final = grupo.loc[grupo['ano'] == 2024, 'populacao'].values[0]
    ax.annotate(f'{pop_final/1_000_000:.2f} mi',
                xy=(2024, pop_final), xytext=(2024.3, pop_final),
                fontsize=7.5, color=CORES[fase], fontweight='bold', va='center')

# ── Limpeza visual ────────────────────────────────────────────────────
for spine in ['top', 'right']:
    ax.spines[spine].set_visible(False)
ax.spines['left'].set_color('#cccccc')
ax.spines['bottom'].set_color('#cccccc')
ax.tick_params(length=0, labelcolor='#555555', labelsize=10)
ax.grid(axis='y', color='#e5e5e5', linewidth=0.8, linestyle='--', zorder=0)
ax.set_axisbelow(True)

# ── Eixos ─────────────────────────────────────────────────────────────
ax.yaxis.set_major_formatter(
    mticker.FuncFormatter(lambda x, pos: f'{x/1_000_000:.1f} mi')
)
ax.set_xlim(1999, 2025)
ax.set_xticks([2000, 2005, 2010, 2015, 2020, 2024])
ax.set_xlabel('Ano', fontsize=10, color='#555555', labelpad=8)

# ── Legenda dupla (cor = fase | estilo = sexo) ────────────────────────
legend_fase = [
    Line2D([0],[0], color=CORES['adulto'], linewidth=2, label='Adulto (15-59 anos)'),
    Line2D([0],[0], color=CORES['jovem'],  linewidth=2, label='Jovem (0-14 anos)'),
    Line2D([0],[0], color=CORES['idoso'],  linewidth=2, label='Idoso (60+ anos)'),
]
legend_sexo = [
    Line2D([0],[0], color='#888', lw=2, ls='-',   ms=5, label='Homens'),
    Line2D([0],[0], color='#888', lw=2, ls='--', ms=5, label='Mulheres'),
]
leg1 = ax.legend(handles=legend_fase, loc='upper left',
                 frameon=False, fontsize=9.5,
                 title='Fase da vida', title_fontsize=9)
leg2 = ax.legend(handles=legend_sexo, loc='center left',
                 frameon=False, fontsize=9.5,
                 title='Sexo', title_fontsize=9, bbox_to_anchor=(0, 0.42))
ax.add_artist(leg1)

# ── Títulos e fonte ───────────────────────────────────────────────────
ax.set_title('Pernambuco: Índice de Envelhecimento da População',
             fontsize=14, fontweight='bold', color='black', loc='left', pad=18)
fig.text(0.01, -0.02,
         'Fonte: IBGE — Projeções das Populações, Revisão 2024.',
         fontsize=8, color='#999999')

plt.tight_layout()
plt.show()

# %%
pe

# %%
#ajuste dos dados para piramidade populacional
pir_pop = pe.groupby(['sexo', 'grupo_etario']).sum()
pir_pop 

# %%
pir_pop.reset_index(inplace=True)
pir_pop
# %%
pir_pop.drop(columns=[2001,2002,2003,2004,2005,2006,2007, 2008,2009,2010,2011,2012,2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023], inplace=True)
pir_pop
# %%
pir_pop[pir_pop['sexo'] == 'Homens']

# %%
colunas_anos = pir_pop.select_dtypes('number').columns.tolist()
# %%
df_pivo = pir_pop.pivot(
    index=['grupo_etario', 'local', 'fase_vida'],
    columns='sexo',
    values=colunas_anos
)

df_pivo.columns = [f"{sexo.lower()}_{ano}" for ano, sexo in df_pivo.columns]

teste = df_pivo.reset_index(inplace=True)
df_pivo
# %%

# todo adicionar % da populacao que cada barra representa

fig, ax = plt.subplots(figsize=(12, 6))

ax.barh(df_pivo['grupo_etario'], -df_pivo['homens_2024'], color='blue', label='Homens')
ax.barh(df_pivo['grupo_etario'], df_pivo['mulheres_2024'], color='magenta', label='Mulheres')

plt.grid(axis='both', linestyle='--', alpha=0.6)
plt.title('Pirâmide Etária - Pernambuco 2024 ', fontsize=14, pad=10, fontweight='bold', loc='left')
plt.xlabel('População', fontsize=12, fontweight='bold')
plt.ylabel('Grupo Etário', fontsize=12, fontweight='bold')
ax.legend()

ticks = ax.get_xticks()
ax.set_xticklabels([int(abs(tick)) for tick in ticks])

sns.despine()
plt.show()
# %%
df_pivo

# %% 
nasc_viv = pd.read_excel('data/data_fec/total_nascviv.xlsx')
nasc_viv

# %% para taxa de natalidade usar nasc_vivo e total_df
nasc_viv.dtypes
# %% transformando todas as colunas para int
nasc_viv[2009] = nasc_viv[2009].apply(pd.to_numeric, errors='coerce')
nasc_viv[2011] = nasc_viv[2011].apply(pd.to_numeric, errors='coerce')
nasc_viv[2013] = nasc_viv[2013].apply(pd.to_numeric, errors='coerce')
nasc_viv[2015] = nasc_viv[2015].apply(pd.to_numeric, errors='coerce')
nasc_viv[2016] = nasc_viv[2016].apply(pd.to_numeric, errors='coerce')
nasc_viv[2017] = nasc_viv[2017].apply(pd.to_numeric, errors='coerce')
nasc_viv[2019] = nasc_viv[2019].apply(pd.to_numeric, errors='coerce')
nasc_viv[2021] = nasc_viv[2021].apply(pd.to_numeric, errors='coerce')
nasc_viv[2023] = nasc_viv[2023].apply(pd.to_numeric, errors='coerce')
nasc_viv

# %%
nasc_viv.dtypes

# %%
total_df
# %%
nasc_viv_totais = nasc_viv.sum(numeric_only=True)
nasc_viv_totais
# %%
nasc_viv_totais = pd.DataFrame(nasc_viv_totais).reset_index(False)
nasc_viv_totais
# %%
nasc_viv_totais.rename(columns={'index':'anos', 0:'populacao_nasc_vivos'}, inplace=True)
nasc_viv_totais
# %%
df_natalidade = total_df.merge(
    nasc_viv_totais,
    how='left',
    left_on='anos',
    right_on='anos',
)
df_natalidade
# %% criando nova coluna que eh a taxa da natalidade de cada ano

df_natalidade['taxa_natalidade'] = (df_natalidade['populacao_nasc_vivos'] / df_natalidade['populacao']) * 1000
df_natalidade
# %%
plt.figure(figsize=(10,5))

plt.plot(df_natalidade['anos'], df_natalidade['taxa_natalidade'], color='#1D4ED8', linewidth=1.5)

ax = plt.gca()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.title('Taxa Bruta de Natalidade em Pernambuco (2000-2024)', fontsize=14, fontweight='bold', loc='left', pad=10)
plt.xlabel('Ano')
plt.ylabel('Nascimentos por 1.000 hab.')

plt.show()
# %%
mort = pd.read_excel('data/data_mort/tabua-vida-form.xlsx')
mort
# %%
mort.dtypes
# %% mudando o tipo de dado de obj para float da populacao de mortos por ano.
colunas_anos = mort.columns.drop('Faixa Etária')
mort[colunas_anos] = mort[colunas_anos].apply(pd.to_numeric, errors='coerce')
mort.dtypes
# %%
soma_mort = mort.sum(numeric_only=True)
soma_mort

# %%
soma_mort = pd.DataFrame(soma_mort).reset_index(False)
soma_mort

# %%
soma_mort.rename(columns={'index' :'anos', 0:'pop_mortos'}, inplace=True)
soma_mort
# %%
tx_mort = total_df.merge(
    soma_mort,
    how='left',
    left_on='anos',
    right_on='anos'
)

tx_mort
# %%
tx_mort['taxa_mort_bruta'] = (tx_mort['pop_mortos'] / tx_mort['populacao']) * 1000
tx_mort
# %%
# Todo pesqquisar o porque desse crescimento da tx de mortalidade no estado. e colocar marcacoes de tempo
plt.figure(figsize=(10,5))

plt.plot(tx_mort['anos'], tx_mort['taxa_mort_bruta'], color="#D8201D", linewidth=1.5)

ax = plt.gca()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.title('Taxa Bruta de Mortalidade em Pernambuco (2000-2024)', fontsize=14, fontweight='bold', loc='left', pad=10)
plt.xlabel('Ano')
plt.ylabel('Mortes por 1.000 hab.')

# %%
causas_mort = pd.read_csv('data/data_mort/sim_cnv_obt10uf012941177_6_239_134.csv', encoding='latin-1', sep=';')

# %%
causas_mort.dtypes
# %% transformando em numerico as colunas que vieram como string
colunas_anos = causas_mort.columns.drop('Capítulo CID-10')
causas_mort[colunas_anos] = causas_mort[colunas_anos].apply(pd.to_numeric, errors='coerce')
causas_mort.dtypes

# %%
causas_mort['Causa'] = causas_mort['Capítulo CID-10'].str.replace(r'^[IXV]+\.\s*', '', regex=True)
# %%
anos = [str(ano) for ano in range(2000, 2025)]
causas_mort[anos] = causas_mort[anos].apply(pd.to_numeric, errors='coerce').fillna(0)
# %% grafico das top 10 causas de morte NO PE 2000-2024
causas_mort['Total_Periodo'] = causas_mort[anos].sum(axis=1)

df_top10 = causas_mort.sort_values('Total_Periodo', ascending=False).head(10)

plt.figure(figsize=(12, 6))
sns.barplot(data=df_top10, x='Total_Periodo', y='Causa', palette='Blues_r')

plt.title('Top 10 Causas de Morte em Pernambuco (2000-2024)', fontsize=14, fontweight='bold')
plt.xlabel('Total de Óbitos Acumulados no Período')
plt.ylabel('')
sns.despine()
plt.tight_layout()
plt.show()
# %%
# Calcula o total de mortes no período inteiro para descobrir o Top 5
causas_mort['Total_Periodo'] = causas_mort[anos].sum(axis=1)

# Isola os nomes das 5 doenças que mais mataram na soma total dos anos
top_5_causas = causas_mort.sort_values('Total_Periodo', ascending=False)['Causa'].head(7).tolist()

# Configuração visual do gráfico
plt.figure(figsize=(14, 7))
sns.set_theme(style="whitegrid") # Coloca linhas de grade horizontais e verticais suaves

# Plota uma linha conectando os pontos para cada uma das 5 doenças
for causa in top_5_causas:
    # Extrai os valores exatos de mortes ano a ano para a doença atual
    dados_causa = causas_mort[causas_mort['Causa'] == causa][anos].values.flatten()
    
    # Plota a linha (marker='o' coloca a bolinha em cima de cada ano)
    plt.plot(anos, dados_causa, label=causa, marker='o', linewidth=2.5)

# Títulos e rótulos
plt.title('Evolução das 7 Principais Causas de Morte em Pernambuco (2000-2024)', fontsize=15, fontweight='bold', pad=15)
plt.xlabel('Ano', fontsize=12)
plt.ylabel('Número de Óbitos', fontsize=12)
plt.xticks(rotation=45) # Inclina os anos em 45 graus para não ficarem amontoados

# Ajusta a legenda para ficar do lado de fora direito do gráfico
plt.legend(title='Causas de Morte', bbox_to_anchor=(0, 1), loc='upper left')

# Remove a borda superior e direita do quadro do gráfico
sns.despine()

# Ajusta o layout para a legenda não ser cortada ao salvar
plt.tight_layout()

# Exibe o gráfico
plt.show()
# %% dados de urbanizacao
urbanizacao = pd.read_excel('data/data_geral/tabela202.xlsx')
urbanizacao
# %%

df = pd.read_excel('data/data_geral/tabela202.xlsx')
df_estado = df.iloc[0:2].copy()
df_estado['municipio'] = 'Pernambuco'

df_long = pd.melt(
    df_estado, 
    id_vars=['municipio', 'situacao'], 
    value_vars=['2000', '2010'], 
    var_name='Ano', 
    value_name='Populacao'
)
df_long['Populacao_Milhoes'] = df_long['Populacao'] / 1_000_000

taxa_urbanizacao = {
    '2000': 76.5,  # 76.5% da população era urbana em 2000
    '2010': 80.2   # 80.2% da população era urbana em 2010
}

plt.figure(figsize=(12, 6))

ax = sns.barplot(
    data=df_long, 
    x='Ano', 
    y='Populacao_Milhoes', 
    hue='situacao', 
    palette=['#1D4ED8', '#9CA3AF']
)

for i, container in enumerate(ax.containers):
    # i == 0 significa que estamos lendo as barras da categoria 'Urbana'
    is_urbana = (i == 0) 
    
    for j, bar in enumerate(container):
        altura = bar.get_height()
        ano = ['2000', '2010'][j] # j=0 é o ano 2000, j=1 é o ano 2010
        
        # Se for urbana, adiciona o valor em milhões E a taxa ao lado/abaixo
        if is_urbana:
            # \n quebra a linha para o texto não ficar largo demais e bater na outra barra
            texto = f'{altura:.2f} M\n({taxa_urbanizacao[ano]}%)'
        else:
            # Se for rural, mantém apenas o valor em milhões
            texto = f'{altura:.2f} M'
            
        ax.annotate(texto,
                    (bar.get_x() + bar.get_width() / 2., altura),
                    ha='center', va='bottom',
                    fontsize=10, fontweight='bold', color='#1F2937',
                    xytext=(0, 3), textcoords='offset points')

plt.title('Crescimento da Pop. Urbana e Retração Rural em PE', fontsize=14, fontweight='bold', loc='left', pad=15)

plt.xlabel('Ano Censitário', fontsize=11, color='#4B5563')
plt.ylabel('População (em Milhões)', fontsize=11, color='#4B5563')
sns.despine()
plt.tight_layout()

plt.show()
# %%
