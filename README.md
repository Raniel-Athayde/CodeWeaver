# 🧵 CodeWeaver - Central Hub & Architecture Guide

Bem-vindo ao repositório central do **CodeWeaver**. Este ramo (`main`) não contém código de implementação; ele serve como o **mapa arquitetural** e guia de navegação para todo o ecossistema do projeto.

---

## 🌟 O que é o CodeWeaver?

O **CodeWeaver** é um framework extensível (Meta-Compiler Framework) projetado para simplificar a criação de linguagens de programação, interpretadores e compiladores. Ele utiliza o conceito de **Frozen Spots** (núcleo invariante) e **Hotspots** (pontos de extensão) para permitir que desenvolvedores foquem na gramática e lógica de suas linguagens, enquanto o framework gerencia o fluxo de execução e a infraestrutura.

---

## 🗺 Estratégia de Ramos (Branching Model)

Para manter a separação de interesses e facilitar o reuso, o projeto é organizado em três pilares fundamentais hospedados em ramos distintos:

### 📦 [Ramo: framework](https://github.com/Raniel-Athayde/CodeWeaver/tree/framework)
O coração do sistema. Contém as abstrações e o motor de execução.
- **Foco:** Interfaces (`BaseLexer`, `BaseParser`, `BaseInterpreter`), `Engine` de execução e inversão de controle.
- **Uso:** Evolução do framework em si. Alterações aqui impactam todas as aplicações.

### 🚀 [Ramo: application](https://github.com/Raniel-Athayde/CodeWeaver/tree/application)
A camada de implementação e uso prático.
- **Foco:** Implementações concretas (ex: `MathLang`), analisadores específicos e lógica de negócio de alto nível.
- **Uso:** Desenvolvimento de novas linguagens ou funcionalidades baseadas no framework.

### 🧪 [Ramo: beta](https://github.com/Raniel-Athayde/CodeWeaver/tree/beta)
O playground experimental e arquitetura distribuída.
- **Foco:** Refatoração para **Microsserviços**, conteinerização com Docker e testes de escalabilidade.
- **Uso:** Exploração de novas arquiteturas e prototipação de infraestrutura.

---

## 🛠 Como Navegar e Contribuir

### 1. Clonando o Repositório
```bash
git clone https://github.com/Raniel-Athayde/CodeWeaver.git
cd CodeWeaver
```

### 2. Escolhendo seu Contexto
Dependendo do que você deseja fazer, mude para o ramo apropriado:

- **Para contribuir com o Core:**
  ```bash
  git checkout framework
  ```
- **Para criar uma nova Linguagem/App:**
  ```bash
  git checkout application
  ```
- **Para testar a Arquitetura de Microsserviços:**
  ```bash
  git checkout beta
  ```

### 3. Fluxo de Trabalho
1. Identifique se sua mudança é estrutural (`framework`) ou funcional (`application`).
2. Crie uma branch de funcionalidade a partir do ramo base correto.
3. Submeta seu Pull Request para o ramo base correspondente.

---

## 🏗 Princípios de Design

O CodeWeaver é regido por princípios rígidos de engenharia de software para garantir extensibilidade:

1. **Inversão de Controle (IoC):** O framework controla o fluxo (Tokenização -> Parsing -> Execução). Você apenas fornece as peças.
2. **SOLID:** Ênfase total em Responsabilidade Única e Aberto/Fechado.
3. **Pluggability:** Toda nova linguagem deve ser um "plug-in" sobre as interfaces do framework.

---
*CodeWeaver - Tecendo linguagens com simplicidade e elegância.*
