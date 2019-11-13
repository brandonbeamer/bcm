"use strict";

// requires "modal_dialog.css"
// Adds model dialog functionality to pages

var ModalDialog = (function(){
  let self = {};

  function close_dialog(container_elem) {
    container_elem.remove();
  }
  // options: 'title':string, 'message':string, 'text_input':bool, 'result_callback':function
  function build_dialog(options){
    if(options.text_input && options.callback !== undefined) {
      console.error('Building an input dialog without a callback?');
    }

    let container_div = document.createElement('div');
    container_div.classList.add('modal-dialog-container');

    let box_div = document.createElement('div');
    box_div.classList.add('modal-dialog-box');
    container_div.append(box_div);

    let title_h1 = document.createElement('h1');
    title_h1.textContent = options.title || 'Message';
    box_div.append(title_h1)

    let msg_p = document.createElement('p');
    msg_p.textContent = options.message || '';
    box_div.append(msg_p);

    let text_input = null;
    if(options.text_input) {
      let input_div = document.createElement('div');
      let text_input = document.createElement('input');
      text_input.type = 'text';
      input_div.append(text_input);
      box_div.append(input_div);
    }

    let button_div = document.createElement('div');
    button_div.classList.add('modal-dialog-button-row');
    box_div.append(button_div);

    let ok_button = document.createElement('button');
    ok_button.classList.add('accent');
    ok_button.textContent = 'OK';
    ok_button.onclick = function() {
      if(options.result_callback) {
        if(text_input !== null) {
          options.result_callback(text_input.value.trim());
        }else {
          options.result_callback(true);
        }
      }

      close_dialog(container_div);
    }
    button_div.append(ok_button);

    let cancel_button = document.createElement('button');
    cancel_button.textContent= 'Cancel';
    cancel_button.onclick = function() {
      options.result_callback(false);
      close_dialog(container_div);
    }
    button_div.append(cancel_button);

    document.body.append(container_div);

  }

  // verifyDialog is a simple OK/Cancel dialog with a title and a message
  self.verifyDialog = function(title, message, callback) {
    build_dialog({
      'title': title,
      'message': message,
      'result_callback': callback
    })
  }

  self.inputDialog = function(title, message, callback) {
    build_dialog({
      'title': title,
      'message': message,
      'text_input': true,
      'result_callback': callback
    })
  }

  return self;
})();
