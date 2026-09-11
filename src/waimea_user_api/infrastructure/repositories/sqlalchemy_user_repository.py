from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from waimea_user_api.domain.entities.user import User
from waimea_user_api.infrastructure.database.models.user import User as UserModel


class SqlAlchemyUserRepository:
    """
    Implementação concreta do UserRepository usando SQLAlchemy.

    Esta classe pertence à infrastructure porque conhece:
    - SQLAlchemy
    - AsyncSession
    - o modelo ORM UserModel

    O restante da aplicação não precisa conhecer esses detalhes.
    """

    def __init__(self, session: AsyncSession):
        # A sessão será utilizada para conversar com o banco.
        self._session = session

    async def create(self, user: User) -> User:
        # Aqui transformamos a entidade de domínio
        # em um modelo ORM que o SQLAlchemy entende.
        user_model = UserModel(
            name=user.name,
            email=user.email,
            password=user.password,
            role_id=user.role_id,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )

        # Adiciona o objeto à transação atual.
        self._session.add(user_model)

        # Envia o INSERT para o banco sem finalizar a transação.
        # Isso permite que o banco gere o ID do usuário.
        await self._session.flush()

        # Atualiza o objeto com os dados gerados/armazenados pelo banco.
        # Ex.: o ID gerado pelo PostgreSQL.
        await self._session.refresh(user_model)

        # Voltamos para a entidade de domínio.
        # Dessa forma, quem chamou o repository não recebe um objeto
        # dependente de SQLAlchemy.
        return User(
            id=user_model.id,
            name=user_model.name,
            email=user_model.email,
            password=user_model.password,
            role_id=user_model.role_id,
            created_at=user_model.created_at,
            updated_at=user_model.updated_at,
        )

    async def find_by_email(self, email: str) -> User | None:
        # Monta a consulta SQL através do SQLAlchemy.
        query = select(UserModel).where(UserModel.email == email)

        # Executa a consulta de forma assíncrona.
        result = await self._session.execute(query)

        # Obtém o usuário encontrado ou None.
        user_model = result.scalar_one_or_none()

        if user_model is None:
            return None

        # Novamente fazemos a conversão:
        # ORM Model -> Entidade de domínio.
        return User(
            id=user_model.id,
            name=user_model.name,
            email=user_model.email,
            password=user_model.password,
            role_id=user_model.role_id,
            created_at=user_model.created_at,
            updated_at=user_model.updated_at,
        )