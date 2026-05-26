# %% 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

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

#todo deixar isso mais bonitinho

((cresc_pop_final[2024] - cresc_pop_final[2000]) / cresc_pop_final[2000]) * 100

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
# %% calculando o indice de envelhecimento da populacao

cond = pe['grupo_etario'].isin(lista_jovens), pe['grupo_etario'].isin(['60-64','65-69','70-74','75-79','80-84','85-89','90+'])
chce = ['jovem', 'idoso']
# %%
pe['fase_vida'] = np.select(cond, chce, 'adulto')
pe
# %%
ind_env = pe.groupby(['fase_vida']).sum(numeric_only=True)
ind_env
# %%
teste = ind_env.T
teste

# %%
teste.reset_index(inplace=True)
teste
# %%
teste.drop(columns=['adulto'], inplace=True)
teste
# %%
teste['indice_envelhecimento'] = (teste['idoso'] / teste['jovem']) * 100
teste
# %%
pir_pop = pe.groupby(['sexo', 'grupo_etario']).sum()
pir_pop 

# %%
pir_pop.reset_index(inplace=True)
# %%
pir_pop
# %%
pir_pop.drop(columns=[2001,2002,2003,2004,2005,2006,2007, 2008,2009,2010,2011,2012,2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023], inplace=True)
# %%
pir_pop
# %%
pir_pop[pir_pop['sexo'] == 'Homens']

# %%
data = {
 "AgeGroup": ["0-4", "5-9", "10-14", "15-19", "20-24", "25-29", "30-34", "35-39", "40-44", "45-49", "50-54", "55-59", "60-64", "65-69", "70-74", "75-79", "80+"],
 "Male": [1500, 1450, 1400, 1350, 1300, 1250, 1200, 1150, 1100, 1050, 900, 750, 600, 450, 300, 150, 50],
 "Female": [1400, 1380, 1320, 1280, 1250, 1220, 1180, 1140, 1100, 1060, 920, 780, 640, 500, 350, 180, 70]
}
df = pd.DataFrame(data)
df
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
# %%
df_pivo
# %%

# todo adicionar % da populacao que cada barra representa

fig, ax = plt.subplots(figsize=(12, 6))

ax.barh(df_pivo['grupo_etario'], -df_pivo['homens_2024'], color='royalblue', label='Homens')
ax.barh(df_pivo['grupo_etario'], df_pivo['mulheres_2024'], color='magenta', label='Mulheres')

plt.grid(axis='x', linestyle='--', alpha=0.6)
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
