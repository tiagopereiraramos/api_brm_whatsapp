import requests

class EvolutionService:
    def __init__(self, base_url: str, apikey: str, instance: str):
        self.base_url = base_url.rstrip("/")
        self.apikey = apikey
        self.instance = instance
        self.headers = {
            "Content-Type": "application/json",
            "apikey": self.apikey
        }

    def send_text_message(self, number: str, text: str, delay: int = 1000) -> dict:
        """
        Envia uma mensagem de texto simples via Evolution API.

        :param number: Número do destinatário (formato: '5567999087301').
        :param text: Texto da mensagem a ser enviada.
        :param delay: Atraso (em milissegundos) para o envio da mensagem.
        :return: Resposta da API.
        """
        url = f"{self.base_url}/message/sendText/{self.instance}"

        payload = {
            "number": number,
            "text": text,
            "delay": delay
        }

        response = requests.post(url, json=payload, headers=self.headers)

        try:
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e), "response": response.text}