from web_scrapper import reactome_scrapper as rs
from portia_utils import file_handler as fh
from portia_utils import util as u
from typing import List


def fetch_entrez_id(gene_id: str):
    return rs.get_entrez_id(gene_id)


def fetch_entrez_id_from_list(gene_id_list: List[str]) -> List[str]:

    entrez_ids: List[str] = []

    for gene_id in gene_id_list:
        entrez_ids.append(fetch_entrez_id(gene_id))

    return entrez_ids


def fetch_entrez_id_from_file(complete_file_path: str):

    gene_id_list: List[str] = fh.readfile(complete_file_path, True)
    entrez_id_list: List[str] = fetch_entrez_id_from_list(gene_id_list)

    return entrez_id_list


def fetch_entrez_id_to_file(complete_read_file_path: str, complete_write_file_path: str):

    entrez_id_list: List[str] = fetch_entrez_id_from_file(complete_read_file_path)
    fh.writefile(
        complete_write_file_path,
        u.convert_list_string(
            entrez_id_list,
            '\n'
        )
    )


def fetch_entrez_id_from_list_to_file(gene_id_list: List[str], complete_write_file_path: str):

    entrez_ids: List[str] = fetch_entrez_id_from_list(gene_id_list)
    fh.writefile(
        complete_write_file_path,
        u.convert_list_string(
            entrez_ids,
            '\n'
        )
    )

