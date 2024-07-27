# Aurora - Assistente Virtual

Este é um assistente virtual desenvolvido para ajudar nos estudos com informações sobre programação, utilizando a tecnologia Streamlit. Ele se comunica com um backend, fazendo uso de funções AWS Lambda e integrações com o banco de dados Aurora. A seguir, você encontrará informações detalhadas sobre como executar e interagir com este projeto.

## Funcionalidades

### Iniciar nova conversa.
- Ao iniciar uma nova conversa é gerado um id único que é usado como chave primaria para armazenar as conversas em um mongoDB.

### Usar exemplos de mensagens pré-definidas.
- São utilizados 3 exemplos para demonstrar ao usuario maneiras de interagir com a Aurora.
```
"Como colocar um link html em italico?"
"Para que serve a tag <pre> em HTML5?"
"O que é âncoras em HTML5?"
```

### Alternar entre diferentes fontes de conhecimento (Aurora e +A Educação).
- É possivel usar o chatbot usando apenas as informações nos dados indexados para pesquisa diponibilizado pela +A Educação ou usar todo poder da Aurora que busca informações além dos dados indexados para responder as duvidas dos usuarios.

### Identificar as principais dificuldades do usuário com base no histórico de mensagens.
- Ao interagir com a Aurora é possivel gerar insights para entender os temas mais conversados. Com isso é possivel enviar conteudos customizados para cada usuario.

## Pré-requisitos

Para executar este projeto localmente, é necessário ter o Python instalado em sua máquina. Além disso, é recomendável configurar um ambiente virtual para isolar as dependências. Certifique-se de ter acesso a um banco de dados Aurora e credenciais válidas da AWS para integração com as funções Lambda.

## Instalação

1. Clone este repositório em sua máquina local

2. Instale as dependências utilizando o gerenciador de pacotes Python, pip:
```bash
pip install -r requirements.txt
```

## Configuração

Antes de executar o projeto, é necessário configurar suas credenciais da AWS. Para isso, use o `.streamlit/secrets.toml` e defina as seguintes variáveis:
- AWS_ACCESS_KEY_ID = "SuaAccessKeyID"
- AWS_SECRET_ACCESS_KEY = "SuaSecretAccessKey"
- AWS_FUNCTION_NAME = "SuaFunctionName"
- AWS_REGION_NAME = "SuaRegião"

## Execução

Após a instalação e configuração, você pode executar o projeto utilizando o seguinte comando:
```bash
streamlit run app.py
```

## Uso

Após executar o projeto, uma interface será aberta no seu navegador padrão. Você verá a interface do assistente virtual, onde poderá interagir digitando suas perguntas na caixa de chat e enviando-as. O assistente responderá às suas perguntas com base no conhecimento disponível.

## Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir uma issue ou enviar um pull request para melhorar este projeto.

---

Com estas instruções, você poderá configurar e executar o assistente virtual +A Educação em sua máquina local. Se precisar de ajuda adicional, não hesite em entrar em contato!
