# 🧵 CodeWeaver Framework

O **CodeWeaver** é um framework modular para processamento de linguagens, projetado para demonstrar os conceitos de **Frozen Spots** (núcleo invariante) e **Hotspots** (pontos de customização) em uma arquitetura de **Microserviços**.

## 🏗️ Arquitetura do Projeto

O projeto é dividido em serviços independentes que se comunicam via HTTP:

*   **Gateway (Porta 5000):** O coração do framework. Contém o motor de execução (Engine) e a implementação da linguagem customizada (MathLang). Oferece a interface Web.
*   **Analyzer (Porta 5001):** Microserviço responsável por realizar otimizações na Árvore de Sintaxe Abstrata (AST).
*   **Notifier (Porta 5002):** Microserviço simulado para envio de notificações e logs de processamento.
*   **Exporter (Porta 5003):** Microserviço responsável por gerar e exportar arquivos de texto contendo o código fonte original.
*   **Importer (Porta 5004):** Microserviço responsável por processar o upload e a leitura de arquivos de texto para carregar código no editor.

## 📂 Estrutura de Pastas

```text
CodeWeaver/
├── gateway/
│   ├── app.py          # Engine do Framework + Hotspots (MathLang)
│   └── index.html      # Interface Frontend
├── analyzer/
│   └── app.py          # Serviço de Otimização Semântica
├── notifier/
│   └── app.py          # Serviço de Notificação
├── exporter/
│   └── app.py          # Serviço de Exportação de Código
├── importer/
│   └── app.py          # Serviço de Importação de Código
└── Como executar.txt    # Guia rápido de inicialização
```

## 🚀 Como Executar

Para rodar o projeto completo, abra **5 terminais** diferentes e execute os comandos abaixo na ordem:

### 1. Iniciar os Serviços de Infraestrutura (Analyzer, Notifier, Exporter, Importer)
```bash
python3 analyzer/app.py
python3 notifier/app.py
python3 exporter/app.py
python3 importer/app.py
```

### 2. Iniciar o Gateway (Principal)
```bash
cd gateway
python3 app.py
```

Após iniciar os serviços, acesse:
👉 **[http://localhost:5000](http://localhost:5000)**

## 🛠️ Conceitos de Reuso Aplicados

1.  **Frozen Spots (Engine):** A classe `CodeWeaverEngine` define o fluxo fixo de compilação (Lexer -> Parser -> Optimizer -> Interpreter) que não muda.
2.  **Hotspots (Customização):** As classes `MathLangLexer`, `MathLangParser` e `MathLangInterpreter` são as extensões que definem como a nossa linguagem específica funciona.
3.  **Microserviços:** A integração com serviços externos (`Analyzer`, `Exporter`) demonstra como o framework pode ser estendido de forma distribuída.

