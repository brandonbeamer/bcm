"use strict";

// Grabs JSON-encoded object from global SERVER_DATA_JSON variable and
// makes it accessibe through ServerData namespace

var ServerData = null;

if(SERVER_DATA_JSON !== undefined) {
  ServerData = JSON.parse(SERVER_DATA_JSON);
  // console.log(ServerData);
} else {
  console.error('Could not find SERVER_DATA_JSON variable.')
}
