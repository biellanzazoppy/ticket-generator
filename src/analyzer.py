"""
Módulo responsável por enviar o PDF para a API da OpenAI e retornar o título gerado.
O PDF é convertido em imagens (uma por página) e enviado via vision do GPT-4o.
"""

import base64
import io
from openai import OpenAI
from pdf2image import convert_from_bytes

from config import MODELO
from src.prompt import build_system_prompt


def pdf_para_imagens_base64(pdf_bytes: bytes) -> list[str]:
    """
    Converte cada página do PDF em uma imagem PNG base64.
    """
    imagens = convert_from_bytes(pdf_bytes, dpi=150, fmt="PNG")
    resultado = []
    for img in imagens:
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
        resultado.append(b64)
    return resultado


def analisar_documento(pdf_bytes: bytes, api_key: str, titulo_doc: str = "") -> str:
    """
    Envia o PDF (como imagens de páginas) para a API da OpenAI (GPT-4o)
    e retorna o título do ticket gerado.
    """
    system_prompt = build_system_prompt()
    imagens_b64 = pdf_para_imagens_base64(pdf_bytes)

    # Monta o conteúdo: todas as páginas como imagem + instrução de texto
    content = []
    for b64 in imagens_b64:
        content.append({
            "type": "image_url",
            "image_url": {
                "url": f"data:image/png;base64,{b64}",
                "detail": "high",
            },
        })

    instrucao = (
        "Analise este documento completamente, incluindo todos os textos e imagens. "
        "Gere o título do ticket seguindo exatamente o padrão especificado."
    )

    if titulo_doc:
        instrucao = (
            f"O nome da empresa para o campo [Empresa] do título é EXATAMENTE '{titulo_doc}'. "
            f"Use este nome sem nenhuma alteração, abreviação ou substituição. "
            f"IGNORE qualquer outro nome encontrado no conteúdo do documento para este campo. "
        ) + instrucao

    content.append({"type": "text", "text": instrucao})

    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model=MODELO,
        max_tokens=1024,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": content},
        ],
    )

    return response.choices[0].message.content.strip()