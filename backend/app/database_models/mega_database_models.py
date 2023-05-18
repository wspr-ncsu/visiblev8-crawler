from sqlalchemy import Column, Integer, String, Text, UniqueConstraint, ForeignKey, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
import app.database_models.other_postprocessor_models as opm

Base = declarative_base()

class UrlsImportSchema(Base):
    __tablename__ = 'urls_import_schema'

    id = Column(Integer, primary_key=True)
    sha256 = Column(String, unique=True, nullable=False)
    url_full = Column(Text)
    url_scheme = Column(Text)
    url_hostname = Column(Text)
    url_port = Column(Text)
    url_path = Column(Text)
    url_query = Column(Text)
    url_etld1 = Column(Text)
    url_stemmed = Column(Text)

class Urls(Base):
    __tablename__ = 'urls'

    id = Column(Integer, primary_key=True)
    sha256 = Column(LargeBinary, unique=True, nullable=False)
    url_full = Column(Text)
    url_scheme = Column(Text)
    url_hostname = Column(Text)
    url_port = Column(Text)
    url_path = Column(Text)
    url_query = Column(Text)
    url_etld1 = Column(Text)
    url_stemmed = Column(Text)

class MegaScripts(Base):
    __tablename__ = 'mega_scripts'

    id = Column(Integer, primary_key=True)
    sha2 = Column(LargeBinary, nullable=False)
    sha3 = Column(LargeBinary, nullable=False)
    size = Column(Integer, nullable=False)
    __table_args__ = (UniqueConstraint('sha2', 'sha3', 'size'), )

class MegaScriptsImportSchema(Base):
    __tablename__ = 'mega_scripts_import_schema'

    sha2 = Column(LargeBinary, primary_key=True, nullable=False)
    sha3 = Column(LargeBinary, primary_key=True, nullable=False)
    size = Column(Integer, primary_key=True, nullable=False)

class MegaInstances(Base):
    __tablename__ = 'mega_instances'

    id = Column(Integer, primary_key=True)
    instance_hash = Column(String, unique=True, nullable=False)
    logfile_id = Column(Integer, ForeignKey(opm.LogFile.id))
    script_id = Column(Integer, ForeignKey('mega_scripts.id'))
    isolate_ptr = Column(Text, nullable=False)
    runtime_id = Column(Integer, nullable=False)
    origin_url_id = Column(Integer, ForeignKey('urls.id'))
    script_url_id = Column(Integer, ForeignKey('urls.id'))
    eval_parent_hash = Column(String)

class MegaInstancesImportSchema(Base):
    __tablename__ = 'mega_instances_import_schema'

    instance_hash = Column(String, primary_key=True, nullable=False, unique=True)
    logfile_id = Column(Integer, ForeignKey(opm.LogFile.id))
    script_id = Column(Integer, ForeignKey('mega_scripts.id'))
    isolate_ptr = Column(Text, nullable=False)
    runtime_id = Column(Integer, nullable=False)
    origin_url_sha256 = Column(LargeBinary)
    script_url_sha256 = Column(LargeBinary)
    eval_parent_hash = Column(LargeBinary)

class MegaFeatures(Base):
    __tablename__ = 'mega_features'

    id = Column(Integer, primary_key=True)
    sha256 = Column(String, unique=True, nullable=False)
    full_name = Column(Text, nullable=False)
    receiver_name = Column(Text)
    member_name = Column(Text)
    idl_base_receiver = Column(Text)
    idl_member_role = Column(String(1))

class MegaFeaturesImportSchema(Base):
    __tablename__ = 'mega_features_import_schema'

    sha256 = Column(String, primary_key=True, nullable=False)
    full_name = Column(Text, nullable=False)
    receiver_name = Column(Text)
    member_name = Column(Text)
    idl_base_receiver = Column(Text)
    idl_member_role = Column(String(1))

class MegaUsages(Base):
    __tablename__ = 'mega_usages'

    instance_id = Column(Integer, ForeignKey('mega_instances.id'), primary_key=True, nullable=False)
    feature_id = Column(Integer, ForeignKey('mega_features.id'), primary_key=True, nullable=False)
    origin_url_id = Column(Integer, ForeignKey('urls.id'), nullable=False)
    usage_offset = Column(Integer, nullable=False)
    usage_mode = Column(String(1), nullable=False)
    usage_count = Column(Integer, nullable=False)

class MegaUsagesImportSchema(Base):
    __tablename__ = 'mega_usages_import_schema'

    instance_id = Column(Integer, ForeignKey('mega_instances.id'), primary_key=True, nullable=False)
    feature_id = Column(Integer, ForeignKey('mega_features.id'), primary_key=True, nullable=False)
    origin_url_sha256 = Column(LargeBinary, nullable=False)
    usage_offset = Column(Integer, nullable=False)
    usage_mode = Column(String(1), nullable=False)
    usage_count = Column(Integer, nullable=False)