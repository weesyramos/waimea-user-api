QUESTÃO 1)
Minha decisão seria usar a Clean Architecture (poderia ser também a Hexagonal, porém tenho maior conhecimento na Clean), usando Python + FastAPI.
A escolha do FastAPI é, na minha opinião, crucial para a solução do problema, pois podemos fazer requisições HTTP assíncronas. Mesmo com o enunciado sendo explícito de que o retorno precisa ser síncrono, será necessário fazer uma requisição para a API que retorna o CNPJ e outra para a que retorna o CEP, e o FastAPI é o ideal para essa solução.
Eu também escolhi dois tipos de Design Patterns, sendo eles o Circuit Breaker e o Strategy. O Circuit Breaker ficaria responsável pelas retentativas e pela chamada do fallback para o provedor B. O Strategy fica responsável por alternar entre os provedores.
A Clean Architecture é essencial pois, se for preciso mudar alguma API externa de consulta, poderemos fazer isso sem impactar em nada o restante do código, apenas implementando a nova chamada.

QUESTÃO 2)
Como a intenção é trazer o mínimo de impacto possível, eu optaria pelo disparo de um evento assíncrono para um serviço de messageria (RabbitMQ, por exemplo). Adicionaríamos poucas linhas de código e um bloco try/except para que, mesmo que o serviço de messageria ou o banco de dados fiquem inoperantes, a falha seja totalmente isolada e nunca interfira no lançamento do foguete. Essa abordagem adicionaria apenas pouquíssimos milissegundos à execução do servidor.
Uma observação importante: caso todos os dados necessários para popular o relatório já estejam presentes nos logs da aplicação, poderíamos utilizar uma captura passiva desses dados através de um serviço de observabilidade. Essa abordagem alternativa teria um impacto de zero absoluto na execução do lançamento do foguete.

QUESTÃO 3)
A primeira coisa que eu identifiquei para melhorar é a conexão com o Redis, que é feita toda vez que a rota é chamada (connection=Redis()). Acredito que isso, por si só, já inviabilizaria o teste de P99 em 30ms, pois esgotaria as portas do servidor. O ideal seria inicializar um pool de conexões na inicialização da aplicação. Dessa forma, toda a aplicação estará pronta para utilizar o Redis quando, e se, necessário.
Após essa refatoração, usaria o Locust — que é um gerador de carga em Python — para executar os testes de performance, idealmente em um ambiente espelho do servidor de produção.

QUESTÃO 4)
Primeiro problema identificado é em .config onde uma credencial está exposta. Mesmo sendo um fallback e uma credencial de desenvolvimento não é interessante expor harded-code. Ideal é que essas credenciais esteja em variáveis de ambientes locais.

Exceptions genéricas e sem retorno é um problema grande no troubleshooting (debug). 

1. A captura dessa Exception pode ser qualquer uma, não tem como saber o que deu de errado na execução do código, se foi um problema de conexão com o banco, um erro de configuração ou um timeout, por exemplo.

2. Aqui o ponto de maior falha desse trecho de código: Não está sendo logado nenhum erro. Simplesmente a aplicação retorna um False e não trará nenhum beneficio na hora de debbugar o ocorrido. O certo é fazer algo como um logger.exception(e) no mínimo.

Também achei estranho já nessa estrutura existir um manager.py. Analisando o arquivo, vi que ele implementa um Orchestrator, mas nesse caso não vejo uma necessidade real para essa camada. O método simplesmente acessa o repository, enquanto já existe um RegistrationService para essa responsabilidade. Então acaba sendo criada uma abstração a mais sem necessidade, aumentando a complexidade da aplicação. Mesmo pensando que o projeto possa crescer no futuro, eu prefiro criar esse tipo de camada quando existir uma necessidade concreta de orquestrar várias etapas ou serviços, e não antecipadamente. 

QUESTÃO 6)
1.Credenciais do banco

As credenciais do banco estão diretamente no código-fonte. Seria melhor utilizar variáveis de ambiente ou algum mecanismo de secrets, evitando que usuário e senha fiquem expostos no código e no histórico do Git.

2.Exportação da senha

O `SELECT * FROM users` também traz o campo de senha, que depois é colocado no arquivo Excel. Mesmo que seja um hash, não parece necessário exportar esse tipo de informação. Eu deixaria apenas os campos realmente necessários.

3.Volume de dados

O robô busca todos os usuários de uma vez com `SELECT * FROM users`. Isso pode funcionar com poucos registros, mas pode causar problemas de memória e desempenho conforme a tabela crescer. Seria interessante processar os dados em lotes ou utilizar streaming.

4.Geração dos arquivos

A rotina gera um novo arquivo a cada execução, sem nenhuma política para excluir ou arquivar os arquivos antigos. Com o tempo, isso pode ocupar bastante espaço em disco. Seria interessante definir uma política de retenção para esses arquivos.

QUESTÃO 7)
Minha escolha certamente é o Adapter Pattern, dessa forma cria uma interface única de comunicação com serviços externos. Sendo assim, cada fornecedor teria seu proprio adapter mas com uma mesma interface.
