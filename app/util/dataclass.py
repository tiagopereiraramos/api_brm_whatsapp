from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional, Dict

# Enum para status da empresa
class StatusEmpresa(str, Enum):
    ATIVO = "ativo"
    INATIVO = "inativo"

@dataclass
class Empresa:
    _id: Optional[str]
    nome: str
    status: StatusEmpresa
    hash_autenticacao: str
    valor_mensalidade: float
    data_inicio_contrato: datetime  # Nova coluna: quando o contrato começou
    data_fim_contrato: Optional[datetime] = None  # Nova coluna: quando o contrato termina (se aplicável)
    ciclo_pagamento: Optional[str] = "mensal"  # Exemplo: "mensal", "anual", etc.
    observacoes: Optional[str] = None  

# Enum para status de envio de mensagem
class StatusEnvio(str, Enum):
    SUCESSO = "sucesso"
    ERRO = "erro"
    PENDENTE = "pendente"

# Dataclass para Mensagem
@dataclass
class Mensagem:
    _id: Optional[str]
    empresa_id: str
    numero_destino: str
    template: str
    payload: Dict[str, str]
    status_envio: StatusEnvio
    tentativas: int
    data_envio: Optional[datetime] = None

# Enum para tipo de WhatsApp
class TipoWhatsapp(str, Enum):
    OFICIAL = "oficial"
    EVOLUTION = "evolution"

# Dataclass para Configuração de WhatsApp
@dataclass
class ConfiguracaoWhatsapp:
    _id: Optional[str]
    empresa_id: str
    tipo: TipoWhatsapp
    token: str
    remetente_padrao: str

# Dataclass para Relatório Mensal
@dataclass
class RelatorioMensal:
    _id: Optional[str]
    empresa_id: str
    mes_ano: str
    total_enviadas: int
    total_sucesso: int
    total_erro: int
    
@dataclass
class TemplateCobranca:
    nome_aluno: str  # Nome do aluno para quem se refere a cobrança
    serie: str  # Série ou turma do aluno
    nome_resp_financeiro: str  # Nome do responsável financeiro
    num_resp_financ: str  # Número de WhatsApp do responsável financeiro (com DDI)
    boleto_base_64: Optional[str] = None  # Boleto em formato Base64 (opcional)
    boleto_link: Optional[str] = None  # Link para download do boleto (opcional)
    mes_ano_cobranca: str  # Mês e ano da cobrança (ex: "2025-04")
    numero_boleto: str  # Número identificador do boleto
    texto_envio: Optional[str] = None  # Texto personalizado para envio

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