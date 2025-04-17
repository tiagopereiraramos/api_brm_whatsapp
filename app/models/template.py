from dataclasses import dataclass
from typing import Optional

@dataclass
class TemplateCobranca:
    nome_aluno: str
    serie: str
    nome_resp_financeiro: str
    num_resp_financ: str
    boleto_base_64: Optional[str] = None
    boleto_link: Optional[str] = None
    mes_ano_cobranca: str
    numero_boleto: str
    texto_envio: Optional[str] = None

    def gerar_texto_envio(self) -> str:
        """
        Gera automaticamente o texto da mensagem de cobrança usando os campos do template.
        """
        return (
            f"Olá {self.nome_resp_financeiro},\n\n"
            f"Segue a cobrança referente ao aluno {self.nome_aluno}, série {self.serie}.\n"
            f"Mês de referência: {self.mes_ano_cobranca}.\n"
            f"Número do boleto: {self.numero_boleto}.\n\n"
            f"Você pode acessar o boleto pelo link: {self.boleto_link}\n\n"
            f"Qualquer dúvida, estamos à disposição.\n\n"
            f"Atenciosamente,\nEquipe Financeira."
        )