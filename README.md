# Sistema de Gerenciamento de Barbearia (CLI)

Sistema interativo via terminal baseado em Linha de Comando (CLI - *Command Line Interface*) desenvolvido em Python. O projeto aplica de forma rigorosa os conceitos de **Programação Orientada a Objetos (POO)** e herança para gerenciar os fluxos operacionais, financeiros e de agendamento de uma barbearia profissional[cite: 1, 2].

O sistema divide os níveis de acesso e permissões entre três perfis de usuários: **Administradores**, **Barbeiros** e **Clientes**, garantindo regras de negócio customizadas para cada papel.

---

## 📂 Organização de Pastas e Arquivos

O projeto está organizado seguindo o padrão de pacotes e módulos do Python, separando a lógica de negócio (modelos) do fluxo de execução principal:

```text
agendamento-barbearia/
│
├── models/
│   └── classes.py       # Definição e encapsulamento das Classes (Entidades e Regras de Negócio)
│
├── main.py              # Ponto de entrada do sistema (Menus interativos e fluxo CLI)
└── README.md            # Documentação técnica do projeto (Este arquivo)
