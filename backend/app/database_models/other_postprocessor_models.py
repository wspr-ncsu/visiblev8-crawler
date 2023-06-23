from sqlalchemy import Column, Integer, BigInteger, Boolean, String, Text, Enum, ARRAY, ForeignKey, Float, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB, JSON
import enum

Base = declarative_base()

class LogFile(Base):
    __tablename__ = 'logfile'
    id = Column(Integer, primary_key=True)
    mongo_oid = Column(Text, nullable=False)
    uuid = Column(Text, nullable=False, unique=True)
    root_name = Column(Text, nullable=False)
    size = Column(BigInteger, nullable=False)
    lines = Column(Integer, nullable=False)
    submissionid = Column(Text)

class ScriptBlobs(Base):
    __tablename__ = 'script_blobs'
    id = Column(Integer, primary_key=True)
    script_hash = Column(Text, nullable=False)
    script_code = Column(Text, nullable=False)
    sha256sum = Column(Text, nullable=False)
    size = Column(Integer, nullable=False)

class Adblock(Base):
    __tablename__ = 'adblock'
    id = Column(Integer, primary_key=True)
    url = Column(Text, nullable=False)
    origin = Column(Text, nullable=False)
    blocked = Column(Boolean, nullable=False)

class ThirdPartyFirstParty(Base):
    __tablename__ = 'thirdpartyfirstparty'
    id = Column(Integer, primary_key=True)
    sha2 = Column(Text, nullable=False)
    root_domain = Column(Text, nullable=False)
    url = Column(Text, nullable=False)
    first_origin = Column(Text, nullable=False)
    property_of_root_domain = Column(Text, nullable=False)
    property_of_first_origin = Column(Text, nullable=False)
    property_of_script = Column(Text, nullable=False)
    is_script_third_party_with_root_domain = Column(Boolean, nullable=False)
    is_script_third_party_with_first_origin = Column(Boolean, nullable=False)
    script_origin_tracking_value = Column(Float, nullable=False)

class JsApiFeaturesSummary(Base):
    __tablename__ = 'js_api_features_summary'
    logfile_id = Column(Integer, ForeignKey('logfile.id'), primary_key=True)
    all_features = Column(JSON, nullable=False)
    logfile = relationship("LogFile", backref="js_api_features_summary")

class ScriptFlow(Base):
    __tablename__ = 'script_flow'
    id = Column(Integer, primary_key=True)
    isolate = Column(Text, nullable=False)
    visiblev8 = Column(Boolean, nullable=False)
    code = Column(Text, nullable=False)
    first_origin = Column(Text)
    url = Column(Text)
    apis = Column(ARRAY(Text), nullable=False)
    evaled_by = Column(Integer)

class FeatureUsage(Base):
    __tablename__ = 'feature_usage'
    id = Column(Integer, primary_key=True)
    logfile_id = Column(Integer, ForeignKey('logfile.id'), nullable=False)
    visit_domain = Column(Text, nullable=False)
    security_origin = Column(Text, nullable=False)
    script_hash = Column(Text, nullable=False)
    script_offset = Column(Integer, nullable=False)
    feature_name = Column(Text, nullable=False)
    feature_use = Column(String(1), nullable=False)
    use_count = Column(Integer, nullable=False)
    logfile = relationship("LogFile", backref="feature_usage")

class MultiOriginObj(Base):
    __tablename__ = 'multi_origin_obj'
    id = Column(Integer, primary_key=True)
    objectid = Column(Integer, nullable=False)
    origins = Column(ARRAY(Text), nullable=False)
    num_of_origins = Column(Integer, nullable=False)
    urls = Column(ARRAY(Text), nullable=False)

class MultiOriginApiNames(Base):
    __tablename__ = 'multi_origin_api_names'
    id = Column(Integer, primary_key=True)
    objectid = Column(Integer, nullable=False)
    origin = Column(Text, nullable=False)
    api_name = Column(Text, nullable=False)

class ScriptCreation(Base):
    __tablename__ = 'script_creation'
    id = Column(Integer, primary_key=True)
    logfile_id = Column(Integer, ForeignKey('logfile.id'), nullable=False)
    visit_domain = Column(Text, nullable=False)
    script_hash = Column(Text, nullable=False)
    script_url = Column(Text)
    eval_parent_hash = Column(LargeBinary)
    isolate_ptr = Column(Text)
    runtime_id = Column(Integer)
    first_origin = Column(Text)
    logfile = relationship("LogFile", backref="script_creation")

class PolyFeatureUsage(Base):
    __tablename__ = 'poly_feature_usage'
    id = Column(Integer, primary_key=True)
    logfile_id = Column(Integer, ForeignKey('logfile.id'), nullable=False)
    visit_domain = Column(Text, nullable=False)
    security_origin = Column(Text, nullable=False)
    script_hash = Column(LargeBinary, nullable=False)
    script_offset = Column(Integer, nullable=False)
    feature_name = Column(Text, nullable=False)
    feature_use = Column(String(1), nullable=False)
    use_count = Column(Integer, nullable=False)
    logfile = relationship("LogFile", backref="poly_feature_usage")

class ScriptGenesisEnum(enum.Enum):
    unknown = 'unknown'
    static = 'static'
    eval = 'eval'
    include = 'include'
    insert = 'insert'
    write_include = 'write_include'
    write_insert = 'write_insert'

class ScriptCausality(Base):
    __tablename__ = 'script_causality'
    id = Column(Integer, primary_key=True)
    logfile_id = Column(Integer, ForeignKey('logfile.id'), nullable=False)
    visit_domain = Column(Text, nullable=False)
    child_hash = Column(Text, nullable=False)
    genesis = Column(Enum(ScriptGenesisEnum, __name__='script_genesis'), nullable=False, default=ScriptGenesisEnum.unknown)
    parent_hash = Column(Text)
    by_url = Column(Text)
    parent_cardinality = Column(Integer)
    child_cardinality = Column(Integer)
    logfile = relationship("LogFile", backref="script_causality")

class CreateElements(Base):
    __tablename__ = 'create_elements'
    id = Column(Integer, primary_key=True)
    logfile_id = Column(Integer, ForeignKey('logfile.id'), nullable=False)
    visit_domain = Column(Text, nullable=False)
    security_origin = Column(Text, nullable=False)
    script_hash = Column(Text, nullable=False)
    script_offset = Column(Integer, nullable=False)
    tag_name = Column(Text, nullable=False)
    create_count = Column(Integer, nullable=False)
    logfile = relationship("LogFile", backref="create_elements")

class PageCaptchaSystems(Base):
    __tablename__ = 'page_captcha_systems'
    id = Column(Integer, primary_key=True)
    page_mongo_oid = Column(Text, nullable=False)
    logfile_mongo_oid = Column(Text, nullable=False)
    captcha_systems = Column(JSONB, nullable=False)
