type Link = {
  text: string;
  url: string;
};

type Replay = {
  id: string;
  user: Link | string;
  game: Link;
  difficulty: string;
  shot: string;
  route: string;
  score: Link;
  uploadDate: string;
  comment: string;
  replay: Link;
  character: string | undefined;
  season: string | undefined;
  goast: string | undefined;
};

type Filters = {
  [key in keyof Replay]?: string;
};

const replayTableBatchSize = 50;
const replayTableBodyHtml = document.getElementById('replay-table-body')!;
const displayedColumns = [
  "user", "game", "difficulty", "shot", "route", "score", "upload date", "comment", "replay"
];

var activeFilters: Filters = initializeFilters();
var allReplays: Array<Replay> = [];
var tableResetCounter: number = 0;

requestAndInitializeReplays();
initializeFilters();

async function requestAndInitializeReplays(): Promise<void> {
  const requestUri = window.location.pathname === '/'
    ? window.location.origin + '/replays/index/json'
    : window.location.origin + window.location.pathname + "/json";

  try {
    const response = await fetch(requestUri);

    if (!response.ok) {
      replayTableBodyHtml.innerHTML =
        '<p style="color: red;">Failed to load replays</p>';
      return;
    }

    const reader = response.body!.getReader();
    const decoder = new TextDecoder('utf-8');
    let buffer = '';

    while (true) {
      const { done, value } = await reader.read();
      if (done) {
        return;
      }

      buffer += decoder.decode(value, { stream: true });
      const jsonStrings = buffer.split('\n');

      const newReplays: Array<Replay> = [];
      while (jsonStrings.length > 1) {
        const jsonString = jsonStrings.shift()!;
        const replay: Replay = JSON.parse(jsonString);
        newReplays.push(replay);
      }
      // The final string might be incomplete, so instead of parsing it we store it in the buffer
      buffer = jsonStrings[0] || '';

      addReplaysToTable(filterReplays(activeFilters, newReplays));
      allReplays.push(...newReplays);
    }

  } catch (error) {}
}

function initializeFilters(): Filters {
  activeFilters = {};
  const allButtons = document.querySelectorAll('button[filtertype]')
  for (const button of allButtons) {
    // @ts-ignore
    const filterType: keyof Replay = button.getAttribute('filtertype')!;
    activeFilters[filterType] = 'All';
  }
  return activeFilters;
}

function onClick(elm: Element): void {
  // @ts-ignore
  const filterType: keyof Replay = elm.getAttribute('filterType')!;
  const value = elm.getAttribute('value')!;

  activeFilters = updateFilters(activeFilters, filterType, value);
  updateButtons(activeFilters);
  const filteredReplays = filterReplays(activeFilters, allReplays);
  clearTableHtml();
  addReplaysToTable(filteredReplays);
}

function updateButtons(activeFilters: Filters): void {
  const allButtons = document.querySelectorAll('button[filtertype]')
  for (const button of allButtons) {
    // @ts-ignore
    const filterType: keyof Replay = button.getAttribute('filtertype')!;
    // @ts-ignore
    const value: string = button["value"];
    if (activeFilters[filterType] === value) {
      button.className = "button pressed";
    }
    else {
      button.className = "button";
    }
  }
}

function updateFilters(
  filters: Filters, filterType: keyof Replay, value: string
): Filters {
  filters[filterType] = value;
  return filters;
}

function filterReplays(filters: Filters, replays: Array<Replay>): Array<Replay> {
  let filteredReplays = [...replays];
  for (const [filterType, allowedValues] of Object.entries(filters)) {
    if (allowedValues !== "All") {
      filteredReplays = filteredReplays.filter((replay) => {
        // @ts-ignore
        return replay[filterType] === allowedValues;
      });
    }
  }
  return filteredReplays;
}

function addReplaysToTable(replays: Array<Replay>): void {
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

function constructAndRenderTableBatch(
  replays: Array<Replay>, startIndex: number, endIndex: number
): void {
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

function populateTable(
  replays: Array<Replay>, startIndex: number, endIndex: number
): void {
  for (let i = startIndex; i < endIndex; i++) {
    const replay = replays[i];
    const row = document.createElement('tr');
    for (const [columnName, value] of Object.entries(replay)) {
      const cell = createTableCell(columnName, value!)
      if (cell) {
        row.appendChild(cell);
      }
    }
    replayTableBodyHtml.appendChild(row);
  }
}

function createTableCell(
  columnName: string, value: string | Link
): HTMLTableCellElement | null {
  const cell = document.createElement('td');
  if (!displayedColumns.includes(columnName)) {
    return null;
  }
  // @ts-ignore
  if (columnName === "game" && !showGameColumn) {
    return null;
  }
  // @ts-ignore
  if (columnName === "route" && !showRouteColumn) {
    return null;
  }

  if (typeof value === "object") {
    cell.appendChild(createLinkHtml(value));
  } else {
    const text = document.createTextNode(value);
    cell.appendChild(text);
  }
  if (columnName === "shot" || columnName === "route" || columnName === "score") {
    cell.className = "nowrap";
  } else if (columnName === "comment") {
    cell.className = "comment-cell"
  }
  return cell;
}

function createLinkHtml(link: Link): HTMLAnchorElement {
  const linkHtml = document.createElement('a'); // 'a' as in the <a> HTML tag
  linkHtml.href = link.url;
  const linkTextHtml = document.createTextNode(link.text);
  linkHtml.appendChild(linkTextHtml)
  return linkHtml;
}

function clearTableHtml(): void {
  replayTableBodyHtml.innerHTML = '';
  tableResetCounter++;
}

try {
  // @ts-ignore
  module.exports = {updateFilters, filterReplays};
} catch(error) {
  // Shut up error in console but do nothing
}

function ensureTickboxSync(): void {
  activeFilters = initializeFilters();
  for(const elm of document.querySelectorAll(".checkbox-list input[type=checkbox]:checked")) {
    onClick(elm);
  }
}

window.addEventListener("pageshow", event => {
  ensureTickboxSync();
});
