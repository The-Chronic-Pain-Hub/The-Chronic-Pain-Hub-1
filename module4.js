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
    `${prettifyLabel(provider.city)}, ${provider.state}`
  ].filter(Boolean);
  location.textContent = addressParts.join(" | ");

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

  meta.append(medicaid, type);
  card.append(title, specialty, location, contact, meta);
  return card;
}

function populateModule4() {
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
  const hpsa = data.wiHpsa;
  const npi = data.npiPainProviders;

  document.getElementById("snapshot-hpsa").textContent = hpsa.totalDesignated;
  document.getElementById("snapshot-counties").textContent = hpsa.countiesRepresented;
  document.getElementById("snapshot-rural").textContent = hpsa.ruralDesignated;
  document.getElementById("snapshot-providers").textContent = npi.totalResults;
  document.getElementById("snapshot-caption").textContent = `Snapshot refreshed ${generatedDate} from public Wisconsin HRSA and NPI source data.`;
  document.getElementById("module4-refresh").textContent = `Source snapshot: ${generatedDate}`;
  document.getElementById("hpsa-note").textContent = hpsa.note;

  const hpsaSourceLink = document.getElementById("hpsa-source-link");
  hpsaSourceLink.href = hpsa.sourceUrl;
  hpsaSourceLink.textContent = `Open ${hpsa.sourceLabel}`;

  const npiSourceLink = document.getElementById("npi-source-link");
  npiSourceLink.href = npi.sourceUrl;
  npiSourceLink.textContent = `Open ${npi.sourceLabel}`;

  const metricGrid = document.getElementById("hpsa-metrics");
  [
    createMetricCard("WI designated areas", hpsa.totalDesignated),
    createMetricCard("Rural designations", hpsa.ruralDesignated),
    createMetricCard("Metro and non-rural", hpsa.metroDesignated),
    createMetricCard("Counties represented", hpsa.countiesRepresented)
  ].forEach(card => metricGrid.appendChild(card));

  const countyPriorityList = document.getElementById("county-priority-list");
  hpsa.countyPriority.forEach(item => countyPriorityList.appendChild(createPriorityItem(item)));

  const topShortageList = document.getElementById("top-shortage-list");
  hpsa.topShortageAreas.forEach(item => topShortageList.appendChild(createShortageItem(item)));

  const providerGrid = document.getElementById("provider-grid");
  npi.providers.forEach(provider => providerGrid.appendChild(createProviderCard(provider)));
}

populateModule4();
