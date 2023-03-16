// Initialize global variables if they were not provided by html
// Needed for jest environment
if (typeof allReplays === 'undefined') {
  allReplays = [];
  showGameColumn = true;
}

var activeFilters = [];

// initialize table content
populateTable(allReplays);


function onClick(elm) {
  const filterType = elm.getAttribute('filterType');
  const value = elm.getAttribute('value');
  
  activeFilters = updateFilters(activeFilters, filterType, value);
  const filteredReplays = filterReplays();
  console.log(activeFilters)
  populateTable(filteredReplays);
}

function updateFilters(filters, filterType, value) {
  if (filters[filterType] === undefined) {
    filters[filterType] = [];
  }
  const indexOfValue = filters[filterType].indexOf(value);
  if (indexOfValue == -1) {
    filters[filterType].push(value);
  }
  else {
    filters[filterType].splice(indexOfValue, 1);
    if (filters[filterType].length == 0) {
      delete filters[filterType];
    }
  }
  return filters;
}

function filterReplays() {
  let filteredReplays = [...allReplays];
  activeFilters.forEach((filter) => {
    filterType = filter.filterType;
    allowedValues = filter.values;
    filteredReplays = filteredReplays.filter((tableEntry) => {
      console.log(tableEntry);
      return allowedValues.includes(tableEntry[filterType]);
    });
  });
  return filteredReplays;
}

function populateTable(replays) {
  const replayTableHtml = document.getElementById('replay-table');
  const tbody = replayTableHtml.getElementsByTagName('tbody')[0];
  
  // Clear the existing rows from the table body
  tbody.innerHTML = '';

  for (let i = 0; i < replays.length; i++) {
    const row = document.createElement('tr');
    const replay  = replays[i]
    const replayKeysAndValues = Object.entries(replay);
    for (let j = 0; j < replayKeysAndValues.length; j++) {
      const columnName = replayKeysAndValues[j][0];
      const value = replayKeysAndValues[j][1];
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
  if (columnName === "Replay") {
    const link = document.createElement('a');
    link.href = value;
    const linkText = document.createTextNode('Download');
    link.appendChild(linkText);
    cell.appendChild(link);
  }
  else {
    const text = document.createTextNode(value);
    cell.appendChild(text);
  }
  return cell;
}

module.exports = updateFilters;
