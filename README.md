# Processamento de Referências para IRaMuTeQ

Este repositório contém dois scripts Python que realizam o processamento de arquivos BibTeX extraídos de bases de dados científicas, como **Web of Science** e **Scopus**, com o objetivo de gerar um arquivo formatado compatível com o **IRaMuTeQ**. 

## Descrição Geral

Os scripts têm as seguintes funções principais:

1. **Mesclar arquivos BibTeX**: Unifica os arquivos BibTeX de diferentes bases de dados em um único arquivo, removendo duplicatas.
2. **Formatar dados para IRaMuTeQ**: Processa o arquivo unificado e extrai resumos, palavras-chave e outros campos relevantes, formatando o conteúdo para uso no IRaMuTeQ.

## Requisitos

- Python 3.12.7
- Para instalar as bibliotecas pode ser usado `requirements.txt` ou o UV
```bash
uv sync

# Ou

pip install -r requirements.txt
```


## Scripts Disponíveis

### 1. **`mesclar_bib.py`**
Este script unifica arquivos BibTeX provenientes de diferentes bases de dados, removendo duplicatas. Ele utiliza o DOI como identificador principal e, caso não haja DOI, combina título e autores para identificar duplicatas.

#### Funcionalidades:
- **Unificação de arquivos BibTeX:** Junta arquivos `wos.bib` (Web of Science) e `scopus.bib` (Scopus) em um único arquivo `referencial_unificado.bib`.
- **Identificação de duplicatas:**
  - Referências com DOI são priorizadas.
  - Em caso de ausência de DOI, a combinação de título e autores é utilizada.
- **Prioridade de fontes:** Dá preferência a entradas do primeiro arquivo em caso de conflito.

#### Como usar:
1. Substitua os nomes dos arquivos `file1` e `file2` pelos caminhos reais dos arquivos BibTeX.
2. Execute o script:
   ```bash
   python mesclar_bib.py `file1` `file2`
   ````

3. O arquivo referencial_unificado.bib será gerado com estatísticas sobre as referências processadas.
#### Saída:
 - Arquivo BibTeX unificado (`referencial_unificado.bib`).
 - Estatísticas:
    - Total de referências únicas.
    - Número de referências identificadas por DOI.
    - Número de referências identificadas por título/autores.

### 2. **`extrair_resumos_iramuteq.py`**
Este script processa o arquivo BibTeX unificado para gerar um arquivo de texto formatado, compatível com o **IRaMuTeQ**.

#### Funcionalidades:
- **Extração de resumos:** Seleciona referências contendo resumo, autor e ano.
- **Normalização de texto:**
  - Substituição de siglas por expressões completas.
  - Transformação de locuções em palavras compostas com underscores (_).
  - Remoção de pontuação, hífens, possessivos e stopwords.
  - Conversão para caixa baixa (lowercase).
- **Formatação para IRaMuTeQ:** Gera um arquivo `.txt` estruturado para análise textual.

#### Como usar:
1. Certifique-se de que o arquivo `referencial_unificado.bib` gerado pelo script anterior está no mesmo diretório.
2. Execute o script:
   ```bash
   python extrair_resumos_iramuteq.py
   ```
3. O arquivo `iramuteq_formatado.txt` será gerado.

#### Saída:
- Arquivo `.txt` pronto para importação no IRaMuTeQ (`iramuteq_formatado.txt`).
- Estatísticas sobre o número de resumos processados.

---

## Exemplo de Fluxo de Trabalho

1. Extraia arquivos completos, com todas as referências e opções, em BibTeX de **Web of Science** e **Scopus**.
2. Use o script `mesclar_bib.py` para unificar os arquivos e remover duplicatas.
3. Execute o script `extrair_resumos_iramuteq.py` para preparar os dados para o IRaMuTeQ.
4. Importe o arquivo `iramuteq_formatado.txt` no IRaMuTeQ para realizar a análise textual.
