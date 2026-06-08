# 🧵 CodeWeaver

<p align="center">
  <strong>Framework extensível para criação de linguagens, interpretadores e compiladores com arquitetura baseada em Frozen Spots e Hotspots.</strong>
</p>

<p align="center">
  <a href="https://github.com/Raniel-Athayde/CodeWeaver"><img alt="GitHub repo" src="https://img.shields.io/badge/GitHub-CodeWeaver-181717?style=flat-square&logo=github"></a>
  <img alt="Python" src="https://img.shields.io/badge/Python-3.x-3776AB?style=flat-square&logo=python&logoColor=white">
  <img alt="Arquitetura" src="https://img.shields.io/badge/Arquitetura-Microserviços%20%2B%20Framework-6f42c1?style=flat-square">
  <img alt="Status" src="https://img.shields.io/badge/status-em%20desenvolvimento-2ea44f?style=flat-square">
</p>

---

## Visão geral

O **CodeWeaver** é um projeto acadêmico de engenharia de software que explora a construção de um **Meta-Compiler Framework**: uma base reutilizável para desenvolver linguagens de programação, interpretadores e compiladores.

A proposta central é separar o que permanece estável no processo de execução de uma linguagem (**Frozen Spots**) daquilo que pode variar conforme a linguagem implementada (**Hotspots**). Assim, o framework controla o fluxo principal de compilação/interpretação, enquanto cada aplicação fornece componentes específicos como lexer, parser e interpreter.

---

## Objetivos do projeto

- Fornecer uma estrutura reutilizável para criação de linguagens simples.
- Aplicar princípios de **inversão de controle**, **baixo acoplamento** e **alta coesão**.
- Demonstrar a separação entre núcleo do framework e implementações específicas.
- Evoluir a arquitetura para um modelo distribuído com serviços independentes.
- Servir como base didática para estudos de compiladores, interpretadores e arquitetura de software.

---

## Conceitos principais

### Frozen Spots

São as partes invariantes do framework. No CodeWeaver, o fluxo principal é controlado pela engine:

```text
Código-fonte → Lexer → Parser → Otimização → Interpreter → Resultado
```

Esse fluxo é definido pelo framework e não precisa ser reimplementado por cada nova linguagem.

### Hotspots

São os pontos de extensão do sistema. Cada linguagem pode fornecer suas próprias implementações para:

- análise léxica;
- análise sintática;
- interpretação/execução;
- regras semânticas;
- integrações adicionais.

### Exemplo atual: MathLang

A aplicação presente no repositório implementa uma linguagem simples chamada **MathLang**, com suporte a:

- operações aritméticas básicas;
- expressões com precedência;
- variáveis;
- comando `PRINT`;
- execução integrada ao gateway HTTP.

---

## Arquitetura

O projeto combina um núcleo de framework com uma aplicação de exemplo e serviços auxiliares.

```text
+-------------------+        +-------------------------+
| Interface Web     | -----> | Gateway / MathLang App  |
+-------------------+        +-----------+-------------+
                                    |
                                    v
                          +-------------------+
                          | CodeWeaver Engine |
                          +---------+---------+
                                    |
             +----------------------+----------------------+
             |                      |                      |
             v                      v                      v
        MathLang Lexer        MathLang Parser       MathLang Interpreter
             |
             v
+-------------------+   +-------------------+   +-------------------+
| Analyzer Service  |   | Notifier Service  |   | Exporter/Importer |
| porta 5001        |   | porta 5002        |   | portas 5003/5004  |
+-------------------+   +-------------------+   +-------------------+
```

### Componentes

| Componente | Função |
| --- | --- |
| `framework/` | Núcleo reutilizável do CodeWeaver, incluindo engine, interfaces e serviços base. |
| `gateway/` | Aplicação principal, interface web e integração da MathLang com o framework. |
| `gateway/modules/mathlang/` | Implementação concreta de lexer, parser e interpreter da linguagem MathLang. |
| `analyzer/` | Serviço auxiliar de análise/otimização da AST. |
| `notifier/` | Serviço responsável por notificações após a execução. |
| `exporter/` | Serviço para exportação de código. |
| `importer/` | Serviço para importação de código. |

---

## Modelo de branches

O repositório organiza diferentes frentes de desenvolvimento em ramos específicos:

| Branch | Papel |
| --- | --- |
| [`main`](https://github.com/Raniel-Athayde/CodeWeaver/tree/main) | Página principal do projeto, documentação e versão integrada. |
| [`framework`](https://github.com/Raniel-Athayde/CodeWeaver/tree/framework) | Desenvolvimento do núcleo reutilizável do framework. |
| [`application`](https://github.com/Raniel-Athayde/CodeWeaver/tree/application) | Implementações concretas e evolução da aplicação MathLang. |
| [`beta`](https://github.com/Raniel-Athayde/CodeWeaver/tree/beta) | Experimentações, microsserviços, conteinerização e testes de arquitetura. |

---

## Como executar

### 1. Clone o repositório

```bash
git clone https://github.com/Raniel-Athayde/CodeWeaver.git
cd CodeWeaver
```

### 2. Instale as dependências necessárias

O projeto utiliza Python 3. Caso ainda não tenha a dependência HTTP instalada:

```bash
python3 -m pip install requests
```

### 3. Inicie os serviços

Abra cinco terminais separados e execute:

```bash
# Terminal 1 - serviço de análise
cd analyzer
python3 app.py
```

```bash
# Terminal 2 - serviço de notificação
cd notifier
python3 app.py
```

```bash
# Terminal 3 - serviço de exportação
cd exporter
python3 app.py
```

```bash
# Terminal 4 - serviço de importação
cd importer
python3 app.py
```

```bash
# Terminal 5 - gateway principal
cd gateway
python3 app.py
```

Depois, acesse no navegador:

```text
http://localhost:5000
```

O gateway utiliza a porta `5000` e se comunica com os serviços auxiliares nas portas `5001` a `5004`.

---

## Exemplo de uso da MathLang

```text
x = 10 + 5
y = x * 2
PRINT y
```

Fluxo esperado:

1. O gateway recebe o código.
2. A engine aciona o lexer da MathLang.
3. O parser gera a AST.
4. O analyzer pode otimizar a estrutura intermediária.
5. O interpreter executa a AST.
6. O notifier registra o resultado da execução.

---

## Princípios de design

- **Inversão de Controle (IoC):** o framework define o fluxo; a linguagem fornece as implementações concretas.
- **Aberto/Fechado:** novas linguagens podem ser adicionadas sem alterar o núcleo principal.
- **Separação de responsabilidades:** cada serviço tem um papel bem delimitado.
- **Extensibilidade:** a arquitetura favorece evolução incremental e substituição de componentes.
- **Clareza didática:** o projeto busca tornar explícita a comunicação entre framework, aplicação e serviços.

---

## Contribuidores

Este projeto foi desenvolvido em colaboração por:

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/Raniel-Athayde">
        <img src="https://avatars.githubusercontent.com/Raniel-Athayde?s=100" width="100px;" alt="Foto de Raniel Athayde"/><br />
        <sub><b>Raniel Athayde</b></sub>
      </a>
      <br />
      <sub>Desenvolvimento, arquitetura e documentação</sub>
    </td>
    <td align="center">
      <a href="https://github.com/brieueu">
        <img src="https://avatars.githubusercontent.com/brieueu?s=100" width="100px;" alt="Foto de Gabriel"/><br />
        <sub><b>Gabriel</b></sub>
      </a>
      <br />
      <sub>Colaboração, integração e documentação</sub>
    </td>
  </tr>
</table>

> Observação: para aparecer também na área automática de **Contributors** do GitHub, o perfil precisa ter commits na branch principal reconhecidos por um e-mail associado à conta do GitHub. Esta seção garante o crédito diretamente no README da página principal do projeto.

---

## Estado atual

O CodeWeaver está em desenvolvimento e já possui:

- núcleo de execução reutilizável;
- aplicação MathLang integrada;
- gateway HTTP com interface web;
- serviços auxiliares de análise, notificação, importação e exportação;
- documentação de arquitetura e execução.

---

## Próximos passos sugeridos

- Adicionar um arquivo `requirements.txt` para facilitar a instalação das dependências.
- Criar testes automatizados para lexer, parser, interpreter e serviços.
- Documentar formalmente a gramática da MathLang.
- Adicionar exemplos de novas linguagens implementadas sobre o framework.
- Evoluir a execução via Docker Compose para simplificar a inicialização dos serviços.

---

<p align="center">
  <strong>CodeWeaver — tecendo linguagens com simplicidade, extensão e arquitetura.</strong>
</p>
