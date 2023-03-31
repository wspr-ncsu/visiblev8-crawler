from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import BigInteger, Text, TIMESTAMP
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class Base(DeclarativeBase):
    pass

class Submission(Base):
    __tablename__ = 'submissions'
    __table_args__ = { "schema": "vv8_backend" }
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    start_time: Mapped[str] = mapped_column(TIMESTAMP, nullable=False)
    end_time: Mapped[str] = mapped_column(TIMESTAMP)
    url: Mapped[str] = mapped_column(Text, nullable=False)
    
    vv8_req_id: Mapped[str] = mapped_column(Text, nullable=False)
    log_parser_req_id: Mapped[str] = mapped_column(Text)
    mongo_id: Mapped[str] = mapped_column(Text)
    __mapper_args__ = { 'eager_defaults': True }