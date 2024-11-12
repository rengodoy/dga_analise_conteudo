import bibtexparser
import re
import spacy
from nltk.corpus import stopwords
from nltk import download
import string

# Carregar stopwords e modelo de Spacy para inglês
download("stopwords")
stopwords_en = set(stopwords.words("english"))

# Dicionário de substituições de siglas e expressões para expressões completas e únicas
substituicoes_siglas = {
    "od": "open_data",
    "ogd": "open_government_data",
    "government open datum": "open_government_data",
    "oss": "open_source_software",
    "gdp": "gross_domestic_product",
    "eu": "european_union",
    "ai": "artificial_intelligence",
    "ict": "information_and_communication_technology",
    "iot": "internet_of_things",
    "ml": "machine_learning",
    "vgi": "volunteered_geographic_information",
    "foia": "freedom_of_information_act",
    "sdgs": "sustainable_development_goals",
    "odi": "open_data_initiative",
    "odc": "open_data_charter",
    "uav": "unmanned_aerial_vehicle",
    "ngo": "non_governmental_organization",
    "gaap": "government_as_a_platform",
    "vcc": "value_co_creation",
    "vcd": "value_co_destruction",
    "gcc": "gulf_cooperation_council",
    "auk": "australia_uk_us_alliance",
    "bh": "bahrain",
    "kw": "kuwait",
    "ksa": "kingdom_of_saudi_arabia",
    "uae": "united_arab_emirates",
    "designmethodologyapproach": "design_methodology_approach",
    "sme": "small_mediumsize_enterprise",
    "smes": "small_mediumsize_enterprise",
    "gnn": "graph_neural_networks",
    "shi": "Singapore Housing Index",
    #  " data ": " datum ",
}

# Lista de locuções para serem substituídas com underline
locucoes = [
    "public administration",
    "public sector",
    "open data",
    "data sharing",
    "covid 19",
    "public health",
    "digital health",
    "e government",
    "open government data",
    "open government",
    "data driven",
    "circular economy",
    "digital economy",
    "innovation policy",
    "artificial intelligence",
    "machine learning",
    "data privacy",
    "public management",
    "organizational culture",
    "risk management",
    "social value",
    "data ethics",
    "intellectual property",
    "sustainable development",
    "citizen engagement",
    "social participation",
    "public value",
    "data governance",
    "information technology",
    "digital transformation",
    "data security",
    "privacy concerns",
    "data protection",
    "metadata standard",
    "data infrastructure",
    "data quality",
    "economic growth",
    "social impact",
    "public policy",
    "performance measurement",
    "service quality",
    "benchmarking standards",
    "decision making",
    "organizational performance",
    "resource allocation",
    "open covid pledge",
    "transparency international",
    "sustainable development goals",
    "design methodology approach",
    "small mediumsize enterprise",
    "singapore housing index",
]


# Função para carregar e combinar dois arquivos BibTeX
def parsear_bibtex(arquivo):
    with open(arquivo, encoding="utf-8", errors="ignore") as bibtex_file1:
        bib_database = bibtexparser.load(bibtex_file1)

    return bib_database


# Função para extrair dados do banco de dados BibTeX combinado
def extrair_dados(bib_database):
    dados_extracao = []
    quantidade_exportado = 0
    for index, entry in enumerate(bib_database.entries):
        if "abstract" in entry and "author" in entry and "year" in entry:
            ano = entry["year"]
            if "author_keywords" in entry:
                keywords = entry["author_keywords"].split(";")
            elif "keywords" in entry:
                keywords = entry["keywords"].split(";")
            else:
                keywords = []
            resumo = entry["abstract"]
            resumo_limpo = resumo.split("©")[0].strip()  # Remover o texto após "©"
            dados_extracao.append([ano, resumo_limpo, keywords, index])
            quantidade_exportado += 1
    return quantidade_exportado, dados_extracao


# Função para substituir siglas por expressões completas
def substituir_siglas(resumos):
    for resumo in resumos:
        for sigla, expressao in substituicoes_siglas.items():
            # Substituir siglas ignorando maiúsculas/minúsculas
            resumo[1] = re.sub(r"\b" + re.escape(sigla) + r"\b", expressao, resumo[1], flags=re.IGNORECASE)
    return resumos


# Trata locuções substantivas para que as mesmas apareçam juntas com underline
def trata_locucoes_substantivas(resumos):
    for locucao in locucoes:
        locucao_sublinhado = locucao.lower().replace(" ", "_")
        for resumo in resumos:
            resumo[1] = resumo[1].lower().replace(locucao, locucao_sublinhado)
    return resumos


# Remover hífens e pontuação
def remover_pontuacao_e_hifen(resumos):
    for resumo in resumos:
        resumo[1] = resumo[1].replace("-", "_")
        resumo[1] = resumo[1].translate(str.maketrans("", "", string.punctuation))
        dict_pontuacao = {ord(char): " " for char in string.punctuation}
        resumo[1] = resumo[1].translate(dict_pontuacao)
    return resumos


# Remover stopwords
def remover_stopwords(resumos):
    for resumo in resumos:
        palavras = resumo[1].split()
        palavras = [palavra for palavra in palavras if palavra not in stopwords_en]
        resumo[1] = " ".join(palavras)
    return resumos


# Função para remover o possessivo de palavras
def remover_possessivo(resumos):
    for resumo in resumos:
        resumo[1] = re.sub(r"’s\b|\'s\b", "", resumo[1])
    return resumos


# Função para remover aspas do texto
def remover_aspas(resumos):
    for resumo in resumos:
        resumo[1] = re.sub(r"[\"']", "", resumo[1])
    return resumos


# Função principal para processar o texto
def processar_texto(arquivo):
    # Carregar arquivo BibTeX
    bib_database = parsear_bibtex(arquivo)
    # Extração dos dados
    quantidade_exportado, dados_extracao = extrair_dados(bib_database)

    # Aplicar transformações no texto

    resumos = remover_pontuacao_e_hifen(dados_extracao)
    resumos = remover_possessivo(resumos)
    resumos = remover_stopwords(resumos)
    resumos = trata_locucoes_substantivas(resumos)
    resumos = remover_aspas(resumos)
    resumos = substituir_siglas(resumos)

    return resumos, quantidade_exportado


# Processar texto e salvar em arquivo formatado para Iramuteq
arquivo_bibtex = "referencial_unificado.bib"

resumos, quantidade_exportado = processar_texto(arquivo_bibtex)
output_file = "iramuteq_formatado.txt"
with open(output_file, "w", encoding="utf-8-sig") as f:
    for resumo in resumos:
        cabecalho = "**** *ano_" + resumo[0] + "\n"
        f.write(cabecalho + resumo[1].replace("\n", " ") + "\n")

print(f"Foram exportados dados de {quantidade_exportado} artigos e salvos em {output_file}")
