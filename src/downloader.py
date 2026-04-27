"""
Módulo responsável por baixar e converter o Google Docs em PDF.
"""

import requests
from config import DOWNLOAD_TIMEOUT

def extrair_titulo_doc(doc_id: str, api_key: str = "") -> str:
    """
    Extrai o título do Google Doc e usa IA para identificar apenas o nome da empresa.
    """
    import re
    url = f"https://docs.google.com/document/d/{doc_id}/mobilebasic"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            match = re.search(r"<title>(.*?)</title>", response.text)
            if match:
                titulo_completo = match.group(1).strip()
                titulo_completo = re.sub(r"\s*[-–]\s*Google Docs.*$", "", titulo_completo).strip()

                # Usa IA para extrair apenas o nome da empresa
                if api_key and titulo_completo:
                    from openai import OpenAI
                    client = OpenAI(api_key=api_key)
                    resp = client.chat.completions.create(
                        model="gpt-4o",
                        max_tokens=50,
                        messages=[
                            {
                                "role": "system",
                                "content": (
                                    "Você extrai apenas o nome da empresa de um título de documento. "
                                    "O nome da empresa geralmente é o primeiro termo do título, antes de colchetes, traços ou descrições. "
                                    "Retorne APENAS o nome da empresa, sem explicações, sem pontuação extra."
                                )
                            },
                            {
                                "role": "user",
                                "content": f"Título do documento: {titulo_completo}\n\nQual é o nome da empresa?"
                            }
                        ],
                    )
                    return resp.choices[0].message.content.strip()

                return titulo_completo
    except Exception:
        pass

    return ""

def extrair_url_exportacao(url: str) -> str:
    """
    Converte qualquer variação de URL do Google Docs para a URL de exportação em PDF.
    """
    url = url.strip()

    if "docs.google.com/document/d/" not in url:
        raise ValueError(
            "URL inválida. Certifique-se de que é um link do Google Docs.\n"
            "   Formato esperado: https://docs.google.com/document/d/SEU_ID/edit"
        )

    partes = url.split("/document/d/")
    doc_id = partes[1].split("/")[0].split("?")[0].split("#")[0]

    if not doc_id:
        raise ValueError("Não foi possível extrair o ID do documento da URL fornecida.")

    return f"https://docs.google.com/document/d/{doc_id}/export?format=pdf"


def baixar_pdf(export_url: str) -> bytes:
    """
    Faz o download do PDF a partir da URL de exportação do Google Docs.
    Retorna os bytes do PDF.
    """
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }

    try:
        response = requests.get(
            export_url,
            headers=headers,
            timeout=DOWNLOAD_TIMEOUT,
            allow_redirects=True,
        )
    except requests.exceptions.Timeout:
        raise TimeoutError(
            f"O download excedeu o tempo limite de {DOWNLOAD_TIMEOUT}s. "
            "Verifique sua conexão e tente novamente."
        )
    except requests.exceptions.ConnectionError:
        raise ConnectionError(
            "Não foi possível conectar ao Google Docs. "
            "Verifique sua conexão com a internet."
        )

    if response.status_code == 403:
        raise PermissionError(
            "Acesso negado ao documento (HTTP 403).\n"
            "   Verifique se o link está configurado como público: "
            "Compartilhar → Qualquer pessoa com o link → Leitor."
        )
    elif response.status_code == 404:
        raise FileNotFoundError(
            "Documento não encontrado (HTTP 404). Verifique se o link está correto."
        )
    elif response.status_code != 200:
        raise ConnectionError(
            f"Erro ao baixar o documento. Código HTTP: {response.status_code}"
        )

    if len(response.content) < 500:
        raise ValueError(
            "O documento retornado parece inválido ou vazio. "
            "Verifique se o link é público e está correto."
        )

    return response.content
