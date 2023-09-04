"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
const replayTableBatchSize = 50;
const replayTableBodyHtml = document.getElementById('replay-table-body');
const displayedColumns = [
    "user", "game", "difficulty", "shot", "route", "score", "uploadDate", "comment", "replay"
];
var activeFilters = initializeFilters();
var allReplays = [];
var tableResetCounter = 0;
requestAndInitializeReplays();
initializeFilters();
function requestAndInitializeReplays() {
    return __awaiter(this, void 0, void 0, function* () {
        const requestUri = window.location.pathname === '/'
            ? window.location.origin + '/replays/index/json'
            : window.location.origin + window.location.pathname + "/json";
        try {
            const response = yield fetch(requestUri);
            if (!response.ok) {
                replayTableBodyHtml.innerHTML =
                    '<p style="color: red;">Failed to load replays</p>';
                return;
            }
            const reader = response.body.getReader();
            const decoder = new TextDecoder('utf-8');
            let buffer = '';
            while (true) {
                const { done, value } = yield reader.read();
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
        }
        catch (error) { }
    });
}
function initializeFilters() {
    activeFilters = {};
    const allButtons = document.querySelectorAll('button[filtertype]');
    for (const button of allButtons) {
        // @ts-ignore
        const filterType = button.getAttribute('filtertype');
        activeFilters[filterType] = 'All';
    }
    return activeFilters;
}
function onClick(elm) {
    // @ts-ignore
    const filterType = elm.getAttribute('filterType');
    const value = elm.getAttribute('value');
    activeFilters = updateFilters(activeFilters, filterType, value);
    updateButtons(activeFilters);
    const filteredReplays = filterReplays(activeFilters, allReplays);
    clearTableHtml();
    addReplaysToTable(filteredReplays);
}
function updateButtons(activeFilters) {
    const allButtons = document.querySelectorAll('button[filtertype]');
    for (const button of allButtons) {
        // @ts-ignore
        const filterType = button.getAttribute('filtertype');
        // @ts-ignore
        const value = button["value"];
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
                // @ts-ignore
                return replay[filterType] === allowedValues;
            });
        }
    }
    return filteredReplays;
}
function addReplaysToTable(replays) {
    let startIndex = 0;
    let endIndex = Math.min(replayTableBatchSize, replays.length);
    while (startIndex < replays.length) {
        constructAndRenderTableBatch(replays, startIndex, endIndex);
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
        populateTable(replays, startIndex, endIndex);
    }, 1);
}
function populateTable(replays, startIndex, endIndex) {
    for (let i = startIndex; i < endIndex; i++) {
        const replay = replays[i];
        const row = document.createElement('tr');
        for (const [columnName, value] of Object.entries(replay)) {
            const cell = createTableCell(columnName, value);
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
    }
    else {
        const text = document.createTextNode(value);
        cell.appendChild(text);
    }
    if (columnName === "shot" || columnName === "route" || columnName === "score") {
        cell.className = "nowrap";
    }
    else if (columnName === "comment") {
        cell.className = "comment-cell";
    }
    return cell;
}
function createLinkHtml(link) {
    const linkHtml = document.createElement('a'); // 'a' as in the <a> HTML tag
    linkHtml.href = link.url;
    const linkTextHtml = document.createTextNode(link.text);
    linkHtml.appendChild(linkTextHtml);
    return linkHtml;
}
function clearTableHtml() {
    replayTableBodyHtml.innerHTML = '';
    tableResetCounter++;
}
try {
    // @ts-ignore
    module.exports = { updateFilters, filterReplays };
}
catch (error) {
    // Shut up error in console but do nothing
}
function ensureTickboxSync() {
    activeFilters = initializeFilters();
    for (const elm of document.querySelectorAll(".checkbox-list input[type=checkbox]:checked")) {
        onClick(elm);
    }
}
window.addEventListener("pageshow", event => {
    ensureTickboxSync();
});
