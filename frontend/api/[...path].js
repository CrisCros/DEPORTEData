const DEFAULT_BACKEND_ORIGIN = 'http://35.169.239.40:8000';
const DEFAULT_GRAFANA_ORIGIN = 'http://35.169.239.40:3000';

function normalizeOrigin(value, fallback) {
  const origin = (value || fallback || '').trim();
  return origin.replace(/\/+$/, '');
}

function shouldHaveBody(method) {
  return !['GET', 'HEAD'].includes((method || 'GET').toUpperCase());
}

async function readRawBody(req) {
  const chunks = [];
  for await (const chunk of req) {
    chunks.push(Buffer.isBuffer(chunk) ? chunk : Buffer.from(chunk));
  }
  return Buffer.concat(chunks);
}

function forwardHeaders(req) {
  const headers = new Headers();
  for (const [key, value] of Object.entries(req.headers)) {
    if (!value) continue;
    const lower = key.toLowerCase();
    if (['host', 'connection', 'content-length'].includes(lower)) continue;
    headers.set(key, Array.isArray(value) ? value.join(', ') : value);
  }
  return headers;
}

function applyResponseHeaders(res, upstream) {
  upstream.headers.forEach((value, key) => {
    const lower = key.toLowerCase();
    if (['transfer-encoding', 'connection', 'content-encoding'].includes(lower)) {
      return;
    }
    res.setHeader(key, value);
  });
}

export const config = {
  api: {
    bodyParser: false,
    externalResolver: true,
  },
};

export default async function handler(req, res) {
  const pathValue = req.query.path;
  const segments = Array.isArray(pathValue) ? pathValue : (pathValue ? [pathValue] : []);
  const [head, ...tail] = segments;

  const isGrafana = head === 'grafana';
  const origin = normalizeOrigin(
    isGrafana ? process.env.GRAFANA_ORIGIN : process.env.BACKEND_ORIGIN,
    isGrafana ? DEFAULT_GRAFANA_ORIGIN : DEFAULT_BACKEND_ORIGIN,
  );

  const upstreamPath = '/' + (isGrafana ? tail : segments).join('/');
  const rawQuery = req.url.includes('?') ? req.url.slice(req.url.indexOf('?')) : '';
  const upstreamUrl = `${origin}${upstreamPath}${rawQuery}`;

  try {
    const upstreamResponse = await fetch(upstreamUrl, {
      method: req.method,
      headers: forwardHeaders(req),
      body: shouldHaveBody(req.method) ? await readRawBody(req) : undefined,
      redirect: 'manual',
    });

    res.statusCode = upstreamResponse.status;
    applyResponseHeaders(res, upstreamResponse);
    const payload = Buffer.from(await upstreamResponse.arrayBuffer());
    res.end(payload);
  } catch (error) {
    res.statusCode = 502;
    res.setHeader('Content-Type', 'application/json; charset=utf-8');
    res.end(JSON.stringify({
      error: 'Proxy upstream request failed',
      upstreamUrl,
      details: error instanceof Error ? error.message : 'unknown error',
    }));
  }
}
