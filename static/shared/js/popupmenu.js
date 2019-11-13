"use strict"; // defer

// Popup Menu Implementation
// Popup elements call PopupMenu.doPopup(elem, menu) on click
// where 'elem' is a container element that can contain the popup and be
// have style 'position: relative'
// where 'menu' is an array of arrays like this:
// [
//   ['Item1', callback1], // callbacks are called w
//   ['Item2', callback2],
//   '---', // non-arrays are interpreted as separators
// ]

var PopupMenu = (function(){
  function create_menu(elem, data) {
    elem.style.position = 'relative';

    let ul = document.createElement('ul');

    for(let item of data) {
      let text = item[0];
      let callback = item[1];
      let li = null;
      if(text[0] == '-') {
        li = document.createElement('div');
        li.classList.add('popup-menu-divider');
      }else{
        li = document.createElement('li');
        li.innerHTML = text;
        li.onclick = callback;
      }
      ul.append(li);

    }

    ul.classList.add('popup-menu');
    elem.before(ul);
    document.addEventListener('click', function(){ul.remove()}, {'once': true});
  }

  // document.addEventListener('click', remove_menu);

  let self = {};

  self.do_popup = function(elem, data) {
    setTimeout(function(){create_menu(elem, data)}, 0);
  }

  return self;
})();

// BCM.PopupMenu.do_popup(['foo', 'bar', 'baz']);
