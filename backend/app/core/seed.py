from app.core.database import SessionLocal
from app.core.security import hash_password
from app.countdown.models import Countdown
from app.declarations.models import Declaration
from app.romance.models import RomanceQuote
from app.routine.models import Task
from app.users.models import User


def seed_database() -> None:
    db = SessionLocal()
    try:
        if db.query(User).first():
            return

        standard_user = User(
            username="demo",
            email="demo@routine.app",
            password_hash=hash_password("demo123"),
            is_special=False,
        )
        special_user = User(
            username="special",
            email="special@routine.app",
            password_hash=hash_password("love123"),
            is_special=True,
        )
        db.add_all([standard_user, special_user])
        db.commit()
        db.refresh(special_user)

        initial_tasks = [
            Task(
                user_id=special_user.id,
                title="Acordar",
                task_date="2026-11-24",
                start_minutes=480,
                duration=15,
                color="coral",
                icon="bi-sun-fill",
                is_completed=True,
                is_inbox=False,
            ),
            Task(
                user_id=special_user.id,
                title="Alongamento e treino",
                task_date="2026-11-24",
                start_minutes=495,
                duration=30,
                color="blue",
                icon="bi-heart-pulse",
                is_completed=True,
                is_inbox=False,
            ),
            Task(
                user_id=special_user.id,
                title="Revisar Árvore Binária de Busca",
                task_date="2026-11-24",
                start_minutes=570,
                duration=30,
                color="green",
                icon="bi-diagram-3",
                is_completed=False,
                is_inbox=False,
            ),
            Task(
                user_id=special_user.id,
                title="Dormir",
                task_date="2026-11-24",
                start_minutes=1320,
                duration=30,
                color="blue",
                icon="bi-moon-fill",
                is_completed=False,
                is_inbox=False,
            ),
            Task(
                user_id=special_user.id,
                title="Lavar roupa",
                task_date=None,
                start_minutes=None,
                duration=60,
                color="blue",
                icon="bi-basket",
                is_completed=False,
                is_inbox=True,
            ),
        ]
        db.add_all(initial_tasks)

        countdown = Countdown(
            user_id=special_user.id,
            title="Até Nosso Próximo Encontro",
            target_date="2026-12-20",
        )
        db.add(countdown)

        declarations = [
            Declaration(
                user_id=special_user.id,
                question="Em qual mês comemoramos nosso aniversário de namoro?",
                expected_answer="setembro",
                content="Cada mês ao seu lado continua sendo a melhor parte da minha rotina.",
                is_unlocked=False,
            ),
            Declaration(
                user_id=special_user.id,
                question="Quantos anos completamos juntos em 2026?",
                expected_answer="4",
                content="Quatro anos de história, companheirismo e planos que só crescem.",
                is_unlocked=False,
            ),
            Declaration(
                user_id=special_user.id,
                question="Qual estrutura de dados organiza os horários deste aplicativo?",
                expected_answer="arvore binaria",
                content="Mesmo em um projeto de Engenharia de Software, fiz questão de guardar um cantinho especial para nós.",
                is_unlocked=False,
            ),
        ]
        db.add_all(declarations)

        quotes = [
            RomanceQuote(
                quote="Você enfeitiçou minha alma, em corpo e mente, e eu amo, amo, amo você.",
                author="Jane Austen",
                book_title="Orgulho e Preconceito",
            ),
            RomanceQuote(
                quote="Seja lá do que as nossas almas são feitas, a dele e a minha são iguais.",
                author="Emily Brontë",
                book_title="O Morro dos Ventos Uivantes",
            ),
            RomanceQuote(
                quote="Você é o meu coração, a minha vida e o meu único pensamento.",
                author="Arthur Conan Doyle",
                book_title="A Companhia Branca",
            ),
        ]
        db.add_all(quotes)
        db.commit()
    finally:
        db.close()