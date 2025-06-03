const express = require('express');
const app = express();
const server = require('http').Server(app);
const io = require('socket.io')(server);
const port = process.env.PORT || 4000;
const { v4: uuidv4 } = require('uuid');
const { ExpressPeerServer } = require('peer');
const peer = ExpressPeerServer(server, {
  debug: true
});

app.use('/peerjs', peer);
app.set('view engine', 'ejs');
app.use(express.static('public'));

// Root route
app.get('/', (req, res) => {
  const roomId = uuidv4();
  res.send(roomId);
});

// Room-specific route
app.get('/:room', (req, res) => {
  const roomId = req.params.room;
  const html = `
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Room ID</title>
    </head>
    <body>
      <h1>Room ID: ${roomId}</h1>
      <p>Welcome to the video chat room!</p>
    </body>
    </html>
  `;
  res.send(html);
});

// Socket.io connection
io.on('connection', (socket) => {
  socket.on('newUser', (id, room) => {
    socket.join(room);
    socket.to(room).broadcast.emit('userJoined', id);
    socket.on('disconnect', () => {
      socket.to(room).broadcast.emit('userDisconnect', id);
    });
  });
});

// Server listening
server.listen(port, () => {
  console.log("Server running on port: " + port);
});
