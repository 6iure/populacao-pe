# %% 
import pandas as pd

# %%
df_all = pd.read_excel('data/data_geral/dinamica_populacional_pe.xlsx')
df_all.head()
# %%
pe = df_all[df_all['LOCAL'] == 'Pernambuco']
pe.head()
# %% calculo da taxa de crescimento populacional de ambos, apenas mulheres e apenas homens

def calcular_total_pop(df, sexo):
    mascara = (df['SEXO'] == sexo)
    df_filtrado = df[mascara]

    # Etapa 2 — definir colunas numéricas
    colunas_anos = list(range(2000, 2025))

    # Etapa 3 — somar ao longo das linhas
    total = df_filtrado[colunas_anos].sum()

    # Etapa 4 — montar nova linha
    linha_total = {
        'GRUPO ETÁRIO': 'Total',
        'SEXO':          sexo,
    }
    for ano in colunas_anos:
        linha_total[ano] = total[ano]     # ← adicionar cada ano ao dicionário

    # Etapa 5 — concatenar
    df_nova_linha = pd.DataFrame([linha_total])
    df_com_total  = pd.concat([df_filtrado, df_nova_linha], ignore_index=True)

    return df_com_total
# %%
pe_ambos = calcular_total_pop(pe, 'Ambos')
pe_ambos.head(20)

# %%
pe_homens  = calcular_total_pop(pe, 'Homens')
pe_homens.head(20)

# %%
pe_mulheres = calcular_total_pop(pe, 'Mulheres')
pe_mulheres
# %%
# def calculo_cresc_pop (df, posicao[]):
