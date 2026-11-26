from app.core.database import SessionLocal
from app.core.security import hash_password
from app.countdown.models import Countdown
from app.declarations.models import Declaration
from app.romance.models import RomanceQuote
from app.users.models import User


def seed_database() -> None:
    db = SessionLocal()
    try:
        if db.query(User).first():
            return

        standard_user = User(
            name="demo",
            email="demo@routine.app",
            password_hash=hash_password("demo123"),
            is_special=False,
        )
        special_user = User(
            name="Maria Fernanda",
            email="mariafernandaalvesreis944@gmail.com",
            password_hash=hash_password("Maria123"),
            is_special=True,
        )
        db.add_all([standard_user, special_user])
        db.commit()
        db.refresh(special_user)

        countdown = Countdown(
            user_id=special_user.id,
            title="Até Nosso Próximo Encontro",
            target_date="2026-12-20",
        )
        db.add(countdown)

        declarations = [
            Declaration(
                user_id=special_user.id,
                question="Em qual mês começamos a namorar?",
                expected_answer="setembro|9|09|mes 9|nono mes",
                content="Setembro trouxe a primavera, mas foi você quem floresceu a minha vida inteira. Desde então, virou oficialmente o meu mês favorito no calendário.",
                is_unlocked=False,
            ),
            Declaration(
                user_id=special_user.id,
                question="Qual é o dia exato do nosso aniversário de namoro?",
                expected_answer="29|vinte e nove|dia 29|29/09|29 de setembro",
                content="Dia 29 deixou de ser só mais uma data comum para virar o lembrete de que escolher você foi a melhor decisão da minha vida.",
                is_unlocked=False,
            ),
            Declaration(
                user_id=special_user.id,
                question="Quem disse 'eu te amo' primeiro?",
                expected_answer="lelio|voce|vc|lelio roberto",
                content="Fui eu mesmo! E se eu pudesse voltar no tempo, diria de novo ainda mais cedo — porque amar você sempre foi fácil demais para guardar só para mim.",
                is_unlocked=False,
            ),
            Declaration(
                user_id=special_user.id,
                question="Qual é o meu time de futebol?",
                expected_answer="flamengo|mengao|fla|crf",
                content="Sou Flamengo de coração, mas pode ficar tranquila: no meu peito você é titular absoluta, camisa 10 e a única que me faz vibrar todos os dias.",
                is_unlocked=False,
            ),
            Declaration(
                user_id=special_user.id,
                question="Qual é o sabor de pizza que a gente sempre pede?",
                expected_answer="bacon|de bacon|pizza de bacon",
                content="Dizem que tudo fica melhor com bacon, mas na verdade tudo só fica perfeito mesmo quando eu divido a fatia (e a vida) com você.",
                is_unlocked=False,
            ),
            Declaration(
                user_id=special_user.id,
                question="Qual apelido o Percy gosta de chamar a Annabeth?",
                expected_answer="sabidinha",
                content="Acertou, Sabidinha! Assim como o Percy pela Annabeth, eu atravessaria qualquer labirinto e enfrentaria qualquer desafio só para continuar do seu lado.",
                is_unlocked=False,
            ),
            Declaration(
                user_id=special_user.id,
                question="Eu prefiro sorvete ou açaí?",
                expected_answer="sorvete|sorvetinho",
                content="Sorvete ganha fácil do açaí, mas nem o sabor mais doce da sorveteria consegue competir com o gosto do seu beijo.",
                is_unlocked=False,
            ),
        ]
        db.add_all(declarations)

        quotes = [
            RomanceQuote(
                quote="Por favor, nunca se esqueça de que o sol se levanta e se põe com o seu sorriso. Pelo menos para mim. Você é a única coisa neste planeta que merece devoção.",
                author="Taylor Jenkins Reid",
                book_title="Os Sete Maridos de Evelyn Hugo",
            ),
            RomanceQuote(
                quote="As pessoas acham que intimidade tem a ver com sexo. Mas intimidade tem a ver com verdade. Quando você percebe que pode contar a sua verdade para alguém, quando você pode se mostrar para essa pessoa, ficar diante dela despida e a resposta dela é 'você está segura comigo' — isso é intimidade.",
                author="Taylor Jenkins Reid",
                book_title="Os Sete Maridos de Evelyn Hugo",
            ),
            RomanceQuote(
                quote="Você não sabe o quão rápido estava correndo, o quanto estava se esforçando, o quão verdadeiramente exausta estava, até que alguém fica atrás de você e diz: 'Está tudo bem, você pode cair agora. Eu te seguro.'",
                author="Taylor Jenkins Reid",
                book_title="Os Sete Maridos de Evelyn Hugo",
            ),
            RomanceQuote(
                quote="Nunca deixe ninguém fazer você se sentir comum.",
                author="Taylor Jenkins Reid",
                book_title="Os Sete Maridos de Evelyn Hugo",
            ),
            RomanceQuote(
                quote="Você é minha pessoa favorita. Sempre foi. Sempre será. Eu te amo. Amo tudo o que você é.",
                author="Colleen Hoover",
                book_title="É Assim que Começa",
            ),
            RomanceQuote(
                quote="No futuro, se por algum milagre você achar que é capaz de se apaixonar de novo, se apaixone por mim. Você ainda é minha pessoa preferida. E sempre será.",
                author="Colleen Hoover",
                book_title="É Assim que Acaba",
            ),
            RomanceQuote(
                quote="Eu correria oito quilômetros só para te abraçar.",
                author="Colleen Hoover",
                book_title="É Assim que Começa",
            ),
            RomanceQuote(
                quote="Às vezes você vai precisar que eu segure sua mão enquanto descemos uma colina, e às vezes vou precisar que você me guie enquanto subimos uma montanha. Mas a partir deste momento, vamos enfrentar tudo juntos.",
                author="Colleen Hoover",
                book_title="É Assim que Começa",
            ),
            RomanceQuote(
                quote="Obrigado por ser a parte mais reconfortante da minha vida neste momento. Obrigado por sempre ser o farol de que eu preciso toda vez que me sinto perdido. Eu me sinto grato pela sua existência.",
                author="Colleen Hoover",
                book_title="É Assim que Começa",
            ),
            RomanceQuote(
                quote="Prometo que te amarei mais durante as tempestades do que te amarei durante os dias perfeitos.",
                author="Colleen Hoover",
                book_title="Todas as Suas (Im)perfeições",
            ),
            RomanceQuote(
                quote="Prometo te amar mais quando você estiver chorando do que quando você estiver sorrindo. Prometo te amar mais quando você estiver doente do que quando você estiver saudável.",
                author="Colleen Hoover",
                book_title="Todas as Suas (Im)perfeições",
            ),
            RomanceQuote(
                quote="Se eu fosse um carpinteiro, eu construiria para você uma janela para minha alma. Mas eu deixaria a janela fechada e trancada. Assim, toda vez que você tentasse olhar por ela, tudo que veria seria seu próprio reflexo. Você veria que minha alma é um reflexo de você.",
                author="Colleen Hoover",
                book_title="Pausa",
            ),
            RomanceQuote(
                quote="Eu quero ser o seu fim, mas você tem que deixar isso começar.",
                author="Colleen Hoover",
                book_title="Talvez um Dia",
            ),
            RomanceQuote(
                quote="Eu quero que você me ouça te amar.",
                author="Colleen Hoover",
                book_title="Talvez um Dia",
            ),
            RomanceQuote(
                quote="É você. Meu coração quer você.",
                author="Colleen Hoover",
                book_title="Talvez um Dia",
            ),
            RomanceQuote(
                quote="Sabe em quantas portas bati até te encontrar?",
                author="Colleen Hoover",
                book_title="É Assim que Acaba",
            ),
            RomanceQuote(
                quote="Você está em todos os meus lugares mais felizes.",
                author="Emily Henry",
                book_title="Lugar Feliz",
            ),
            RomanceQuote(
                quote="Você é como a gravidade. Tudo continua girando, mas minha mente sempre está com uma mão em você.",
                author="Emily Henry",
                book_title="Lugar Feliz",
            ),
            RomanceQuote(
                quote="Porque não há lugar onde eu não iria por você.",
                author="Emily Henry",
                book_title="Lugar Feliz",
            ),
            RomanceQuote(
                quote="Você é uma parte de mim. Você está tão no fundo do meu coração que eu não conseguiria tirá-lo mesmo que tentasse, e não quero. Eu sei o quão sortudo sou por ter você.",
                author="Emily Henry",
                book_title="Lugar Feliz",
            ),
            RomanceQuote(
                quote="Você não é minhas férias. Você é meu lar.",
                author="Emily Henry",
                book_title="De Férias com Você",
            ),
            RomanceQuote(
                quote="Se tem uma coisa que eu sei, é que, onde quer que você esteja, é lá que devo estar.",
                author="Emily Henry",
                book_title="De Férias com Você",
            ),
            RomanceQuote(
                quote="Porque você é minha melhor amiga e estou apaixonado por você.",
                author="Emily Henry",
                book_title="Nem te Conto",
            ),
            RomanceQuote(
                quote="Quando a gente ama alguém, quer fazer este mundo parecer diferente para essa pessoa. Dar um sentido a todas as coisas ruins e amplificar as boas. É isso que você faz para mim.",
                author="Emily Henry",
                book_title="Leitura de Verão",
            ),
            RomanceQuote(
                quote="Eu gostaria que você pudesse se ver do jeito que eu vejo você.",
                author="Ali Hazelwood",
                book_title="A Hipótese do Amor",
            ),
            RomanceQuote(
                quote="Eu gostava de você quando não te conhecia, e agora que te conheço só piorou. Às vezes, muitas vezes, sempre, penso em você antes de adormecer.",
                author="Ali Hazelwood",
                book_title="A Hipótese do Amor",
            ),
            RomanceQuote(
                quote="Existe algo que você precisa? Diga. É seu. Se eu tiver, é seu.",
                author="Ali Hazelwood",
                book_title="A Hipótese do Amor",
            ),
            RomanceQuote(
                quote="Quando eu finalmente te beijar, não haverá nenhuma dúvida em sua mente de que é real.",
                author="Elena Armas",
                book_title="Uma Farsa de Amor na Espanha",
            ),
            RomanceQuote(
                quote="Eu vou te dar o mundo. A lua. As estrelas. Qualquer coisa que você pedir, é seu. Sou seu.",
                author="Elena Armas",
                book_title="Uma Farsa de Amor na Espanha",
            ),
        ]
        db.add_all(quotes)
        db.commit()
    finally:
        db.close()