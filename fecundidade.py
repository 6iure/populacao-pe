# %% 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.lines as mlines 
import matplotlib.ticker as mticker
from matplotlib.lines import Line2D
import re
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
fig, ax = plt.subplots(figsize=(12, 6))
ax.set_facecolor('#F7F9FC')
fig.patch.set_facecolor('#F7F9FC')


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

taxa_homens = 16.8745071
taxa_mulheres = 17.2181902
taxa_ambos = 17.052837

#legenda p mostrar crescimento populacional
handle_ambos = mlines.Line2D([], [], color='#1a4f7a', linewidth=2.8, 
                             label=f'Ambos: {taxa_ambos:.2f}%')

handle_mulheres = mlines.Line2D([], [], color="#FFFFFF", linewidth=2, linestyle='--', 
                                label=f'Mulheres: {taxa_mulheres:.2f}%')

handle_homens = mlines.Line2D([], [], color="#FFFFFF", linewidth=2, linestyle='-.', 
                              label=f'Homens: {taxa_homens:.2f}%')

ax.legend(handles=[handle_ambos, handle_mulheres, handle_homens], 
          title='Crescimento Populacional no Período', 
          loc='upper left', 
          frameon=False, 
          fontsize=9, 
          title_fontsize=10)

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
# GRAFICO DE LINHAS PARA MOSTRAR A RAZAO DE DEPENDENCIA
plt.figure(figsize=(12,6))

plt.plot(dependencia['ano'], dependencia['rdj'], color="#2166AC", linestyle='-.', linewidth=2, label='Jovens (0-14)') 
plt.plot(dependencia['ano'], dependencia['rdi'], color="#D73027", linestyle='--', linewidth=2, label='Idosos (65+)')

plt.plot(dependencia['ano'], dependencia['rdt'], color="#1A9641", linestyle='-', linewidth=3, label='Razão de Dependência Total')

ax = plt.gca()
ax.spines['left'].set_color('#D1D5DB')  
ax.spines['bottom'].set_color('#D1D5DB')
ax.grid(axis='x', color='#dddddd', linewidth=0.8, linestyle='--', zorder=0)

plt.title('Evolução da Razão de Dependência em Pernambuco', fontsize=16, fontweight='bold', color='#1F2937', loc='left', pad=15)

plt.xlabel('Ano', fontsize=11, color='#4B5563', labelpad=10)
plt.ylabel('Dependentes para cada 100 ativos', fontsize=11, color='#4B5563', labelpad=10)

sns.despine()
plt.xticks(dependencia['ano'], rotation=0) 
plt.legend(frameon=False, loc='upper right', fontsize=10)
plt.tight_layout()
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
# grafico de indice de envelhecimento da populacao
CORES   = {'jovem': '#2A6F97', 'adulto': '#1A9641', 'idoso': '#A63A50'}
ESTILOS = {'Homens': '-',  'Mulheres': '--'}

fig, ax = plt.subplots(figsize=(12, 7))
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

for spine in ['top', 'right']:
    ax.spines[spine].set_visible(False)
ax.spines['left'].set_color('#cccccc')
ax.spines['bottom'].set_color('#cccccc')
ax.tick_params(length=0, labelcolor='#555555', labelsize=10)
ax.grid(axis='both', color='#e5e5e5', linewidth=0.8, linestyle='--', zorder=0)
ax.set_axisbelow(True)

ax.yaxis.set_major_formatter(
    mticker.FuncFormatter(lambda x, pos: f'{x/1_000_000:.1f} mi')
)
ax.set_xlim(1999, 2025)
ax.set_xticks([2000, 2005, 2010, 2015, 2020, 2024])
ax.set_xlabel('Ano', fontsize=10, color='#555555', labelpad=8)

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

ax.set_title('Pernambuco: Índice de Envelhecimento da População',
             fontsize=14, fontweight='bold', color='black', loc='left', pad=18)

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
pop_total_2024 = df_pivo['homens_2024'].sum() + df_pivo['mulheres_2024'].sum()

fig, ax = plt.subplots(figsize=(11, 7))
ax.set_facecolor('#F7F9FC')
fig.patch.set_facecolor('#F7F9FC')

ax.barh(df_pivo['grupo_etario'], -df_pivo['homens_2024'], color='#2A6F97', label='Homens')
ax.barh(df_pivo['grupo_etario'], df_pivo['mulheres_2024'], color='#A63A50', label='Mulheres')

# Mostrando as porcentagens que cada populacao representa nas barras
for idx, row in df_pivo.iterrows():
    pct_h = (row['homens_2024'] / pop_total_2024) * 100
    pct_m = (row['mulheres_2024'] / pop_total_2024) * 100
    
    ax.text(-row['homens_2024'], row['grupo_etario'], f'{pct_h:.1f}%', ha='right', va='center', fontweight='semibold', fontsize=8, color="black", alpha=0.4)
    ax.text(row['mulheres_2024'], row['grupo_etario'], f'{pct_m:.1f}%', ha='left', va='center', fontweight='semibold', fontsize=8, color='black', alpha=0.4)

for spine in ['top', 'right']:
    ax.spines[spine].set_visible(False)
ax.spines['left'].set_color('#cccccc')
ax.spines['bottom'].set_color('#cccccc')

plt.title('Pirâmide Etária - Pernambuco 2024 ', fontsize=14, pad=10, fontweight='bold', loc='left')
plt.xlabel('População', fontsize=12, fontweight='bold', color='#555555')
plt.ylabel('Grupo Etário', fontsize=12, fontweight='bold', color='#555555')
ax.legend()

ticks = ax.get_xticks()
ax.set_xticklabels([int(abs(tick)) for tick in ticks])

sns.despine()
plt.show()
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

fig, ax = plt.subplots(figsize=(12, 6))
ax.set_facecolor('#F7F9FC')
fig.patch.set_facecolor('#F7F9FC')

df_natalidade['anos'] = df_natalidade['anos'].astype(int)

ax.plot(df_natalidade['anos'], df_natalidade['taxa_natalidade'], 
        color='#2A6F97', linewidth=3, label='Taxa de Natalidade')


try:
    # --- Anotação 1: Epicentro do Zika Vírus (2016) ---
    v_2016 = df_natalidade.loc[df_natalidade['anos'] == 2016, 'taxa_natalidade'].values[0]
    ax.annotate(
        'Crise do Zika Vírus (2016)\nPernambuco foi o epicentro.\nO medo da microcefalia gerou\num recuo abrupto de nascimentos.',
        xy=(2016, v_2016), 
        xytext=(2008, v_2016 - 1.5),  # Posiciona o texto à esquerda e abaixo do ponto
        arrowprops=dict(arrowstyle="->", color='#A63A50', lw=1.2, connectionstyle="arc3,rad=-0.1"),
        fontsize=9.5, color='#4A5568', fontweight='medium',
        bbox=dict(boxstyle="round,pad=0.4", fc="#F7F9FC", ec="#E2E8F0", alpha=0.9)
    )
    
    # Marcador discreto no ponto exato de 2016
    ax.plot(2016, v_2016, marker='o', color='#A63A50', markersize=6)

    # --- Anotação 2: Impacto da COVID-19 (2021) ---
    v_2021 = df_natalidade.loc[df_natalidade['anos'] == 2021, 'taxa_natalidade'].values[0]
    ax.annotate(
        'Pandemia de COVID-19 (2021)\nIncerteza econômica e sanitária\nlevaram ao adiamento do\nplanejamento familiar.',
        xy=(2021, v_2021), 
        xytext=(2014, v_2021 - 2.5),  
        arrowprops=dict(arrowstyle="->", color='#A63A50', lw=1.2, connectionstyle="arc3,rad=0.1"),
        fontsize=9.5, color='#4A5568', fontweight='medium',
        bbox=dict(boxstyle="round,pad=0.4", fc="#F7F9FC", ec="#E2E8F0", alpha=0.9)
    )
    
    ax.plot(2021, v_2021, marker='o', color='#A63A50', markersize=6)
    
except IndexError:
    print("Aviso: Verifique se a coluna 'anos' está preenchida corretamente de 2000 a 2024.")


anos_lista = sorted(df_natalidade['anos'].unique())
anos_exibidos = [ano for i, ano in enumerate(anos_lista) if i % 4 == 0 or ano == anos_lista[-1]]
ax.set_xticks(anos_exibidos)
ax.set_xticklabels(anos_exibidos, rotation=0)

ax.set_xlim(anos_lista[0] - 0.5, anos_lista[-1] + 0.5)

for spine in ['top', 'right']:
    ax.spines[spine].set_visible(False)
ax.spines['left'].set_color('#cccccc')
ax.spines['bottom'].set_color('#cccccc')

ax.tick_params(axis='both', colors='#555555', labelsize=10.5)

plt.suptitle('Taxa Bruta de Natalidade em Pernambuco (2000-2024)', 
             fontsize=15, fontweight='bold', color='#1A202C', x=0.04, y=0.98, ha='left')


plt.xlabel('Ano', fontsize=11, fontweight='bold', color='#555555', labelpad=12)
plt.ylabel('Nascimentos por 1.000 hab.', fontsize=11, fontweight='bold', color='#555555', labelpad=12)

sns.despine()
plt.tight_layout()
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
fig, ax = plt.subplots(figsize=(12, 6))
ax.set_facecolor('#F7F9FC')
fig.patch.set_facecolor('#F7F9FC')

cor_linha = '#A63A50' 
ax.plot(tx_mort['anos'], tx_mort['taxa_mort_bruta'], color=cor_linha, linewidth=2.5)

try:
    y_2016 = tx_mort.loc[tx_mort['anos'] == 2016, 'taxa_mort_bruta'].values[0]
    y_2021 = tx_mort.loc[tx_mort['anos'] == 2021, 'taxa_mort_bruta'].values[0]

    # Pico 1: Crise das Arboviroses (Zika e Chikungunya causaram forte excesso de óbitos em idosos)
    ax.annotate('2015-2016\nSurto de Arboviroses\n(Zika/Chikungunya)', 
                xy=(2016, y_2016), 
                xytext=(-80, 40), textcoords='offset points',
                arrowprops=dict(arrowstyle="->", color='#888888', connectionstyle="arc3,rad=-0.1"),
                fontsize=9, color='#4A5568', fontweight='medium', ha='center')

    # Pico 2: Pandemia de COVID-19 (O maior pico de mortalidade da história recente do estado)
    ax.annotate('2020-2021\nMáximo Histórico\n(Pandemia de COVID-19)', 
                xy=(2021, y_2021), 
                xytext=(-85, -45), textcoords='offset points',
                arrowprops=dict(arrowstyle="->", color='#888888', connectionstyle="arc3,rad=0.15"),
                fontsize=9, color='#4A5568', fontweight='bold', ha='center')
except IndexError:
    pass

for spine in ['top', 'right']:
    ax.spines[spine].set_visible(False)
ax.spines['left'].set_color('#cccccc')
ax.spines['bottom'].set_color('#cccccc')

ax.tick_params(axis='both', colors='#555555', labelsize=10)

plt.title('Taxa Bruta de Mortalidade em Pernambuco (2000-2024)', fontsize=14, pad=15, fontweight='bold', loc='left')
plt.xlabel('Ano', fontsize=12, fontweight='bold', color='#555555')
plt.ylabel('Mortes por 1.000 hab.', fontsize=12, fontweight='bold', color='#555555')


sns.despine()
plt.tight_layout()
plt.show()

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
df_top10 = causas_mort.sort_values('Total_Periodo', ascending=False).head(10).copy()

df_top10['Causa_Limpa'] = df_top10['Causa'].apply(
    lambda x: re.sub(r'^[IXV]+\.\s*', '', str(x)).split('ex clínd')[0].strip()
)

fig, ax = plt.subplots(figsize=(12, 6.5))
ax.set_facecolor('#F7F9FC')
fig.patch.set_facecolor('#F7F9FC')

bars = ax.barh(df_top10['Causa_Limpa'], df_top10['Total_Periodo'], color='#2A6F97', height=0.7)
ax.invert_yaxis()

max_valor = df_top10['Total_Periodo'].max()
for bar in bars:
    width = bar.get_width()
    
    valor_formatado = f'{int(width):,}'.replace(',', '.')
    
    ax.text(width + (max_valor * 0.01), 
            bar.get_y() + bar.get_height()/2, 
            f' {valor_formatado}', 
            va='center', ha='left', 
            fontsize=9.5, fontweight='semibold', color='#4A5568')

ax.set_xticks([]) 
for spine in ['top', 'right', 'bottom']:
    ax.spines[spine].set_visible(False)

ax.spines['left'].set_color('#cccccc')
ax.tick_params(axis='y', colors='#555555', labelsize=10.5)

plt.suptitle('As 10 Principais Causas de Morte em Pernambuco (2000-2024)', 
             fontsize=15, fontweight='bold', color='#1A202C', x=0.04, y=0.97, ha='left')



ax.set_xlim(0, max_valor * 1.12)
sns.despine(left=False, bottom=True)
plt.tight_layout()
plt.show()
# %%
causas_mort['Total_Periodo'] = causas_mort[anos].sum(axis=1)
top_7_causas = causas_mort.sort_values('Total_Periodo', ascending=False)['Causa'].head(7).tolist()

plt.figure(figsize=(14, 7))
sns.set_theme(style="whitegrid") 

for causa in top_7_causas:
    dados_causa = causas_mort[causas_mort['Causa'] == causa][anos].values.flatten()
    
    plt.plot(anos, dados_causa, label=causa, marker='o', linewidth=2.5)

# Títulos e rótulos
plt.title('Evolução das 7 Principais Causas de Morte em Pernambuco (2000-2024)', fontsize=15, fontweight='bold', pad=15)
plt.xlabel('Ano', fontsize=12)
plt.ylabel('Número de Óbitos', fontsize=12)
plt.xticks(rotation=45) 

plt.legend(title='Causas de Morte', bbox_to_anchor=(0, 1), loc='upper left')
sns.despine()
plt.tight_layout()
plt.show()
# %%
df = pd.read_excel('data/data_geral/tabela202.xlsx')
df_estado = df.iloc[0:2].copy()
df_estado['municipio'] = 'Pernambuco'
# %%
df_long = pd.melt(
    df_estado, 
    id_vars=['municipio', 'situacao'], 
    value_vars=['2000', '2010'], 
    var_name='Ano', 
    value_name='Populacao'
)
df_long['Populacao_Milhoes'] = df_long['Populacao'] / 1_000_000
# %%
taxa_urbanizacao = {
    '2000': 76.5,  # 76.5% da população era urbana em 2000
    '2010': 80.2   # 80.2% da população era urbana em 2010
}

# %%
plt.figure(figsize=(12, 6))

ax = sns.barplot(
    data=df_long, 
    x='Ano', 
    y='Populacao_Milhoes', 
    hue='situacao', 
    palette=['#2A6F97', '#A63A50']
)

for i, container in enumerate(ax.containers):
    is_urbana = (i == 0) 
    
    for j, bar in enumerate(container):
        altura = bar.get_height()
        ano = ['2000', '2010'][j]
        
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