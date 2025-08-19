from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, ForeignKey, NVARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class ContractType(Base):
    __tablename__ = "contract_types"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(NVARCHAR(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    contracts = relationship("Contract", back_populates="contract_type")

class Partner(Base):
    __tablename__ = "partners"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(NVARCHAR(255), unique=True, nullable=False)
    partner_type = Column(NVARCHAR(50), nullable=False, default="Khách hàng")  # Khách hàng, Nhà cung cấp
    tax_id = Column(NVARCHAR(50), nullable=True)
    address = Column(Text, nullable=True)
    phone = Column(NVARCHAR(50), nullable=True)
    email = Column(NVARCHAR(255), nullable=True)
    contact_person = Column(NVARCHAR(255), nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

class Department(Base):
    __tablename__ = "departments"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(NVARCHAR(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(NVARCHAR(50), unique=True, nullable=False)
    color = Column(NVARCHAR(20), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

class Contract(Base):
    __tablename__ = "contracts"

    id = Column(Integer, primary_key=True, index=True)
    original_filename = Column(NVARCHAR(255), nullable=False)
    original_path = Column(Text, nullable=False)
    text_path = Column(Text, nullable=False)
    docx_path = Column(Text, nullable=False)
    parsed_json = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    status = Column(NVARCHAR(32), nullable=False, default="pending")
    expiration_date = Column(DateTime(timezone=True), nullable=True)
    contract_type_id = Column(Integer, ForeignKey("contract_types.id"), nullable=True)

    # Relationships
    contract_type = relationship("ContractType", back_populates="contracts")