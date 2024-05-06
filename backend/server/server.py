import grpc
import sys
sys.path.append('../')
import logging
import pymongo
from concurrent import futures
import tickets_pb2
import tickets_pb2_grpc

class TicketService(tickets_pb2_grpc.TicketServiceServicer):
    def __init__(self):
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.client["TicketBooking"]
        self.collection = self.db["TicketList"]
        logging.info("Connected to MongoDB")

    def AddTicket(self, request, context):
        logging.info("Received AddTicket request: %s", request)
        ticket_data = {
            "id": request.id,
            "name": request.name,
            "event": request.event,
            "venue": request.venue,
            "date": request.date,
            "price": request.price
        }
        self.collection.insert_one(ticket_data)
        return request

    def GetAllTickets(self, request, context):
        logging.info("Received GetAllTickets request")
        ticket_list = []
        for ticket_data in self.collection.find():
            ticket = tickets_pb2.Ticket(
                id=ticket_data["id"],
                name=ticket_data["name"],
                event=ticket_data["event"],
                venue=ticket_data["venue"],
                date=ticket_data["date"],
                price=ticket_data["price"]
            )
            ticket_list.append(ticket)
        return tickets_pb2.TicketList(tickets=ticket_list)
    
    def GetTicket(self, request, context):
        logging.info("Received GetTicket request for ticket ID: %s", request.id)
        ticket_data = self.collection.find_one({"id": request.id})
        if ticket_data:
            ticket = tickets_pb2.Ticket(
                id=ticket_data["id"],
                name=ticket_data["name"],
                event=ticket_data["event"],
                venue=ticket_data["venue"],
                date=ticket_data["date"],
                price=ticket_data["price"]
            )
            return ticket
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Ticket not found")
            return tickets_pb2.Ticket()
        
    def UpdateTicket(self, request, context):
        logging.info("Received UpdateTicket request for ticket ID: %s", request.id)
        ticket_data = self.collection.find_one({"id": request.id})
        if ticket_data:
            updated_ticket_data = {
                "id": request.id,
                "name": request.name,
                "event": request.event,
                "venue": request.venue,
                "date": request.date,
                "price": request.price
            }
            self.collection.update_one({"id": request.id}, {"$set": updated_ticket_data})
            return tickets_pb2.Empty() 
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Ticket not found")
            return tickets_pb2.Empty()

    def DeleteTicket(self, request, context):
        logging.info("Received DeleteTicket request for ticket ID: %s", request.id)
        result = self.collection.delete_one({"id": request.id})
        if result.deleted_count > 0:
            return tickets_pb2.Empty()
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Ticket not found")
            return tickets_pb2.Empty()

def serve():
    logging.basicConfig(level=logging.INFO)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    tickets_pb2_grpc.add_TicketServiceServicer_to_server(TicketService(), server)
    server.add_insecure_port('[::]:5000')
    server.start()
    logging.info("Listening on port 5000")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
