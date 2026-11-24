# Routine Organizer

O Routine Organizer é uma aplicação web desenvolvida para facilitar o planejamento da rotina diária, unindo usabilidade moderna ao uso prático de estruturas de dados. O projeto tem como núcleo uma Árvore Binária de Busca (ABB) implementada manualmente em Python, responsável por organizar os compromissos do usuário em ordem cronológica e evitar conflitos de horário.

## Sobre o Software

Diferente de agendas convencionais que delegam a ordenação diretamente ao banco de dados, o sistema carrega as tarefas do período em uma estrutura `BinaryTree` própria no backend. Cada atividade é indexada a partir do seu horário de início convertido em minutos inteiros (`time_key`, onde `08:30` equivale a `510`).

A partir dessa estrutura, o software realiza:
- **Ordenação automática:** utiliza o percurso *in-order* da árvore para devolver as atividades sempre em ordem cronológica.
- **Prevenção de conflitos:** impede o agendamento de duas tarefas no mesmo dia e horário.
- **Busca e remoção eficientes:** localiza tarefas por horário e trata os três casos clássicos de remoção em árvores binárias (nó folha, um filho e dois filhos).
- **Cálculo de tempo livre:** identifica automaticamente os intervalos disponíveis entre o término de uma atividade e o início da próxima.

Além do organizador principal, a aplicação conta com controle de acesso baseado em perfis via JWT. Usuários padrão têm acesso completo ao gerenciamento de rotina e caixa de entrada, enquanto o perfil especial desbloqueia módulos personalizados de contagem regressiva, declarações interativas com quiz e citações literárias.

## Funcionalidades

- **Gestão de Rotina:** Cadastro, edição, marcação de conclusão com destaque visual e exclusão de tarefas.
- **Múltiplas Visualizações:** Alternância entre linha do tempo diária, grade semanal e calendário mensal, com navegação rápida entre datas.
- **Caixa de Entrada (Inbox):** Espaço para anotar tarefas sem horário definido e agendá-las na rotina quando necessário.
- **Autenticação e Permissões:** Registro e login com token JWT, protegendo rotas exclusivas diretamente no backend.
- **Experiência de Uso:** Interface responsiva em português, alternância entre temas claro e escuro e suporte a PWA (`manifest.json`).

## Tecnologias

- **Backend:** Python, FastAPI, SQLAlchemy, SQLite, PyJWT e Uvicorn.
- **Frontend:** HTML5, CSS3, Bootstrap 5.3 e JavaScript.
