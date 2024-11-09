import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.bwriter import BibTexWriter

def merge_bibtex_files(file1_path, file2_path, output_path):
    """
    Unifica dois arquivos BibTeX removendo entradas duplicadas.
    Usa DOI como identificador principal, e título+autores como backup.
    
    Args:
        file1_path (str): Caminho para o primeiro arquivo BibTeX
        file2_path (str): Caminho para o segundo arquivo BibTeX
        output_path (str): Caminho para salvar o arquivo unificado
    """
    # Configurar o parser para preservar formatação
    parser = BibTexParser()
    parser.ignore_nonstandard_types = False
    parser.expect_multiple_parse = True
    
    # Ler o primeiro arquivo
    with open(file1_path, 'r', encoding='utf-8') as file1:
        bib1 = bibtexparser.load(file1, parser=parser)
    
    # Ler o segundo arquivo
    with open(file2_path, 'r', encoding='utf-8') as file2:
        bib2 = bibtexparser.load(file2, parser=parser)
    
    # Criar dicionários para armazenar entradas únicas
    entries_by_doi = {}      # Entradas com DOI
    entries_by_content = {}  # Entradas sem DOI
    
    def normalize_doi(doi):
        """Normaliza o DOI removendo espaços e convertendo para minúsculas."""
        if doi:
            return doi.lower().strip()
        return None
    
    def get_content_key(entry):
        """Gera uma chave de comparação baseada no título e autores."""
        title = entry.get('title', '').lower().strip()
        authors = entry.get('author', '').lower().strip()
        return f"{title}|{authors}"
    
    def process_entry(entry, is_from_first_file=True):
        """
        Processa uma entrada BibTeX e a adiciona ao dicionário apropriado.
        Prioriza entradas do primeiro arquivo em caso de duplicatas.
        """
        doi = normalize_doi(entry.get('doi'))
        
        if doi:
            if doi not in entries_by_doi or is_from_first_file:
                entries_by_doi[doi] = entry
        else:
            # Se não tem DOI, usa título e autores
            content_key = get_content_key(entry)
            if content_key not in entries_by_content or is_from_first_file:
                entries_by_content[content_key] = entry
    
    # Processar entradas do primeiro arquivo (tem prioridade)
    for entry in bib1.entries:
        process_entry(entry, True)
    
    # Processar entradas do segundo arquivo
    for entry in bib2.entries:
        process_entry(entry, False)
    
    # Unir todas as entradas únicas
    merged_entries = list(entries_by_doi.values()) + list(entries_by_content.values())
    
    # Criar nova base de dados BibTeX com entradas únicas
    merged_db = bibtexparser.bibdatabase.BibDatabase()
    merged_db.entries = merged_entries
    
    # Configurar o writer para manter a formatação adequada
    writer = BibTexWriter()
    writer.indent = '    '
    writer.order_entries_by = None
    
    # Salvar o arquivo unificado
    with open(output_path, 'w', encoding='utf-8') as output_file:
        output_file.write(writer.write(merged_db))
    
    # Retornar estatísticas
    return {
        'total_entries': len(merged_entries),
        'entries_with_doi': len(entries_by_doi),
        'entries_without_doi': len(entries_by_content)
    }

# Exemplo de uso
if __name__ == "__main__":
    # Substituir com os caminhos reais dos arquivos
    file1 = "wos.bib"
    file2 = "scopus.bib"
    output = "referencial_unificado.bib"
    
    stats = merge_bibtex_files(file1, file2, output)
    print(f"Arquivo unificado criado com {stats['total_entries']} referências únicas:")
    print(f"- {stats['entries_with_doi']} referências identificadas por DOI")
    print(f"- {stats['entries_without_doi']} referências identificadas por título/autores")