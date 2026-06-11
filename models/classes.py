from datetime import datetime

class Usuario:
    def __init__(self, id_user: int, nome: str, telefone: str, email: str):
        self.id = id_user
        self.nome = nome
        self.telefone = telefone
        self.email = email
        self.logado = False

    def login(self):
        self.logado = True
        return True

    def logout(self):
        self.logado = False
        return True


class Cliente(Usuario):
    def __init__(self, id_user: int, nome: str, telefone: str, email: str, preferencias: str = "", historico: str = ""):
        super().__init__(id_user, nome, telefone, email)
        self.preferencias = preferencias
        self.historicoServicos = historico

    def cadastrarDadosContato(self, novo_telefone: str, novo_email: str):
        self.telefone = novo_telefone
        self.email = novo_email


class Barbeiro(Usuario):
    def __init__(self, id_user: int, nome: str, telefone: str, email: str, comissao: float):
        super().__init__(id_user, nome, telefone, email)
        self.agenda = []  
        self.comissao = comissao  

    def visualizarAgenda(self):
        agenda_ativa = [a for a in self.agenda if a.status != "Cancelado"]
        return sorted(agenda_ativa, key=lambda x: x.dataHora)

    def consultarComissoes(self, pagamentos_sistema):
        total_comissao = 0.0
        for pgt in pagamentos_sistema:
            if pgt.status == "Concluido" and pgt.agendamento.barbeiro.id == self.id:
                total_comissao += pgt.valor * (self.comissao / 100.0)
        return total_comissao


class Administrador(Usuario):
    def __init__(self, id_user: int, nome: str, telefone: str, email: str):
        super().__init__(id_user, nome, telefone, email)


class Servico:
    def __init__(self, id_servico: int, tipo: str, valor: float):
        self.id = id_servico
        self.tipo = tipo  
        self.valor = valor


class Agendamento:
    def __init__(self, id_agendamento: int, cliente: Cliente, barbeiro: Barbeiro, servico: Servico, data_hora: datetime):
        self.id = id_agendamento
        self.cliente = cliente
        self.barbeiro = barbeiro
        self.servico = servico
        self.dataHora = data_hora
        self.status = "Agendado"  

    def remarcar(self, nova_data_hora: datetime):
        self.dataHora = nova_data_hora
        self.status = "Remarcado"

    def cancelar(self):
        self.status = "Cancelado"

    def enviarLembrete(self):
        print(f"\n[NOTIFICAÇÃO - WhatsApp/E-mail enviado para {self.cliente.nome}]:")
        print(f"Lembrete: Seu horário para {self.servico.tipo} está confirmado para {self.dataHora.strftime('%d/%m/%Y %H:%M')}.")


class Pagamento:
    def __init__(self, id_pagamento: int, agendamento: Agendamento, metodo: str):
        self.id = id_pagamento
        self.agendamento = agendamento
        self.valor = agendamento.servico.valor
        self.metodo = metodo  
        self.status = "Concluido"
