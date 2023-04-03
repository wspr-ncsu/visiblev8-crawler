from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import ARRAY, BigInteger, Boolean, Text, TIMESTAMP
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
    postprocessor_delete_log_after_parsing: Mapped[bool] = mapped_column(Boolean, nullable=True)
    postprocessor_used: Mapped[str] = mapped_column(Text, nullable=True)
    postprocessor_output_format: Mapped[str] = mapped_column(Text, nullable=True)
    crawler_args: Mapped[str] = mapped_column(ARRAY(Text), nullable=True)
    vv8_req_id: Mapped[str] = mapped_column(Text, nullable=False)
    log_parser_req_id: Mapped[str] = mapped_column(Text)
    mongo_id: Mapped[str] = mapped_column(Text)
    __mapper_args__ = { 'eager_defaults': True }