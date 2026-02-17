/* AI Act Advisors — Client-side filtering */
function applyFilters() {
  const cards = document.querySelectorAll('.listing-card');
  const country = (document.getElementById('filter-country') || {}).value || '';
  const sector = (document.getElementById('filter-sector') || {}).value || '';
  const size = (document.getElementById('filter-size') || {}).value || '';
  const searchText = ((document.getElementById('search-text') || {}).value || '').toLowerCase();

  let visible = 0;
  cards.forEach(card => {
    const cCountry = card.dataset.country || '';
    const cSize = card.dataset.size || '';
    const cSectors = card.dataset.sectors || '';
    const cServices = card.dataset.services || '';
    const cText = card.textContent.toLowerCase();

    let show = true;
    if (country && cCountry !== country) show = false;
    if (sector && !cSectors.includes(sector)) show = false;
    if (size && cSize !== size) show = false;
    if (searchText && !cText.includes(searchText)) show = false;

    card.style.display = show ? '' : 'none';
    if (show) visible++;
  });

  const counter = document.getElementById('results-count');
  if (counter) counter.textContent = visible;

  const noResults = document.getElementById('no-results');
  if (noResults) noResults.style.display = visible === 0 ? '' : 'none';
}

function clearFilters() {
  const selects = document.querySelectorAll('.filter-bar select');
  selects.forEach(s => s.value = '');
  const searchInput = document.getElementById('search-text');
  if (searchInput) searchInput.value = '';
  applyFilters();
}

// Live search on keyup
document.addEventListener('DOMContentLoaded', function() {
  const searchInput = document.getElementById('search-text');
  if (searchInput) {
    searchInput.addEventListener('keyup', function(e) {
      if (e.key === 'Enter' || this.value.length >= 2 || this.value.length === 0) {
        applyFilters();
      }
    });
  }

  // Filter selects auto-apply
  document.querySelectorAll('.filter-bar select').forEach(sel => {
    sel.addEventListener('change', applyFilters);
  });
});
