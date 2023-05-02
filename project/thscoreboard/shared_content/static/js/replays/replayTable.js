const replayTableBatchSize = 50;
const replayTableBodyHtml = document.getElementById('replay-table-body');
const displayedColumns = [
  "User", "Game", "Difficulty", "Shot", "Route", "Score", "Upload Date", "Comment", "Replay"
];

// Initialize global variables if they were not provided by html
// Needed for jest environment

var activeFilters = {};
var allReplays = [];

try {
  requestAndInitializeReplays();
} catch(error) {
  // Catch ReferenceError for test suite but do nothing
}

function requestAndInitializeReplays() {
  const requestUri = window.location.pathname === '/'
    ? window.location.origin + '/replays/index/json'
    : window.location.origin + window.location.pathname + "/json";

  fetch(requestUri, {
    headers: {
      'Accept-Encoding': 'gzip'
    },
    priority: 'high'
  })
  .then(response => {
    if (!response.ok) {
      replayTableBodyHtml.innerHTML =
        '<p style="color: red;">Failed to load replays</p>';
    }
    return response.json();
  })
  .then(replayJson => {
    allReplays = replayJson
    const filteredReplays = filterReplays(activeFilters, allReplays);
    constructAndRenderReplayTable(filteredReplays);
  });
}

function onClick(elm) {
  const filterType = elm.getAttribute('filterType');
  const value = elm.getAttribute('value');

  activeFilters = updateFilters(activeFilters, filterType, value);
  const filteredReplays = filterReplays(activeFilters, allReplays);
  constructAndRenderReplayTable(filteredReplays);
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

function constructAndRenderReplayTable(replays) {
  clearTableHtml();

  let startIndex = 0;
  let endIndex = Math.min(replayTableBatchSize, replays.length);
  while (startIndex < replays.length) {
    isFirstBatch = startIndex === 0;
    constructAndRenderTableBatch(
      replays, startIndex, endIndex, isFirstBatch
    );
    startIndex += replayTableBatchSize;
    endIndex += replayTableBatchSize;
    endIndex = Math.min(endIndex, replays.length);
  }
}

function constructAndRenderTableBatch(replays, startIndex, endIndex, isFirstBatch) {
  if (isFirstBatch) {
    populateTable(replays, startIndex, endIndex);
  } else {
    delayedPopulateTable(replays, startIndex, endIndex);
  }
}

function delayedPopulateTable(replays, startIndex, endIndex) {
  // Delays the execution of the populateTable function to prevent blocking the
  // main thread and improve performance. This allows other code to run, such
  // as UI updates, while the table is being populated.
  setTimeout(() => {
    populateTable(replays, startIndex, endIndex)
  }, 1);
}

function populateTable(replays, startIndex, endIndex) {
  for (let i = startIndex; i < endIndex; i++) {
    const replay = replays[i];
    const row = document.createElement('tr');
    for (const [columnName, value] of Object.entries(replay)) {
      const cell = createTableCell(columnName, value)
      if (cell) {
        row.appendChild(cell);
      }
    }
    replayTableBodyHtml.appendChild(row);
  }
}

 function createTableCell(columnName, value) {
  const cell = document.createElement('td');
  if (!displayedColumns.includes(columnName)) {
    return null;
  }
  if (columnName === "Game" && !showGameColumn) {
    return null;
  }
  if (columnName === "Route" && !showRouteColumn) {
    return null;
  }

  // Value is primitive or has type {"text": ..., "url": ...}
  if (typeof value === "object") {
    cell.appendChild(createLink(value.url, value.text));
  } else {
    const text = document.createTextNode(value);
    cell.appendChild(text);
  }
  if (columnName === "Shot" || columnName === "Route" || columnName === "Score") {
    cell.className = "nowrap";
  } else if (columnName === "Comment") {
    cell.className = "comment-cell"
  }
  return cell;
}

function createLink(url, text) {
  const link = document.createElement('a'); // 'a' as in the <a> HTML tag
  link.href = url;
  const linkText = document.createTextNode(text);
  link.appendChild(linkText)
  return link;
}

function clearTableHtml() {
  replayTableBodyHtml.innerHTML = '';
}

try {
  module.exports = {updateFilters, filterReplays};
} catch(error) {
  // Shut up error in console but do nothing
}
