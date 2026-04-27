"""
Gerador de Título de Ticket de Suporte Técnico
Ponto de entrada da aplicação.
"""

import os
import sys
from dotenv import load_dotenv

from src.downloader import extrair_url_exportacao, baixar_pdf, extrair_titulo_doc
from src.analyzer import analisar_documento


def separador(char: str = "─", largura: int = 52) -> str:
    return char * largura


def main():
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("\n❌ ERRO: Variável OPENAI_API_KEY não encontrada.")
        print("   Crie um arquivo .env com: OPENAI_API_KEY=sua_chave_aqui")
        sys.exit(1)

    print()
    print(separador("═"))
    print("  🎫  GERADOR DE TÍTULO DE TICKET DE SUPORTE")
    print(separador("═"))

    while True:
        print()
        print("Cole o link do Google Docs (ou 'sair' para encerrar):")
        url_input = input("  → ").strip()

        if url_input.lower() in ("sair", "exit", "quit", "q"):
            print("\n👋 Encerrando. Até logo!\n")
            break

        if not url_input:
            print("⚠️  Nenhum link fornecido. Tente novamente.")
            continue

        try:
            print()
            print("⏳ Preparando URL de exportação...")
            export_url = extrair_url_exportacao(url_input)

            # Extrai o doc_id para buscar o título
            doc_id = url_input.split("/document/d/")[1].split("/")[0].split("?")[0]

            print("⏳ Baixando documento...")
            pdf_bytes = baixar_pdf(export_url)
            tamanho_kb = len(pdf_bytes) / 1024
            print(f"✅ Documento baixado ({tamanho_kb:.1f} KB)")

            print("⏳ Identificando nome da empresa...")
            titulo_doc = extrair_titulo_doc(doc_id, api_key)
            if titulo_doc:
                print(f"✅ Empresa identificada: {titulo_doc}")
            else:
                print("⚠️  Não foi possível extrair o título — a IA tentará identificar.")

            print("🤖 Analisando com IA...")
            resultado = analisar_documento(pdf_bytes, api_key, titulo_doc)

            print()
            print(separador())
            print(resultado)
            print()
            print(separador())

        except (ValueError, PermissionError, FileNotFoundError,
                ConnectionError, TimeoutError) as e:
            print(f"\n❌ {e}")
        except Exception as e:
            print(f"\n❌ Erro inesperado: {e}")
            print("   Verifique sua chave de API e tente novamente.")

        print()
        input("Pressione Enter para gerar outro ticket...")


if __name__ == "__main__":
    main()