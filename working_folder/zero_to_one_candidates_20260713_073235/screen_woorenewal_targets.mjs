import { writeFile } from "node:fs/promises";

const runFolder = "/Users/igor/Desktop/discussion_panel/working_folder/zero_to_one_candidates_20260713_073235";
const asOf = new Date("2026-07-13T00:00:00+02:00");
const searches = ["woocommerce", "woo commerce", "woocommerce order", "woocommerce inventory"];
const pagesPerSearch = 3;

const operationalTerms = [
  "order", "fulfil", "fulfill", "return", "shipment", "shipping", "delivery",
  "inventory", "stock", "catalog", "checkout", "subscription", "invoice", "packing",
  "warehouse", "product feed", "variation", "booking", "rental", "quote", "purchase order"
];
const excludedTerms = [
  "payment", "stripe", "paypal", "crypto", "facebook", "google ads", "marketing",
  "analytics", "ai content", "chatbot", "dropship", "affiliate", "theme", "elementor"
];
const largeAuthors = [
  "automattic", "woocommerce", "paypal", "stripe", "google", "facebook", "meta",
  "yith", "wp factory", "wpfactory", "themehigh", "tyche", "barn2", "webtoffee",
  "extendons", "wisdm", "woocommerce.com"
];

function stripHtml(value = "") {
  return value.replace(/<[^>]*>/g, " ").replace(/&[^;]+;/g, " ").replace(/\s+/g, " ").trim();
}

function csv(value) {
  const text = String(value ?? "");
  return `"${text.replaceAll('"', '""')}"`;
}

function ageDays(dateText) {
  const match = String(dateText || "").match(/^(\d{4}-\d{2}-\d{2})\s+(\d{1,2}):(\d{2})(am|pm)\s+GMT$/i);
  if (!match) return null;
  let hour = Number(match[2]) % 12;
  if (match[4].toLowerCase() === "pm") hour += 12;
  const parsed = new Date(`${match[1]}T${String(hour).padStart(2, "0")}:${match[3]}:00Z`);
  return Number.isNaN(parsed.valueOf()) ? null : Math.max(0, Math.round((asOf - parsed) / 86400000));
}

function scorePlugin(plugin) {
  const author = stripHtml(plugin.author).toLowerCase();
  const text = `${plugin.name} ${plugin.short_description} ${Object.values(plugin.tags || {}).join(" ")}`.toLowerCase();
  const installs = Number(plugin.active_installs || 0);
  const days = ageDays(plugin.last_updated);
  const workflowHits = operationalTerms.filter(term => text.includes(term));
  const exclusionHits = excludedTerms.filter(term => text.includes(term));
  const isLargeAuthor = largeAuthors.some(term => author.includes(term));
  const externalHomepage = plugin.homepage && !plugin.homepage.includes("wordpress.org");
  let score = 0;
  if (installs >= 1000 && installs <= 20000) score += 3;
  else if (installs >= 100 && installs <= 50000) score += 2;
  else if (installs > 50000 && installs <= 100000) score += 1;
  if (workflowHits.length) score += 2;
  if (days !== null && days >= 180 && days <= 1095) score += 2;
  else if (days !== null && days >= 90 && days < 180) score += 1;
  if (externalHomepage) score += 1;
  if ((plugin.num_ratings || 0) >= 10) score += 1;
  if ((plugin.requires_plugins || []).includes("woocommerce")) score += 1;
  if (exclusionHits.length) score -= 3;
  if (isLargeAuthor) score -= 4;
  return {
    score,
    days,
    workflowHits: workflowHits.join("; "),
    exclusionHits: exclusionHits.join("; "),
    externalHomepage: Boolean(externalHomepage),
    isLargeAuthor
  };
}

const collected = new Map();
for (const search of searches) {
  for (let page = 1; page <= pagesPerSearch; page += 1) {
    const url = new URL("https://api.wordpress.org/plugins/info/1.2/");
    url.searchParams.set("action", "query_plugins");
    url.searchParams.set("request[search]", search);
    url.searchParams.set("request[page]", String(page));
    url.searchParams.set("request[per_page]", "100");
    for (const field of ["description", "sections", "icons", "banners", "screenshots", "versions"]) {
      url.searchParams.set(`request[fields][${field}]`, "0");
    }
    const response = await fetch(url, { headers: { "User-Agent": "WooRenewal-research/1.0" } });
    if (!response.ok) throw new Error(`WordPress API ${response.status}: ${url}`);
    const body = await response.json();
    for (const plugin of body.plugins || []) {
      if (!collected.has(plugin.slug)) collected.set(plugin.slug, plugin);
    }
  }
}

const rows = [...collected.values()]
  .map(plugin => ({ plugin, screen: scorePlugin(plugin) }))
  .sort((a, b) => b.screen.score - a.screen.score || Number(b.plugin.active_installs) - Number(a.plugin.active_installs));

const csvHeader = [
  "rank", "screen_score", "slug", "name", "author", "active_installs", "last_updated",
  "age_days", "rating_percent", "rating_count", "support_threads", "support_resolved",
  "requires_woocommerce", "workflow_terms", "exclusion_terms", "external_homepage",
  "homepage", "wordpress_url", "public_screen_status", "paid_sites", "renewal_rate",
  "support_hours", "asking_price", "atomic_assignability"
];
const csvRows = rows.map((row, index) => {
  const { plugin, screen } = row;
  const status = screen.score >= 7
    ? "priority_data_room_candidate_not_supply_proof"
    : screen.score >= 5
      ? "secondary_screen"
      : "reject_or_low_priority";
  return [
    index + 1, screen.score, plugin.slug, plugin.name, stripHtml(plugin.author),
    plugin.active_installs, plugin.last_updated, screen.days, plugin.rating, plugin.num_ratings,
    plugin.support_threads, plugin.support_threads_resolved,
    (plugin.requires_plugins || []).includes("woocommerce"), screen.workflowHits,
    screen.exclusionHits, screen.externalHomepage, plugin.homepage,
    `https://wordpress.org/plugins/${plugin.slug}/`, status,
    "unknown", "unknown", "unknown", "unknown", "unknown"
  ].map(csv).join(",");
});

const priority = rows.filter(row =>
  row.screen.days !== null &&
  row.screen.days >= 90 &&
  Number(row.plugin.active_installs || 0) >= 1000 &&
  Number(row.plugin.active_installs || 0) <= 50000 &&
  !row.screen.isLargeAuthor &&
  !row.screen.exclusionHits &&
  Boolean(row.screen.workflowHits)
);
const report = `# WooRenewal Public Target Screen\n\n` +
  `- Screen date: 2026-07-13\n` +
  `- Official source: WordPress.org Plugin Information API\n` +
  `- Unique public plugins screened: ${rows.length}\n` +
  `- Public pre-data-room leads: ${priority.length}\n` +
  `- Supply conclusion: **not proven**. Public WordPress metadata does not disclose paid-site count, renewal cohorts, support hours, asking price, billing transferability, contractor IP, or atomic account assignment.\n\n` +
  `## Method\n\n` +
  `The screen ranks independent WooCommerce-related plugins using public proxies only: installed-base size, operational-workflow relevance, update staleness, external homepage, review count, and explicit WooCommerce dependency. Payments, marketing, themes, large platform authors, and other excluded shapes are penalized. The score is a sourcing priority, not a business-quality or Zero-to-One score.\n\n` +
  `## Public Pre-Data-Room Leads\n\n` +
  `| Rank | Plugin | Installs | Last update | Screen | Public status |\n|---:|---|---:|---|---:|---|\n` +
  priority.slice(0, 30).map((row, index) => {
    const p = row.plugin;
    return `| ${index + 1} | [${p.name}](https://wordpress.org/plugins/${p.slug}/) | ${Number(p.active_installs).toLocaleString("en-US")} | ${p.last_updated} | ${row.screen.score} | Needs primary data room |`;
  }).join("\n") +
  `\n\n## Gate Interpretation\n\n` +
  `No plugin in this public screen qualifies as a proven acquisition target. A target becomes plausible only after primary evidence confirms at least 100 paying sites, at least 75% annual renewal, low support burden, acceptable price/terms, clean IP/security, and atomic assignability of the official update, billing, licence, customer, brand, domain, and support assets.\n`;

await writeFile(`${runFolder}/woorenewal_public_target_screen.csv`, `${csvHeader.map(csv).join(",")}\n${csvRows.join("\n")}\n`);
await writeFile(`${runFolder}/research_woorenewal_public_target_screen.md`, report);

console.log(JSON.stringify({ uniqueScreened: rows.length, priorityCandidates: priority.length, top: priority.slice(0, 10).map(row => ({ slug: row.plugin.slug, score: row.screen.score, installs: row.plugin.active_installs, last_updated: row.plugin.last_updated })) }, null, 2));
