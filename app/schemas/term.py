from pydantic import BaseModel


class FinancialTerm(BaseModel):
    code: str
    name: str
    name_ru: str
    category: str
    description: str