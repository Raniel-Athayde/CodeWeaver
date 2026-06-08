# 🧵 CodeWeaver

<p align="center">
  <strong>Framework didático em Python para reuso de software, microserviços e construção de linguagens extensíveis.</strong>
</p>

<p align="center">
  <a href="https://github.com/Raniel-Athayde/CodeWeaver"><img alt="GitHub" src="https://img.shields.io/badge/GitHub-CodeWeaver-181717?style=flat-square&logo=github"></a>
  <img alt="Python" src="https://img.shields.io/badge/Python-3.x-3776AB?style=flat-square&logo=python&logoColor=white">
  <img alt="Arquitetura" src="https://img.shields.io/badge/Arquitetura-Microserviços-6f42c1?style=flat-square">
  <img alt="Status" src="https://img.shields.io/badge/status-acadêmico%20%2F%20em%20desenvolvimento-2ea44f?style=flat-square">
</p>

---

## Sobre o projeto

O **CodeWeaver** é um framework acadêmico desenvolvido em Python para demonstrar conceitos de **reuso de software**, **arquitetura de microserviços** e **compiladores/interpretadores extensíveis**.

A ideia principal é separar o fluxo fixo de execução do framework dos pontos que podem ser personalizados por cada linguagem.

```text
Código-fonte → Lexer → Parser → Otimização → Interpreter → Resultado
```

No projeto, esse fluxo é usado para executar uma linguagem de exemplo chamada **MathLang**.

---

## Conceitos aplicados

- **Frozen Spots:** partes fixas do framework, como o pipeline de execução.
- **Hotspots:** pontos de extensão, como lexer, parser e interpreter.
- **Template Method:** o framework define a sequência de execução e as implementações concretas preenchem as etapas variáveis.
- **Injeção de dependências:** a engine recebe os componentes da linguagem sem depender diretamente de uma implementação específica.
- **Microserviços:** funcionalidades auxiliares são separadas em serviços independentes.

---

## Arquitetura simplificada

```text
Interface Web
    ↓
Gateway / MathLang App
    ↓
CodeWeaver Engine
    ↓
Lexer → Parser → Analyzer → Interpreter → Notifier
                    ↓
             Importer / Exporter
```

### Estrutura principal

| Pasta | Descrição |
| --- | --- |
| `framework/` | Núcleo reutilizável do framework. |
| `gateway/` | Interface web, API principal e integração com a MathLang. |
| `gateway/modules/mathlang/` | Lexer, parser e interpreter da linguagem de exemplo. |
| `analyzer/` | Serviço de análise/otimização. |
| `notifier/` | Serviço de notificação. |
| `importer/` | Serviço de importação de código. |
| `exporter/` | Serviço de exportação de código. |
| `docs/` | Relatório técnico/artigo do projeto. |

---

## Artigo / relatório técnico

O relatório completo do projeto está disponível em:

📄 [CodeWeaver Framework: relatório técnico sobre reuso de software em arquitetura de microserviços](docs/codeweaver-relatorio.pdf)

O documento apresenta a motivação, metodologia, diagramas, análise arquitetural, padrões de projeto utilizados, limitações e possibilidades de evolução do CodeWeaver.

---

## Como executar

Clone o repositório:

```bash
git clone https://github.com/Raniel-Athayde/CodeWeaver.git
cd CodeWeaver
```

Instale a dependência principal, se necessário:

```bash
python3 -m pip install requests
```

Inicie os serviços em terminais separados:

```bash
cd analyzer && python3 app.py
cd notifier && python3 app.py
cd exporter && python3 app.py
cd importer && python3 app.py
cd gateway && python3 app.py
```

Depois acesse:

```text
http://localhost:5000
```

O gateway roda na porta `5000` e se comunica com os serviços auxiliares nas portas `5001` a `5004`.

---

## Exemplo de código MathLang

```text
x = 10 + 5
y = x * 2
PRINT y
```

---

## Branches do projeto

| Branch | Finalidade |
| --- | --- |
| [`main`](https://github.com/Raniel-Athayde/CodeWeaver/tree/main) | Documentação principal e versão integrada. |
| [`framework`](https://github.com/Raniel-Athayde/CodeWeaver/tree/framework) | Núcleo reutilizável do framework. |
| [`application`](https://github.com/Raniel-Athayde/CodeWeaver/tree/application) | Implementação da aplicação MathLang. |
| [`beta`](https://github.com/Raniel-Athayde/CodeWeaver/tree/beta) | Experimentos com microserviços e evolução arquitetural. |

---

## Contribuidores

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/Raniel-Athayde">
        <img src="https://avatars.githubusercontent.com/Raniel-Athayde?s=100" width="100px;" alt="Raniel Athayde"/><br />
        <sub><b>Raniel Ferreira Athayde</b></sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/brieueu">
        <img src="https://avatars.githubusercontent.com/brieueu?s=100" width="100px;" alt="José Gabriel de Almeida Vieira"/><br />
        <sub><b>José Gabriel de Almeida Vieira</b></sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/AsimovMolediver">
        <img src="https://avatars.githubusercontent.com/AsimovMolediver?s=100" width="100px;" alt="Pedro Henrique Balbino Rocha"/><br />
        <sub><b>Pedro Henrique Balbino Rocha</b></sub>
      </a>
    </td>
  </tr>
</table>

> A seção acima registra explicitamente os autores e colaboradores no README. A lista automática de contributors do GitHub depende dos commits reconhecidos na branch principal e dos e-mails associados a cada conta.

---

<p align="center">
  <strong>CodeWeaver — reuso, extensão e arquitetura aplicados à construção de linguagens.</strong>
</p>
