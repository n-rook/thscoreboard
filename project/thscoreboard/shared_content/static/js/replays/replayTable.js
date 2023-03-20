// Initialize global variables if they were not provided by html
// Needed for jest environment
if (typeof allReplays === 'undefined') {
  allReplays = [];
  showGameColumn = true;
  gameId = "th01";
  replayId = "aaaa";
}

var activeFilters = {};

// initialize table content
populateTable(allReplays);


function onClick(elm) {
  const filterType = elm.getAttribute('filterType');
  const value = elm.getAttribute('value');
  
  activeFilters = updateFilters(activeFilters, filterType, value);
  const filteredReplays = filterReplays(activeFilters, allReplays);
  populateTable(filteredReplays);
}

function updateFilters(filters, filterType, value) {
  if (filters[filterType] === undefined) {
    filters[filterType] = [];
  }
  const indexOfValue = filters[filterType].indexOf(value);
  if (indexOfValue === -1) {
    filters[filterType].push(value);
  }
  else {
    filters[filterType].splice(indexOfValue, 1);
    if (filters[filterType].length === 0) {
      delete filters[filterType];
    }
  }
  return filters;
}

function filterReplays(filters, replays) {
  let filteredReplays = [...replays];
  for (const [filterType, allowedValues] of Object.entries(filters)) {
    filteredReplays = filteredReplays.filter((replay) => {
      return allowedValues.includes(replay[filterType]);
    });
  };
  return filteredReplays;
}

function populateTable(replays) {
  const replayTableHtml = document.getElementById('replay-table');
  const tbody = replayTableHtml.getElementsByTagName('tbody')[0];
  
  // Clear the existing rows from the table body
  tbody.innerHTML = '';

  for (const replay of replays) {
    const row = document.createElement('tr');
    for (const [columnName, value] of Object.entries(replay)) {
      const cell = createTableCell(columnName, value)
      if (cell) {
        row.appendChild(cell);
      }
    }
    tbody.appendChild(row);
  }
}

function createTableCell(columnName, value) {
  const cell = document.createElement('td');
  if (columnName === "Game" && !showGameColumn) {
    return null;
  }

  // Value is primitive or has type {"text": ..., "url": ...}
  if (typeof value === "object") {
    const link = document.createElement('a'); // 'a' as in html <a> tag
    link.href = value.url;
    const linkText = document.createTextNode(value.text);
    link.appendChild(linkText);
    cell.appendChild(link);
  } else {
    const text = document.createTextNode(value);
    cell.appendChild(text);
  }
  return cell;
}

module.exports = {updateFilters, filterReplays};
