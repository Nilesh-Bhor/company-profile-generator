from pydantic import BaseModel, HttpUrl
from typing import List, Optional

class Overview(BaseModel):
    name: str
    website: Optional[HttpUrl]
    description: str
    industry: str
    founded: str
    employees: str
    certifications: Optional[str]
    location: str
    mission: Optional[str]
    vision: Optional[str]
    industry_served: Optional[str]
    logo: Optional[HttpUrl]

class GeographicPresence(BaseModel):
    presence_type: str
    locations: str

class FinancialMetric(BaseModel):
    year: str
    ebit: Optional[str]
    ebitda: Optional[str]
    revenue: Optional[str]
    growth: Optional[str]
    gross_profit: Optional[str]
    net_profit: Optional[str]
    assets: Optional[str]
    market_cap: Optional[str]
    ownership: Optional[str]

class FinancialHighlights(BaseModel):
    overview: str
    metrics: List[FinancialMetric]

class ProductServiceItem(BaseModel):
    name: str
    category: str
    description: str

class ProductsServices(BaseModel):
    description: str
    items: List[ProductServiceItem]

class LeadershipMember(BaseModel):
    name: str
    position: str
    bio: str

class Leadership(BaseModel):
    description: str
    members: List[LeadershipMember]

class ClientsCompetitors(BaseModel):
    major_clients: Optional[str]
    major_competitors: Optional[str]

class StrategicObjective(BaseModel):
    name: str
    description: str

class StrategicPriorities(BaseModel):
    description: str
    objectives: List[StrategicObjective]

class KeyEvent(BaseModel):
    date: str
    description: str
    source: Optional[HttpUrl]

class KeyEvents(BaseModel):
    description: str
    events: List[KeyEvent]

class CompanyProfileResponse(BaseModel):
    overview: Overview
    geographic_presence: List[GeographicPresence]
    financial_highlights: FinancialHighlights
    products_services: ProductsServices
    leadership: Leadership
    clients_competitors: ClientsCompetitors
    strategic_priorities: StrategicPriorities
    key_events: KeyEvents
    sources: List[str]