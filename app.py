import numpy as np
import pandas as pd
import seaborn as sns
import plotly.express as px
import streamlit as st


def carrega_dataset(nome_dataset):
    return sns.load_dataset(nome_dataset)


# CORPO
st.markdown("""
            # iNalyze
            ### *A sua ferramenta para análise dados*
            ---
            """)


## CORPO - Carregando o dataset
st.header('Dataset')
nome_dataset = st.text_input('Qual o nome do dataset que deseja carregar?',
                             value='penguins')

if nome_dataset:
    df = carrega_dataset(nome_dataset)
        
# SIDEBAR
with st.sidebar:
    st.title('Filtros')
    cols_selected = \
        st.multiselect('Filtre os campos que deseja analisar:',
                       options=list(df.columns),
                       default=list(df.columns))
    
    frac_sample = \
        st.slider('Defina o percentual do dataset para análise:', 
                  min_value=1, max_value=100, value=50, step=1)

df_selected = df[cols_selected].sample(frac=frac_sample/100)
    
    
## CORPO - Info do dataset
with st.expander('Dados do Dataset'):
    st.header('Dados do Dataset')
    st.subheader('Primeiros registros')
    st.write(df_selected.head())
    
    st.subheader('Colunas')
    for col in df_selected.columns:
        st.text(f'- {col}')
        
    st.subheader('Dados Faltantes')
    st.write(df_selected.isna().sum()[df_selected.isna().sum() > 0])

    st.subheader('Estatísticas Descritivas')
    st.write(df_selected.describe())


## CORPO - Análise Univariada
st.header('Análise Univariada')
univar_campo =  \
    st.selectbox('Selecione o campo que deseja avaliar a distribuição:',
                 options=list(df_selected.select_dtypes(include=np.number)))


st.plotly_chart(px.histogram(data_frame=df_selected, x=univar_campo))
st.plotly_chart(px.box(data_frame=df_selected, y=univar_campo))


## CORPO - Análise Bivariada
st.header('Análise Bivariada')
bivar_graf_option = \
    st.radio('Escolha um tipo de gráfico:',
             options=['dispersão', 'boxplot', 'pairplot'])

if bivar_graf_option == 'dispersão':
    campo_dispersao_1 =  \
        st.selectbox('Selecione primeira variável numérica:',
                     options=list(df_selected.select_dtypes(include=np.number)))
        
    campo_dispersao_2 =  \
        st.selectbox('Selecione segunda variável numérica:',
                     options=list(df_selected.select_dtypes(include=np.number)))
        
    st.plotly_chart(
        px.scatter(data_frame=df_selected, 
                   x=campo_dispersao_1, 
                   y=campo_dispersao_2)
    )
        
elif bivar_graf_option == 'boxplot':
    campo_boxplot_num =  \
        st.selectbox('Selecione uma variável numérica:',
                     options=list(df_selected.select_dtypes(include=np.number)))
        
    campo_boxplot_cat =  \
        st.selectbox('Selecione uma variável categórica:',
                     options=list(df_selected.select_dtypes(exclude=np.number)))
        
    st.plotly_chart(
        px.box(data_frame=df_selected, 
                   x=campo_boxplot_cat, 
                   y=campo_boxplot_num)
    )
    
else:
    pairplot = sns.pairplot(df_selected)
    st.pyplot(pairplot)
    


# ATIVIDADES
# Refatore o código, aplicando as modificações:

# 1 - Modularize o código passando a função "carrega_dataset" para um módulo

# 2 - Crie um slider no sidebar que permita filtrar uma amostra do dataset.
#     Para realizar amostragem, utilize o método sample do dataframe pandas.

# 3 - Adicione uma seção de análise multivariada:
#   3.1 - Adicione a possibilidade de segmentação no gráfico de dispersao
#   3.2 - Adicione checkbox que permita incluir linha de tendência 
#         no gráfico de dispersão
#   3.3 - Adicione a possibilidade de segmentação no gráfico de boxplot
#   3.4 - Adicione a possibilidade de segmentação no gráfico de pairplot