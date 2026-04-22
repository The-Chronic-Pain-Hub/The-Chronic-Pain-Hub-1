const MODULE4_BACKEND_BASE_URL = window.MODULE4_BACKEND_BASE_URL || "";
const NPI_PAIN_QUERY = {
  version: "2.1",
  state: "WI",
  taxonomy_description: "Pain",
  limit: "10"
};

function formatDisplayDate(dateString) {
  if (!dateString) {
    return "Unknown";
  }

  const parsed = new Date(`${dateString}T00:00:00`);

  if (Number.isNaN(parsed.getTime())) {
    return dateString;
  }

  return new Intl.DateTimeFormat("en-US", {
    month: "long",
    day: "numeric",
    year: "numeric"
  }).format(parsed);
}

function buildBackendNpiUrl() {
  const params = new URLSearchParams(NPI_PAIN_QUERY);
  return `${MODULE4_BACKEND_BASE_URL}/api/nppes?${params.toString()}`;
}

function prettifyLabel(value) {
  if (!value) {
    return "";
  }

  const trimmed = value.trim();
  const lettersOnly = trimmed.replace(/[^A-Za-z]/g, "");
  const isMostlyUppercase = lettersOnly && lettersOnly === lettersOnly.toUpperCase();

  if (!isMostlyUppercase) {
    return trimmed;
  }

  return trimmed
    .toLowerCase()
    .replace(/\b\w/g, character => character.toUpperCase());
}

function getPreferredAddress(addresses) {
  if (!Array.isArray(addresses)) {
    return {};
  }

  return addresses.find(address => address.address_purpose === "LOCATION") || {};
}

function getProviderName(item) {
  const basic = item.basic || {};

  if (basic.organization_name) {
    return basic.organization_name;
  }

  return [
    basic.name_prefix,
    basic.first_name,
    basic.middle_name,
    basic.last_name,
    basic.name_suffix
  ].filter(Boolean).join(" ").replace(/\s+/g, " ").trim() || `NPI ${item.number || "unknown"}`;
}

function getProviderSpecialty(item) {
  const taxonomies = Array.isArray(item.taxonomies) ? item.taxonomies : [];
  const descriptions = taxonomies
    .map(taxonomy => taxonomy.desc || taxonomy.code)
    .filter(Boolean);

  return descriptions.slice(0, 2).join(", ") || "Pain-focused provider";
}

function hasMedicaidIdentifier(item) {
  const identifiers = Array.isArray(item.identifiers) ? item.identifiers : [];

  return identifiers.some(identifier => {
    const description = `${identifier.desc || ""} ${identifier.issuer || ""}`.toLowerCase();
    return description.includes("medicaid");
  });
}

function normalizeNppesProvider(item) {
  const basic = item.basic || {};
  const address = getPreferredAddress(item.addresses);

  return {
    npi: String(item.number || ""),
    name: getProviderName(item),
    enumerationType: item.enumeration_type || "NPI",
    specialty: getProviderSpecialty(item),
    city: address.city || "",
    state: address.state || "",
    phone: address.telephone_number || basic.authorized_official_telephone_number || "",
    address1: address.address_1 || "",
    address2: address.address_2 || "",
    postalCode: address.postal_code || "",
    taxonomyCode: ((item.taxonomies || [])[0] || {}).code || "",
    acceptsMedicaid: hasMedicaidIdentifier(item),
    lastUpdated: basic.last_updated || ""
  };
}

async function fetchLivePainProviders() {
  const response = await fetch(buildBackendNpiUrl());

  if (!response.ok) {
    throw new Error(`Module 4 backend returned ${response.status}`);
  }

  const payload = await response.json();
  const results = Array.isArray(payload.results) ? payload.results : [];

  return {
    sourceLabel: "Live Module4 backend NPI query",
    sourceUrl: buildBackendNpiUrl(),
    totalResults: results.length,
    providers: results
      .map(normalizeNppesProvider)
      .filter(provider => provider.state === "WI")
  };
}

function createMetricCard(label, value) {
  const card = document.createElement("div");
  card.className = "metric-card";

  const number = document.createElement("span");
  number.className = "metric-value";
  number.textContent = value;

  const text = document.createElement("span");
  text.className = "metric-label";
  text.textContent = label;

  card.append(number, text);
  return card;
}

function createPriorityItem(item) {
  const wrapper = document.createElement("article");
  wrapper.className = "priority-item";

  const county = document.createElement("h4");
  county.textContent = item.county;

  const meta = document.createElement("p");
  meta.textContent = `${item.shortageAreas} shortage areas tracked here`;

  const score = document.createElement("p");
  score.className = "priority-meta";
  score.textContent = `Peak score ${item.maxScore || "NA"} | Rural areas ${item.ruralAreas}`;

  wrapper.append(county, meta, score);
  return wrapper;
}

function createShortageItem(item) {
  const wrapper = document.createElement("article");
  wrapper.className = "shortage-item";

  const title = document.createElement("h4");
  title.textContent = prettifyLabel(item.name);

  const summary = document.createElement("p");
  summary.textContent = `${item.county} | ${prettifyLabel(item.city)} | Score ${item.score || "NA"}`;

  const meta = document.createElement("p");
  meta.className = "priority-meta";
  meta.textContent = `${item.designationType} | ${item.ruralStatus}`;

  wrapper.append(title, summary, meta);
  return wrapper;
}

function createProviderCard(provider) {
  const card = document.createElement("article");
  card.className = "provider-card";

  const title = document.createElement("h4");
  title.textContent = prettifyLabel(provider.name);

  const specialty = document.createElement("p");
  specialty.className = "provider-specialty";
  specialty.textContent = provider.specialty;

  const location = document.createElement("p");
  const addressParts = [
    prettifyLabel(provider.address1),
    prettifyLabel(provider.address2),
    [prettifyLabel(provider.city), provider.state, provider.postalCode].filter(Boolean).join(", ")
  ].filter(Boolean);
  location.textContent = addressParts.join(" | ") || "Listed practice location unavailable";

  const contact = document.createElement("p");
  contact.textContent = provider.phone ? `Phone ${provider.phone}` : `NPI ${provider.npi}`;

  const meta = document.createElement("div");
  meta.className = "provider-meta";

  const medicaid = document.createElement("span");
  medicaid.className = provider.acceptsMedicaid ? "provider-pill provider-pill-positive" : "provider-pill";
  medicaid.textContent = provider.acceptsMedicaid ? "Medicaid ID on file" : "No Medicaid ID shown";

  const type = document.createElement("span");
  type.className = "provider-pill";
  type.textContent = provider.enumerationType;

  const updated = document.createElement("span");
  updated.className = "provider-pill";
  updated.textContent = provider.lastUpdated ? `Updated ${formatDisplayDate(provider.lastUpdated)}` : "Update date unavailable";

  meta.append(medicaid, type, updated);
  card.append(title, specialty, location, contact, meta);
  return card;
}

function renderProviderGrid(npi) {
  const providerGrid = document.getElementById("provider-grid");
  providerGrid.innerHTML = "";

  if (!npi.providers.length) {
    const empty = document.createElement("p");
    empty.className = "dashboard-note";
    empty.textContent = "No live pain-provider matches were returned by the backend.";
    providerGrid.appendChild(empty);
    return;
  }

  npi.providers.forEach(provider => providerGrid.appendChild(createProviderCard(provider)));
}

function renderStaticSnapshot(data, npi, generatedDate, isLiveBackend) {
  const hpsa = data.wiHpsa;

  document.getElementById("snapshot-hpsa").textContent = hpsa.totalDesignated;
  document.getElementById("snapshot-counties").textContent = hpsa.countiesRepresented;
  document.getElementById("snapshot-rural").textContent = hpsa.ruralDesignated;
  document.getElementById("snapshot-providers").textContent = npi.totalResults;
  document.getElementById("snapshot-caption").textContent = isLiveBackend
    ? `Shortage snapshot refreshed ${generatedDate}; provider matches are loaded from the Module4 backend.`
    : `Shortage snapshot refreshed ${generatedDate}; bundled provider data is showing because the backend is unavailable.`;
  document.getElementById("module4-refresh").textContent = isLiveBackend
    ? `Backend API connected. HRSA snapshot: ${generatedDate}`
    : `Backend unavailable. Showing bundled provider snapshot from ${generatedDate}.`;
  document.getElementById("hpsa-note").textContent = hpsa.note;

  const hpsaSourceLink = document.getElementById("hpsa-source-link");
  hpsaSourceLink.href = hpsa.sourceUrl;
  hpsaSourceLink.textContent = `Open ${hpsa.sourceLabel}`;

  const metricGrid = document.getElementById("hpsa-metrics");
  metricGrid.innerHTML = "";
  [
    createMetricCard("WI designated areas", hpsa.totalDesignated),
    createMetricCard("Rural designations", hpsa.ruralDesignated),
    createMetricCard("Metro and non-rural", hpsa.metroDesignated),
    createMetricCard("Counties represented", hpsa.countiesRepresented)
  ].forEach(card => metricGrid.appendChild(card));

  const countyPriorityList = document.getElementById("county-priority-list");
  countyPriorityList.innerHTML = "";
  hpsa.countyPriority.forEach(item => countyPriorityList.appendChild(createPriorityItem(item)));

  const topShortageList = document.getElementById("top-shortage-list");
  topShortageList.innerHTML = "";
  hpsa.topShortageAreas.forEach(item => topShortageList.appendChild(createShortageItem(item)));
}

async function populateModule4() {
  const data = window.module4Data;

  if (!data || !data.wiHpsa || !data.npiPainProviders) {
    const refreshNode = document.getElementById("module4-refresh");
    const captionNode = document.getElementById("snapshot-caption");

    if (refreshNode) {
      refreshNode.textContent = "Module 4 snapshot data could not be loaded.";
    }

    if (captionNode) {
      captionNode.textContent = "The local Module 4 data bundle is missing.";
    }

    return;
  }

  const generatedDate = formatDisplayDate(data.generatedAt);
  let npi = data.npiPainProviders;
  let isLiveBackend = false;
  const npiSourceLink = document.getElementById("npi-source-link");

  try {
    npi = await fetchLivePainProviders();
    isLiveBackend = true;
    npiSourceLink.href = npi.sourceUrl;
    npiSourceLink.textContent = "Open live backend NPI query";
  } catch (error) {
    npiSourceLink.href = npi.sourceUrl;
    npiSourceLink.textContent = "Open fallback NPI query";
  }

  renderStaticSnapshot(data, npi, generatedDate, isLiveBackend);
  renderProviderGrid(npi);
}

populateModule4();
