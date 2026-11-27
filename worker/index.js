// Puerta de acceso de la demo: sirve los ficheros de dist/ solo a quien ha introducido la contraseña.
// La contraseña es el secreto APP_PASSWORD del Worker (wrangler secret put APP_PASSWORD); nunca está en el código.
// Tras acertar, se entrega una cookie firmada con HMAC que caduca a las SESSION_HOURS horas.

const COOKIE = 'demo_session';
const SESSION_HOURS = 12;
const FAIL_DELAY_MS = 1200; // frena los intentos de adivinar la contraseña

const enc = new TextEncoder();

async function hmac(secret, data) {
  const key = await crypto.subtle.importKey('raw', enc.encode(secret), { name: 'HMAC', hash: 'SHA-256' }, false, ['sign']);
  const sig = await crypto.subtle.sign('HMAC', key, enc.encode(data));
  return btoa(String.fromCharCode(...new Uint8Array(sig))).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
}

async function sameText(a, b) {
  // Compara en tiempo constante: hashea ambos para igualar longitudes.
  const [ha, hb] = await Promise.all([a, b].map(s => crypto.subtle.digest('SHA-256', enc.encode(s))));
  return crypto.subtle.timingSafeEqual(ha, hb);
}

async function makeToken(secret) {
  const exp = Date.now() + SESSION_HOURS * 3600 * 1000;
  return `${exp}.${await hmac(secret, 'session:' + exp)}`;
}

async function validToken(secret, token) {
  if (!token) return false;
  const [exp, sig] = token.split('.');
  if (!exp || !sig || !(+exp > Date.now())) return false;
  return sameText(sig, await hmac(secret, 'session:' + exp));
}

function readCookie(req, name) {
  const m = (req.headers.get('Cookie') || '').match(new RegExp('(?:^|;\\s*)' + name + '=([^;]+)'));
  return m ? decodeURIComponent(m[1]) : null;
}

function safeNext(v) {
  // Solo rutas relativas de este mismo sitio, para no abrir redirecciones a otros dominios.
  return typeof v === 'string' && v.startsWith('/') && !v.startsWith('//') && !v.startsWith('/\\') ? v : '/';
}

const esc = s => s.replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

function loginPage(next, failed, status = 200) {
  const html = `<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow"><title>Acceso · AI Use Case Suite</title>
<style>
*{box-sizing:border-box}body{margin:0;min-height:100vh;display:grid;place-items:center;background:#f2f0eb;color:#18160f;font:15px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}
form{width:min(360px,90vw);background:#fff;border:1px solid #e2ded5;border-radius:14px;padding:32px}
h1{font:400 1.6rem Georgia,serif;margin:0 0 6px}p{margin:0 0 22px;color:#7a7568;font-size:.9rem}
label{display:block;font:500 .7rem ui-monospace,Menlo,monospace;letter-spacing:.08em;text-transform:uppercase;color:#9a9588;margin-bottom:8px}
input{width:100%;padding:11px 12px;border:1px solid #d8d4ca;border-radius:8px;font:inherit;background:#faf9f6}input:focus{outline:2px solid #18160f;outline-offset:1px}
button{margin-top:16px;width:100%;padding:11px;border:0;border-radius:8px;background:#18160f;color:#fff;font:inherit;cursor:pointer}
.err{margin:12px 0 0;color:#a3261b;font-size:.85rem}
</style></head><body>
<form method="post" action="/login">
<h1>AI Use Case Suite</h1><p>Demo privada. Introduce la contraseña para continuar.</p>
<label for="pw">Contraseña</label>
<input id="pw" name="password" type="password" autocomplete="current-password" required autofocus>
<input type="hidden" name="next" value="${esc(next)}">
<button type="submit">Entrar</button>
${failed ? '<p class="err" role="alert">Contraseña incorrecta.</p>' : ''}
</form></body></html>`;
  return new Response(html, { status, headers: { 'Content-Type': 'text/html; charset=utf-8', 'Cache-Control': 'no-store', 'X-Robots-Tag': 'noindex, nofollow' } });
}

function cookieHeader(value, maxAge) {
  return `${COOKIE}=${value}; Path=/; Max-Age=${maxAge}; HttpOnly; Secure; SameSite=Lax`;
}

export default {
  async fetch(req, env) {
    const secret = env.APP_PASSWORD;
    if (!secret) return new Response('Acceso no configurado (falta el secreto APP_PASSWORD).', { status: 503 });

    const url = new URL(req.url);

    if (url.pathname === '/login') {
      if (req.method === 'POST') {
        const form = await req.formData().catch(() => null);
        const pw = form && form.get('password');
        const next = safeNext(form && form.get('next'));
        if (typeof pw === 'string' && await sameText(pw, secret)) {
          return new Response(null, { status: 303, headers: { Location: next, 'Set-Cookie': cookieHeader(await makeToken(secret), SESSION_HOURS * 3600), 'Cache-Control': 'no-store' } });
        }
        await new Promise(r => setTimeout(r, FAIL_DELAY_MS));
        return loginPage(next, true, 401);
      }
      return loginPage(safeNext(url.searchParams.get('next')), false);
    }

    if (url.pathname === '/logout') {
      return new Response(null, { status: 303, headers: { Location: '/login', 'Set-Cookie': cookieHeader('', 0), 'Cache-Control': 'no-store' } });
    }

    if (!await validToken(secret, readCookie(req, COOKIE))) {
      if (req.method === 'GET' && (req.headers.get('Accept') || '').includes('text/html')) {
        return Response.redirect(`${url.origin}/login?next=${encodeURIComponent(url.pathname + url.search)}`, 303);
      }
      return new Response('No autorizado', { status: 401, headers: { 'Cache-Control': 'no-store' } });
    }

    const res = await env.ASSETS.fetch(req);
    const out = new Response(res.body, res);
    out.headers.set('Cache-Control', 'private, no-store');
    out.headers.set('X-Robots-Tag', 'noindex, nofollow');
    return out;
  },
};
