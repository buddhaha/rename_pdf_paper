import re
import os
import argparse




# Parse command line arguments
parser = argparse.ArgumentParser(description='Rename a downloaded PDF file based on a BibTeX entry.')
parser.add_argument('pdf_file', metavar='PDF_FILE', help='the PDF file to be renamed')
parser.add_argument('bibtex_file', metavar='BIBTEX_FILE', help='the BibTeX file containing the entry for the PDF')
parser.add_argument("dir", nargs='?', const="biblio")
args = parser.parse_args()



print(f"arguments pdf: {args.pdf_file}")
print(f"arguments bib: {args.bibtex_file}")

if args.dir:
    biblio_dir = args.dir
else:
    biblio_dir = 'biblio'

print(f"arguments dir: {biblio_dir}")

if not os.path.exists(args.pdf_file):
    print(f"pdf file {pdf_file} does not exists")

if not os.path.exists(args.bibtex_file):
    print(f"pdf file {bibtex_file} does not exists")

# Check if the directory exists
if not os.path.exists(biblio_dir):
    os.makedirs(biblio_dir)

def rename_file(pdf_path: str, bibtex_path: str, biblio_dir: str) -> None:
    with open(bibtex_path, 'r') as f:
        bibtex_str = f.read()
    parsed_string = get_filename_from_bibtex(bibtex_str)
    save_destination = os.path.join(biblio_dir, parsed_string)
    os.rename(pdf_path, save_destination)
    return None

def get_filename_from_bibtex(bibtex_citation: str) -> str:
    # Extract the year, author, and title from the BibTeX citation
    year_match = re.search(r'year\s*=\s*{(\d+)}', bibtex_citation)
    author_match = re.search(r'author\s*=\s*{([^{}]+)}', bibtex_citation)
    title_match = re.search(r'title\s*=\s*{(.+?)}', bibtex_citation, re.DOTALL)

    if not year_match or not author_match or not title_match:
        return None

    year = year_match.group(1)
    author = author_match.group(1)
    title = title_match.group(1)

    # Clean up the author and title strings
    author = re.sub(r'[^\w\s-]', '', author)
    author = re.sub(r'\s+', '_', author)
    title = re.sub(r'[^\w\s-]', '', title)
    title = re.sub(r'\s+', '_', title)
    print(f"author: {author}")
    print(f"title: {title}")
    print(f"year: {year}")

    # Combine the year, author, and title into a filename string
    filename = f"{year}_{author}_{title}.pdf"
    return filename


rename_file(args.pdf_file, args.bibtex_file, biblio_dir)