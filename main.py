from fastapi import FastAPI, APIRouter,Query
from typing import Annotated,List
from fastapi.params import Depends
from fastapi_pagination import  Page, add_pagination, paginate
from fastapi import BackgroundTasks
from sqlalchemy import func

import models
from sqlalchemy.orm import Session
import schemas
from database import engine, SessionLocal


# app setup
app = FastAPI()
add_pagination(app)

models.Base.metadata.create_all(bind=engine)
def get_db():
    db =SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency =Annotated[Session, Depends(get_db)]
# GLOBAL VARIABLES
def offset(page:int , page_size:int):
    api_offset = (page - 1) * page_size
    return api_offset

# client function
# @app.get("/app/v1/clients")
# def get_all_users(db: db_dependency, limit: int = Query(10, le=100))-> Page[schemas.Client]:
#     clients = db.query(models.Client).limit(limit).all()
#     return paginate(clients)
@app.get("/app/v1/clients")
def get_all_users(db: db_dependency,page:int = Query(1, ge=1), page_size: int = Query(1000,ge=1,le=2000)):
    # calculating the offset
    query_offset = offset(page, page_size)
    # fetching chunked data
    clients = db.query(models.Client).offset(query_offset).limit(page_size).all()
    total_count =  db.query(func.count(models.Client.id)).scalar()
    return {
        "data":clients,
        "page":page,
        "page_size":page_size,
        "total_count":total_count
    }


@app.post("/app/v1/register")
def create_client(client: schemas.Client, db: db_dependency):
    client = models.Client(username=client.username, password=client.password,Gender=client.gender,age=client.age,balance=client.balance,email=client.email)
    db.add(client)
    db.commit()
    db.refresh(client)
    return client
# client ticket booking function
@app.get("/app/v1/booked_tickets")
def get_all_booked_tickets(db: db_dependency, page: int = Query(1, ge=1), page_size:int = Query(1000, ge=1,le=2000) ):
    query_offset = offset(page, page_size)
    booked_tickets = db.query(models.BookedTicket).offset(query_offset).limit(page_size).all()
    total_count = db.query(func.count(models.BookedTicket.id)).scalar()
    return {
        "data":booked_tickets,
        "page":page,
        "page_size":page_size,
        "total_count":total_count
    }

@app.get("/app/v1/booked_tickets/{ticket_id}")
def display_ticket(ticket_id: int, db: db_dependency):
    return db.query(models.BookedTicket).filter(models.BookedTicket.id == ticket_id).first()

@app.post("/app/v1/book_ticket")
def book_ticket(ticket:schemas.BoockedTickets, db: db_dependency):
    getting_specific_route = db.query(models.Route_ticket).filter(models.Route_ticket.id==ticket.route_id).first()
    unit_price_route = getting_specific_route.unit_price
    total_price  = ticket.number_seats * unit_price_route
    if ticket.route_id:
        ticket = models.BookedTicket(route_id=ticket.route_id,client_id=ticket.client_id,created_at=ticket.created_at,expires_at=ticket.expires_at,number_seats=ticket.number_seats,total_price=total_price,feed_back_description=ticket.feed_back,active=True)
        db.add(ticket)
        db.commit()
        db.refresh(ticket)
        return ticket
    else:
        return "no available tickets for the current route"

@app.delete("/app/v1/booked_tickets/sell/{ticket_id}",summary="sell a ticket")
def sell_ticket(ticket_id: int, db: db_dependency):
    ticket_to_be_deleted = db.query(models.BookedTicket).filter(models.BookedTicket.id==ticket_id).first()
    if ticket_to_be_deleted:
        paid_balance_on_ticket = ticket_to_be_deleted.total_price
        client = db.query(models.Client).filter(models.Client.id == ticket_to_be_deleted.client_id).first()
        client.balance += paid_balance_on_ticket
        refunded_ticket =  models.RefundedTicket(refundedTicket_id=ticket_id)
        db.add(refunded_ticket)
        db.query(models.BookedTicket).filter(models.BookedTicket.id == ticket_id).delete()
        db.commit()
        return "success fully sold ! check Your Balance "
    else:
        return " Ticket to be sold not found !"

client_router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
    responses={404: {"description": "Client not found"}}
)


# admin panel
@app.get("/app/v1/admins")
def get_all_admins(db: db_dependency):
    return db.query(models.Admin).all()

@app.put("/app/v1/route_ticket/delete/{route_ticket_id}")
def delete_ticket(route_ticket_id: int, db: db_dependency):
    db.query(models.Route_ticket).filter(models.Route_ticket.id==route_ticket_id).delete()
    return " success fully deleted !"

@app.post("/app/v1/route_ticket")
def create_route_ticket( route_ticket : schemas.routesTicket, db: db_dependency):
    source = db.query(models.Districts).filter(models.Districts.id==route_ticket.source_id).first()
    destination = db.query(models.Districts).filter(models.Districts.id==route_ticket.destination_id).first()
    company = db.query(models.Company).filter(models.Company.id==route_ticket.company_id).first()
    if source and destination and company:
        route_ticket = models.Route_ticket(id=route_ticket.id,source_id=route_ticket.source_id,destination_id=route_ticket.destiantion_id,number_seats=route_ticket.number_seats,unit_price=route_ticket.unit_price)
        db.add(route_ticket)
        db.commit()
        db.refresh(route_ticket)
        return route_ticket
    else:
        return  " source or destination not found"

@app.put("/app/v1/route_ticket/update/{routed_ticket_id}")
def update_route_ticket(routed_ticket_id:int ,updated_route_ticket: schemas.update_route_ticket, db: db_dependency):
    route_ticket = db.query(models.Route_ticket).filter(models.Route_ticket.id==routed_ticket_id).first()
    updated_company_id = db.query(models.Company).filter(models.Company.id==updated_route_ticket.company_id).first()

    if not route_ticket and not updated_company_id:
        return "route ticket not found"
    else:
        route_ticket.source_id = updated_route_ticket.source_id
        route_ticket.destination_id = updated_route_ticket.destiantion_id
        route_ticket.number_seats = updated_route_ticket.number_seats
        route_ticket.unit_price = updated_route_ticket.unit_price
        db.commit()
        db.refresh(route_ticket)
        return route_ticket
    



