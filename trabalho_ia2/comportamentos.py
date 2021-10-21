from icecream import ic
from pade.misc.utility import display_message
from pade.behaviours.protocols import TimedBehaviour
from pade.acl.messages import ACLMessage
from pade.behaviours.protocols import FipaRequestProtocol

from procurar_opniao import procura_opniao


class ComportamentoPesquisador(FipaRequestProtocol):
    '''Definindo o comportamento do pesquisador.'''
    def __init__(self, agent, nome):
        super(ComportamentoPesquisador, self).__init__(agent=agent,
                                          message=None,
                                          is_initiator=False)
        self.tweets = procura_opniao(nome, 1)

    def handle_request(self, message):
        super(ComportamentoPesquisador, self).handle_request(message)
        display_message(self.agent.aid.localname, self.tweets)
        resp = message.create_reply()
        resp.set_performative(ACLMessage.INFORM)

        if len(self.tweets) > 0:
            resp.set_content(str(self.tweets[list(self.tweets.keys())[0]]['nome_conta']))
        else:
            print('**************')
            print(self.tweets)
            resp.set_content(str(self.tweets))

        self.agent.send(resp)

class ComportamentoResposta(FipaRequestProtocol):
    '''Definindo comportamento do Agente de resposta'''
    def __init__(self, agent, message):
        super(ComportamentoResposta, self).__init__(agent=agent, message=message, is_initiator=True)

    def handle_inform(self, message):
        display_message(self.agent.aid.localname, message.content)

class ComportamentoTemporal(TimedBehaviour):
    '''Definindo comportamento de tempo, quanto tempo os agentes serão acionados.'''
    def __init__(self, agent, time, message):
        super(ComportamentoTemporal, self).__init__(agent, time)
        self.message = message

    def on_time(self):
        super(ComportamentoTemporal, self).on_time()
        self.agent.send(self.message)