# Documentação para Desenvolvedores - Projeto Django

<br/>

## Estrutura do Projeto

O projeto Django segue a estrutura padrão, com os seguintes diretórios principais:

- *ProjectAcademPy/*: Diretório raiz do projeto.
  - *AcademPy/*: Aplicação principal do projeto.
    - *migrations/*: Arquivos de migração do banco de dados.
    - *static/*: Arquivos estáticos (CSS, JavaScript, etc.).
    - *templates/*: Templates HTML.
    - *views.py*: Arquivo contendo as views da aplicação.
    - *models.py*: Arquivo contendo os modelos de dados.
    - *urls.py*: Arquivo de configuração de URLs da aplicação.
  - *projeto_django/*: Configurações do projeto Django.

## Modelos de Dados

### Administrador

- Atributos:
  - usuario: Um usuário do Django associado ao administrador.

### Professor

- Atributos:
  - usuario: Um usuário do Django associado ao professor.
  - especializacao: Especialização do professor.
  - disponibilidade_manha, disponibilidade_tarde, disponibilidade_noite: Disponibilidade de horários do professor.

### Disciplina

- Atributos:
  - nome: Nome da disciplina.

### Cronograma

- Atributos:
  - dt_criacao: Data e hora de criação do cronograma.

### Turma

- Atributos:
  - nome: Nome da turma.
  - turno: Turno da turma (manhã, tarde, noite).

### Aula

- Atributos:
  - cronograma: Cronograma ao qual a aula está associada.
  - disciplina: Disciplina ministrada na aula.
  - professor: Professor responsável pela aula.
  - dia_semana: Dia da semana da aula (1 a 7, representando segunda a domingo).
  - turma: Turma na qual a aula será ministrada.
  - horario: Horário da aula.

## Funcionalidades Implementadas

- Cadastro de administradores e professores.
- Cadastro, edição e exclusão de disciplinas e turmas.
- Geração de cronogramas de aulas.
- Visualização do cronograma de aulas por dia da semana e turma.
- Autenticação de usuários e controle de acesso.

## Próximos Passos

- Implementar a funcionalidade de edição de cronogramas de aulas.
- Melhorar a interface do usuário para uma experiência mais intuitiva.
- Refatorar o código para seguir as melhores práticas de desenvolvimento.

## Ambiente de Desenvolvimento

Para configurar um ambiente de desenvolvimento local, siga as instruções fornecidas no arquivo README.md do projeto.

## Suporte

Para obter assistência adicional ou relatar problemas técnicos, entre em contato com a autora raf.llosilva@gmail.com

<br/><br/><br/><br/>

---

## Instruções de deploy

Faça uma pequena pesquisa sobre como fazer o [*deploy*](https://en.wikipedia.org/wiki/Software_deployment) de um projeto web com Python e Django e escreva aqui algumas orientações breves.  Fazer o *deploy* não é obrigatório para a avaliação, mas é importante que os desenvolvedores do projeto tenham ao menos uma noção de como isso é feito.

Sugestões de serviços de hospedagem para pesquisar:
* Vercell
* PythonAnywhere
* AWS Elastic Beanstalk (não recomendamos o uso deste serviço sem supervisão, pois pode gerar cobranças inesperadas)

## Modelagem de banco de dados

Coloque aqui a modelagem do banco de dados desenvolvido no projeto. Você pode colocar diagramas conceituais e lógicos, ou até mesmo descrever textualmente o que cada uma das tabelas e atributos representam. 
