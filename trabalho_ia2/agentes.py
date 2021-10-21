from pade.core.agent import Agent
from pade.acl.aid import AID
from pade.acl.messages import ACLMessage

from comportamentos import ComportamentoPesquisador, ComportamentoResposta, ComportamentoTemporal


class AgentePesquisador(Agent):
    '''Agente que pesquisará os tweets.'''
    def __init__(self, aid, nome):
        super(AgentePesquisador, self).__init__(aid=aid)
        self.comport_request = ComportamentoPesquisador(self, nome)
        self.behaviours.append(self.comport_request)

class AgenteResposta(Agent):
    '''Agente que responderá.'''
    def __init__(self, aid, recebedor):
        super(AgenteResposta, self).__init__(aid=aid)
        mensagem = ACLMessage(ACLMessage.REQUEST)
        mensagem.set_protocol(ACLMessage.FIPA_REQUEST_PROTOCOL)
        mensagem.add_receiver(AID(name=recebedor))
        mensagem.set_content('Tem algum tweet aí?')

        self.comport_request = ComportamentoResposta(self, mensagem)
        self.comport_temp = ComportamentoTemporal(self, 10.0, mensagem)
        self.behaviours.append(self.comport_request)
        self.behaviours.append(self.comport_temp)