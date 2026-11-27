# Arquitectura

La demo es una página estática que llama a la API de Claude desde el navegador con la clave que pega el usuario.
Se publica con un Worker de Cloudflare que exige contraseña antes de servir cualquier fichero.

## Contexto (C4 nivel 1)

```mermaid
C4Context
  title AI Use Case Suite: contexto
  Person(user, "Asistente a la demo", "Tiene la contraseña de la demo")
  System(suite, "AI Use Case Suite", "Demo de casos de uso documentales")
  System_Ext(claude, "API de Claude", "api.anthropic.com")
  System_Ext(github, "GitHub", "Repositorio privado y GitHub Actions")
  Rel(user, suite, "Usa", "HTTPS")
  Rel(suite, claude, "Analiza documentos", "HTTPS, clave del usuario")
  Rel(github, suite, "Despliega", "wrangler deploy")
```

## Contenedores (C4 nivel 2)

```mermaid
C4Container
  title AI Use Case Suite: contenedores
  Person(user, "Asistente a la demo")
  System_Boundary(cf, "Cloudflare") {
    Container(worker, "Worker de acceso", "Cloudflare Worker, worker/index.js", "Pide la contraseña (secreto APP_PASSWORD) y emite una cookie firmada de 12 h")
    Container(assets, "Ficheros de la app", "Workers Static Assets, dist/", "index.html, js, locales, prompts, data")
  }
  Container(spa, "App en el navegador", "HTML + JS", "Pestañas, visor PDF, demo sin conexión")
  System_Ext(claude, "API de Claude")
  Rel(user, worker, "Pide páginas", "HTTPS")
  Rel(worker, assets, "Sirve solo con cookie válida")
  Rel(worker, spa, "Entrega")
  Rel(spa, claude, "Llama", "HTTPS")
```

## Despliegue

- `make build` copia a `dist/` una lista blanca de ficheros (`scripts/build.sh`). Nunca se publican `key`, `Demo docs/` ni el material interno.
- `make deploy` publica el Worker; `make secret` guarda o cambia la contraseña como secreto del Worker.
- GitHub Actions (`.github/workflows/deploy.yml`) despliega en cada push a `main` cuando la variable `CLOUDFLARE_DEPLOY` vale `true` y existen los secretos `CLOUDFLARE_API_TOKEN` y `CLOUDFLARE_ACCOUNT_ID`.
- No hay Terraform: el único recurso es el Worker, declarado en `wrangler.jsonc`.
