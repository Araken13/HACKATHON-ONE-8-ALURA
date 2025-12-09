# 🐳 Guia: Rodando TUDO no Docker

Para rodar a aplicação completa (API, Frontend, Banco e Grafana) usando apenas Docker, sem instalar Node ou Python na sua máquina (host), siga este guia.

## 📋 Pré-requisitos

Apenas o **Docker Desktop** instalado e rodando.

---

## 🚀 Passo Único: Iniciar Tudo

Abra o terminal na pasta do projeto e rode:

```bash
docker compose up --build
```

*(O `--build` garante que as imagens serão recriadas com as alterações recentes).*

> **Aguarde alguns minutos** na primeira vez, pois ele vai baixar as imagens e instalar as dependências do Frontend (npm install) e Backend (pip install).

---

## 🌐 Acessando os Serviços

| Serviço | URL | Credenciais |
| :--- | :--- | :--- |
| **Frontend** | [http://localhost:5173](http://localhost:5173) | - |
| **API** | [http://localhost:8000](http://localhost:8000) | - |
| **Docs API** | [http://localhost:8000/docs](http://localhost:8000/docs) | - |
| **Grafana** | [http://localhost:3000](http://localhost:3000) | `admin` / `admin` |

---

## 🛠️ Comandos Úteis

### Parar Tudo

```bash
docker compose down
```

### Ver Logs (se rodou com -d)

```bash
docker compose logs -f
```

### Acessar Terminal do Frontend (ex: para instalar nova lib)

```bash
docker compose exec frontend sh
```

*Dentro do container, você pode rodar `npm install nova-lib`.*

### Acessar Terminal da API

```bash
docker compose exec api bash
```

---

## ❓ Como Funciona?

- O **Frontend** roda em um container Node.js e está configurado para redirecionar as chamadas (`/predict`) internamente para o container da **API**.
- A **API** roda em um container Python e conecta internamente com o container do **Banco**.
- O código do seu computador (Windows/WSL) é espelhado dentro dos containers (`volumes`), então se você editar um arquivo `.tsx` ou `.py`, a aplicação atualiza sozinha (**Hot Reload**).
