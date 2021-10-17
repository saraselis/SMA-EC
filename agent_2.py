from pade.misc.utility import display_message, start_loop
from pade.core.agent import Agent
from pade.acl.aid import AID
from sys import argv
from icecream import ic
from pade.behaviours.protocols import TimedBehaviour
from pade.acl.messages import ACLMessage
from pade.behaviours.protocols import FipaRequestProtocol
import datetime


import twitter
from icecream import ic


def procura_opniao(nome: str, qtd: int) -> dict:
    api = twitter.Api(consumer_key='DZrBY0sLDabOHA4kamFXUE9Fv',
                        consumer_secret='ROCiQ1lCwANaRoyba6Rd8ySOfLGTBN45FFXjaQGuyzUYx5cVsu',
                        access_token_key='1412833284799840264-Birb2frgY83nL1AHz66l5kMTKEzgvb',
                        access_token_secret='dOAfIfrn505qoXI2Apq5impWc3fVlLAfW0Sd6myzMJ1iV')

    response = api.GetSearch(term=nome, result_type='recent', count=qtd)

    tweets = {}

    for i in response:
        tweets[i.__getattribute__('id_str')] = {
            'nome_conta' : i.__getattribute__('in_reply_to_screen_name'),
            'tweet' : i.__getattribute__('text').replace("\n", ""),
            'data': i.__getattribute__('created_at')
        }

    return tweets


class ComportamentoVendedor(FipaRequestProtocol):
    """FIPA Request Behaviour of the Time agent.
    """
    def __init__(self, agent, nome):
        super(ComportamentoVendedor, self).__init__(agent=agent,
                                          message=None,
                                          is_initiator=False)

        self.produtos = procura_opniao(nome, 1)

        
    def handle_request(self, message):
        # 'age qnd recebe uma fipa request'
        super(ComportamentoVendedor, self).handle_request(message)
        display_message(self.agent.aid.localname, self.produtos)
        # now = datetime.now()
        reply = message.create_reply()
        reply.set_performative(ACLMessage.INFORM)
        reply.set_content(str(self.produtos[list(self.produtos.keys())[0]]['nome_conta']))
        self.agent.send(reply)

class ComportamentoComprador(FipaRequestProtocol):
    def __init__(self, agent, message):
        super(ComportamentoComprador, self).__init__(agent=agent, message=message, is_initiator=True)

    def handle_inform(self, message):
        display_message(self.agent.aid.localname, message.content)

class ComportamentoTemporal(TimedBehaviour):
    def __init__(self, agent, time, message):
        super(ComportamentoTemporal, self).__init__(agent, time)

        self.message = message

    def on_time(self):
        super(ComportamentoTemporal, self).on_time()
        self.agent.send(self.message)


class AgenteVendedor(Agent):
    def __init__(self, aid, nome):
        super(AgenteVendedor, self).__init__(aid=aid)
        self.comport_request = ComportamentoVendedor(self, nome)
        self.behaviours.append(self.comport_request)

class AgenteComprador(Agent):
    def __init__(self, aid, recebedor):
        super(AgenteComprador, self).__init__(aid=aid)
        mensagem = ACLMessage(ACLMessage.REQUEST)
        mensagem.set_protocol(ACLMessage.FIPA_REQUEST_PROTOCOL)
        mensagem.add_receiver(AID(name=recebedor))
        mensagem.set_content('Me da um dinheiro aiii')

        self.comport_request = ComportamentoComprador(self, mensagem)
        self.comport_temp = ComportamentoTemporal(self, 10.0, mensagem)
        self.behaviours.append(self.comport_request)
        self.behaviours.append(self.comport_temp)

jogadoras = ['Benkarth', 'Magull']

def envia_agentes(jogadoras):
    agents_per_process = 1
    c = 0
    agents = list()
    for i in range(len(jogadoras)):
        ic(i)
        port = int(argv[1]) + c
        nome_agent_vendedor = 'agent_vendedor_{}@localhost:{}'.format(port, port)
        agente_vendedor = AgenteVendedor(AID(name=nome_agent_vendedor), jogadoras[i])
        agents.append(agente_vendedor)

        nome_agent_comprador = 'agent_comprador_{}@localhost:{}'.format(port - 10000, port-10000)
        agente_comprador = AgenteComprador(AID(name=nome_agent_comprador), nome_agent_vendedor)
        agents.append(agente_comprador)


        c += 1000


    start_loop(agents)

envia_agentes(jogadoras)

# if __name__ == '__main__':

#     agents_per_process = 1
#     c = 0
#     agents = list()
#     for i in range(agents_per_process):
#         port = int(argv[1]) + c
#         nome_agent_vendedor = 'agent_vendedor_{}@localhost:{}'.format(port, port)
#         agente_vendedor = AgenteVendedor(AID(name=nome_agent_vendedor), 'Benkarth')
#         agents.append(agente_vendedor)

#         nome_agent_comprador = 'agent_comprador_{}@localhost:{}'.format(port - 10000, port-10000)
#         agente_comprador = AgenteComprador(AID(name=nome_agent_comprador), nome_agent_vendedor)
#         agents.append(agente_comprador)


#         c += 1000


#     start_loop(agents)