from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    quizzes_port: int = 5050
    quizzes_host: str = '0.0.0.0'
    
    # Database settings
    quizzes_db_host: str = 'localhost'
    quizzes_db_port: int = 5433
    quizzes_db_name: str = 'quizzes_db'
    quizzes_db_user: str = 'quizzes_user'
    quizzes_db_password: str = 'quizzes_password'
    
    # Auth service URL
    auth_base_url: str

    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.quizzes_db_user}:{self.quizzes_db_password}@{self.quizzes_db_host}:{self.quizzes_db_port}/{self.quizzes_db_name}"


settings = Settings()
