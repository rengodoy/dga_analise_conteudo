import bibtexparser
from bibtexparser.bparser import BibTexParser
from collections import defaultdict

def check_missing_doi(bib_file_path):
    """
    Analisa um arquivo BibTeX e identifica entradas sem DOI.
    
    Args:
        bib_file_path (str): Caminho para o arquivo BibTeX
    
    Returns:
        dict: Estatísticas e informações sobre as entradas sem DOI
    """
    # Configurar o parser
    parser = BibTexParser()
    parser.ignore_nonstandard_types = False
    parser.expect_multiple_parse = True
    
    # Ler o arquivo BibTeX
    with open(bib_file_path, 'r', encoding='utf-8') as bibfile:
        bib_database = bibtexparser.load(bibfile, parser=parser)
    
    # Inicializar contadores e listas
    entries_without_doi = []
    entries_with_doi = []
    entry_types = defaultdict(int)
    entries_without_doi_by_type = defaultdict(list)
    
    # Analisar cada entrada
    for entry in bib_database.entries:
        entry_type = entry.get('ENTRYTYPE', 'unknown')
        entry_types[entry_type] += 1
        
        # Verificar se tem DOI
        doi = entry.get('doi', '').strip()
        
        if not doi:
            # Coletar informações da entrada sem DOI
            entry_info = {
                'title': entry.get('title', 'No title'),
                'author': entry.get('author', 'No author'),
                'year': entry.get('year', 'No year'),
                'key': entry.get('ID', 'No key')
            }
            entries_without_doi.append(entry_info)
            entries_without_doi_by_type[entry_type].append(entry_info)
        else:
            entries_with_doi.append(entry)
    
    # Preparar estatísticas
    stats = {
        'total_entries': len(bib_database.entries),
        'entries_with_doi': len(entries_with_doi),
        'entries_without_doi': len(entries_without_doi),
        'entry_types': dict(entry_types),
        'entries_without_doi_by_type': dict(entries_without_doi_by_type)
    }
    
    # Imprimir relatório
    print("\n=== Relatório de Análise do Arquivo BibTeX ===")
    print(f"\nArquivo analisado: {bib_file_path}")
    print(f"Total de entradas: {stats['total_entries']}")
    print(f"Entradas com DOI: {stats['entries_with_doi']}")
    print(f"Entradas sem DOI: {stats['entries_without_doi']}")
    
    print("\nDistribuição por tipo de entrada:")
    for entry_type, count in stats['entry_types'].items():
        missing_count = len(entries_without_doi_by_type.get(entry_type, []))
        print(f"- {entry_type}: {count} total, {missing_count} sem DOI")
    
    if entries_without_doi:
        print("\nDetalhes das entradas sem DOI:")
        for entry_type, entries in entries_without_doi_by_type.items():
            print(f"\n{entry_type.upper()}:")
            for entry in entries:
                print(f"- {entry['title'][:70]}...")
                print(f"  Autores: {entry['author'][:70]}...")
                print(f"  Ano: {entry['year']}")
                print(f"  Chave: {entry['key']}")
    
    return stats

# Exemplo de uso
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        print("Uso: python check_missing_doi.py arquivo.bib")
        sys.exit(1)
    
    bib_file = sys.argv[1]
    try:
        stats = check_missing_doi(bib_file)
    except Exception as e:
        print(f"Erro ao processar o arquivo: {e}")
        sys.exit(1)