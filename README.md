# Sistema de Gerenciamento de Barbearia (CLI)

Sistema interativo via terminal baseado em Linha de Comando (CLI) desenvolvido em Python. O projeto aplica os conceitos de Programação Orientada a Objetos (POO) e herança para gerenciar os fluxos operacionais, financeiros e de agendamento de uma barbearia profissional.

O sistema divide os níveis de acesso e permissões entre três perfis de usuários: Administradores, Barbeiros e Clientes, garantindo regras de negócio customizadas para cada papel.

---

## 📂 Organização de Pastas e Arquivos

O projeto está organizado seguindo o padrão de pacotes e módulos do Python, separando a lógica de negócio do fluxo de execução principal:

* **agendamento-barbearia/** (Pasta Raiz)
  * **models/** (Pasta)
    * **classes.py** (Definição de todas as Classes e Entidades)
  * **main.py** (Ponto de entrada do sistema, menus interativos e fluxo CLI)
  * **README.md** (Documentação técnica do projeto)

> **Nota de Importação:** No arquivo main.py, as classes são importadas via "from models.classes import ...".

---

## 🛠️ Tecnologias e Requisitos de Ambiente

* **Linguagem:** Python (Versão mínima recomendada: 3.10 ou superior).
* **Dependências Externas:** Nenhuma. O sistema foi concebido utilizando exclusivamente as bibliotecas nativas e padrão do ecossistema Python (sys e datetime).
* **Banco de Dados:** Persistência em Memória Volátil. Visando a agilidade de testes desta versão, os dados são populados e mantidos em estruturas de listas e dicionários. Portanto, dispensa-se a necessidade de execução de dumps de bancos relacionais (SQL).

---

## 💾 Carga Inicial de Dados (Massa de Teste Automatizada)

Para facilitar a avaliação e simular o comportamento de produção, o sistema já inicia com uma carga pré-configurada de entidades. Os e-mails listados abaixo devem ser utilizados para realizar o login e validar as funcionalidades correspondentes:

### 👥 Usuários Cadastrados

* **Administrador:** Lucas Ferreira (Admin) | E-mail: admin@barbearia.com | Controle total, relatórios e baixas financeiras.
* **Barbeiro 1:** Rafael Bruno | E-mail: rafael@barbearia.com | Agenda vinculada e comissão fixada em 40%.
* **Barbeiro 2:** Lucas Silvério | E-mail: lucas@barbearia.com | Agenda vinculada e comissão fixada em 35%.
* **Cliente:** Lars | E-mail: cliente@email.com | Histórico de serviços e preferências de corte salvas.

### 💈 Serviços Disponíveis
* **ID 1:** Corte — R$ 45,00
* **ID 2:** Barba — R$ 30,00
* **ID 3:** Tratamento Completo — R$ 70,00

---

## 🚀 Instruções de Instalação e Execução

Siga os passos abaixo no terminal do seu sistema operacional para clonar, configurar e rodar o projeto:

1. **Clonar o Repositório do GitHub:**
   git clone https://github.com/eng-rafaelbruno/agendamento-barbearia.git

2. **Navegar até o diretório raiz do projeto:**
   cd agendamento-barbearia

3. **Executar a aplicação:**
   python main.py

---

## 💻 Roteiro de Testes e Funcionalidades

Ao iniciar o programa com o comando acima, selecione a opção 1. Fazer Login e siga os roteiros abaixo para testar cada função do sistema:

### 🔹 1. Teste do Fluxo do Cliente
* **Acesso:** Faça login com o e-mail cliente@email.com.
* **Função 1 (Solicitar Agendamento):** Escolha o serviço, selecione um dos barbeiros e insira uma data/hora futura no formato estipulado (Ex: 18/06/2026 14:00). O sistema disparará uma simulação visual de Notificação de Lembrete via WhatsApp destinada ao cliente.
* **Função 2 e 3 (Remarcar/Cancelar):** Permite alterar o horário ou cancelar o agendamento recém-criado, atualizando dinamicamente o estado (status) da entidade.
* **Função 4 (Atualizar Contato):** Altera o telefone e e-mail em tempo de execução.
* **Saída:** Selecione a opção 5 para efetuar o Logout.

### 🔹 2. Teste do Fluxo do Barbeiro
* **Acesso:** Faça login com o e-mail rafael@barbearia.com.
* **Função 1 (Visualizar Agenda):** Lista de forma ordenada todos os agendamentos ativos vinculados estritamente a este profissional, ocultando marcações canceladas.
* **Função 2 (Consultar Comissões):** Exibe o saldo acumulado com base nos pagamentos já homologados pelo Administrador.
* **Saída:** Selecione a opção 3 para efetuar o Logout.

### 🔹 3. Teste do Fluxo do Administrador
* **Acesso:** Faça login com o e-mail admin@barbearia.com.
* **Função 1 e 2 (Cadastros):** Permite a inserção em tempo de execução de novos profissionais (Barbeiros) e novos tipos de Serviços na base de dados.
* **Função 3 (Registrar Pagamento):** Selecione o agendamento criado pelo cliente na etapa anterior e insira a forma de pagamento (pix, cartao ou dinheiro). Esta ação altera o status do agendamento para concluído e injeta o valor na contabilidade financeira.
* **Função 4 (Emitir Relatórios Operacionais):** Consolida os dados financeiros em tempo real, exibindo o Faturamento Bruto total da barbearia e a divisão exata do rateio de comissões devida a cada barbeiro pelas regras contratuais.
* **Saída:** Selecione a opção 5 para efetuar o Logout.
