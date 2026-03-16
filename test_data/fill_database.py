#!/usr/bin/env python3
"""
Скрипт для заполнения базы данных валидными тестовыми данными по всем моделям.

Использование:
    python fill_database.py
    или
    docker compose exec backend python fill_database.py
"""
import sys
import os
from datetime import datetime, timedelta
from random import choice, randint, sample

# Добавляем корневую директорию в путь
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal, init_db
from app.models.user import User
from app.models.board import Board
from app.models.task import Task
from app.models.board_member import BoardMember
from app.models.comment import TaskComment
from app.models.audit_log import AuditLog
from app.core.security import get_password_hash


def create_users(db):
    """Создание пользователей разных ролей"""
    print("\n📝 Создание пользователей...")

    users_data = [
        # Администраторы
        {"username": "admin", "email": "admin@example.com", "password": "admin123", "role": "admin"},
        {"username": "alice_admin", "email": "alice@example.com", "password": "password123", "role": "admin"},

        # Обычные пользователи
        {"username": "bob_user", "email": "bob@example.com", "password": "password123", "role": "user"},
        {"username": "charlie", "email": "charlie@example.com", "password": "password123", "role": "user"},
        {"username": "diana", "email": "diana@example.com", "password": "password123", "role": "user"},
        {"username": "eve", "email": "eve@example.com", "password": "password123", "role": "user"},

        # Гости
        {"username": "guest1", "email": "guest1@example.com", "password": "password123", "role": "guest"},
        {"username": "guest2", "email": "guest2@example.com", "password": "password123", "role": "guest"},
    ]

    # Оптимизация: проверяем существующих пользователей одним запросом
    emails = [u["email"] for u in users_data]
    existing_users = {u.email: u for u in db.query(User).filter(User.email.in_(emails)).all()}

    created_users = []
    new_users = []

    for user_data in users_data:
        if user_data["email"] in existing_users:
            print(f"   ⚠ Пользователь {user_data['email']} уже существует, пропускаем")
            created_users.append(existing_users[user_data["email"]])
        else:
            user = User(
                username=user_data["username"],
                email=user_data["email"],
                password_hash=get_password_hash(user_data["password"]),
                role=user_data["role"],
                created_at=datetime.utcnow() - timedelta(days=randint(1, 30))
            )
            new_users.append(user)
            created_users.append(user)

    # Используем add_all вместо bulk_save_objects для сохранения связи с сессией
    if new_users:
        db.add_all(new_users)
        db.commit()
        # Обновляем ID для новых пользователей
        for user in new_users:
            db.refresh(user)
        print(f"   ✓ Создано {len(new_users)} пользователей")

    return created_users


def create_boards(db, users):
    """Создание досок с разными настройками"""
    print("\n📋 Создание досок...")

    admin_users = [u for u in users if u.role == "admin"]
    regular_users = [u for u in users if u.role == "user"]
    all_creators = admin_users + regular_users

    boards_data = [
        {
            "title": "Проект Разработка",
            "description": "Основная доска для разработки нового функционала",
            "public": False,
            "archived": False,
        },
        {
            "title": "Маркетинг и Продвижение",
            "description": "Задачи по маркетингу и продвижению продукта",
            "public": False,
            "archived": False,
        },
        {
            "title": "Публичная Доска",
            "description": "Доска для публичного просмотра проектов",
            "public": True,
            "archived": False,
        },
        {
            "title": "Техническая Поддержка",
            "description": "Обработка запросов пользователей и баг-репортов",
            "public": False,
            "archived": False,
        },
        {
            "title": "Архивные Проекты",
            "description": "Завершенные проекты",
            "public": False,
            "archived": True,
        },
        {
            "title": "Публичный Roadmap",
            "description": "Публичный план развития продукта",
            "public": True,
            "archived": False,
        },
        {
            "title": "Дизайн Системы",
            "description": "Работа над дизайном интерфейса",
            "public": False,
            "archived": False,
        },
        {
            "title": "Тестирование",
            "description": "QA и тестирование функционала",
            "public": False,
            "archived": False,
        },
    ]

    # Оптимизация: проверяем существующие доски одним запросом
    titles = [b["title"] for b in boards_data]
    existing_boards = {b.title: b for b in db.query(Board).filter(Board.title.in_(titles)).all()}

    created_boards = []
    new_boards = []

    for i, board_data in enumerate(boards_data):
        if board_data["title"] in existing_boards:
            print(f"   ⚠ Доска '{board_data['title']}' уже существует, пропускаем")
            created_boards.append(existing_boards[board_data["title"]])
        else:
            creator = choice(all_creators)
            board = Board(
                title=board_data["title"],
                description=board_data["description"],
                public=board_data["public"],
                archived=board_data["archived"],
                created_by=creator.id,
                created_at=datetime.utcnow() - timedelta(days=randint(1, 60))
            )
            new_boards.append(board)
            created_boards.append(board)

    # Используем add_all вместо bulk_save_objects для сохранения связи с сессией
    if new_boards:
        db.add_all(new_boards)
        db.commit()
        # Обновляем ID для новых досок
        for board in new_boards:
            db.refresh(board)
        print(f"   ✓ Создано {len(new_boards)} досок")

    return created_boards


def create_tasks(db, boards, users):
    """Создание задач на досках"""
    print("\n✅ Создание задач...")

    statuses = ["todo", "in_progress", "done"]
    priorities = ["low", "medium", "high"]

    task_templates = [
        {
            "title": "Настроить CI/CD pipeline",
            "description": "Настроить автоматическую сборку и деплой",
            "status": "in_progress",
            "priority": "high",
        },
        {
            "title": "Добавить аутентификацию",
            "description": "Реализовать систему входа и регистрации",
            "status": "done",
            "priority": "high",
        },
        {
            "title": "Создать API документацию",
            "description": "Написать документацию для всех эндпоинтов",
            "status": "todo",
            "priority": "medium",
        },
        {
            "title": "Оптимизировать запросы к БД",
            "description": "Улучшить производительность запросов",
            "status": "in_progress",
            "priority": "medium",
        },
        {
            "title": "Добавить unit тесты",
            "description": "Покрыть код unit тестами",
            "status": "todo",
            "priority": "high",
        },
        {
            "title": "Обновить дизайн",
            "description": "Улучшить UI/UX интерфейса",
            "status": "todo",
            "priority": "low",
        },
        {
            "title": "Исправить баги",
            "description": "Исправить найденные ошибки",
            "status": "in_progress",
            "priority": "high",
        },
        {
            "title": "Добавить логирование",
            "description": "Настроить систему логирования",
            "status": "done",
            "priority": "medium",
        },
        {
            "title": "Настроить мониторинг",
            "description": "Улучшить производительность приложения",
            "status": "done",
            "priority": "high",
        },
        {
            "title": "Провести code review",
            "description": "Проверить код на соответствие стандартам",
            "status": "todo",
            "priority": "medium",
        },
    ]

    created_tasks = []
    new_tasks = []
    board_users = [u for u in users if u.role != "guest"]  # Гости не создают задачи

    for board in boards:
        if board.archived:
            # Для архивных досок создаем меньше задач
            num_tasks = randint(2, 4)
        else:
            num_tasks = randint(5, 10)

        for i in range(num_tasks):
            template = choice(task_templates)
            creator = choice(board_users)

            task = Task(
                title=template["title"],
                description=template["description"],
                status=template["status"],
                priority=template["priority"],
                order=i,
                board_id=board.id,
                created_by=creator.id,
                created_at=datetime.utcnow() - timedelta(days=randint(0, 30)),
                updated_at=datetime.utcnow() - timedelta(days=randint(0, 15))
            )
            new_tasks.append(task)
            created_tasks.append(task)

    # Используем add_all вместо bulk_save_objects для сохранения связи с сессией
    if new_tasks:
        db.add_all(new_tasks)
        db.commit()
        # Обновляем ID для новых задач
        for task in new_tasks:
            db.refresh(task)
        print(f"   ✓ Создано {len(new_tasks)} задач")

    return created_tasks


def create_board_members(db, boards, users):
    """Добавление участников к доскам"""
    print("\n👥 Добавление участников к доскам...")

    # Оптимизация: получаем все существующие связи одним запросом
    active_boards = [b for b in boards if not b.archived]
    if not active_boards:
        return

    board_ids = [b.id for b in active_boards]
    existing_members = {
        (bm.board_id, bm.user_id)
        for bm in db.query(BoardMember).filter(BoardMember.board_id.in_(board_ids)).all()
    }

    new_members = []
    total_added = 0

    for board in active_boards:
        # Создатель доски уже является участником через связь
        # Добавляем еще несколько участников
        potential_members = [u for u in users if u.id != board.created_by]
        num_members = randint(1, min(3, len(potential_members)))
        selected_members = sample(potential_members, num_members)

        for member in selected_members:
            # Проверяем, не добавлен ли уже
            if (board.id, member.id) not in existing_members:
                board_member = BoardMember(
                    board_id=board.id,
                    user_id=member.id
                )
                new_members.append(board_member)
                existing_members.add((board.id, member.id))
                total_added += 1

    # Массовая вставка всех участников одним коммитом
    if new_members:
        db.bulk_save_objects(new_members)
        db.commit()
        print(f"   ✓ Добавлено {total_added} участников к доскам")


def create_comments(db, tasks, users):
    """Создание комментариев к задачам"""
    print("\n💬 Создание комментариев...")

    comment_templates = [
        "Отличная работа!",
        "Нужно доработать этот момент",
        "Можно улучшить производительность",
        "Готово к ревью",
        "Требуется дополнительная информация",
        "Исправлено в последней версии",
        "Отличная идея!",
        "Нужно обсудить детали",
        "Работа выполнена",
        "Требуется тестирование",
    ]

    new_comments = []
    task_users = [u for u in users if u.role != "guest"]

    for task in tasks:
        # Добавляем комментарии только к активным задачам
        if task.status != "done":
            num_comments = randint(0, 3)

            for _ in range(num_comments):
                comment = TaskComment(
                    task_id=task.id,
                    user_id=choice(task_users).id,
                    content=choice(comment_templates),
                    created_at=datetime.utcnow() - timedelta(days=randint(0, 10))
                )
                new_comments.append(comment)

    # Массовая вставка всех комментариев одним коммитом
    if new_comments:
        db.bulk_save_objects(new_comments)
        db.commit()
        print(f"   ✓ Создано {len(new_comments)} комментариев")


def create_audit_logs(db, users, boards, tasks):
    """Создание логов аудита"""
    print("\n📊 Создание логов аудита...")

    actions = ["create", "update", "delete", "login", "logout", "view"]
    new_logs = []

    # Логи для досок
    for board in boards:
        log = AuditLog(
            user_id=board.created_by,
            action="create",
            entity_type="board",
            entity_id=board.id,
            details=f'{{"title": "{board.title}", "public": {str(board.public).lower()}}}',
            created_at=board.created_at
        )
        new_logs.append(log)

    # Логи для задач
    for task in tasks[:20]:  # Логируем первые 20 задач
        log = AuditLog(
            user_id=task.created_by,
            action=choice(["create", "update"]),
            entity_type="task",
            entity_id=task.id,
            details=f'{{"title": "{task.title}", "status": "{task.status}"}}',
            created_at=task.created_at
        )
        new_logs.append(log)

    # Логи входа пользователей
    for user in users[:5]:  # Логируем входы для первых 5 пользователей
        for _ in range(randint(1, 5)):
            log = AuditLog(
                user_id=user.id,
                action="login",
                entity_type="user",
                entity_id=user.id,
                details=f'{{"username": "{user.username}"}}',
                created_at=datetime.utcnow() - timedelta(days=randint(0, 30))
            )
            new_logs.append(log)

    # Массовая вставка всех логов одним коммитом
    if new_logs:
        db.bulk_save_objects(new_logs)
        db.commit()
        print(f"   ✓ Создано {len(new_logs)} логов аудита")


def main():
    """Основная функция"""
    print("=" * 70)
    print("🚀 Заполнение базы данных тестовыми данными")
    print("=" * 70)

    # Инициализация БД
    print("\n📦 Инициализация базы данных...")
    init_db()
    print("✓ База данных готова")

    db = SessionLocal()

    try:
        # Создание данных
        users = create_users(db)
        boards = create_boards(db, users)
        tasks = create_tasks(db, boards, users)
        create_board_members(db, boards, users)
        create_comments(db, tasks, users)
        create_audit_logs(db, users, boards, tasks)

        # Статистика
        print("\n" + "=" * 70)
        print("📊 Статистика созданных данных:")
        print("=" * 70)
        print(f"   👤 Пользователей: {db.query(User).count()}")
        print(f"   📋 Досок: {db.query(Board).count()}")
        print(f"   ✅ Задач: {db.query(Task).count()}")
        print(f"   👥 Участников досок: {db.query(BoardMember).count()}")
        print(f"   💬 Комментариев: {db.query(TaskComment).count()}")
        print(f"   📊 Логов аудита: {db.query(AuditLog).count()}")
        print("=" * 70)
        print("\n✅ База данных успешно заполнена!")
        print("\n💡 Данные для входа:")
        print("   Администратор: admin@example.com / admin123")
        print("   Пользователь: bob@example.com / password123")
        print("   Гость: guest1@example.com / password123")

    except Exception as e:
        db.rollback()
        print(f"\n❌ Ошибка при заполнении базы данных: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    main()

