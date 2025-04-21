# Monitoramento de Tráfego de Rede

Este projeto implementa uma aplicação web para **simulação de monitoramento de tráfego de rede** em uma pequena infraestrutura. Utiliza:

- **Frontend**: Streamlit (interface dinâmica)
- **Backend**: Flask (API REST)
- **Banco de Dados**: SQLite (persistência leve)
- **Containerização**: Docker Compose (multi‑serviços)

---

## 📁 Estrutura de Pastas
```
projeto-monitoramento/
├── backend/
│   ├── app.py            # Aplicação Flask e definição da API
│   └── requirements.txt  # Dependências do backend
├── frontend/
│   ├── app.py            # Interface Streamlit
│   └── requirements.txt  # Dependências do frontend
├── Dockerfile            # Dockerfile genérico para ambos os serviços
└── docker-compose.yml    # Orquestração dos containers
```

---

## 🚀 Como Executar

1. **Pré-requisitos**:
   - Docker
   - Docker Compose

2. **No diretório raiz** do projeto:
   ```bash
   # Remove containers órfãos ou antigos
   docker compose down --remove-orphans

   # Constrói imagens e sobe containers em segundo plano
   docker compose up --build -d
   ```

3. **Acesse**:
   - **Frontend (UI Streamlit)**: `http://localhost:8501`
   - **API Flask**: `http://localhost:5000/devices`

4. **Para parar/remover**:
   ```bash
   docker compose down
   ```

---

## 🖥️ Funcionalidades

1. **Registro de Dispositivos**
   - Campos: **Endereço IP**, **Nome**, **Taxa de tráfego** (Mbps)
   - Envia via `POST /devices` para o backend.

2. **Dashboard de Tráfego**
   - Gráfico de barras com cores:
     - **Normal** (≤ 50 Mbps)
     - **Alto** (> 50 Mbps)
   - Label dos dispositivos dispostos horizontalmente no eixo X.

3. **Listagem e Remoção**
   - Tabela com **IP**, **Nome**, **Taxa**, **Status**.
   - Botão **Remover** que chama `DELETE /devices/{id}` e atualiza a interface.

---

## 🔌 Endpoints da API

| Método | Rota            | Descrição                        | Request Payload         |
|--------|-----------------|----------------------------------|-------------------------|
| POST   | `/devices`      | Adiciona um novo dispositivo     | `{ ip, nome, trafego }` |
| GET    | `/devices`      | Retorna todos os dispositivos    | *(nenhum)*              |
| DELETE | `/devices/{id}` | Remove dispositivo por **ID**    | *(nenhum)*              |

---

## 📜 Tecnologias e Dependências

- **Python 3.11**
- **Flask** / **flask-cors**
- **Streamlit** / **requests** / **pandas** / **altair**
- **SQLite** (via módulo `sqlite3` do Python)
- **Docker** / **Docker Compose**

---

## ✨ Contribuição

1. Faça um **fork** deste repositório.
2. Crie uma **branch** com sua feature/bugfix: `git checkout -b feature/nome-da-feature`
3. **Commit** suas alterações: `git commit -m "Descrição do commit"`
4. Faça **push**: `git push origin feature/nome-da-feature`
5. Abra um **pull request** para análise.


