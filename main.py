import sys
from datetime import datetime
from models.classes import Cliente, Barbeiro, Administrador, Servico, Agendamento, Pagamento

#  BASE DE DADOS EM MEMÓRIA
usuarios = [
    Administrador(1, "Lucas Ferreira (Admin)", "62999999999", "admin@barbearia.com"),
    Barbeiro(2, "Rafael Bruno", "62988888888", "rafael@barbearia.com", comissao=40.0),
    Barbeiro(3, "Lucas Silvério", "62977777777", "lucas@barbearia.com", comissao=35.0),
    Cliente(4, "Lars", "62966666666", "cliente@email.com", preferencias="Cabelo Degradê", historico="Corte antigo em 10/04")
]

servicos = [
    Servico(1, "Corte", 45.00),
    Servico(2, "Barba", 30.00),
    Servico(3, "Tratamento Completo", 70.00)
]

agendamentos = []
pagamentos = []

# FUNÇÕES AUXILIARES DE CONTROLE 
def buscar_usuario_por_email(email):
    for u in usuarios:
        if u.email.lower() == email.strip().lower():
            return u
    return None

def verificar_choque_horario(barbeiro, data_hora):
    for ag in agendamentos:
        if ag.barbeiro.id == barbeiro.id and ag.status != "Cancelado":
            diferenca = abs((ag.dataHora - data_hora).total_seconds() / 60)
            if diferenca < 30:
                return True
    return False

#  MENUS INTERATIVOS
def menu_cliente(cliente):
    global agendamentos
    while True:
        print(f"\nPAINEL DO CLIENTE: {cliente.nome}")
        print("1. Solicitar Agendamento")
        print("2. Remarcar Agendamento")
        print("3. Cancelar Agendamento")
        print("4. Atualizar Dados de Contato")
        print("5. Fazer Logout")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            print("\n--- Serviços Disponíveis ---")
            for s in servicos:
                print(f"[{s.id}] {s.tipo} - R$ {s.valor:.2f}")
            try:
                id_serv = int(input("ID do Serviço: "))
                serv = next((s for s in servicos if s.id == id_serv), None)

                print("\n--- Barbeiros Disponíveis ---")
                barbeiros = [u for u in usuarios if isinstance(u, Barbeiro)]
                for b in barbeiros:
                    print(f"[{b.id}] {b.nome}")
                id_barb = int(input("ID do Barbeiro: "))
                barb = next((b for b in barbeiros if b.id == id_barb), None)

                if not serv or not barb:
                    print("Serviço ou Barbeiro inválido!")
                    continue

                data_str = input("Digite a data e hora (DD/MM/AAAA HH:MM): ")
                dt_agendamento = datetime.strptime(data_str, "%d/%m/%Y %H:%M")
                if verificar_choque_horario(barb, dt_agendamento):
                    print("Erro: Este barbeiro já possui um agendamento nesse horário!")
                    continue
                
                novo_id = len(agendamentos) + 1
                novo_ag = Agendamento(novo_id, cliente, barb, serv, dt_agendamento)
                agendamentos.append(novo_ag)
                barb.agenda.append(novo_ag)
                print(f"Sucesso: Agendamento #{novo_id} solicitado!")
                novo_ag.enviarLembrete()
            except ValueError:
                print("Entrada ou formato de data inválido!")

        elif opcao == "2":
            meus_ag = [a for a in agendamentos if a.cliente.id == cliente.id and a.status != "Cancelado"]
            if not meus_ag:
                print("Você não possui agendamentos ativos.")
                continue
            for a in meus_ag:
                print(f"[{a.id}] {a.servico.tipo} com {a.barbeiro.nome} em {a.dataHora.strftime('%d/%m/%Y %H:%M')} ({a.status})")
            
            try:
                id_ag = int(input("ID do Agendamento para remarcar: "))
                ag = next((a for a in meus_ag if a.id == id_ag), None)
                if ag:
                    nova_data_str = input("Nova data e hora (DD/MM/AAAA HH:MM): ")
                    nova_dt = datetime.strptime(nova_data_str, "%d/%m/%Y %H:%M")
                    if verificar_choque_horario(ag.barbeiro, nova_dt):
                        print("Erro: Horário indisponível para este barbeiro!")
                        continue
                    ag.remarcar(nova_dt)
                    print("Agendamento remarcado com sucesso!")
                    ag.enviarLembrete()
                else:
                    print("ID inválido.")
            except ValueError:
                print("Entrada inválida!")

        elif opcao == "3":
            meus_ag = [a for a in agendamentos if a.cliente.id == cliente.id and a.status != "Cancelado"]
            if not meus_ag:
                print("Você não possui agendamentos para cancelar.")
                continue
            for a in meus_ag:
                print(f"[{a.id}] {a.servico.tipo} em {a.dataHora.strftime('%d/%m/%Y %H:%M')}")
            try:
                id_ag = int(input("ID do Agendamento para cancelar: "))
                ag = next((a for a in meus_ag if a.id == id_ag), None)
                if ag:
                    ag.cancelar()
                    print("Agendamento cancelado com sucesso.")
                else:
                    print("ID não encontrado.")
            except ValueError:
                print("ID inválido.")

        elif opcao == "4":
            tel = input("Novo Telefone: ")
            email = input("Novo E-mail: ")
            cliente.cadastrarDadosContato(tel, email)
            print("Dados updated com sucesso!")

        elif opcao == "5":
            cliente.logout()
            print("Logout efetuado.")
            break


def menu_barbeiro(barbeiro):
    while True:
        print(f"\n--- PAINEL DO BARBEIRO: {barbeiro.nome} ---")
        print("1. Visualizar Minha Agenda")
        print("2. Consultar Minhas Comissões")
        print("3. Fazer Logout")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            agenda = barbeiro.visualizarAgenda()
            if not agenda:
                print("Sua agenda está vazia para os próximos dias.")
            else:
                print("\n--- Seus Horários Marcados ---")
                for ag in agenda:
                    print(f"[{ag.dataHora.strftime('%d/%m/%Y %H:%M')}] Cliente: {ag.cliente.nome} | Serviço: {ag.servico.tipo} | Status: {ag.status}")

        elif opcao == "2":
            comissao_total = barbeiro.consultarComissoes(pagamentos)
            print(f"\nSeu saldo atual acumulado de comissões é: R$ {comissao_total:.2f} (Taxa: {barbeiro.comissao}%)")

        elif opcao == "3":
            barbeiro.logout()
            print("Logout efetuado.")
            break


def menu_administrador(admin):
    global servicos, usuarios, pagamentos, agendamentos
    while True:
        print(f"\nPAINEL DO ADMINISTRADOR")
        print("1. Cadastrar/Gerenciar Serviços")
        print("2. Cadastrar/Gerenciar Usuários")
        print("3. Registrar Pagamento / Baixa de Agendamento")
        print("4. Emitir Relatórios Operacionais")
        print("5. Fazer Logout")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            print("\n[1] Listar  [2] Adicionar Novo")
            sub = input("Escolha: ")
            if sub == "1":
                for s in servicos:
                    print(f"ID: {s.id} | {s.tipo} - R$ {s.valor:.2f}")
            elif sub == "2":
                tipo = input("Tipo do Serviço (ex: Sobrancelha): ")
                val = float(input("Valor do Serviço: R$ "))
                novo_id = len(servicos) + 1
                servicos.append(Servico(novo_id, tipo, val))
                print("Serviço cadastrado com sucesso!")

        elif opcao == "2":
            print("\n[1] Listar Todos  [2] Cadastrar Novo Barbeiro")
            sub = input("Escolha: ")
            if sub == "1":
                for u in usuarios:
                    tipo_u = type(u).__name__
                    print(f"ID: {u.id} | Nome: {u.nome} | Tipo: {tipo_u} | Email: {u.email}")
            elif sub == "2":
                nome = input("Nome do Barbeiro: ")
                tel = input("Telefone: ")
                email = input("Email de Acesso: ")
                comis = float(input("Porcentagem de comissão (ex: 40): "))
                novo_id = len(usuarios) + 1
                usuarios.append(Barbeiro(novo_id, nome, tel, email, comis))
                print(f"Barbeiro {nome} cadastrado!")

        elif opcao == "3":
            ag_abertos = [a for a in agendamentos if a.status in ["Agendado", "Remarcado"]]
            if not ag_abertos:
                print("Nenhum agendamento pendente de finalização.")
                continue
            
            print("\n--- Selecione o Agendamento Concluído ---")
            for a in ag_abertos:
                print(f"[{a.id}] Cliente: {a.cliente.nome} | {a.servico.tipo} com {a.barbeiro.nome} - R$ {a.servico.valor:.2f}")
            
            try:
                id_ag = int(input("ID do Agendamento realizado: "))
                ag = next((a for a in ag_abertos if a.id == id_ag), None)
                if ag:
                    metodo = input("Forma de pagamento (pix / cartao / dinheiro): ").strip().lower()
                    if metodo not in ['pix', 'cartao', 'dinheiro']:
                        print("Método inválido.")
                        continue
                    
                    novo_pg_id = len(pagamentos) + 1
                    novo_pg = Pagamento(novo_pg_id, ag, metodo)
                    pagamentos.append(novo_pg)
                    
                    ag.status = "Concluido"
                    print(f"Pagamento de R$ {novo_pg.valor:.2f} registrado! Caixa atualizado.")
                else:
                    print("Agendamento inválido.")
            except ValueError:
                print("ID inválido.")

        elif opcao == "4":
            print("\n RELATÓRIO CONSOLIDADO ")
            faturamento = sum(p.valor for p in pagamentos)

            print(f"Faturamento Total Bruto: R$ {faturamento:.2f}")
            print(f"Quantidade de Atendimentos Realizados: {len(pagamentos)}")
            print(f"Agendamentos Cancelados/Perdidos: {len([a for a in agendamentos if a.status == 'Cancelado'])}")
            print("-------------------------------------")
            print("Comissões a pagar por Barbeiro:")
            
            barbeiros = [u for u in usuarios if isinstance(u, Barbeiro)]
            for b in barbeiros:
                print(f" - {b.nome}: R$ {b.consultarComissoes(pagamentos):.2f}")
            print("=====================================")

        elif opcao == "5":
            admin.logout()
            print("Logout efetuado.")
            break


def iniciar_sistema():
    while True:
        print("\nSISTEMA DE GERENCIAMENTO BARBEARIA")
        print("1. Fazer Login")
        print("2. Sair do Programa")
        escolha = input("Selecione uma opção: ")

        if escolha == "1":
            email_input = input("Digite seu e-mail de acesso: ")
            user = buscar_usuario_por_email(email_input)

            if user:
                user.login()
                print(f"\n✓ Login bem-sucedido! Bem-vindo, {user.nome}.")
                
                if isinstance(user, Administrador):
                    menu_administrador(user)
                elif isinstance(user, Barbeiro):
                    menu_barbeiro(user)
                elif isinstance(user, Cliente):
                    menu_cliente(user)
            else:
                print("Erro: E-mail não cadastrado no sistema.")

        elif escolha == "2":
            print("Fechando o sistema. Até logo!")
            sys.exit()
        else:
            print("Opção inválida!")


if __name__ == "__main__":
    iniciar_sistema()
