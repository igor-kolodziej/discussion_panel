import { writeFile } from "node:fs/promises";

const base = "https://marketplace.atlassian.com";
const runFolder = "/Users/igor/Desktop/discussion_panel/working_folder/zero_to_one_candidates_20260713_073235";

async function getJson(url) {
  const response = await fetch(url, { headers: { "User-Agent": "LegacyBridge-research/1.0" } });
  if (!response.ok) throw new Error(`${response.status} ${url}`);
  return response.json();
}

const all = [];
for (let offset = 0; offset < 1000; offset += 50) {
  const url = new URL("/rest/2/addons", base);
  url.searchParams.set("application", "jira");
  url.searchParams.set("hosting", "dataCenter");
  url.searchParams.set("withVersion", "true");
  url.searchParams.set("offset", String(offset));
  url.searchParams.set("limit", "50");
  const body = await getJson(url);
  const addons = body?._embedded?.addons || [];
  all.push(...addons);
  if (addons.length < 50) break;
}

const small = all
  .filter(addon => {
    const installs = Number(addon?._embedded?.distribution?.totalInstalls || 0);
    const version = addon?._embedded?.version;
    return installs >= 5 && installs <= 500 && version?.paymentModel === "atlassian";
  })
  .sort((a, b) => Number(b?._embedded?.distribution?.totalInstalls || 0) - Number(a?._embedded?.distribution?.totalInstalls || 0));

const shortlist = [];
const candidates = small;
for (let index = 0; index < candidates.length; index += 12) {
  const batch = candidates.slice(index, index + 12);
  const checked = await Promise.all(batch.map(async addon => {
    const cloudUrl = new URL(`/rest/2/addons/${encodeURIComponent(addon.key)}`, base);
    cloudUrl.searchParams.set("hosting", "cloud");
    cloudUrl.searchParams.set("withVersion", "true");
    let cloud = false;
    try {
      const details = await getJson(cloudUrl);
      cloud = Boolean(details?._embedded?.version?.deployment?.cloud || details?._embedded?.version?.deployment?.connect);
    } catch {
      cloud = false;
    }
    return { addon, cloud };
  }));
  shortlist.push(...checked);
}

const dcOnly = shortlist.filter(row => !row.cloud);

for (let index = 0; index < dcOnly.length; index += 10) {
  const batch = dcOnly.slice(index, index + 10);
  const priced = await Promise.all(batch.map(async row => {
    const pricingUrl = `${base}/rest/2/addons/${encodeURIComponent(row.addon.key)}/pricing/datacenter/live`;
    try {
      const pricing = await getJson(pricingUrl);
      const commercial = (pricing?.items || []).filter(item => item.licenseType === "COMMERCIAL");
      const atTier = tier => commercial.find(item => Number(item.unitCount) === tier)?.amount ?? "";
      return {
        ...row,
        minAnnualPriceUsd: commercial.length ? Math.min(...commercial.map(item => Number(item.amount))) : "",
        price500Usd: atTier(500),
        price2000Usd: atTier(2000)
      };
    } catch {
      return { ...row, minAnnualPriceUsd: "", price500Usd: "", price2000Usd: "" };
    }
  }));
  dcOnly.splice(index, batch.length, ...priced);
}

function clean(value = "") {
  return String(value).replace(/<[^>]+>/g, " ").replace(/\s+/g, " ").trim();
}

function csv(value) {
  return `"${String(value ?? "").replaceAll('"', '""')}"`;
}

const header = ["rank", "name", "key", "vendor", "installs", "downloads", "reviews", "stars", "last_modified", "release_date", "cloud_version_found", "min_annual_price_usd", "price_500_users_usd", "price_2000_users_usd", "tagline", "marketplace_url", "seller_status", "paid_customers", "revenue", "asking_price", "transfer_interest"];
const rows = dcOnly.map((row, index) => {
  const a = row.addon;
  return [
    index + 1,
    a.name,
    a.key,
    a?._embedded?.vendor?.name,
    a?._embedded?.distribution?.totalInstalls,
    a?._embedded?.distribution?.downloads,
    a?._embedded?.reviews?.count,
    a?._embedded?.reviews?.averageStars,
    a?._embedded?.lastModified,
    a?._embedded?.version?.release?.date,
    row.cloud,
    row.minAnnualPriceUsd,
    row.price500Usd,
    row.price2000Usd,
    clean(a.tagLine),
    `${base}${a?._links?.alternate?.href || ""}`,
    "unknown",
    "unknown",
    "unknown",
    "unknown",
    "unknown"
  ].map(csv).join(",");
});

const affordableBand = dcOnly.filter(row => {
  const installs = Number(row.addon?._embedded?.distribution?.totalInstalls || 0);
  return installs >= 5 && installs <= 60;
});

const reportRows = affordableBand.slice(0, 60).map((row, index) => {
  const a = row.addon;
  return `| ${index + 1} | [${a.name}](${base}${a?._links?.alternate?.href || ""}) | ${a?._embedded?.vendor?.name || ""} | ${a?._embedded?.distribution?.totalInstalls || 0} | ${a?._embedded?.reviews?.count || 0} | ${row.minAnnualPriceUsd || "n/a"} | ${row.price500Usd || "n/a"} | ${a?._embedded?.version?.release?.date || ""} |`;
});

const report = `# Atlassian Data Center Legacy-App Public Screen\n\n` +
  `- Screen date: 2026-07-13\n` +
  `- Official source: Atlassian Marketplace REST API\n` +
  `- Jira Data Center apps screened: ${all.length}\n` +
  `- Small paid-via-Atlassian apps (5–500 installs): ${small.length}\n` +
  `- Small apps checked for a Cloud version: ${shortlist.length}\n` +
  `- No Cloud version found in the public API check: ${dcOnly.length}\n\n` +
  `- No-Cloud apps in the 5–60-install affordability band: ${affordableBand.length}\n\n` +
  `The screen proves a sizeable public pool of small paid Data Center apps and identifies apps without a detected Cloud version. It does not prove that any vendor wants to sell, that the install count equals paid active customers, that app revenue is affordable, or that code/customer obligations transfer inside the founder's capital cap.\n\n` +
  `## Public Legacy Leads In The 5–60-Install Band\n\n` +
  `| Rank | App | Vendor | Installs | Reviews | Minimum annual price (USD) | 500-user annual price (USD) | Latest DC release |\n|---:|---|---|---:|---:|---:|---:|---|\n` +
  reportRows.join("\n") +
  `\n\n## Gate Interpretation\n\n` +
  `A lead becomes acquisition-plausible only after the vendor supplies proof of paid active licences, revenue, renewal, support burden, code/IP, cloud-gap scope, and written willingness to transfer through Atlassian's official process under the cash cap. No vendor was contacted.\n`;

await writeFile(`${runFolder}/atlassian_legacy_app_screen.csv`, `${header.map(csv).join(",")}\n${rows.join("\n")}\n`);
await writeFile(`${runFolder}/research_atlassian_legacy_app_screen.md`, report);

console.log(JSON.stringify({ screened: all.length, smallPaid: small.length, cloudChecked: shortlist.length, dcOnly: dcOnly.length, affordabilityBand: affordableBand.length, top: affordableBand.slice(0, 10).map(row => ({ name: row.addon.name, installs: row.addon?._embedded?.distribution?.totalInstalls, vendor: row.addon?._embedded?.vendor?.name, minimumAnnualPriceUsd: row.minAnnualPriceUsd, price500Usd: row.price500Usd, release: row.addon?._embedded?.version?.release?.date })) }, null, 2));
