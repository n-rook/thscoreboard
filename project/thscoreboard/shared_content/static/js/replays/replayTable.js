const replayTableBatchSize = 50;
const replayTableBodyHtml = document.getElementById('replay-table-body');
const displayedColumns = [
  "User", "Game", "Difficulty", "Shot", "Route", "Score", "Upload Date", "Comment", "Replay"
];

var activeFilters = {};
var allReplays = [];
var tableResetCounter = 0;

initializeFilters();
requestAndInitializeReplays();

async function requestAndInitializeReplays() {
  const requestUri = window.location.pathname === '/'
    ? window.location.origin + '/replays/index/json'
    : window.location.origin + window.location.pathname + "/json";

  try {
    const response = await fetch(requestUri, {priority: 'high'});

    if (!response.ok) {
      replayTableBodyHtml.innerHTML =
        '<p style="color: red;">Failed to load replays</p>';
      return;
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder('utf-8');
    let buffer = '';

    while (true) {
      const { done, value } = await reader.read();
      if (done) {
        return;
      }

      buffer += decoder.decode(value, { stream: true });
      const jsonStrings = buffer.split('\n');

      const newReplays = [];
      while (jsonStrings.length > 1) {
        const jsonString = jsonStrings.shift();
        const replay = JSON.parse(jsonString);
        newReplays.push(replay);
      }
      // The final string might be incomplete, so instead of parsing it we store it in the buffer
      buffer = jsonStrings[0] || '';

      addReplaysToTable(filterReplays(activeFilters, newReplays));
      allReplays.push(...newReplays);
    }

  } catch (error) {}
}

function initializeFilters() {
  const allButtons = document.querySelectorAll('button[filtertype]')
  for (const button of allButtons) {
    const filterType = button.getAttribute('filtertype');
    activeFilters[filterType] = 'All';
  }
}

function onClick(elm) {
  const filterType = elm.getAttribute('filterType');
  const value = elm.getAttribute('value');

  activeFilters = updateFilters(activeFilters, filterType, value);
  updateButtons(activeFilters);
  const filteredReplays = filterReplays(activeFilters, allReplays);
  clearTableHtml();
  addReplaysToTable(filteredReplays);
}

function updateButtons(activeFilters) {
  const allButtons = document.querySelectorAll('button[filtertype]')
  for (const button of allButtons) {
    const filterType = button.getAttribute('filtertype');
    const value = button.value;
    if (activeFilters[filterType] === value) {
      button.className = "button pressed";
    }
    else {
      button.className = "button";
    }
  }
}

function updateFilters(filters, filterType, value) {
  filters[filterType] = value;
  return filters;
}

function filterReplays(filters, replays) {
  let filteredReplays = [...replays];
  for (const [filterType, allowedValues] of Object.entries(filters)) {
    if (allowedValues !== "All") {
      filteredReplays = filteredReplays.filter((replay) => {
        return replay[filterType] === allowedValues;
      });
    }
  };
  return filteredReplays;
}

function addReplaysToTable(replays){
  let startIndex = 0;
  let endIndex = Math.min(replayTableBatchSize, replays.length);
  while (startIndex < replays.length) {
    constructAndRenderTableBatch(
      replays, startIndex, endIndex
    );
    startIndex += replayTableBatchSize;
    endIndex += replayTableBatchSize;
    endIndex = Math.min(endIndex, replays.length);
  }
}

function constructAndRenderTableBatch(replays, startIndex, endIndex) {
  const tableResetsAtSchedulingTime = tableResetCounter;
  // Delays the execution of the populateTable function to prevent blocking the
  // main thread and improve performance. This allows other code to run, such
  // as UI updates, while the table is being populated.
  setTimeout(() => {
    const tableResetsAtCallTime = tableResetCounter;
    if (tableResetsAtCallTime != tableResetsAtSchedulingTime) {
      // table was reset, call is invalid
      return;
    }

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
  tableResetCounter++;
}

try {
  module.exports = {updateFilters, filterReplays};
} catch(error) {
  // Shut up error in console but do nothing
}
