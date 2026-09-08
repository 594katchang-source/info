import fs from 'node:fs';
import http from 'node:http';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const scriptDirectory = path.dirname(fileURLToPath(import.meta.url));
const siteRoot = path.resolve(scriptDirectory, '..', '..', '..');
const defaultPath = '/teach/nutritionranking/index.html';
const requestedPort = Number.parseInt(process.env.NUTRIRANK_PORT ?? '8000', 10);
const port = Number.isInteger(requestedPort) && requestedPort > 0 ? requestedPort : 8000;

const contentTypes = new Map([
  ['.html', 'text/html; charset=utf-8'],
  ['.css', 'text/css; charset=utf-8'],
  ['.js', 'application/javascript; charset=utf-8'],
  ['.json', 'application/json; charset=utf-8'],
  ['.png', 'image/png'],
  ['.jpg', 'image/jpeg'],
  ['.jpeg', 'image/jpeg'],
  ['.ico', 'image/x-icon'],
]);

const server = http.createServer((request, response) => {
  try {
    const requestUrl = new URL(request.url ?? '/', `http://${request.headers.host ?? 'localhost'}`);
    const pathname = decodeURIComponent(requestUrl.pathname === '/' ? defaultPath : requestUrl.pathname);
    const requestedPath = pathname.endsWith('/') ? `${pathname}index.html` : pathname;
    const pathSegments = requestedPath.split('/').filter(Boolean);
    const filePath = path.resolve(siteRoot, `.${requestedPath}`);
    const isInsideSite = filePath === siteRoot || filePath.startsWith(`${siteRoot}${path.sep}`);

    if (!isInsideSite || pathSegments.some((segment) => segment.startsWith('.'))) {
      response.writeHead(403, { 'Content-Type': 'text/plain; charset=utf-8' });
      response.end('403 - Forbidden');
      return;
    }

    if (!fs.existsSync(filePath) || !fs.statSync(filePath).isFile()) {
      response.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' });
      response.end('404 - File Not Found');
      console.log(`[404] ${pathname}`);
      return;
    }

    response.writeHead(200, {
      'Content-Type': contentTypes.get(path.extname(filePath).toLowerCase()) ?? 'application/octet-stream',
      'Access-Control-Allow-Origin': '*',
      'Cache-Control': 'no-store',
    });
    fs.createReadStream(filePath).pipe(response);
    console.log(`[200] ${pathname}`);
  }
  catch (error) {
    response.writeHead(500, { 'Content-Type': 'text/plain; charset=utf-8' });
    response.end('500 - Internal Server Error');
    console.error(error);
  }
});

server.listen(port, '127.0.0.1', () => {
  console.log(`NutriRank is available at http://127.0.0.1:${port}/teach/nutritionranking/`);
  console.log('Press Ctrl+C to stop the server.');
});
