# 🧵 CodeWeaver Framework

O **CodeWeaver** é um framework modular para processamento de linguagens, projetado para demonstrar os conceitos de **Frozen Spots** (núcleo invariante) e **Hotspots** (pontos de customização) em uma arquitetura de **Microserviços**.

## 🏗️ Arquitetura do Projeto

O projeto é dividido em serviços independentes que se comunicam via HTTP:

*   **Gateway (Porta 5000):** O coração do framework. Contém o motor de execução (Engine) e a implementação da linguagem customizada (MathLang). Oferece a interface Web.
*   **Analyzer (Porta 5001):** Microserviço responsável por realizar otimizações na Árvore de Sintaxe Abstrata (AST).
*   **Notifier (Porta 5002):** Microserviço simulado para envio de notificações e logs de processamento.

## 📂 Estrutura de Pastas

```text
CodeWeaver/
├── gateway/
│   ├── app.py          # Engine do Framework + Hotspots (MathLang)
│   └── templates/
│       └── index.html  # Interface Frontend
├── analyzer/
│   └── app.py          # Serviço de Otimização Semântica
├── notifier/
│   └── app.py          # Serviço de Notificação
└── Como executar.txt    # Guia rápido de inicialização
```

## 🚀 Como Executar

Para rodar o projeto completo, abra **3 terminais** diferentes e execute os comandos abaixo na ordem:

### 1. Iniciar o Analyzer
```bash
cd analyzer
python app.py
```

### 2. Iniciar o Notifier
```bash
cd notifier
python app.py
```

### 3. Iniciar o Gateway (Principal)
```bash
cd gateway
python app.py
```

Após iniciar os três serviços, acesse:
👉 **[http://localhost:5000](http://localhost:5000)**

## 🛠️ Conceitos de Reuso Aplicados

1.  **Frozen Spots (Engine):** A classe `CodeWeaverEngine` define o fluxo fixo de compilação (Lexer -> Parser -> Optimizer -> Interpreter) que não muda.
2.  **Hotspots (Customização):** As classes `MathLangLexer`, `MathLangParser` e `MathLangInterpreter` são as extensões que definem como a nossa linguagem específica funciona.
3.  **Microserviços:** A integração com serviços externos (`Analyzer`) demonstra como o framework pode ser estendido de forma distribuída.
