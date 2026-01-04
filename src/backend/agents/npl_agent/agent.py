from google.adk.agents.llm_agent import Agent
# from google.adk.agents import AgentServer
from pydantic import BaseModel, Field

class TargetModel(BaseModel):
    name: str = Field(description="nome da pessoa alvo")
    type: str = Field(description="tipo de pessoa alvo")
    description: str = Field(description="descrição da pessoa alvo")

class EventModel(BaseModel):
    type: str = Field(description="tipo de compromisso (consulta médica, reunião, aniversário, etc)")
    name: str = Field(description="nome do evento")
    description: str = Field(description="descrição do evento")
    date: str = Field(description="data do evento")
    time: str = Field(description="horário do evento")
    target: TargetModel = Field(description="informações da pessoa alvo participante/aniversariante/empresa (caso tenha o nome, descrição)")
    location: str = Field(description="local do evento")
    
npl_agent = Agent(
    model='gemini-2.0-flash-001',
    name='npl_agent',
    description='Um conversor de texto para objeto json',
    instruction="""
    Você é um conversor de texto para objeto json. 
    Você receberá um texto de um agendamento de compromisso (reunião, consulta médica, aniversário, etc) e a data e horário atual.

    Regras para data (Obrigatório): 
    A data e horário informados no início da mensagem são a ÚNICA referência temporal válida. 
    Você DEVE usar essa data como base para inferir datas relativas quando o usuário não informar uma data explícita.
    Exemplos de data relativa:
        - "hoje": use a data base informada
        - "amanhã": data base + 1 dia
        - "depois de amanhã": data base + 2 dias
        - "daqui a N dias": data base + N dias
        - "próxima sexta", "próxima segunda", etc

    Caso nenhuma data relativa ou explícita seja informada, você deve usar a data base informada.
    Caso nenhum horário relativo ou explícito seja informado, você deve usar o horário da data base informada.

    Regras para a extração de dados do agendamento (Obrigatório):    
    Você recebe um texto e extrai os dados necessários para um agendamento de compromisso.
    O texto pode conter linguagem coloquial, erros de ortografia, etc, você deve entender o contexto e extrair as informações necessárias.
    Ignore informações que não sejam relevantes para o agendamento de compromisso, como saudações, agradecimentos, etc.
    Você monta um objeto json com as informações extraídas.
    Você vai extrair os seguintes campos:
    - tipo de compromisso (consulta médica, reunião, aniversário, etc)
    - data do evento
        - Converta a data para o formato YYYY-MM-DD.
    - horário  
        - Converta o horário para o formato HH:MM.
    - informações da pessoa alvo participante/aniversariante/empresa (caso tenha o nome, descrição)
        As informações da pessoa alvo "target" serão: 
        name - o nome da pessoa alvo, 
        type - o tipo, esse você vai gerar de acordo com o evento. Exemplo: se o evento for um aniversário, o tipo será "aniversariante". Se for uma reunião, o tipo será "empresa" ou "chefe". e o target name o nome da empresa ou chefe. 
        description - a descrição da pessoa alvo, por exemplo características do aniversariante ou da empresa.
    - local do evento (caso tenha o local)
    - descrição do evento (caso tenha a descrição).

    Essa regra é muito importante. Você não deve retornar nenhum outro texto além do objeto json, a única coisa que pode ser retornada é o objeto json.

    """,
    output_schema=EventModel,
    output_key="event_model"
)

# if __name__ == "__main__":
#     print("Iniciando o servidor do npl_agent na porta 8080...")
#     server = AgentServer(agent=npl_agent, port=8080)
#     server.run()
root_agent = npl_agent
