# MOMENT x vivenu Dashboard MVP

Dashboard externe Next.js pour partager a chaque organisateur une vue lecture seule des ventes vivenu, sans ouvrir l'acces seller vivenu.

## Ce qui est livre

- App Next.js avec pages admin et organisateur
- Schema Prisma aligne sur les noms vivenu les plus utiles: `sellerId`, `eventId`, `transactionId`, `saleStatus`, `updatedAt`
- Couche serveur pour API key, lien organisateur prive, cron et webhook
- Mode demo actif par defaut pour pouvoir naviguer sans brancher l'API tout de suite

## URL utiles

- `/`
- `/admin/sellers`
- `/admin/events`
- `/o/[token]`
- `/api/admin/sellers`
- `/api/admin/events/import`
- `/api/admin/events/[eventId]/access`
- `/api/cron/sync`
- `/api/webhooks/vivenu`

## Demarrage

```bash
cp .env.example .env.local
npm install
npm run dev
```

## Parametrage simple

Le projet essaie maintenant d'utiliser exactement les noms de la doc vivenu.

### 1. Variables a remplir dans `.env.local`

```env
DATABASE_URL="postgresql://postgres:postgres@localhost:5432/moment_dashboard?schema=public"
APP_URL="http://localhost:3000"
APP_SECRET="change-me-with-a-long-random-secret"

VIVENU_API_BASE_URL="https://vivenu.dev/api"
VIVENU_API_KEY=""
VIVENU_WEBHOOK_HMAC_KEY="change-me"

CRON_SECRET="change-me"
USE_DEMO_DATA="true"
```

### 2. A quoi correspond chaque valeur

- `VIVENU_API_BASE_URL`
  Valeur recommandee: `https://vivenu.dev/api`
- `VIVENU_API_KEY`
  L'API key creee dans le dashboard vivenu
- `VIVENU_WEBHOOK_HMAC_KEY`
  La valeur `hmacKey` configuree sur le webhook vivenu
- `sellerId`
  L'identifiant vendeur vivenu
- `eventId`
  L'identifiant evenement vivenu

## Comment recuperer les infos vivenu

### Seller

Il te faut:

- `sellerId`
- `API key`

Dans le projet, le formulaire admin seller attend maintenant:

- `name`: ton libelle interne MOMENT
- `sellerId`: le vrai `sellerId` vivenu
- `apiKey`: la vraie API key vivenu

### Event

Il te faut:

- `eventId`
- le `sellerId` rattache

Dans le projet, le formulaire admin event attend maintenant:

- `sellerId`
- `eventId`
- `organizerName`

## Mapping avec la doc vivenu

Le code est aligne sur la doc officielle:

- `GET /api/events/{id}`
- `GET /api/transactions/rich`
- query incrementale avec `updatedAt[$gt]`
- pagination avec `top` et `skip`
- webhook signe via `x-vivenu-signature` et `hmacKey`

## Flux recommande

### Import initial

1. Renseigner `sellerId` et `API key`
2. Importer un `eventId`
3. Appeler `GET /api/events/{id}`
4. Appeler `GET /api/transactions/rich?event=<eventId>&top=100&skip=0`
5. Stocker les donnees localement
6. Generer le lien organisateur

### Sync incrementale

1. Lire `lastTransactionsSyncAt`
2. Appeler `GET /api/transactions/rich?event=<eventId>&updatedAt[$gt]=...&top=100&skip=0`
3. Upsert les transactions
4. Mettre a jour les KPI et `sync_state`

### Webhook

Configurer au minimum:

- `transaction.complete`
- `transaction.canceled`
- `transaction.partiallyCanceled`

Le secret a mettre dans vivenu s'appelle `hmacKey`, et dans le projet il est lu depuis `VIVENU_WEBHOOK_HMAC_KEY`.

## Mode demo

Tant que `USE_DEMO_DATA="true"`, le dashboard fonctionne avec:

- `VIVENU_DEMO_SELLER_ID`
- `VIVENU_DEMO_EVENT_ID`
- `ORGANIZER_ACCESS_TOKEN`

Lien demo:

- `/o/demo-organizer-token`

## Fichiers importants

- [lib/vivenu.ts](/Users/julien/Documents/MOMENT%20DASHBOARD%20/lib/vivenu.ts)
- [prisma/schema.prisma](/Users/julien/Documents/MOMENT%20DASHBOARD%20/prisma/schema.prisma)
- [app/admin/sellers/page.tsx](/Users/julien/Documents/MOMENT%20DASHBOARD%20/app/admin/sellers/page.tsx)
- [app/admin/events/page.tsx](/Users/julien/Documents/MOMENT%20DASHBOARD%20/app/admin/events/page.tsx)
- [app/api/webhooks/vivenu/route.ts](/Users/julien/Documents/MOMENT%20DASHBOARD%20/app/api/webhooks/vivenu/route.ts)

## Sources officielles vivenu

- [Introduction API](https://docs.vivenu.dev/introduction)
- [Events](https://docs.vivenu.dev/events)
- [Transactions](https://docs.vivenu.dev/transactions)
- [Webhooks](https://docs.vivenu.dev/webhooks)
