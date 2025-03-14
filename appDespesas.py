import streamlit as st
import pandas as pd
import plotly.express as px

# Configurando o formato dos valores monetários
# colocando para a tela ficar mais larga
pd.options.display.float_format = '{:.2f}'.format
st.set_page_config(layout="wide", page_title='Despesas Públicas do Governo do Estado do Rio de Janeiro',
                   page_icon=':moneybag:', initial_sidebar_state='expanded')


# Criando um titulo no side bar
st.sidebar.subheader('Painel de Despesas Públicas do Governo do Estado do Rio de Janeiro.')




option = st.sidebar.radio(
    'Escolha a categoria os Dados que quer Acessar: ',
    ['Executivo', 'Legislativo', 'Judiciário']
)
st.sidebar.write("""
    Os dados foram coletados pelo portal da transparência do governo do estado no link [https://www.rj.gov.br/transparencia/](https://www.rj.gov.br/transparencia/).
    As atualizações dos dados são mensais e os dados serão atualizados conforme a possibilidade de obtenção dos mesmos.
    Desenvolvido por Christian Basilio Oliveira. [LinkedIn](https://www.linkedin.com/in/christianbasilioo/)
""")
if option == 'Executivo':
    st.subheader('Despesas do Executivo')
    page = st.selectbox(
        'Selecione a página que deseja visualizar do Poder Executivo:',
        ['Consulta Geral', 'Distribuição por Elemento', 'Distribuição por Órgão', 'Distribuição por Função']
    )

    despensasGeraisExecutivo = pd.read_csv('despesas_executivo.csv', sep=';', encoding='utf-8')
    # formatando os valores de Valor Pago
    despensasGeraisExecutivo['Valor Pago'] = despensasGeraisExecutivo["Valor Pago"].str.replace(',', '.').astype(float)

    if page == 'Consulta Geral':
        totalPago = despensasGeraisExecutivo['Valor Pago'].sum()
        totalPago = f'R${totalPago:,.2f}'
        st.markdown(
            f"""
            <div style='display: flex; justify-content: center; align-items: center; height: 100%; padding: 40px;'>
                <div style='text-align: center; background-color: white; color: green; padding: 10px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);'>
                    <h5 style='color: green;'>Despesas do Executivo do Governo do Estado do Rio de Janeiro</h5>
                    <h3>{totalPago}</h3>
                </div>
            </div>
            """, 
            unsafe_allow_html=True
        )
        st.write("Na ferramenta abaixo voce pode consultar os dados com base nos dois filtros abaixo:")
        search = st.text_input('Digite o que deseja procurar na tabela:')
        coluna = st.selectbox('Escolha a coluna que deseja procurar:', despensasGeraisExecutivo.columns)
        st.write('Tabela Agregada de Despesas Gerais do Executivo complreta para Download.')
        if search:
            filtered_data = despensasGeraisExecutivo[despensasGeraisExecutivo[coluna].astype(str).str.contains(search, case=False, na=False)]
        else:
            filtered_data = despensasGeraisExecutivo

        st.dataframe(filtered_data)

    elif page == 'Distribuição por Elemento':
        totalPago = despensasGeraisExecutivo['Valor Pago'].sum()

        col1, col2 = st.columns(2)
        with col1:
            st.write("Distribuição dos Valores Pagos por Elemento")
            elementoExecutivo = despensasGeraisExecutivo.groupby(['Nome Elemento'])['Valor Pago'].sum().sort_values(ascending=False).reset_index()
            elementoExecutivo['Percentual'] = round((elementoExecutivo['Valor Pago'] / elementoExecutivo['Valor Pago'].sum()) * 100,2)
            elementoExecutivo['Nome Elemento'] = elementoExecutivo['Nome Elemento'][:25]
            fig = px.bar(elementoExecutivo, x='Nome Elemento', y='Valor Pago', text_auto=".2f", labels={'Nome Elemento': 'Elemento', 'Valor Pago': 'Valor Pago (R$)'})
            st.plotly_chart(fig)

        with col2:
            st.write("Tabela Agregada de Elementos e Valores Pagos")
            elementoExecutivo = elementoExecutivo.sort_values(by='Valor Pago', ascending=False)
            elementoExecutivo['Valor Pago'] = elementoExecutivo['Valor Pago'].apply(lambda x: f'R${x:,.2f}')
            st.data_editor(
                elementoExecutivo,
                column_config={
                    "Nome Elemento": "Elemento",
                    "Valor Pago": st.column_config.NumberColumn("Valor Pago (R$)", format="R$ %.2f",min_value=0, max_value=totalPago)
                },
                hide_index=True
            )

    elif page == 'Distribuição por Órgão':
        totalPago = despensasGeraisExecutivo['Valor Pago'].sum()

        col3, col4 = st.columns(2)
        with col3:
            st.write("Distribuição dos Valores Pagos por Órgão")
            orgaoExecutivo = despensasGeraisExecutivo.groupby(['Nome Órgão'])['Valor Pago'].sum().sort_values(ascending=False).reset_index()
            orgaoExecutivo['Percentual'] = round((orgaoExecutivo['Valor Pago'] / orgaoExecutivo['Valor Pago'].sum()) * 100,2)
            orgaoExecutivo['Nome Órgão'] = orgaoExecutivo['Nome Órgão'][:25]
            fig = px.bar(orgaoExecutivo, x='Nome Órgão', y='Valor Pago', labels={'Nome Órgão': 'Orgão', 'Valor Pago': 'Valor Pago (R$)'})
            st.plotly_chart(fig)

        with col4:
            st.write("Tabela Agregada de Órgãos e Valores Pagos")
            orgaoExecutivo = orgaoExecutivo.sort_values(by='Valor Pago', ascending=False)
            orgaoExecutivo['Valor Pago'] = orgaoExecutivo['Valor Pago'].apply(lambda x: f'R${x:,.2f}')
            st.data_editor(
                orgaoExecutivo,
                column_config={
                    "Nome Órgão": "Órgão",
                    "Valor Pago": st.column_config.NumberColumn("Valor Pago (R$)", format="R$ %.2f", min_value=0, max_value=totalPago)
                },
                hide_index=True
            )

    elif page == 'Distribuição por Função':
        st.write("Distribuição dos Valores Pagos por Função")
        funcaoSelecionada = st.selectbox('Selecione a Função:', despensasGeraisExecutivo['Nome Função'].unique())

        funcaoExecutivo = despensasGeraisExecutivo[despensasGeraisExecutivo['Nome Função'] == funcaoSelecionada]
        funcaoExecutivo = funcaoExecutivo.groupby(['Nome Função', 'Nome Sub Função', 'Histórico'])['Valor Pago'].sum().sort_values(ascending=False).reset_index()
        funcaoExecutivo['Percentual'] = round((funcaoExecutivo['Valor Pago'] / funcaoExecutivo['Valor Pago'].sum()) * 100, 2)
        st.write("----")
        col5, col6 = st.columns(2)
        with col5:
            st.write("Distribuição dos Valores Pagos por Sub Função")
            fig = px.pie(funcaoExecutivo, names='Nome Sub Função', values='Valor Pago', hole=0.4, labels={'Nome Sub Função': 'Sub Função', 'Valor Pago': 'Valor Pago (R$)'})
            st.plotly_chart(fig)

        with col6:
            st.write("Tabela Agregada de Sub Funções e Valores Pagos")
            search_funcao = st.text_input('Digite o que deseja procurar na tabela de Sub Funções:')
            coluna_funcao = st.selectbox('Escolha a coluna que deseja procurar:', funcaoExecutivo.columns)

            if search_funcao:
                funcaoExecutivo = funcaoExecutivo[funcaoExecutivo[coluna_funcao].astype(str).str.contains(search_funcao, case=False, na=False)]
            
            funcaoExecutivo = funcaoExecutivo.sort_values(by='Valor Pago', ascending=False)
            funcaoExecutivo['Valor Pago'] = funcaoExecutivo['Valor Pago'].apply(lambda x: f'R${x:,.2f}')
            st.data_editor(
                funcaoExecutivo,
                column_config={
                    "Nome Sub Função": "Sub Função",
                    "Valor Pago": st.column_config.NumberColumn("Valor Pago (R$)", format="R$ %.2f"),
                    "Percentual": "Percentual (%)"
                },
                hide_index=True
            )

elif option == 'Legislativo':
    st.subheader('Despesas do Legislativo')
    # Aqui você pode adicionar o código para carregar e exibir os dados do Legislativo
    despensasGeraisLegislativo = pd.read_csv('despesas_legislativo.csv', sep=';', encoding='utf-8')
    despensasGeraisLegislativo['Valor Pago'] = despensasGeraisLegislativo['Valor Pago'].str.replace(',', '.').astype(float)

    # Criando as partes separadas

    page = st.selectbox(
        'Selecione a página que deseja visualizar do Poder Legislativo:',
        ['Consulta Geral', 'Distribuição por Elemento', 'Distribuição por Órgão', 'Distribuição por Função']
    )

    if page == 'Consulta Geral':
        totalPago = despensasGeraisLegislativo['Valor Pago'].sum()
        totalPago = f'R${totalPago:,.2f}'
        st.markdown(
            f"""
            <div style='display: flex; justify-content: center; align-items: center; height: 100%; padding: 40px;'>
                <div style='text-align: center; background-color: white; color: green; padding: 10px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);'>
                    <h5 style='color: green;'>Despesas do Legislativo do Governo do Estado do Rio de Janeiro</h5>
                    <h3>{totalPago}</h3>
                </div>
            </div>
            """, 
            unsafe_allow_html=True
        )
        st.write("Na ferramenta abaixo voce pode consultar os dados com base nos dois filtros abaixo:")

        search = st.text_input('Digite o que deseja procurar na tabela:')
        coluna = st.selectbox('Escolha a coluna que deseja procurar:', despensasGeraisLegislativo.columns)
        st.write('Tabela Agregada de Despesas Gerais do Legislativo complreta para Download.')
        if search:
            filtered_data = despensasGeraisLegislativo[despensasGeraisLegislativo[coluna].astype(str).str.contains(search, case=False, na=False)]
        else:
            filtered_data = despensasGeraisLegislativo

        st.dataframe(filtered_data)

    elif page == 'Distribuição por Elemento':
        totalPago = despensasGeraisLegislativo['Valor Pago'].sum()

        col1, col2 = st.columns(2)
        with col1:
            st.write("Distribuição dos Valores Pagos por Elemento")
            elementoLegislativo = despensasGeraisLegislativo.groupby(['Nome Elemento'])['Valor Pago'].sum().sort_values(ascending=False).reset_index()
            elementoLegislativo['Percentual'] = round((elementoLegislativo['Valor Pago'] / elementoLegislativo['Valor Pago'].sum()) * 100,2)
            elementoLegislativo['Nome Elemento'] = elementoLegislativo['Nome Elemento'][:25]
            fig = px.bar(elementoLegislativo, x='Nome Elemento', y='Valor Pago', labels={'Nome Elemento': 'Elemento', 'Valor Pago': 'Valor Pago (R$)'})
            st.plotly_chart(fig)

        with col2:
            st.write("Tabela Agregada de Elementos e Valores Pagos")
            elementoLegislativo = elementoLegislativo.sort_values(by='Valor Pago', ascending=False)
            elementoLegislativo['Valor Pago'] = elementoLegislativo['Valor Pago'].apply(lambda x: f'R${x:,.2f}')
            st.data_editor(
                elementoLegislativo,
                column_config={
                    "Nome Elemento": "Elemento",
                    "Valor Pago": st.column_config.NumberColumn("Valor Pago (R$)", format="R$ %.2f",min_value=0, max_value=totalPago)
                },
                hide_index=True
            )

    elif page == 'Distribuição por Órgão':
        totalPago = despensasGeraisLegislativo['Valor Pago'].sum()

        col3, col4 = st.columns(2)
        with col3:
            st.write("Distribuição dos Valores Pagos por Órgão"
            "Órgão")
            orgaoLegislativo = despensasGeraisLegislativo.groupby(['Nome Órgão'])['Valor Pago'].sum().sort_values(ascending=False).reset_index()
            orgaoLegislativo['Percentual'] = round((orgaoLegislativo['Valor Pago'] / orgaoLegislativo['Valor Pago'].sum()) * 100,2)
            orgaoLegislativo['Nome Órgão'] = orgaoLegislativo['Nome Órgão'][:25]
            fig = px.bar(orgaoLegislativo, x='Nome Órgão', y='Valor Pago', labels={'Nome Órgão': 'Orgão', 'Valor Pago': 'Valor Pago (R$)'},
                         # colocando o angulo 90 graus
                            
                         )
            st.plotly_chart(fig)

        with col4:
            st.write("Tabela Agregada de Órgãos e Valores Pagos")
            orgaoLegislativo = orgaoLegislativo.sort_values(by='Valor Pago', ascending=False)
            orgaoLegislativo['Valor Pago'] = orgaoLegislativo['Valor Pago'].apply(lambda x: f'R${x:,.2f}')
            st.data_editor(
                orgaoLegislativo,
                column_config={
                    "Orgao": "Órgão",
                    "Valor Pago": st.column_config.NumberColumn("Valor Pago (R$)", format="R$ %.2f", min_value=0, max_value=totalPago)
                },
                hide_index=True
            )

    elif page == 'Distribuição por Função':
        st.write("Distribuição dos Valores Pagos por Função")
        funcaoSelecionada = st.selectbox('Selecione a Função:', despensasGeraisLegislativo['Nome Função'].unique())

        funcaoLegislativo = despensasGeraisLegislativo[despensasGeraisLegislativo['Nome Função'] == funcaoSelecionada]
        funcaoLegislativo = funcaoLegislativo.groupby(['Nome Função', 'Nome Sub Função', 'Histórico'])['Valor Pago'].sum().sort_values(ascending=False).reset_index()
        funcaoLegislativo['Percentual'] = round((funcaoLegislativo['Valor Pago'] / funcaoLegislativo['Valor Pago'].sum()) * 100, 2)
        st.write("----")
        col5, col6 = st.columns(2)
        with col5:
            st.write("Distribuição dos Valores Pagos por Sub Função")
            fig = px.pie(funcaoLegislativo, names='Nome Sub Função', values='Valor Pago', hole=0.4, labels={'Nome Sub Função': 'Sub Função', 'Valor Pago': 'Valor Pago (R$)'})
            st.plotly_chart(fig)

        with col6:
            st.write("Tabela Agregada de Sub Funções e Valores Pagos")
            search_funcao = st.text_input('Digite o que deseja procurar na tabela de Sub Funções:')
            coluna_funcao = st.selectbox('Escolha a coluna que deseja procurar:', funcaoLegislativo.columns)

            if search_funcao:
                funcaoLegislativo = funcaoLegislativo[funcaoLegislativo[coluna_funcao].astype(str).str.contains(search_funcao, case=False, na=False)]
            
            funcaoLegislativo = funcaoLegislativo.sort_values(by='Valor Pago', ascending=False)
            funcaoLegislativo['Valor Pago'] = funcaoLegislativo['Valor Pago'].apply(lambda x: f'R${x:,.2f}')
            st.data_editor(
                funcaoLegislativo,
                column_config={
                    "Nome Sub"
                    "Sub Função": "Sub Função",
                    "Valor Pago": st.column_config.NumberColumn("Valor Pago (R$)", format="R$ %.2f"),
                    "Percentual": "Percentual (%)"
                },
                hide_index=True
            )




elif option == 'Judiciário':
    st.subheader('Despesas do Judiciário')
    despensasGeraisJudiciario = pd.read_csv('despesas_judiciario.csv', sep=';', encoding='utf-8')
    despensasGeraisJudiciario['Valor Pago'] = despensasGeraisJudiciario['Valor Pago'].str.replace(',', '.').astype(float)

    page = st.selectbox(
        'Selecione a página que deseja visualizar do Poder Judiciário:',
        ['Consulta Geral', 'Distribuição por Elemento', 'Distribuição por Órgão', 'Distribuição por Função']
    )

    if page == 'Consulta Geral':
        totalPago = despensasGeraisJudiciario['Valor Pago'].sum()
        totalPago = f'R${totalPago:,.2f}'
        st.markdown(
            f"""
            <div style='display: flex; justify-content: center; align-items: center; height: 100%; padding: 40px;'>
                <div style='text-align: center; background-color: white; color: green; padding: 10px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);'>
                    <h5 style='color: green;'>Despesas do Judiciário do Governo do Estado do Rio de Janeiro</h5>
                    <h3>{totalPago}</h3>
                </div>
            </div>
            """, 
            unsafe_allow_html=True
        )
        st.write("Na ferramenta abaixo voce pode consultar os dados com base nos dois filtros abaixo:")

        search = st.text_input('Digite o que deseja procurar na tabela:')
        coluna = st.selectbox('Escolha a coluna que deseja procurar:', despensasGeraisJudiciario.columns)
        st.write('Tabela Agregada de Despesas Gerais do Judiciário completa para Download.')
        if search:
            filtered_data = despensasGeraisJudiciario[despensasGeraisJudiciario[coluna].astype(str).str.contains(search, case=False, na=False)]
        else:
            filtered_data = despensasGeraisJudiciario

        st.dataframe(filtered_data)

    elif page == 'Distribuição por Elemento':
        totalPago = despensasGeraisJudiciario['Valor Pago'].sum()

        col1, col2 = st.columns(2)
        with col1:
            st.write("Distribuição dos Valores Pagos por Elemento")
            elementoJudiciario = despensasGeraisJudiciario.groupby(['Nome Elemento'])['Valor Pago'].sum().sort_values(ascending=False).reset_index()
            elementoJudiciario['Percentual'] = round((elementoJudiciario['Valor Pago'] / elementoJudiciario['Valor Pago'].sum()) * 100,2)
            elementoJudiciario['Nome Elemento'] = elementoJudiciario['Nome Elemento'][:25]
            fig = px.bar(elementoJudiciario, x='Nome Elemento', y='Valor Pago', labels={'Nome Elemento': 'Elemento', 'Valor Pago': 'Valor Pago (R$)'})
            st.plotly_chart(fig)

        with col2:
            st.write("Tabela Agregada de Elementos e Valores Pagos")
            elementoJudiciario = elementoJudiciario.sort_values(by='Valor Pago', ascending=False)
            elementoJudiciario['Valor Pago'] = elementoJudiciario['Valor Pago'].apply(lambda x: f'R${x:,.2f}')
            st.data_editor(
                elementoJudiciario,
                column_config={
                    "Nome Elemento": "Elemento",
                    "Valor Pago": st.column_config.NumberColumn("Valor Pago (R$)", format="R$ %.2f", min_value=0, max_value=totalPago)
                },
                hide_index=True
            )

    elif page == 'Distribuição por Órgão':
        totalPago = despensasGeraisJudiciario['Valor Pago'].sum()

        col3, col4 = st.columns(2)
        with col3:
            st.write("Distribuição dos Valores Pagos por Órgão")
            orgaoJudiciario = despensasGeraisJudiciario.groupby(['Nome Órgão'])['Valor Pago'].sum().sort_values(ascending=False).reset_index()
            orgaoJudiciario['Percentual'] = round((orgaoJudiciario['Valor Pago'] / orgaoJudiciario['Valor Pago'].sum()) * 100,2)
            orgaoJudiciario['Nome Órgão'] = orgaoJudiciario['Nome Órgão'][:25]
            fig = px.bar(orgaoJudiciario, x='Nome Órgão', y='Valor Pago', labels={'Nome Órgão': 'Orgão', 'Valor Pago': 'Valor Pago (R$)'})
            st.plotly_chart(fig)

        with col4:
            st.write("Tabela Agregada de Órgãos e Valores Pagos")
            orgaoJudiciario = orgaoJudiciario.sort_values(by='Valor Pago', ascending=False)
            orgaoJudiciario['Valor Pago'] = orgaoJudiciario['Valor Pago'].apply(lambda x: f'R${x:,.2f}')
            st.data_editor(
                orgaoJudiciario,
                column_config={
                    "Nome Órgão": "Órgão",
                    "Valor Pago": st.column_config.NumberColumn("Valor Pago (R$)", format="R$ %.2f", min_value=0, max_value=totalPago)
                },
                hide_index=True
            )

    elif page == 'Distribuição por Função':
        st.write("Distribuição dos Valores Pagos por Função")
        funcaoSelecionada = st.selectbox('Selecione a Função:', despensasGeraisJudiciario['Nome Função'].unique())

        funcaoJudiciario = despensasGeraisJudiciario[despensasGeraisJudiciario['Nome Função'] == funcaoSelecionada]
        funcaoJudiciario = funcaoJudiciario.groupby(['Nome Função', 'Nome Sub Função', 'Histórico'])['Valor Pago'].sum().sort_values(ascending=False).reset_index()
        funcaoJudiciario['Percentual'] = round((funcaoJudiciario['Valor Pago'] / funcaoJudiciario['Valor Pago'].sum()) * 100, 2)
        st.write("----")
        col5, col6 = st.columns(2)
        with col5:
            st.write("Distribuição dos Valores Pagos por Sub Função")
            fig = px.pie(funcaoJudiciario, names='Nome Sub Função', values='Valor Pago', hole=0.4, labels={'Nome Sub Função': 'Sub Função', 'Valor Pago': 'Valor Pago (R$)'})
            st.plotly_chart(fig)

        with col6:
            st.write("Tabela Agregada de Sub Funções e Valores Pagos")
            search_funcao = st.text_input('Digite o que deseja procurar na tabela de Sub Funções:')
            coluna_funcao = st.selectbox('Escolha a coluna que deseja procurar:', funcaoJudiciario.columns)

            if search_funcao:
                funcaoJudiciario = funcaoJudiciario[funcaoJudiciario[coluna_funcao].astype(str).str.contains(search_funcao, case=False, na=False)]
            
            funcaoJudiciario = funcaoJudiciario.sort_values(by='Valor Pago', ascending=False)
            funcaoJudiciario['Valor Pago'] = funcaoJudiciario['Valor Pago'].apply(lambda x: f'R${x:,.2f}')
            st.data_editor(
                funcaoJudiciario,
                column_config={
                    "Nome Sub Função": "Sub Função",
                    "Valor Pago": st.column_config.NumberColumn("Valor Pago (R$)", format="R$ %.2f"),
                    "Percentual": "Percentual (%)"
                },
                hide_index=True
            )




