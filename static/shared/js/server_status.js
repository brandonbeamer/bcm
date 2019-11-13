"use strict";

// Hooks into .server-status element and reports on ongoing communications

var ServerStatus = (function(){
  let self = {};
  let status_elem = document.querySelector('.server-status');
  let task_count = 0;
  let error_flag = false;

  function set_class(className) {
    for(let cls of ['server-status-good', 'server-status-bad', 'server-status-wait'])
      status_elem.classList.remove(cls);
      status_elem.classList.add(className);
  }

  function set_status(message, className) {
    if(className)
      set_class(className);

    status_elem.innerText = message;
  }

  self.updateStatus = function() {
    if(task_count == 0) {
      if(error_flag) {
        set_status('There were problems; try reloading?', 'server-status-bad');
      }else {
        set_status('All changes saved!', 'server-status-good');
        setTimeout(() => set_status(''), 1500);
      }
    }else {
      set_status(`Saving ${task_count > 1 ? task_count + ' ': ''}changes... `,
        'server-status-wait');
    }
  }

  self.incrementTasks = function() {
    task_count++;
    self.updateStatus();
  }

  self.decrementTasks = function() {
    task_count--;
    self.updateStatus();
  }

  self.error = function() {
    error_elem = document.createElement('div');
    error_elem.classList.add('server-status-bad');
    status_elem.after(error_elem);
    error_flag = true;
    setTimeout(() => error_elem.remove(), 5000);
  }

  return self;
})();
