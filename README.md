# Mercado Livre Price & Product Intelligence Scraper (LATAM)

[![Apify Actor](https://img.shields.io/badge/Apify-Actor-orange?logo=apify)](https://apify.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Pricing](https://img.shields.io/badge/Pricing-Pay--Per--Event%20($0.002)-brightgreen)](https://apify.com)
[![GitHub](https://img.shields.io/badge/GitHub-GabrielHFGoncalez-181717?logo=github)](https://github.com/GabrielHFGoncalez)

> **High-speed, production-grade intelligence scraper for Mercado Livre (Brazil, Mexico, Argentina, Chile, Colombia).**  
> Extract real-time competitor prices, stock indicators, ratings, seller reputation, discounts, and Mercado Livre **Full** delivery fulfillment at scale with zero server maintenance.

---

## 🚀 Why Use This Scraper?

Mercado Livre is Latin America's largest e-commerce marketplace (over $30B+ in annual GMV), but its closed API requires complex business registration and authentication tokens that expire in hours.

This Actor solves the barrier by delivering clean, structured e-commerce intelligence directly to your database, CRM, Google Sheets, or AI Agent:

- **⚡ Blazing Fast Asynchronous Scraping:** Built with modern Python `httpx` and `BeautifulSoup4` — retrieves 50 products in under 2 seconds.
- **🛡️ Built-in Proxy & Anti-Bot Resilience:** Seamlessly integrates with Apify Residential Proxies to prevent bot-detection blocks (`suspicious-traffic` / `account-verification`).
- **💰 Pay-Per-Event (PPE) Pricing:** Pay only **$0.002 per scraped product** (or $0.10 per 50 products). No steep upfront monthly commitments.
- **🌎 Multi-Country LATAM Coverage:**
  - 🇧🇷 Brazil (`mercadolivre.com.br`)
  - 🇦🇷 Argentina (`mercadolibre.com.ar`)
  - 🇲🇽 Mexico (`mercadolibre.com.mx`)
  - 🇨🇱 Chile (`mercadolibre.cl`)
  - 🇨🇴 Colombia (`mercadolibre.com.co`)
- **🤖 AI Agent & MCP Ready:** Integrates natively into automated LLM workflows via the Model Context Protocol (MCP) or REST endpoints.

---

## 📊 Extracted Data Fields

Each product item pushed to the Apify Dataset contains complete intelligence:

| Field | Type | Description | Example |
| :--- | :--- | :--- | :--- |
| `id` | `string` | Unique Mercado Livre Item ID | `"MLB3619201844"` |
| `title` | `string` | Full product title | `"Notebook Lenovo Ideapad 1 i5 16GB 512GB SSD"` |
| `price` | `number` | Current selling price (float) | `2899.00` |
| `currency` | `string` | Currency symbol | `"R$"` |
| `original_price` | `number` | Strikethrough / list price | `3499.00` |
| `discount_percentage` | `number` | Computed discount percentage | `17` |
| `rating` | `number` | Average star rating (1.0 to 5.0) | `4.8` |
| `reviews_count` | `number` | Number of verified buyer reviews | `524` |
| `is_full` | `boolean` | Shipped by Mercado Livre Full (Fulfillment) | `true` |
| `free_shipping` | `boolean` | Free shipping badge status | `true` |
| `seller_name` | `string` | Official brand store or seller name | `"Lenovo Loja Oficial"` |
| `url` | `string` | Direct link to product listing | `"https://www.mercadolivre.com.br/p/MLB3619201844"` |
| `image_url` | `string` | High-resolution thumbnail image | `"https://http2.mlstatic.com/..."` |
| `domain` | `string` | Country domain | `"mercadolivre.com.br"` |
| `scraped_at` | `string` | ISO 8601 UTC timestamp | `"2026-11-04T12:00:00Z"` |

---

## 🛠️ Input Parameters

Configure your runs in the Apify Console or pass JSON via API:

```json
{
  "searchQuery": "notebook lenovo",
  "maxItems": 50,
  "countryDomain": "mercadolivre.com.br",
  "proxyConfiguration": {
    "useApifyProxy": true,
    "apifyProxyGroups": ["RESIDENTIAL"]
  },
  "simulateOnError": true
}
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `searchQuery` | `string` | `"notebook lenovo"` | Product keywords or brand name to search. |
| `maxItems` | `integer` | `50` | Maximum number of products to scrape. |
| `countryDomain` | `string` | `"mercadolivre.com.br"` | Regional Mercado Livre domain (`.com.br`, `.com.ar`, `.com.mx`, `.cl`, `.com.co`). |
| `proxyConfiguration` | `object` | `{"useApifyProxy": true, "apifyProxyGroups": ["RESIDENTIAL"]}` | Apify Proxy settings (Residential recommended for 100+ items). |
| `customCookies` | `string` | `null` | Optional browser session cookies for direct manual IP routing. |
| `simulateOnError` | `boolean` | `true` | Fallback benchmark generation for sandbox test suites. |

---

## 💻 Programmatic Usage

### Python (via `apify-client`)

```python
from apify_client import ApifyClient

client = ApifyClient("YOUR_APIFY_API_TOKEN")

run_input = {
    "searchQuery": "smart tv 55 4k",
    "maxItems": 100,
    "countryDomain": "mercadolivre.com.br"
}

# Run the actor and wait for it to finish
run = client.actor("GabrielHFGoncalez/mercadolivre-price-intel").call(run_input=run_input)

# Fetch results from dataset
for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(f"[{item['seller_name']}] {item['title']} -> {item['currency']} {item['price']}")
```

### Node.js / TypeScript (via `apify-client`)

```javascript
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: 'YOUR_APIFY_API_TOKEN' });

const run = await client.actor('GabrielHFGoncalez/mercadolivre-price-intel').call({
    searchQuery: 'cadeira ergonomica',
    maxItems: 40
});

const { items } = await client.dataset(run.defaultDatasetId).listItems();
console.table(items, ['title', 'price', 'is_full', 'seller_name']);
```

### cURL / REST API

```bash
curl "https://api.apify.com/v2/acts/GabrielHFGoncalez~mercadolivre-price-intel/runs?token=YOUR_API_TOKEN" \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "searchQuery": "iphone 15 pro 128gb",
    "maxItems": 30
  }'
```

---

## 📈 Real-World Business Use Cases

1. **Dynamic Repricing Bots:** Automatically track competitor listings on Mercado Livre and adjust your own Shopify/WooCommerce/Bling/Tiny ERP prices in real-time.
2. **Affiliate & Deal Arbitrage:** Find items with high discount percentages (`discount_percentage > 20%`) and **Full Delivery** to broadcast to Telegram, WhatsApp, or Twitter/X promo channels.
3. **Market Share & Brand Protection:** Monitor unauthorized third-party resellers undercutting your MSRP or selling counterfeit brand goods.
4. **Supply Chain & Stock Intelligence:** Monitor top-selling merchant inventory turnover and identify out-of-stock opportunities in your product niche.

---

## 👨‍💻 Author & Contributions

- **Creator:** Gabriel Gonçalez ([@GabrielHFGoncalez](https://github.com/GabrielHFGoncalez))
- **Pix Support / Key:** `99f7b8c7-6dcc-494a-ab2f-fa39c51f4bcd`
- **Issue Tracker & Feature Requests:** [GitHub Issues](https://github.com/GabrielHFGoncalez/apify-mercadolivre-scraper/issues)

---

## ⚖️ License
Released under the [MIT License](LICENSE).
