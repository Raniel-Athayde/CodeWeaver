# 🧵 CodeWeaver

**CodeWeaver** é um framework extensível projetado para simplificar a criação de compiladores e interpretadores. Ele fornece uma arquitetura de núcleo invariante (frozen spots) robusta que gerencia o ciclo de vida e o fluxo de execução do processamento de linguagens, expondo pontos de customização (hotspots) claros para você tecer a lógica da sua própria linguagem.

## ✨ Funcionalidades Principais

* **Inversão de Controle (IoC):** O framework dita o fluxo padrão de processamento de código; você só precisa plugar sua lógica de negócio.
* **Pipeline Flexível:** Estrutura pronta para acoplamento de analisadores léxicos, sintáticos (parsing) e geradores de código.
* **Hotspots Customizáveis:** Interface limpa para estender o comportamento do compilador/interpretador sem reinventar a roda.
* **Foco na Gramática:** Gaste menos tempo brigando com a infraestrutura do sistema e mais tempo definindo a sua AST e suas regras gramaticais.
