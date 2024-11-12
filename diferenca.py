import sys
import argparse
from typing import Dict, Set, Tuple, Optional
from difflib import SequenceMatcher
import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import convert_to_unicode
from tabulate import tabulate
class BibEntry:
    def __init__(self, entry_dict: Dict):
        self.entry_dict = entry_dict
        self.key = entry_dict.get('ID', '')
        self._doi = self._normalize_field('doi')
        self._title = self._normalize_field('title')
        self._authors = self._parse_authors(entry_dict.get('author', ''))
        
    def _normalize_field(self, field: str) -> Optional[str]:
        """Normaliza um campo do BibTeX removendo chaves, espaços extras e convertendo para minúsculas."""
        if field in self.entry_dict:
            value = self.entry_dict[field]
            # Remove chaves e normaliza espaços
            value = value.replace('{', '').replace('}', '')
            value = ' '.join(value.split())
            return value.lower()
        return None
    
    def _parse_authors(self, authors_str: str) -> Set[str]:
        """Converte a string de autores em um conjunto de nomes normalizados."""
        if not authors_str:
            return set()
            
        # Remove chaves e divide por 'and'
        authors = authors_str.replace('{', '').replace('}', '').split(' and ')
        
        # Normaliza cada nome de autor
        normalized_authors = set()
        for author in authors:
            # Remove espaços extras e converte para minúsculas
            author = ' '.join(author.split())
            # Pega apenas o último sobrenome se houver vírgula
            if ',' in author:
                author = author.split(',')[0]
            normalized_authors.add(author.lower())
            
        return normalized_authors

    def is_similar_to(self, other: 'BibEntry', title_threshold: float = 0.85) -> bool:
        """
        Verifica se duas entradas são similares, usando DOI ou título/autores.
        
        Args:
            other: Outra entrada BibTeX para comparação
            title_threshold: Limiar de similaridade para títulos (0 a 1)
        """
        # Primeiro, tenta comparar por DOI
        if self._doi and other._doi:
            return self._doi == other._doi
        
        # Se não tem DOI, verifica título
        if self._title and other._title:
            title_similarity = SequenceMatcher(None, self._title, other._title).ratio()
            
            # Se os títulos são muito similares, verifica os autores
            if title_similarity >= title_threshold:
                # Se alguma entrada não tem autores, considera apenas a similaridade do título
                if not self._authors or not other._authors:
                    return True
                
                # Verifica se há autores em comum
                common_authors = self._authors.intersection(other._authors)
                return len(common_authors) > 0
                
        return False

    def __str__(self) -> str:
        """Retorna uma representação string formatada da entrada."""
        output = []
        output.append(f"Citation key: {self.key}")
        output.append(f"DOI: {self._doi or 'Não disponível'}")
        output.append(f"Título: {self._title or 'Não disponível'}")
        output.append(f"Autores: {', '.join(sorted(self._authors)) if self._authors else 'Não disponível'}")
        output.append("-" * 40)
        
        # Adiciona todos os campos originais
        for field, value in sorted(self.entry_dict.items()):
            if field != 'ID':  # ID já foi mostrado como Citation key
                output.append(f"{field}: {value}")
                
        return '\n'.join(output)

def parse_bib_file(file_path: str) -> Dict[str, BibEntry]:
    """
    Parse um arquivo BIB usando bibtexparser e retorna um dicionário de BibEntries.
    
    Args:
        file_path (str): Caminho para o arquivo .bib
        
    Returns:
        Dict[str, BibEntry]: Dicionário com chave sendo a citation key e valor sendo o objeto BibEntry
    """
    # Configura o parser
    parser = BibTexParser()
    parser.customization = convert_to_unicode
    
    # Lê e parse o arquivo
    with open(file_path, 'r', encoding='utf-8') as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file, parser=parser)
    
    # Converte as entradas em objetos BibEntry
    entries = {}
    for entry in bib_database.entries:
        bib_entry = BibEntry(entry)
        entries[bib_entry.key] = bib_entry
    
    return entries

def find_unique_entries(entries1: Dict[str, BibEntry], 
                       entries2: Dict[str, BibEntry], 
                       title_threshold: float) -> Tuple[Dict[str, BibEntry], Dict[str, BibEntry]]:
    """
    Encontra entradas únicas em cada arquivo, considerando DOI e similaridade de título/autores.
    """
    unique_to_file1 = {}
    unique_to_file2 = {}
    
    # Verifica entradas do arquivo 1
    for key1, entry1 in entries1.items():
        found_similar = False
        for entry2 in entries2.values():
            if entry1.is_similar_to(entry2, title_threshold):
                found_similar = True
                break
        if not found_similar:
            unique_to_file1[key1] = entry1
    
    # Verifica entradas do arquivo 2
    for key2, entry2 in entries2.items():
        found_similar = False
        for entry1 in entries1.values():
            if entry2.is_similar_to(entry1, title_threshold):
                found_similar = True
                break
        if not found_similar:
            unique_to_file2[key2] = entry2
    
    return unique_to_file1, unique_to_file2

def print_summary(unique_to_file1: Dict[str, BibEntry], 
                 unique_to_file2: Dict[str, BibEntry],
                 file1_name: str,
                 file2_name: str):
    """
    Imprime um resumo estatístico das diferenças encontradas.
    """
    print("\n" + "="*100)
    print("RESUMO DAS DIFERENÇAS")
    print("="*100)
    
    # Estatísticas gerais
    print(f"\nTotal de entradas únicas encontradas: {len(unique_to_file1) + len(unique_to_file2)}")
    print(f"- Em {file1_name}: {len(unique_to_file1)} entradas")
    print(f"- Em {file2_name}: {len(unique_to_file2)} entradas")
    
    # Prepara dados para tabelas
    def prepare_table_data(entries: Dict[str, BibEntry]) -> list:
        return [[
            entry.key,
            entry._title or "N/A",
            entry._doi or "N/A"
        ] for entry in entries.values()]
    
    # Imprime tabela para arquivo 1
    if unique_to_file1:
        print(f"\nEntradas únicas em {file1_name}:")
        headers = ["Citation Key", "Título", "DOI"]
        table_data = prepare_table_data(unique_to_file1)
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
        
        # Conta entradas sem DOI
        entries_without_doi = sum(1 for entry in unique_to_file1.values() if not entry._doi)
        print(f"\nEntradas sem DOI: {entries_without_doi}")
    
    # Imprime tabela para arquivo 2
    if unique_to_file2:
        print(f"\nEntradas únicas em {file2_name}:")
        headers = ["Citation Key", "Título", "DOI"]
        table_data = prepare_table_data(unique_to_file2)
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
        
        # Conta entradas sem DOI
        entries_without_doi = sum(1 for entry in unique_to_file2.values() if not entry._doi)
        print(f"\nEntradas sem DOI: {entries_without_doi}")

def main():
    # Configuração do parser de argumentos
    parser = argparse.ArgumentParser(
        description='Compara dois arquivos BibTeX usando DOI ou título/autores.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  %(prog)s arquivo1.bib arquivo2.bib
  %(prog)s --title-threshold 0.90 arquivo1.bib arquivo2.bib
  %(prog)s --brief arquivo1.bib arquivo2.bib
        """
    )
    parser.add_argument('file1', help='Primeiro arquivo BibTeX')
    parser.add_argument('file2', help='Segundo arquivo BibTeX')
    parser.add_argument('--title-threshold', type=float, default=0.85,
                       help='Limiar de similaridade para títulos (0 a 1, padrão: 0.85)')
    parser.add_argument('--brief', action='store_true',
                       help='Mostra apenas o resumo das diferenças')
    
    args = parser.parse_args()
    
    try:
        # Parse os arquivos
        entries1 = parse_bib_file(args.file1)
        entries2 = parse_bib_file(args.file2)
        
        # Encontra as diferenças
        unique_to_file1, unique_to_file2 = find_unique_entries(
            entries1, entries2, args.title_threshold
        )
        
        # Se não for modo resumido, mostra detalhes completos
        if not args.brief:
            print(f"\nEntradas exclusivas em {args.file1} ({len(unique_to_file1)} entradas):")
            print("="*80)
            for key, entry in sorted(unique_to_file1.items()):
                print(f"\n{entry}\n")
            
            print(f"\nEntradas exclusivas em {args.file2} ({len(unique_to_file2)} entradas):")
            print("="*80)
            for key, entry in sorted(unique_to_file2.items()):
                print(f"\n{entry}\n")
        
        # Imprime o resumo estatístico
        print_summary(unique_to_file1, unique_to_file2, args.file1, args.file2)
            
    except FileNotFoundError as e:
        print(f"Erro: Arquivo não encontrado - {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"Erro inesperado: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()