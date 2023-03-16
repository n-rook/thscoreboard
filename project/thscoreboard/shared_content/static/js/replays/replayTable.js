var activeFilters = [];
const allReplays = htmlAllReplays;
const showGameColumn = htmlShowGameColumn;

// initialize table content
populateTable(allReplays);

function onClick(elm) {
  const filterType = elm.getAttribute('filterType');
  const value = elm.getAttribute('value');
  
  updateFilterList(filterType, value);
  const filteredReplays = filterReplays();
  populateTable(filteredReplays);
}

function updateFilterList(filterType, value) {
  const indexOfFilterType = activeFilters.findIndex(
    f => f["filterType"] == filterType
  );
  if (indexOfFilterType == -1) {
    activeFilters.push({filterType: filterType, values: [value]});
  } else {
    const activeFilterValues = activeFilters[indexOfFilterType].values;
    indexOfValue = activeFilterValues.indexOf(value);
    if (indexOfValue == -1) {
      activeFilterValues.push(value);
    }
    else {
      activeFilterValues.splice(indexOfValue);
      if (activeFilterValues.length == 0) {
        activeFilters.splice(indexOfFilterType);
      }
    }
  }
}

function filterReplays() {
  let filteredReplays = [...allReplays];
  activeFilters.forEach((filter) => {
    filterType = filter.filterType;
    allowedValues = filter.values;
    filteredReplays = filteredReplays.filter((tableEntry) => {
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
