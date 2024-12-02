from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from database import Base

class Client(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True, autoincrement=True,index=True)
    username = Column(String,index=True)
    Gender = Column (String,index=True)
    age = Column(Integer, index=True)
    balance = Column(Integer,nullable=False)
    email = Column(String,index=True,unique=True, nullable=False)
    password = Column(String,nullable=False)

class Admin(Base):
    __tablename__ = "admins"
    id = Column(Integer, primary_key=True, autoincrement=True,index=True)
    username = Column(String,index=True)
    email = Column(String,index=True,unique=True, nullable=False)
    password = Column(String,nullable=False)

class Districts(Base):
    __tablename__ = "districts"
    id = Column(Integer, primary_key=True, autoincrement=True,index=True)
    district_name = Column(String,index=True)

class Company(Base):
    __tablename__ = "transport_companies"
    id = Column(Integer, primary_key=True, autoincrement=True,index=True)
    company_name = Column(String,index=True)

class Route_ticket(Base):
    __tablename__ = "route_tickets"
    id = Column(Integer, primary_key=True,index=True)
    source_id = Column(Integer,ForeignKey("districts.id"))
    company_id = Column(Integer,ForeignKey("transport_companies.id"))
    destination_id = Column(Integer,ForeignKey("districts.id"))
    number_seats = Column(Integer,nullable=False)
    unit_price = Column(Integer,nullable=False)


class BookedTicket(Base):
    __tablename__ = "booked_tickets"
    id = Column(Integer, primary_key=True,index=True,autoincrement=True)
    route_id = Column(Integer,ForeignKey("route_tickets.id"))
    client_id = Column(Integer, ForeignKey("clients.id"))
    created_at = Column(DateTime,index =True,nullable=False)
    expires_at = Column(DateTime,index =True, nullable=False)
    number_seats = Column(Integer, index =True)
    total_price = Column(Integer, index =True , nullable= False)
    active = Column(Boolean, index=True)
    feed_back_description = Column (String, index=True)
    #relationships
    client = relationship("Client")
    route = relationship("Route_ticket")

class RefundedTicket(Base):
    __tablename__ = "refunded_tickets"
    id = Column(Integer, primary_key=True, autoincrement=True,index=True)
    refundedTicket_id = Column(Integer,ForeignKey("booked_tickets.id"))

