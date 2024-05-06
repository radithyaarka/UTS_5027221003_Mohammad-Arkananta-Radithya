from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import sys
sys.path.append('../')  # Assuming the parent directory of 'backend' is two levels up
import grpc
import tickets_pb2
import tickets_pb2_grpc
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# gRPC client setup
grpc_channel = grpc.insecure_channel('localhost:5000')  # Assuming gRPC server is running on localhost:5000
grpc_stub = tickets_pb2_grpc.TicketServiceStub(grpc_channel)

# Set the template folder to ../../frontend/
template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../frontend/src/'))
app.template_folder = template_dir

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/addTicket", methods=['GET', 'POST'])
def add_ticket():
    if request.method == 'GET':
        return render_template("index.html")
    elif request.method == 'POST':
        data = request.json
        ticket_request = tickets_pb2.Ticket(
            id=data['id'],
            name=data['name'],
            event=data['event'],
            venue=data['venue'],
            date=data['date'],
            price=data['price']
        )
        response = grpc_stub.AddTicket(ticket_request)
        return jsonify({"message": "Ticket added successfully"})


@app.route("/allTickets")
def get_all_tickets():
    response = grpc_stub.GetAllTickets(tickets_pb2.Empty())
    ticket_list = [{"id": ticket.id, "name": ticket.name, "event": ticket.event, "venue": ticket.venue, "date": ticket.date, "price": ticket.price} for ticket in response.tickets]
    return jsonify({"tickets": ticket_list})

@app.route("/ticket/<ticket_id>")
def get_ticket(ticket_id):
    response = grpc_stub.GetTicket(tickets_pb2.TicketId(id=ticket_id))
    if response.id:
        ticket_data = {"id": response.id, "name": response.name, "event": response.event, "venue": response.venue, "date": response.date, "price": response.price}
        return jsonify(ticket_data)
    else:
        return jsonify({"message": "Ticket not found"}), 404
    
@app.route("/updateTicket/<ticket_id>", methods=['PUT'])
def update_ticket(ticket_id):
    data = request.json
    ticket_request = tickets_pb2.Ticket(
        id=ticket_id,
        name=data['name'],
        event=data['event'],
        venue=data['venue'],
        date=data['date'],
        price=data['price']
    )
    response = grpc_stub.UpdateTicket(ticket_request)
    return jsonify({"message": "Ticket updated successfully"})


@app.route("/deleteTicket/<ticket_id>", methods=['DELETE'])
def delete_ticket(ticket_id):
    response = grpc_stub.DeleteTicket(tickets_pb2.TicketId(id=ticket_id))
    return jsonify({"message": "Ticket deleted successfully"})


if __name__ == '__main__':
    app.run(debug=True)
