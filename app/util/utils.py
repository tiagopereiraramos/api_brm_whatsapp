from datetime import datetime
import hashlib


def generate_hash_token_empresa(nome: str, cnpj: str) -> str:
    """
    Gera um hash token para autenticação da empresa.
    O hash é gerado a partir do nome da empresa, CNPJ e um timestamp atual.
    O hash é gerado usando SHA-256 e truncado para 20 caracteres.
    :param nome: Nome da empresa
    :param cnpj: CNPJ da empresa
    :return: Hash token gerado
    """
    if not nome or not cnpj:
        raise ValueError(
            "Nome e CNPJ são obrigatórios para gerar o hash token.")
    else:
        # Gera o hash token
        # usando SHA-256 e truncando para 20 caracteres
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        palavra_passe = 'brmsolutions'
        return hashlib.sha256(f"{palavra_passe}-{nome}-{cnpj}-{timestamp}".encode()).hexdigest()[
            :20
        ]
