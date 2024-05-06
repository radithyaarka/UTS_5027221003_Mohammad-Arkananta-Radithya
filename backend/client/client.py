import grpc
import sys
sys.path.append('../')  # Assuming the parent directory of 'backend' is two levels up
import tickets_pb2
import tickets_pb2_grpc

def create_ticket(stub):
    ticket_id = input("Enter ticket ID: ")
    name = input("Enter ticket holder name: ")
    event = input("Enter event name: ")
    venue = input("Enter event venue: ")
    date = input("Enter event date (format: YYYY-MM-DD): ")
    price = int(input("Enter ticket price: "))

    ticket = tickets_pb2.Ticket(id=ticket_id, name=name, event=event, venue=venue, date=date, price=price)
    response = stub.AddTicket(ticket)
    print("AddTicket Response:", response)

def get_all_tickets(stub):
    all_tickets = stub.GetAllTickets(tickets_pb2.Empty())
    print("GetAll Response:", all_tickets)

def get_ticket(stub):
    ticket_id = input("Enter ticket ID: ")
    ticket = stub.GetTicket(tickets_pb2.TicketId(id=ticket_id))
    print("GetTicket Response:", ticket)

def update_ticket(stub):
    ticket_id = input("Enter ticket ID to update: ")
    name = input("Enter updated ticket holder name: ")
    event = input("Enter updated event name: ")
    venue = input("Enter updated event venue: ")
    date = input("Enter updated event date (format: YYYY-MM-DD): ")
    price = int(input("Enter updated ticket price: "))

    ticket = tickets_pb2.Ticket(id=ticket_id, name=name, event=event, venue=venue, date=date, price=price)
    response = stub.UpdateTicket(ticket)
    print("UpdateTicket Response:", response)

def delete_ticket(stub):
    ticket_id = input("Enter ticket ID to delete: ")
    response = stub.DeleteTicket(tickets_pb2.TicketId(id=ticket_id))
    print("DeleteTicket Response:", response)

def run():
    channel = grpc.insecure_channel('localhost:5000')
    stub = tickets_pb2_grpc.TicketServiceStub(channel)

    while True:
        print("\n1. Add Ticket\n2. Get All Tickets\n3. Get Ticket\n4. Update Ticket\n5. Delete Ticket\n6. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            create_ticket(stub)
        elif choice == '2':
            get_all_tickets(stub)
        elif choice == '3':
            get_ticket(stub)
        elif choice == '4':
            update_ticket(stub)
        elif choice == '5':
            delete_ticket(stub)
        elif choice == '6':
            break
        else:
            print("Invalid choice! Please enter a valid option.")


if __name__ == '__main__':
    run()
