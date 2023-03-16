const { JSDOM } = require('jsdom');
setupTestDom();
const updateFilterList = require('./replayTable.js');

describe('updateFilterList', () => {
    test('Adds filters', () => {
        activeFilters = updateFilterList([], "Difficulty", "Hard");
        expect(activeFilters).toBe({"Difficulty": ["Hard"]});
    });
  });

function setupTestDom() {
    const dom = new JSDOM(`
    <!DOCTYPE html>
    <html>
      <body>
      <table id="replay-table" class="replay-table">
          <thead>
          </thead>
          <tbody>
          </tbody>
      </table>
      </body>
    </html>
  `);
  
  global.window = dom.window;
  global.document = dom.window.document;
}