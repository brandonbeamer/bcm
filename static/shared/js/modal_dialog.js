"use strict";
// requires "BCM" namespace to be defined
// requires "modal_dialog.css"
// Adds model dialog functionality to pages

BCM.ModalDialog = (function(){
  let self = {};

  let build_dialog = function(options){
    let container = document.createElement('div');
    container.classList.add('modal-dialog-container');

    let title_elem = document.createElement('h1');
    title_elem.textContent = title;

    let msg_elem = document.createElement('p');
    msg_elem.textContent = message;

    let

    container.append(`
      <div class="modal-dialog-box">
        <h1>TITLE</h1>
        <p>MESSAGE</p>
        <div style="text-align: right">
          <button class="accent">OK</button>
          <button>Cancel</button>
        </div>
      </div>
    `);

  }

  // verifyDialog is a simple OK/Cancel dialog with a title and a message
  self.verifyDialog = async function(title, message) {
  }

  return self;
})();
