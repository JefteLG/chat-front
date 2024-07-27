import streamlit as st
import streamlit_chat
import uuid
import boto3
import json

def lambda_aws(user_menssage, user_id, aurora_knowledge):
    aws_access_key_id = st.secrets["AWS_ACCESS_KEY_ID"]
    aws_secret_access_key = st.secrets["AWS_SECRET_ACCESS_KEY"]
    region_name = st.secrets["REGION_NAME"]
    function_name = st.secrets["AWS_FUNCTION_NAME"]
    
    session = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region_name
    )

    lambda_client = session.client('lambda')

    payload = {
        "input": user_menssage,
        "user_id": user_id,
        "gaps_knowledge": True if user_menssage == "gaps_knowledge" else False,
        "aurora_knowledge": "mais_educa" if aurora_knowledge == "mais_educa" else "aurora"
    }

    response = lambda_client.invoke(
        FunctionName=function_name,
        InvocationType='RequestResponse',
        LogType='Tail',
        Payload=json.dumps(payload)
    )

    result = json.loads(response['Payload'].read().decode('utf-8'))
    return result

example_user_prompts = [
    "Como colocar um link html em italico?",
    "Para que serve a tag <pre> em HTML5?",
    "O que é âncoras em HTML5?",
]


def stick_it_good():
    # make header sticky.
    st.markdown(
        """
            <div class='fixed-header'/>
            <style>
                div[data-testid="stVerticalBlock"] div:has(div.fixed-header) {
                    position: sticky;
                    top: 2.875rem;
                    z-index: 999;
                }
                .fixed-header {
                    border-bottom: 1px solid black;
                }
            </style>
        """,
        unsafe_allow_html=True
    )


def userid_change():
    st.session_state.userid = str(uuid.uuid4())
    
    
def complete_messages(nbegin,nend, user_message):
    sleep_msg = f"Aguardando {nbegin}/{nend} respostas da Aurora." if nend > 1 else f"Aguardando resposta da Aurora."
    with st.spinner(sleep_msg):        
        response = lambda_aws(user_message, st.session_state.userid, st.session_state.aurora_scope)
        if response.get("status_code") and response.get("status_code") == 200:
            st.session_state.erro_400 = 1
            if response.get("body").get("output") == "0_0":
                response_content = "Percebi que ainda não tivemos a chance de conversar. Para que eu possa entender melhor como ajudar você, seria ótimo começarmos uma conversa. 😊"
            else:
                response_content = response.get("body").get("output")
        elif response.get("status_code") == 400:
            if st.session_state.erro_400 == 1:
                response_content = "Desculpe, estou um pouco confuso com sua mensagem. Seria possível explicar de uma maneira diferente?"
            elif st.session_state.erro_400 == 2:
                response_content = "Parece que estou tendo dificuldades para entender sua solicitação. Poderia fornecer mais detalhes para que eu possa ajudar melhor?"
            else:
                response_content = "Ainda estou tendo problemas para entender. Recomendo que entre em contato com meu criador pelo e-mail jefte.job@gmail.com ou pelo telefone (63) 9 9998-9241 para relatar o problema em detalhes. Ele ficará felize em ajudar você a resolver essa questão."
            st.session_state.erro_400 = st.session_state.erro_400 + 1
        else:
            response_content = "Identifiquei um problema temporário em nossos serviços que pode estar afetando sua experiência. Peço desculpas pelo inconveniente. Por favor, entre em contato com meu criado para relatar os detalhes do ocorrido. Email: jefte.job@gmail.com ou telefone: (63) 9 9998-9241. Agradecemos sua colaboração e compreensão."

    return response_content

def select_aurora_power(power):
    st.session_state.aurora_scope = power
    

def main():
    st.set_page_config(
        page_title="+A Educação",
        page_icon="🅰️",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    if "messages" not in st.session_state:
        st.session_state.messages = []
        
    with st.container():
        st.title("Assitente +A Educação")
        stick_it_good()

    if "userid" not in st.session_state:
        userid_change()
        select_aurora_power("mais_educa")
        st.session_state.erro_400 = 1
        streamlit_chat.message("Nova Conversa Iniciada.",key='msg'+str(uuid.uuid4()), seed=2)
        streamlit_chat.message("Olá! ✨ Sou a Aurora, a assistente virtual da +A Educação! Estou aqui para tornar seus estudos mais fáceis! Como posso ajudar você hoje?",key='msg'+str(uuid.uuid4()),seed=2)
        streamlit_chat.message("Se quiser conferir alguns exemplos de interação, basta clicar no botão **Exemplos de Mensagens**! Estou aqui de prontidão para ajudar você nos estudos. 💫",key='msg'+str(uuid.uuid4()),seed=2)

    st.sidebar.text_input("User ID", value=st.session_state.userid, key='userid_text', disabled=True)

    if st.sidebar.button("Nova Conversa", key='clear_chat_button'):
        st.session_state.messages = []
        userid_change()
        select_aurora_power("mais_educa")
        st.session_state.messages.append({"role": "assistant", "content": "Nova Conversa Iniciada."})
        

    if st.sidebar.button("Exemplos de Mensagens", key='show_example_conversation'):
        st.session_state.messages = []
        userid_change()
        streamlit_chat.message("Nova Conversa Iniciada.",key='msg'+str(uuid.uuid4()),seed=2)
        for i,up in enumerate(example_user_prompts):
            st.session_state.messages.append({"role": "user", "content": up})
            assistant_content = complete_messages(i,len(example_user_prompts),up)
            st.session_state.messages.append({"role": "assistant", "content": assistant_content})
    for i,message in enumerate(st.session_state.messages):
        if message["role"] == "user":
            streamlit_chat.message(message["content"], is_user=True, key='msg'+str(uuid.uuid4()), seed=7)
        else:
            streamlit_chat.message(message["content"], is_user=False, key='msg'+str(uuid.uuid4()), seed=2)


    if st.sidebar.button("Usar todo poder da Aurora", key='power_aurora'):
        select_aurora_power("aurora")
        aurora_power_msg = "A partir deste momento, estarei aplicando todo o conhecimento adquirido da Aurora."
        streamlit_chat.message(
            aurora_power_msg,
            key='msg'+str(uuid.uuid4()), seed=2
        )
        st.session_state.messages.append({"role": "assistant", "content": aurora_power_msg})


    if st.sidebar.button("Usar apenas os dados da +A educação", key='power_mais_educa'):
        st.session_state.messages = []
        userid_change()
        select_aurora_power("mais_educa")
        st.session_state.messages.append({"role": "assistant", "content": "Nova Conversa Iniciada."})
        streamlit_chat.message("Nova Conversa Iniciada.",key='msg'+str(uuid.uuid4()), seed=2)
        aurora_power_msg = "A partir deste ponto, usarei apenas os conhecimentos da +A Educação para melhorar sua experiência."
        streamlit_chat.message(
            aurora_power_msg,
            key='msg'+str(uuid.uuid4()),
            seed=2
        )
        st.session_state.messages.append({"role": "assistant", "content": aurora_power_msg})


    if st.sidebar.button("Mostrar Principais Dificuldades do Usuario", key='show_user_difficulties'):
        show_user_difficulties_msg_ = "Aguarde um momento enquanto verifico seu histórico de mensagens para identificar as áreas em que posso ajudar melhor."
        streamlit_chat.message(
            show_user_difficulties_msg_,
            key='msg'+str(uuid.uuid4()),
            seed=2
        )
        st.session_state.messages.append({"role": "assistant", "content": show_user_difficulties_msg_})
        assistant_content = complete_messages(0, 1, "gaps_knowledge")
        streamlit_chat.message(assistant_content, key='msg'+str(uuid.uuid4()), seed=2)
        st.session_state.messages.append({"role": "assistant", "content": assistant_content})


    if user_content := st.chat_input("Type your question here."): # using streamlit's st.chat_input because it stays put at bottom, chat.openai.com style.
        streamlit_chat.message(user_content, is_user=True, key='msg'+str(uuid.uuid4()), seed=7)
        st.session_state.messages.append({"role": "user", "content": user_content})
        assistant_content = complete_messages(0, 1, user_content)
        streamlit_chat.message(assistant_content, key='msg'+str(uuid.uuid4()),seed=2)
        st.session_state.messages.append({"role": "assistant", "content": assistant_content})
        #len(st.session_state.messages)


if __name__ == '__main__':
    main()

