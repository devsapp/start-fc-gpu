const http = require('http');
const fs = require('fs');
const path = require('path');


fs.writeFileSync(
  './endpoint.js',
  `window.ENDPOINT = '${process.env?.['ENDPOINT']}'`,
);

const server = http.createServer((req, res) => {
  // 获取请求的文件路径
  const url = req.url === '/' || req.url === '' ? 'index.html' : req.url;

  let filePath = path.join(__dirname, url);

  console.log(filePath);

  // 判断文件是否存在
  fs.access(filePath, fs.constants.F_OK, (err) => {
    if (err) {
      res.statusCode = 404;
      res.end('File not found');
      return;
    }

    // 判断请求的是文件还是目录
    fs.stat(filePath, (err, stats) => {
      if (err) {
        res.statusCode = 500;
        res.end('Internal server error');
        return;
      }

      if (stats.isFile()) {
        // 如果是文件，读取文件并返回
        fs.readFile(filePath, (err, data) => {
          if (err) {
            res.statusCode = 500;
            res.end('Internal server error');
            return;
          }

          const extname = path.extname(filePath);
          let contentType = 'text/plain';
          switch (extname) {
            case '.html':
              contentType = 'text/html';
              break;
            case '.css':
              contentType = 'text/css';
              break;
            case '.js':
              contentType = 'application/javascript';
              break;
            case '.jpg':
              contentType = 'image/jpeg';
              break;
            case '.png':
              contentType = 'image/png';
              break;
            case '.gif':
              contentType = 'image/gif';
              break;
            case '.pdf':
              contentType = 'application/pdf';
              break;
            case '.json':
              contentType = 'application/json';
              break;
          }
          res.setHeader('Content-Type', contentType);

          res.end(data);
        });
      } else {
        res.statusCode = 404;
        res.end('File not found');
        return;
      }
    });
  });
});

server.listen(8000, '0.0.0.0', () => {
  console.log('Server is running at http://0.0.0.0:8000');
});

process.on('SIGTERM', () => {
  console.log('Closing server');
  server.close(() => {
    console.log('Server closed');
  });
});
