// server.js
const http = require('http');

// Simple HTML rendering function
function renderPage(title, message) {
  return `
    <!DOCTYPE html>
    <html>
      <head>
        <title>${title}</title>
        <meta charset="UTF-8" />
      </head>
      <body>
        <h1>${message}</h1>
        <p>Rendered on the server using only JavaScript!</p>
      </body>
    </html>
  `;
}

const server = http.createServer((req, res) => {
  res.writeHead(200, { 'Content-Type': 'text/html' });
  const html = renderPage('SSR Example', 'Hello from Server-Side Rendering');
  res.end(html);
});

server.listen(3000, () => {
  console.log('Server running at http://localhost:3000');
});
