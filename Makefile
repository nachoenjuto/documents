WRANGLER := npx --yes wrangler@4
# Fuera de OneDrive: la sincronización rompe una carpeta que se regenera en cada build.
DIST ?= $(or $(TMPDIR),/tmp/)ai-use-case-suite-dist

.PHONY: run build dev deploy secret logs

run: ## Servidor local sin contraseña (como antes)
	python3 -m http.server 8765 --bind 127.0.0.1

build: ## Copia la app a $(DIST)
	bash scripts/build.sh "$(DIST)"

dev: build ## Worker en local con contraseña (lee .dev.vars)
	$(WRANGLER) dev --port 8787 --assets "$(DIST)"

deploy: build ## Publica el Worker en Cloudflare
	$(WRANGLER) deploy --assets "$(DIST)"

secret: ## Guarda o cambia la contraseña (te la pide por teclado)
	$(WRANGLER) secret put APP_PASSWORD

logs: ## Logs en vivo del Worker
	$(WRANGLER) tail
