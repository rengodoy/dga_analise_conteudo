# BibTeX References Merger

Uma ferramenta Python para unificar arquivos BibTeX, removendo duplicatas de forma inteligente usando DOI como identificador principal e título+autores como fallback.

## Funcionalidades

- Unifica dois arquivos BibTeX em um único arquivo
- Remove entradas duplicadas usando:
  - DOI como identificador principal (normalizado)
  - Combinação de título e autores como identificador secundário
- Preserva a formatação original dos arquivos
- Prioriza entradas do primeiro arquivo em caso de conflitos
- Gera estatísticas sobre o processo de unificação

## Requisitos

- Python 3.12.7 ou superior
- UV 0.5.1 ou superior (opcional, para gerenciamento de dependências)

### Dependências Python

```txt
bibtexparser>=1.4.0
```

## Instalação

1. Clone este repositório ou baixe o script:

```bash
git clone https://seu-repositorio/bibtex-merger.git
cd bibtex-merger
```

2. Crie e ative um ambiente virtual (opcional, mas recomendado):

```bash
# Usando Python venv
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
.\venv\Scripts\activate   # Windows

# OU usando UV
uv venv
```

3. Instale as dependências:

```bash
# Usando pip
pip install -r requirements.txt

# OU usando UV
uv pip install -r requirements.txt
```

## Uso

### Como Módulo

```python
from bibtex_merger import merge_bibtex_files

# Caminhos dos arquivos
arquivo1 = "wos_pre_processado.bib"
arquivo2 = "scopus_pre_processado.bib"
saida = "referencias_unificadas.bib"

# Unificar arquivos
stats = merge_bibtex_files(arquivo1, arquivo2, saida)

# Imprimir estatísticas
print(f"Arquivo unificado criado com {stats['total_entries']} referências únicas:")
print(f"- {stats['entries_with_doi']} referências identificadas por DOI")
print(f"- {stats['entries_without_doi']} referências identificadas por título/autores")
```

### Como Script

Execute diretamente o script modificando as variáveis `file1`, `file2` e `output` no bloco `if __name__ == "__main__":`:

```bash
python bibtex_merger.py
```

## Detalhes de Implementação

O script utiliza duas estratégias para identificar e remover duplicatas:

1. **DOI**: Principal método de identificação. Os DOIs são normalizados (convertidos para minúsculas e espaços removidos) antes da comparação.
2. **Título + Autores**: Método secundário usado quando o DOI não está disponível. Uma chave de comparação é gerada combinando o título e autores normalizados.

Em caso de duplicatas:

- Se uma entrada existir em ambos os arquivos, a versão do primeiro arquivo é mantida
- Entradas únicas de ambos os arquivos são preservadas

## Formato de Saída

O script gera um arquivo BibTeX unificado com:

- Entradas únicas mantendo a formatação original
- Indentação consistente (4 espaços)
- Ordem de entradas preservada

## Contribuição

Sinta-se à vontade para abrir issues ou enviar pull requests com melhorias.

## Licença

[Sua licença aqui]
