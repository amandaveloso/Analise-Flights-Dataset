{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyN8/fmJeh54hW34h/ZJA8MD"
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "code",
      "source": [
        "pip install streamlit pandas openpyxl plotly localtunnel"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "e1oCerb8epx0",
        "outputId": "e43953df-d166-408b-9b7a-9a56b601b937"
      },
      "execution_count": 6,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Requirement already satisfied: streamlit in /usr/local/lib/python3.11/dist-packages (1.45.1)\n",
            "Requirement already satisfied: pandas in /usr/local/lib/python3.11/dist-packages (2.2.2)\n",
            "Requirement already satisfied: openpyxl in /usr/local/lib/python3.11/dist-packages (3.1.5)\n",
            "Requirement already satisfied: plotly in /usr/local/lib/python3.11/dist-packages (5.24.1)\n",
            "\u001b[31mERROR: Could not find a version that satisfies the requirement localtunnel (from versions: none)\u001b[0m\u001b[31m\n",
            "\u001b[0m\u001b[31mERROR: No matching distribution found for localtunnel\u001b[0m\u001b[31m\n",
            "\u001b[0m"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "\n",
        "import streamlit as st\n",
        "import pandas as pd\n",
        "import plotly.express as px # Usaremos Plotly para gráficos interativos e rápidos\n",
        "import numpy as np # Para verificar tipos numérico\n",
        "import openpyxl\n",
        "\n",
        "st.set_page_config(layout=\"wide\") # Layout mais amplo para o dashboard\n",
        "\n",
        "st.title(\"📊 ExcelViz: Gerador de Dashboards Automático\")\n",
        "st.markdown(\"Faça o upload do seu arquivo Excel (.xlsx ou .xls) e visualize seus dados instantaneamente!\")\n",
        "\n",
        "# --- 1. Upload do Arquivo ---\n",
        "uploaded_file = st.file_uploader(\"Escolha um arquivo Excel\", type=[\"xlsx\", \"xls\"])\n",
        "\n",
        "if uploaded_file is not None:\n",
        "    try:\n",
        "        # Carregar o Excel\n",
        "        df = pd.read_excel(uploaded_file)\n",
        "        st.success(\"Arquivo carregado com sucesso!\")\n",
        "\n",
        "        # Exibir as primeiras linhas da tabela para o usuário verificar\n",
        "        st.subheader(\"Prévia dos Dados:\")\n",
        "        st.dataframe(df.head())\n",
        "\n",
        "        # --- 2. Análise e Geração de Dashboard ---\n",
        "        st.subheader(\"Dashboard Automatizado\")\n",
        "\n",
        "        # Separar colunas por tipo para análise\n",
        "        numerical_cols = df.select_dtypes(include=np.number).columns.tolist()\n",
        "        categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()\n",
        "        datetime_cols = df.select_dtypes(include=['datetime64[ns]']).columns.tolist()\n",
        "\n",
        "        # Adicionar opção para o usuário selecionar colunas (opcional, mas bom para personalização)\n",
        "        st.sidebar.subheader(\"Configurações do Dashboard\")\n",
        "        selected_num_col = st.sidebar.selectbox(\"Variável Numérica Principal (para tendências):\", numerical_cols + ['Nenhum'])\n",
        "\n",
        "        st.sidebar.markdown(\"---\")\n",
        "        st.sidebar.write(\"Gráficos de Distribuição:\")\n",
        "        selected_dist_col = st.sidebar.selectbox(\"Variável para Histograma/Barra:\", numerical_cols + categorical_cols + ['Nenhum'])\n",
        "\n",
        "\n",
        "        # --- Seção de Métricas Descritivas ---\n",
        "        if numerical_cols:\n",
        "            st.markdown(\"### Estatísticas Descritivas\")\n",
        "            st.dataframe(df[numerical_cols].describe().T) # Transpor para melhor visualização\n",
        "\n",
        "        # --- Seção de Gráficos ---\n",
        "\n",
        "        # Gráficos para variáveis numéricas\n",
        "        if numerical_cols:\n",
        "            st.markdown(\"### Análise de Variáveis Numéricas\")\n",
        "            num_cols_to_plot = st.multiselect(\"Selecione colunas numéricas para Histograma/Box Plot:\", numerical_cols, default=numerical_cols[:2] if numerical_cols else [])\n",
        "            for col in num_cols_to_plot:\n",
        "                if col:\n",
        "                    # Histograma\n",
        "                    fig_hist = px.histogram(df, x=col, title=f\"Distribuição de {col}\")\n",
        "                    st.plotly_chart(fig_hist, use_container_width=True)\n",
        "\n",
        "                    # Box Plot\n",
        "                    fig_box = px.box(df, y=col, title=f\"Box Plot de {col}\")\n",
        "                    st.plotly_chart(fig_box, use_container_width=True)\n",
        "\n",
        "        # Gráficos de tendências (se houver data e numérica principal selecionada)\n",
        "        if datetime_cols and selected_num_col != 'Nenhum':\n",
        "            st.markdown(f\"### Tendência de {selected_num_col} ao Longo do Tempo\")\n",
        "            # Assumimos que a primeira coluna de data é a principal\n",
        "            date_col = datetime_cols[0]\n",
        "            fig_line = px.line(df, x=date_col, y=selected_num_col,\n",
        "                               title=f\"Tendência de {selected_num_col} por {date_col}\")\n",
        "            st.plotly_chart(fig_line, use_container_width=True)\n",
        "\n",
        "\n",
        "        # Gráficos para variáveis categóricas\n",
        "        if categorical_cols:\n",
        "            st.markdown(\"### Análise de Variáveis Categóricas\")\n",
        "            cat_cols_to_plot = st.multiselect(\"Selecione colunas categóricas para Contagem/Distribuição:\", categorical_cols, default=categorical_cols[:2] if categorical_cols else [])\n",
        "            for col in cat_cols_to_plot:\n",
        "                if col:\n",
        "                    # Contagem de valores (Gráfico de Barras)\n",
        "                    counts = df[col].value_counts().reset_index()\n",
        "                    counts.columns = [col, 'Contagem']\n",
        "                    fig_bar = px.bar(counts, x=col, y='Contagem', title=f\"Contagem de {col}\")\n",
        "                    st.plotly_chart(fig_bar, use_container_width=True)\n",
        "\n",
        "                    # Distribuição (Gráfico de Pizza - para poucas categorias)\n",
        "                    if df[col].nunique() < 15: # Evitar pizzas com muitas fatias\n",
        "                        fig_pie = px.pie(df, names=col, title=f\"Distribuição de {col}\")\n",
        "                        st.plotly_chart(fig_pie, use_container_width=True)\n",
        "\n",
        "        # Gráfico de dispersão entre duas variáveis numéricas (opcional)\n",
        "        if len(numerical_cols) >= 2:\n",
        "            st.markdown(\"### Relação entre Variáveis Numéricas\")\n",
        "            x_scatter = st.selectbox(\"Eixo X (Dispersão):\", numerical_cols)\n",
        "            y_scatter = st.selectbox(\"Eixo Y (Dispersão):\", [col for col in numerical_cols if col != x_scatter])\n",
        "            if x_scatter and y_scatter and x_scatter != y_scatter:\n",
        "                fig_scatter = px.scatter(df, x=x_scatter, y=y_scatter,\n",
        "                                         title=f\"Dispersão de {x_scatter} vs {y_scatter}\")\n",
        "                st.plotly_chart(fig_scatter, use_container_width=True)\n",
        "\n",
        "\n",
        "    except Exception as e:\n",
        "        st.error(f\"Erro ao processar o arquivo. Certifique-se de que é um arquivo Excel válido e bem formatado. Detalhes do erro: {e}\")\n",
        "\n",
        "else:\n",
        "    st.info(\"Aguardando o upload de um arquivo Excel...\")\n",
        "\n",
        "st.markdown(\"---\")\n",
        "st.markdown(\"Desenvolvido para portfólio de Analista de Dados - @SeuNome\")"
      ],
      "metadata": {
        "id": "Ka3ivE0PjaZD"
      },
      "execution_count": null,
      "outputs": []
    }
  ]
}