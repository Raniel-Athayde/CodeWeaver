# CodeWeaver - Arquitetura de Microsserviços

Refatoração do CodeWeaver para uma **arquitetura de microsserviços** escalável com Docker Compose.

## Arquitetura

```
┌──────────────────────────────────────────────────────────────┐
│                    API Gateway (5000)                         │
│              (Interface Web + Orquestração)                  │
└──────────┬──────────────────────────────────────────────────┘
           │
    ┌──────┴──────────────┬──────────────┬──────────────┐
    │                     │              │              │
    v                     v              v              v
┌─────────┐          ┌─────────┐   ┌──────────┐  ┌────────────┐
│  Lexer  │          │ Parser  │   │Optimizer │  │  Backend   │
│ (5001)  │          │ (5002)  │   │ (5003)   │  │  (5004)    │
└─────────┘          └─────────┘   └──────────┘  └────────────┘
    │                                   
    │    ┌────────────────────┬─────────────────┐
    │    │                    │                 │
    v    v                    v                 v
  ┌────────────┐        ┌──────────┐    ┌──────────────┐
  │  Analysis  │        │Notification│   │  (Reserved) │
  │  (5005)    │        │  (5006)    │   │             │
  └────────────┘        └──────────────┘   └──────────────┘
```

## Serviços

| Serviço | Porta | Função |
|---------|-------|--------|
| **API Gateway** | 5000 | Entrada principal, orquestra pipeline |
| **Lexer Service** | 5001 | Tokenização do código |
| **Parser Service** | 5002 | Análise sintática (AST) |
| **Optimizer Service** | 5003 | Otimização da AST |
| **Backend Service** | 5004 | Execução do código |
| **Analysis Service** | 5005 | Análise de qualidade e segurança |
| **Notification Service** | 5006 | Log centralizado de eventos |

## Como Usar

### 1. Com Docker Compose (Recomendado)

```bash
# Na raiz do projeto
docker-compose up --build

# Acessar: http://localhost:5000
```

### 2. Localmente (sem Docker)

```bash
# Terminal 1 - Notification Service
cd notification-service && python app.py

# Terminal 2 - Lexer Service
cd lexer-service && python app.py

# Terminal 3 - Parser Service
cd parser-service && python app.py

# Terminal 4 - Optimizer Service
cd optimizer-service && python app.py

# Terminal 5 - Backend Service
cd backend-service && python app.py

# Terminal 6 - Analysis Service
cd analysis-service && python app.py

# Terminal 7 - API Gateway
cd api-gateway && python app.py
```

### 3. Testar via API

```bash
# Compilar e executar código
curl -X POST http://localhost:5000/api/compile \
  -H "Content-Type: application/json" \
  -d '{"code": "10 + 5 * 2"}'
```

### 4. Monitorar Notificações

```bash
# Ver últimos eventos
curl http://localhost:5006/events?limit=10

# Limpar log
curl -X DELETE http://localhost:5006/events/clear
```

### 5. Verificar Saúde dos Serviços

```bash
curl http://localhost:5000/  # Gateway
curl http://localhost:5001/health  # Lexer
curl http://localhost:5002/health  # Parser
curl http://localhost:5003/health  # Optimizer
curl http://localhost:5004/health  # Backend
curl http://localhost:5005/health  # Analysis
curl http://localhost:5006/health  # Notification
```

## Fluxo de Execução

1. **Frontend** envia código para `POST /api/compile`
2. **API Gateway** orquestra:
   - Lexer tokeniza o código
   - Parser constrói a AST
   - Analysis analisa qualidade (paralelo)
   - Optimizer otimiza
   - Backend executa
   - Notification registra sucesso/erro

## Escalabilidade

Cada microsserviço pode ser:
- **Escalado independentemente** (mais instâncias)
- **Deployado separadamente** (CI/CD)
- **Replaçado** com outra implementação
- **Monitorado** individualmente

## Próximos Passos

- [ ] Adicionar gRPC para comunicação mais rápida
- [ ] Implementar Circuit Breaker para resiliência
- [ ] Adicionar autenticação/autorização
- [ ] Integrar com Kubernetes
- [ ] Adicionar testes unitários
- [ ] Implementar rate limiting
- [ ] Adicionar métricas com Prometheus
