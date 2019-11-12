"use strict";
// defer
// Define the namespace
// Define globals in dataset of 'GLOBALS' element

var BCM = (function(){
  let self = {};

  self.globals = {}

  let elem = document.getElementById('BCM-GLOBALS');
  if(elem !== null) {
    for(let key in elem.dataset) {
      self.globals[key] = elem.dataset[key];
    }
  }

  return self;
})();
