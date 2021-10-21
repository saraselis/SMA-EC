from pade.acl.aid import AID
from pade.misc.utility import start_loop
from sys import argv

from agentes import AgentePesquisador, AgenteResposta


jogadoras = ['Benkarth', 'Sydney Lohmann', 'Giulia Gwinn', 'Zadrazil', 'Ewa Pajor']
# jogadoras = ['Zadrazil', 'Ewa Pajor']

def envia_agentes(jogadoras: list):
    """Envia agentes para procurar opinião sobre as jogadoras.
        Agentes serão enviados para cada uma das jogadoras na lista

    Args:
        jogadoras list: lista com os nomes das jogadoras
    """

    count_porta = 0
    agentes = list()

    for i in range(len(jogadoras)):
        port = int(argv[1]) + count_porta
        nome_agente_pesquisador = 'agent_pesquisador_{}@localhost:{}'.format(port, port)
        agente_pesquisador = AgentePesquisador(AID(name=nome_agente_pesquisador), jogadoras[i])
        agentes.append(agente_pesquisador)

        nome_agente_resposta = 'agent_resposta_{}@localhost:{}'.format(port - 10000, port-10000)
        agente_resposta = AgenteResposta(AID(name=nome_agente_resposta), nome_agente_pesquisador)
        agentes.append(agente_resposta)

        count_porta += 1000

    start_loop(agentes)

envia_agentes(jogadoras)

