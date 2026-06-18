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
# %%
#todo PARA CALCULAR TX BRUTA DE MORTALIDADE E TABUA DE VIDA DA SERIE TEMPORAL
#TODO USAR O ARQ MORT_ANO_TAB_VIDA

# %% para taxa de natalidade usar nasc_vivo e total_df
nasc_viv

# %%
nasc_viv

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
total_df.merge(
    nasc_viv_totais,
    how='left',
    left_on='anos',
    right_on='anos',
)
# %%
nasc_viv_totais.info()
# %%
nasc_viv_totais
# %%
nasc_viv.info()
# %%
