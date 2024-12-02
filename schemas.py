from pydantic import BaseModel,datetime_parse
from typing import Literal
from datetime import datetime



class Client(BaseModel):
    id: int
    username: str
    Gender: Literal['male','female']
    age: int
    balance: int
    email: str
    password: str


class Refunded_ticket(BaseModel):
    refunded_ticket_id: int

class districts(BaseModel):
    name:str

class Admin(BaseModel):
    username: str
    password: str
    email: str

class routesTicket(BaseModel):
    id:int
    source_id: int
    destination_id:int
    number_seats: int
    unit_price: int
    company_id: int

class update_route_ticket(BaseModel):
    source_id: int
    destination_id:int
    number_seats: int
    unit_price: int
    company_id: int




class BoockedTickets(BaseModel):
    id: int
    route_id: int
    client_id: int
    created_at:datetime
    expires_at: datetime
    number_seats: int
    total_price: int
    active: bool
    feed_back_description: str











