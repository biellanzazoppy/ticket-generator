# 🎫 Gerador de Título de Ticket de Suporte

Aplicação CLI que recebe um link público do Google Docs, analisa o conteúdo completo (textos e imagens) usando GPT-4o da OpenAI, e gera automaticamente um título padronizado para tickets de suporte técnico.

---

## 📋 Formato do Título Gerado

```
[Nome da Empresa] [Funcionalidade] [Descrição resumida e específica do problema]
```

**Exemplos:**
```
[Use Kesha] [WHATSAPP] [Ocorreu erro ao linkar a conta do whatsapp (Get WhatsApp Details Failed: Internal Server Error)]
[Alternazero] [CAMPANHA] [Enviou campanha por planilha e a variável {abandoned_cart_URL} foi como NULL]
```

---

## ⚙️ Pré-requisitos

- Python 3.10 ou superior
- Chave de API da OpenAI ([obtenha aqui](https://platform.openai.com/api-keys))
- **poppler** instalado no sistema (necessário para conversão de PDF em imagem)
- O Google Docs deve estar configurado como **público** (qualquer pessoa com o link pode visualizar)

### Instalando o poppler

**Windows:** Baixe em https://github.com/oschwartz10612/poppler-windows/releases, extraia e adicione a pasta `bin` ao PATH do sistema.

**macOS:**
```bash
brew install poppler
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install poppler-utils
```

---

## 🚀 Instalação

**1. Clone ou extraia os arquivos do projeto**

**2. Crie e ative um ambiente virtual (recomendado):**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

**3. Instale as dependências:**
```bash
pip install -r requirements.txt
```

**4. Configure sua chave de API:**

Copie o arquivo de exemplo e adicione sua chave:
```bash
cp .env.example .env
```

Edite o arquivo `.env`:
```
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxx
```

---

## ▶️ Uso

```bash
python main.py
```

Cole o link do Google Docs quando solicitado. O link deve ser no formato:
```
https://docs.google.com/document/d/SEU_ID_AQUI/edit
```

---

## 🔧 Personalização das Funcionalidades

Abra o arquivo `config/funcionalidades.py` e edite a lista:

```python
FUNCIONALIDADES = [
    "WHATSAPP",
    "CAMPANHA",
    # adicione ou remova funcionalidades aqui
]
```

---

## 🖼️ Tipos de Conteúdo Analisados

- ✅ Textos e parágrafos do documento
- ✅ Prints de tela da plataforma
- ✅ Telas de erro (mensagens, popups, códigos HTTP)
- ✅ Capturas do banco de dados (Metabase: gráficos, tabelas, queries)
- ✅ Qualquer imagem presente no documento

---

## ❗ Solução de Problemas

| Erro | Solução |
|------|---------|
| `OPENAI_API_KEY não encontrada` | Crie o arquivo `.env` com sua chave |
| `Acesso negado (403)` | Certifique-se de que o documento está público |
| `Documento não encontrado (404)` | Verifique se o link está correto |
| `Unable to get page count` | Instale o poppler (veja Pré-requisitos) |

---

## 📁 Estrutura do Projeto

```
ticket-generator/
├── main.py                  # Ponto de entrada
├── requirements.txt         # Dependências
├── .env                     # Sua chave de API (não versionar!)
├── .env.example             # Modelo do .env
├── .gitignore
├── config/
│   ├── funcionalidades.py   # ✏️ Edite as funcionalidades aqui
│   ├── settings.py          # Modelo e configurações
│   └── __init__.py
├── src/
│   ├── analyzer.py          # Integração com GPT-4o
│   ├── downloader.py        # Download do Google Docs
│   ├── prompt.py            # System prompt da IA
│   └── __init__.py
└── docs/
    └── README.md
```

---

## 🔒 Segurança

- **Nunca** faça commit do arquivo `.env` com sua chave real
- O `.gitignore` já está configurado para ignorar o `.env`
