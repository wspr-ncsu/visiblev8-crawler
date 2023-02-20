from sqlalchemy.orm import DeclarativeBase
from typing import List
from sqlalchemy import Integer, BigInteger, Text, String, ForeignKey, TIMESTAMP
from typing import Optional
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

class Base(DeclarativeBase):
    pass
class LogEntry(Base):
    __tablename__ = 'log_entries'
    __table_args__ = { "schema": "vv8_logs" }

    log_entry_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    context_id: Mapped[Optional[int]] = mapped_column(ForeignKey("vv8_logs.execution_contexts.context_id"))
    sort_index: Mapped[int] = mapped_column(BigInteger, nullable=False)
    log_type: Mapped[str] = mapped_column(String(30), nullable=False)
    src_offset: Mapped[int] = mapped_column(BigInteger, nullable=False)
    obj: Mapped[Optional[str]] = mapped_column(String(250))
    func: Mapped[Optional[str]] = mapped_column(String(250))
    prop: Mapped[Optional[str]] = mapped_column(String(250))
    args: Mapped[Optional[str]] = mapped_column(Text)
    submission_id: Mapped[int] = mapped_column(BigInteger)

class Isolates(Base):
    __tablename__ = 'isolates'
    __table_args__ = { "schema": "vv8_logs" }

    isolate_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    isolate_value: Mapped[Optional[int]] = mapped_column(BigInteger)
    submission_id: Mapped[int] = mapped_column(BigInteger)

    __mapper_args__ = {"eager_defaults": True}

class WindowOrigins(Base):
    __tablename__ = 'window_origins'
    __table_args__ = { "schema": "vv8_logs" }

    window_origin_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    isolate_id: Mapped[int] = mapped_column(BigInteger)
    url: Mapped[str] = mapped_column(Text)
    submission_id: Mapped[int] = mapped_column(BigInteger)
    __mapper_args__ = {"eager_defaults": True}

class ExecutionContexts(Base):
    __tablename__ = 'execution_contexts'
    __table_args__ = { "schema": "vv8_logs" }

    context_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    window_id: Mapped[int] = mapped_column(ForeignKey("vv8_logs.window_origins.window_origin_id"))
    isolate_id: Mapped[int] = mapped_column(ForeignKey("vv8_logs.isolates.isolate_id"))
    submission_id: Mapped[int] = mapped_column(BigInteger)
    sort_index: Mapped[int] = mapped_column(BigInteger)
    script_id: Mapped[int] = mapped_column(BigInteger)
    url: Mapped[str] = mapped_column(Text)
    src: Mapped[str] = mapped_column(Text)
    submission_id: Mapped[int] = mapped_column(BigInteger)
    __mapper_args__ = {"eager_defaults": True}

class Relationships(Base):
    __tablename__ = 'relationships'
    __table_args__ = { "schema": "vv8_logs" }

    relationship_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    relationship_type: Mapped[str] = mapped_column(String(250), nullable=False)
    from_entity: Mapped[str] = mapped_column(BigInteger, nullable=False)
    to_entity: Mapped[str] = mapped_column(BigInteger, nullable=False)
    submission_id: Mapped[int] = mapped_column(BigInteger)
    __mapper_args__ = {"eager_defaults": True}

class Submission(Base):
    __tablename__ = 'submissions'
    __table_args__ = { "schema": "vv8_logs" }
    submission_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    start_time: Mapped[str] = mapped_column(TIMESTAMP, nullable=False)
    end_time: Mapped[str] = mapped_column(TIMESTAMP)
    url_scheme: Mapped[str] = mapped_column(String(126))
    url_domain: Mapped[str] = mapped_column(String(), nullable=False)
    url_path: Mapped[str] = mapped_column(String(), nullable=False)
    url_query_params: Mapped[str] = mapped_column(String(), nullable=False)
    url_fragment: Mapped[str] = mapped_column(String(), nullable=False)
