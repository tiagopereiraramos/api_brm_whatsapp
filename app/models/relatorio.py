from dataclasses import dataclass
from typing import Optional

@dataclass
class RelatorioMensal:
    _id: Optional[str]
    empresa_id: str
    mes_ano: str
    total_enviadas: int
    total_sucesso: int
    total_erro: int