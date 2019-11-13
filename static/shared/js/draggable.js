"use strict";

// requires BCM
// .drag-hotspot items allow the user to drag
// a .drag-hotspot's nearest .draggable parent will get dragged
// while dragging, nearest .drag-target element will be indicated Neither

BCM.Draggable = (function(){
  let self = {};

  let mouseOriginX = null;
  let mouseOriginY = null;
  let mouseX = null;
  let mouseY = null;
  let dragging = null;
  let initialStyle = {};

  function getDraggableParent(elem) {
    while(!elem.classList.contains('draggable')) {
      if(elem === null) {
        // this really should never execute given how we set things up
        // however the DOM tree might change or something so ...
        console.error('No draggable element found!');
        break;
      }

      elem = elem.parentNode;
    }

    return elem;
  }

  function startDrag(event) {
    dragging = event.target;

    dragging = getDraggableParent(dragging);
    if(dragging === null) return;
    // dragging should point to a .draggable element

    mouseOriginX = mouseX = event.pageX;
    mouseOriginY = mouseY = event.pageY;
    document.addEventListener('mousemove', updateMouse);
    document.addEventListener('mouseup', () => endDrag(hs), {once: true});
    setInterval(updateDrag, 16); // a cool 60 fps
  }

  function endDrag(elem) {
    dragging = null;
    document.removeEventListener('mousemove', updateMouse);
    clearInterval(updateDrag);
  }

  function updateMouse(event) {
    console.log(`${event.pageX}, ${event.pageY}`);
    mouseX = event.pageX;
    mouseY = event.pageY;
  }

  function updateDrag() {
    let top = mouseY - mouseOriginY;
    let left = mouseX - mouseOriginX;

    dragging.style.top = `${top}px`;
    dragging.style.left = `${left}px`;
  }


  let hotSpots = document.querySelectorAll('.drag-hotspot');
  for(let hs of hotSpots) {
    let draggable = getDraggableParent(hs)
    if(draggable === null) {
      console.error('${draggable} is drag-hotspot with no .draggable parent');
      continue;
    }

    hs.addEventListener('mousedown', function(event){
      event.preventDefault();
      startDrag(event);
    });

    draggable.style.position = 'relative'; // all draggables need to be relative
  }

  return self;
})();
