// Initialize global variables if they were not provided by html
// Needed for jest environment

var activeFilters = {};
var allReplays = [];

try {
  // initialize table content
  const xhr = new XMLHttpRequest();
  if(window.location.pathname === '/') {
    xhr.open('GET', window.location.href + 'replays/index/json', true);
  } else {
    xhr.open('GET', window.location.toString() + "/json", true);
  }
  xhr.responseType = 'json';
  xhr.onload = function() {
    if (xhr.status === 200) {
      populateTable(xhr.response);
      allReplays = xhr.response;
    } else {
      document.getElementById('replay-table').innerHTML = '<p style="color: red;">Failed to load replays</p>';
    }
  };
  xhr.send();
} catch(error) {
  // Catch ReferenceError for test suite but do nothing
}

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

function createLink(url, text) {
  const link = document.createElement('a'); // 'a' as in the <a> HTML tag
  link.href = url;
  const linkText = document.createTextNode(text);
  link.appendChild(linkText)
  return link;
}

function createTableCell(columnName, value) {
  const cell = document.createElement('td');
  if (columnName === "Game" && !showGameColumn) {
    return null;
  }

  // Value is primitive or has type {"text": ..., "url": ...}
  if (typeof value === "object") {
    cell.appendChild(createLink(value.url, value.text));
  } else if(columnName == 'User') {
    cell.appendChild(createLink(window.location.origin + '/replays/user/' + value, value));
  } else { 
    const text = document.createTextNode(value);
    cell.appendChild(text);
  }
  return cell;
}

try {
  module.exports = {updateFilters, filterReplays};
} catch(error) {
  // Shut up error in console but do nothing
}