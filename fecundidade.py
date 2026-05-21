# %% 
import pandas as pd
import numpy as np

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
choicelist = ['Idosos', 'Jovens']
# %%
pe['dependencia'] = np.select(condlist, choicelist, 'Ativos')
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
dependencia['rdi'] = (dependencia['Idosos'] / dependencia['Ativos']) * 100
dependencia
# %%
dependencia['rdj'] = (dependencia['Jovens'] / dependencia['Ativos']) * 100
dependencia
# %%
dependencia['rdt'] = ((dependencia['Idosos'] + dependencia['Jovens']) / dependencia['Ativos']) * 100
dependencia
# %%
