from typing import Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel

class ContractTypeBase(BaseModel):
    name: str
    description: Optional[str] = None
class ContractTypeCreate(ContractTypeBase):
    pass
class ContractType(ContractTypeBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

class PartnerBase(BaseModel):
    name: str
    partner_type: str = "Khách hàng"
    tax_id: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    contact_person: Optional[str] = None
    notes: Optional[str] = None
class PartnerCreate(PartnerBase):
    pass
class Partner(PartnerBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

class DepartmentBase(BaseModel):
    name: str
    description: Optional[str] = None
class DepartmentCreate(DepartmentBase):
    pass
class Department(DepartmentBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

class TagBase(BaseModel):
    name: str
    color: Optional[str] = None
class TagCreate(TagBase):
    pass
class Tag(TagBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

class ContractBase(BaseModel):
    original_filename: str
    original_path: str
    text_path: str
    docx_path: str
    parsed_json: Optional[Dict[str, Any]] = None
    status: Optional[str] = "pending"
    expiration_date: Optional[datetime] = None
    contract_type_id: Optional[int] = None

class ContractCreate(ContractBase):
    pass

class Contract(ContractBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True 