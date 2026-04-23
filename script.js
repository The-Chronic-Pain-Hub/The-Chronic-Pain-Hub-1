const anchorLinks = document.querySelectorAll('a[href^="#"]');

anchorLinks.forEach(anchor => {
  anchor.addEventListener('click', event => {
    const targetId = anchor.getAttribute('href');
    const target = document.querySelector(targetId);

    if (target) {
      event.preventDefault();
      target.scrollIntoView({
        behavior: 'smooth',
        block: 'start'
      });
    }
  });
});

const revealElements = document.querySelectorAll('.reveal');

if (revealElements.length) {
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        observer.unobserve(entry.target);
      }
    });
  }, {
    threshold: 0.2
  });

  revealElements.forEach(element => observer.observe(element));
}

const SUPPORT_SEARCH_TERMS = {
  "Sleep support": ["Sleep Medicine*", "Psychologist*"],
  "Mobility and movement": ["Physical Therapist*", "Occupational Therapist*", "Rehabilitation*"],
  "Mental health care": ["Counselor*", "Psychologist*", "Clinical Social Worker*"],
  "Care navigation": ["Pain Medicine*", "Rehabilitation*"],
  "Non-pharmaceutical options": ["Physical Therapist*", "Chiropractor*", "Acupuncturist*"]
};

const zipInput = document.getElementById("zip");
const needSelect = document.getElementById("need");
const supportSearchBtn = document.getElementById("supportSearchBtn");
const supportSearchStatus = document.getElementById("supportSearchStatus");
const supportResults = document.getElementById("supportResults");
const SUPPORT_RESULTS_PAGE_SIZE = 6;
const SUPPORT_RESULTS_API_LIMIT = 25;
let supportSearchState = {
  zip: "",
  need: "",
  providers: [],
  visibleCount: SUPPORT_RESULTS_PAGE_SIZE
};

function escapeHtml(value) {
  return String(value)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
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

function getPreferredAddress(addresses) {
  if (!Array.isArray(addresses)) {
    return {};
  }

  return addresses.find(address => address.address_purpose === "LOCATION") || {};
}

function formatProviderAddress(address) {
  const cityState = [address.city, address.state].filter(Boolean).join(", ");
  const cityLine = [cityState, address.postal_code].filter(Boolean).join(" ");

  return [
    address.address_1,
    address.address_2,
    cityLine
  ].filter(Boolean).join(", ") || "Address not listed";
}

function getProviderSpecialty(item) {
  const taxonomies = Array.isArray(item.taxonomies) ? item.taxonomies : [];
  const descriptions = taxonomies
    .map(taxonomy => taxonomy.desc || taxonomy.code)
    .filter(Boolean);

  return descriptions.slice(0, 2).join(", ") || "Supportive care provider";
}

function normalizeSupportProvider(item) {
  const basic = item.basic || {};
  const address = getPreferredAddress(item.addresses);

  return {
    npi: String(item.number || ""),
    name: getProviderName(item),
    specialty: getProviderSpecialty(item),
    address: formatProviderAddress(address),
    postalCode: String(address.postal_code || ""),
    phone: address.telephone_number || basic.authorized_official_telephone_number || "",
    lastUpdated: basic.last_updated || ""
  };
}

async function fetchSupportProviders(zip, need) {
  const searchTerms = SUPPORT_SEARCH_TERMS[need] || [""];
  const requests = searchTerms.slice(0, 3).map(term => {
    const params = new URLSearchParams({
      version: "2.1",
      postal_code: zip,
      limit: String(SUPPORT_RESULTS_API_LIMIT)
    });

    if (term) {
      params.set("taxonomy_description", term);
    }

    return fetch(`/api/nppes?${params.toString()}`);
  });

  const responses = await Promise.all(requests);

  responses.forEach(response => {
    if (!response.ok) {
      throw new Error(`Module 4 backend returned ${response.status}`);
    }
  });

  const payloads = await Promise.all(responses.map(response => response.json()));
  const providersByNpi = new Map();

  payloads.forEach(payload => {
    const results = Array.isArray(payload.results) ? payload.results : [];
    results.forEach(item => {
      const provider = normalizeSupportProvider(item);

      if (provider.npi && provider.postalCode.startsWith(zip) && !providersByNpi.has(provider.npi)) {
        providersByNpi.set(provider.npi, provider);
      }
    });
  });

  return Array.from(providersByNpi.values());
}

function createSupportResultCard(provider) {
  const phone = provider.phone || "Phone not listed";
  const phoneDigits = provider.phone.replace(/[^\d]/g, "");
  const phoneLink = phoneDigits ? `<a href="tel:${phoneDigits}">Call</a>` : "";

  return `
    <article class="support-result-card">
      <h3>${escapeHtml(provider.name)}</h3>
      <p class="support-specialty">${escapeHtml(provider.specialty)}</p>
      <p>${escapeHtml(provider.address)}</p>
      <p>${escapeHtml(phone)}</p>
      <div class="support-result-actions">
        ${phoneLink}
      </div>
    </article>
  `;
}

function renderSupportResults() {
  if (!supportResults) {
    return;
  }

  const visibleProviders = supportSearchState.providers.slice(0, supportSearchState.visibleCount);
  const remainingCount = supportSearchState.providers.length - visibleProviders.length;
  supportSearchStatus.textContent = `${supportSearchState.providers.length} ${supportSearchState.need.toLowerCase()} matches found with a listed location in ${supportSearchState.zip}. Showing ${visibleProviders.length}.`;

  if (!supportSearchState.providers.length) {
    supportResults.innerHTML = `<div class="support-empty">No ${escapeHtml(supportSearchState.need.toLowerCase())} matches came back with a listed location in ${escapeHtml(supportSearchState.zip)}. Try another need or nearby ZIP code.</div>`;
    return;
  }

  const loadMoreButton = remainingCount > 0
    ? `<button class="load-more-results" type="button" data-load-more-results>Load more (${remainingCount} remaining)</button>`
    : "";

  supportResults.innerHTML = visibleProviders.map(createSupportResultCard).join("") + loadMoreButton;

  const loadMore = supportResults.querySelector("[data-load-more-results]");

  if (loadMore) {
    loadMore.addEventListener("click", () => {
      supportSearchState.visibleCount += SUPPORT_RESULTS_PAGE_SIZE;
      renderSupportResults();
    });
  }
}

async function runSupportSearch() {
  const zip = zipInput.value.trim();
  const need = needSelect.value;

  if (!/^\d{5}$/.test(zip)) {
    supportSearchStatus.textContent = "Enter a valid 5-digit ZIP code.";
    supportResults.innerHTML = "";
    zipInput.focus();
    return;
  }

  supportSearchBtn.disabled = true;
  supportSearchStatus.textContent = `Searching Module 4 care matches for ${zip}...`;
  supportResults.innerHTML = "";

  try {
    const providers = await fetchSupportProviders(zip, need);
    supportSearchState = {
      zip,
      need,
      providers,
      visibleCount: SUPPORT_RESULTS_PAGE_SIZE
    };
    renderSupportResults();
  } catch (error) {
    supportSearchStatus.textContent = "Module 4 backend is unavailable. Start this site with python server.py and try again.";
    supportResults.innerHTML = "";
  } finally {
    supportSearchBtn.disabled = false;
  }
}

if (zipInput && needSelect && supportSearchBtn && supportSearchStatus && supportResults) {
  zipInput.addEventListener("input", () => {
    zipInput.value = zipInput.value.replace(/\D/g, "").slice(0, 5);
  });

  zipInput.addEventListener("keydown", event => {
    if (event.key === "Enter") {
      event.preventDefault();
      runSupportSearch();
    }
  });

  supportSearchBtn.addEventListener("click", runSupportSearch);
}
