import bibtexparser
import re
import os
from unidecode import unidecode
from chardet.universaldetector import UniversalDetector
import spacy
import os, string



pares_substituicao = [
    ('ogd', 'open_government_data'),
]

# Caminho do arquivo bibtex
# arquivo_bibtex = '20240929_WoS_.bib'
arquivo_bibtex = "20240929_Scopus_pre_processado.bib"

# Função para carregar o arquivo BibTeX e extrair os dados necessários
def extrair_dados(bibtex_file):
    with open(bibtex_file, encoding="utf-8", errors="ignore") as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file)
    dados_extracao = []
    quantidade_exportado = 0
    for entry in bib_database.entries:
        if "abstract" in entry and "author" in entry and "year" in entry:
            ano = entry["year"]
            resumo = entry["abstract"]
            # Remover o texto após o símbolo ©
            resumo_limpo = resumo.split('©')[0].strip()
            # Formatação para o Iramuteq
            dados_extracao.append([ano,resumo_limpo])
            quantidade_exportado += 1
    return quantidade_exportado, dados_extracao

# Trata locuções substantivas para que as mesmas apareceçam juntas por underline
def trata_locusoes_substantivas(resumos):
    # Aqui, você deve listar todas as locuções substantivas que deseja tratar.
    locucoes = [
        'public administration',
        'public sector',
        'open data',
        'data sharing',
        'covid 19',
        'public health',
        'digital health',
        'e government',
        'open government data',
        'open government',
        'data driven',
        'circular economy',
        'digital economy',
        'innovation policy',
        'artificial intelligence',
        'machine learning',
        'data privacy',
        'public management',
        'organizational culture',
        'risk management',
        'social value',
        'data ethics',
        'intellectual property',
        'sustainable development',
        'citizen engagement',
        'social participation',
        'public value',
        'data governance',
        'information technology',
        'digital transformation',
        'data security',
        'privacy concerns',
        'data protection',
        'metadata standard',
        'data infrastructure',
        'data quality',
        'economic growth',
        'social impact',
        'public policy',
        'performance measurement',
        'service quality',
        'benchmarking standards',
        'decision making',
        'organizational performance',
        'resource allocation',
        'open covid pledge',
        'transparency international',
        'sustainable development goals'
    ]

    for locucao in locucoes:
        # Converte a locução para minúsculas e substitui espaços por sublinhados
        locucao_sublinhado = locucao.lower().replace(' ', '_')
        for resumo in resumos:
            resumo[1] = resumo[1].lower().replace(locucao.lower(), locucao_sublinhado)
    return resumos

# Substitui os hífens em palavras compostas por underline (_)
def substitui_hifen(resumos):
    for resumo in resumos:
        resumo[1] = resumo[1].replace('-', '_')
    return resumos

# Remove os caracteres especificados
def remove_caracteres(resumos):
    caracteres = ['"', "'", '-', '$', '%', '...', '`', "“", "”", "–"]
    for caractere in caracteres:
        for resumo in resumos:
            resumo[1] = resumo[1].replace(caractere, '')
    return resumos

# Remove expressões
def remove_expressoes(resumos):
    expressoes = ['et al', 'cols']
    for expressao in expressoes:
        for resumo in resumos:
            resumo[1] = re.sub(r'\b' + expressao + r'\b', '', resumo[1], flags=re.IGNORECASE)
    return resumos


def processar_texto(arquivo_bibtex):
    # Extração dos dados
    quantidade_exportado, dados_extracao = extrair_dados(arquivo_bibtex)
    resumos = trata_locusoes_substantivas(dados_extracao)
    resumos = substitui_hifen(resumos)
    resumos = remove_expressoes(resumos)
    resumos = remove_caracteres(resumos)
    resumos = trata_locusoes_substantivas(resumos)
    return resumos, quantidade_exportado


# processando texto
resumos, quantidade_exportado = processar_texto(arquivo_bibtex=arquivo_bibtex)

# Salvando os resultados no formato necessário para o Iramuteq
output_file = 'iramuteq_formatado.txt'
with open(output_file, 'a',  encoding='utf-8-sig') as f:
    for resumo in resumos:
        f.write('**** *ano_'+ resumo[0] + '\n' + resumo[1].replace('\n', ' ') + '\n')
    

print(f"Foram exportados Dados de {quantidade_exportado} artigos e salvos em {output_file}")
