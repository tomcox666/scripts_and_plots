const WebSocket = require('ws');
const wss = new WebSocket.Server({ port: 8080 });

// Store all connected clients in an array
let clients = [];

wss.on('connection', function connection(ws) {
    console.log('New client connected');

    // Push new client to clients array
    clients.push(ws);

    // On message received from client
    ws.on('message', function incoming(message) {
        console.log('Received message from client:', message);

        // Convert Buffer to string
        message = JSON.parse(message);

        // Check if message is not empty
        if(message.message.trim().length > 0){
            // Broadcast message to all connected clients
            clients.forEach(client => {
                if (client !== ws && client.readyState === WebSocket.OPEN) {
                    console.log('Broadcasting message to client');
                    client.send(JSON.stringify({
                        username: message.username,
                        message: message.message,
                        color: message.color
                    }));
                } else {
                    client.send(JSON.stringify({
                        username: message.username,
                        message: message.message,
                        color: message.color
                    }));
                }
            });
        } else {
            ws.send('Error: Message cannot be empty');
        }
    });

    // On client disconnects
    ws.on('close', () => {
        console.log('Client disconnected');

        // Remove disconnected client from clients array
        clients = clients.filter(client => client !== ws);
    });

    // On error
    ws.on('error', (err) => {
        console.log('Error occurred:', err);
    });
});