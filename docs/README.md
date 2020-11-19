# Tutti.ai

> Delivers data you really need.

## What is Tutti?

Tutti is a Docker-based environment that helps you **build your own Human-In-The-Loop AI system** on the fly. With Tutti, you can:
- design & create web annotation interfaces,
- define workflows,
- post microtasks, and
- collect answers & get notified,

\-\- with *surprisingly*-less effort.

## Specs

- Virtual Environment: [Docker Compose](https://docs.docker.jp/compose/)
- Frontend server: [Vue CLI](https://cli.vuejs.org)
- Backend server: [DUCTS](https://ducts.io)
- Reverse-proxy server: [Nginx](https://nginx.org)
- Data stores:
  - [Redis](https://redis.io) (mainly for data caching / indexing / pubsub-ing)
  - [MongoDB](https://mongodb.com) (for storing task-relevant data)


---

Powered by [ifLab Inc.](https://iflab.co.jp)
