const { JSDOM } = require('jsdom');
setupTestDom();
const updateFilters = require('./replayTable.js');

describe('updateFilters', () => {
    test('Adds filters', () => {
        let filters = {};
        filters = updateFilters(filters, "Difficulty", "Hard");
        expect(filters).toEqual({"Difficulty": ["Hard"]});
        filters = updateFilters(filters, "Shot", "Sakuya B");
        expect(filters).toEqual({"Difficulty": ["Hard"], "Shot": ["Sakuya B"]});
        filters = updateFilters(filters, "Shot", "Reimu A");
        expect(filters).toEqual({"Difficulty": ["Hard"], "Shot": ["Sakuya B", "Reimu A"]});
    });
    
    test('Removes filters', () => {
        let filters = {"Difficulty": ["Hard", "Extra"], "Shot": ["Sakuya B", "Reimu A"]};
        filters = updateFilters(filters, "Shot", "Sakuya B");
        expect(filters).toEqual({"Difficulty": ["Hard", "Extra"], "Shot": ["Reimu A"]});
        filters = updateFilters(filters, "Difficulty", "Extra");
        expect(filters).toEqual({"Difficulty": ["Hard"], "Shot": ["Reimu A"]});
    });
    
    test('Deletes filter type if empty', () => {
        let filters = {"Difficulty": ["Hard"], "Shot": ["Sakuya B", "Reimu A"]};
        filters = updateFilters(filters, "Difficulty", "Hard");
        expect(filters).toEqual({"Shot": ["Sakuya B", "Reimu A"]});
        filters = updateFilters(filters, "Shot", "Sakuya B");
        filters = updateFilters(filters, "Shot", "Reimu A");
        expect(filters).toEqual({});
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