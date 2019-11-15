"use strict";

// .drag-hotspot items allow the user to drag
// a .drag-hotspot's nearest .draggable parent will get dragged
// while dragging, nearest .drag-target element will be indicated Neither

var Draggable = (function(){
  let self = {};

  let mouseOriginX = null; // mouse start coordinates
  let mouseOriginY = null;
  let mouseX = null;       // current mouse coordinates
  let mouseY = null;
  let dragging = null;    // element being dragged
  let draggingDx = null;  // offset to center of element from mouse
  let draggingDy = null;

  let intervalId = null;
  let dragType = 'default'; // or 'line-insertion'
  let dragTargets = [];
  let dragClosest = null;

  function getDraggableParent(elem) {
    let origElem = elem;
    while(elem !== document){
      if(elem.classList.contains('draggable')) {
        return elem;
      }
      elem = elem.parentNode;
    }

    return null;
  }

  function clearDragClasses(elem) {
    elem.classList.remove('drag-is-target-below');
    elem.classList.remove('drag-is-target-above');
  }

  function updateTargets() {
    dragTargets = [];
    let targetElements = document.querySelectorAll(`.drag-target.${dragging.dataset.dragTargetClass}`);

    for(let e of targetElements) {
      if(e === dragging) continue;
      let box = e.getBoundingClientRect();
      let x = box.x + window.scrollX + box.width/2;
      let y = box.y + window.scrollY + box.height/2;
      dragTargets.push({'elem': e, 'x': x, 'y': y});
    }
  }

// Returns {'dist': distance, 'dx': x, 'dy': y} dx/dy are components of vector to closest target}
  function getClosestTarget(x, y) {
    let best = null;

    for(let obj of dragTargets) {
      let dx = obj.x - x;
      let dy = obj.y - y;
      let dist = Math.sqrt(dx*dx + dy*dy);

      if(best === null || best.dist > dist) {
        best = {
          'elem': obj.elem, 'dist': dist, 'dx': dx, 'dy': dy
        }
      }
    }

    return best;
  }

  function startDrag(event) {
    dragging = event.target;

    dragging = getDraggableParent(dragging);
    if(dragging === null) return;
    // dragging should point to a .draggable element

    mouseOriginX = mouseX = event.pageX;
    mouseOriginY = mouseY = event.pageY;

    let box = dragging.getBoundingClientRect();
    draggingDx = (box.x + window.scrollX + box.width/2) - mouseX;
    draggingDy = (box.y + window.scrollY + box.height/2) - mouseY;

    updateTargets();

    document.addEventListener('mousemove', updateMouse);
    document.addEventListener('mouseup', endDrag, {once: true});
    intervalId = setInterval(updateDrag, 16); // a cool 60 fps

  }

  function endDrag() {
    updateDrag();
    clearDragClasses(dragClosest.elem);

    dragging.style.top = '0';
    dragging.style.left = '0';
    dragging = null;

    document.removeEventListener('mousemove', updateMouse);
    clearInterval(intervalId);
  }

  function updateMouse(event) {
    mouseX = event.pageX;
    mouseY = event.pageY;
  }

  function updateDrag() {
    let top = mouseY - mouseOriginY;
    let left = mouseX - mouseOriginX;
    dragging.style.top = `${top}px`;
    dragging.style.left = `${left}px`;

    let dragX = mouseX + draggingDx;
    let dragY = mouseY + draggingDy
    let closest = getClosestTarget(dragX, dragY);

    if(closest === null)
      return;


    if(dragClosest !== null) {
      clearDragClasses(dragClosest.elem);
    }

    if(closest.dy > 0) { // then it's below us
      closest.elem.classList.add('drag-is-target-below');
    }else {
      closest.elem.classList.add('drag-is-target-above');
    }

    dragClosest = closest;
  }


  let hotSpots = document.querySelectorAll('.drag-hotspot');
  for(let hs of hotSpots) {
    let draggable = getDraggableParent(hs)
    if(draggable === null) {
      console.error(`${hs} is .drag-hotspot with no .draggable parent`);
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
