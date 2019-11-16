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
  let dragType = 'default'; // or 'abovebelow'
  let dragTargets = [];
  let dragClosest = null;

  let registeredCallbacks = {}; // className -> callback mapping
  let dropCallback = null;

  self.registerDropCallback = function(className, callback) {
    if(registeredCallbacks[className] !== undefined) {
      console.error(`${className} already has a callback.`);
      return;
    }

    if(typeof(callback) !== 'function') {
      console.error(`Callback for ${className} is not a function.`);
      return;
    }

    registeredCallbacks[className] = callback;
  }

  function getDropCallback(elem) {
    for(let c in registeredCallbacks) {
      if(elem.classList.contains(c))
        return registeredCallbacks[c];
    }

    return null;
  }

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
    elem.classList.remove('is-drag-target');
    elem.classList.remove('is-drag-target-below');
    elem.classList.remove('is-drag-target-above');
  }

  function updateTargets() {
    dragTargets = [];
    let targetElements = document.querySelectorAll(dragging.dataset.dragTargetSelector);

    for(let e of targetElements) {
      if(e === dragging) continue;
      if(!e.classList.contains('drag-target')) {
        console.log('Element was targeted for dragging but is not a .drag-target');
        console.log({dragElement: dragging, targetElement: e});
        continue;
      }

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

    let type = dragging.dataset.dragType;
    if(type === undefined) {
      console.error('No data-drag-type attribute set.');
      dragging = null;
      return;
    }

    if(type !== 'default' && type !== 'abovebelow') {
      console.error(`Unrecognized data-drag-type attribute: ${type}`);
      dragging = null
      return;
    }

    if(type === 'default') {
      console.error("'default' drag type not yet implemented.");
      dragging = null;
      return;
    }

    dragType = type;

    dropCallback = getDropCallback(dragging);
    if(dropCallback === null) {
      console.error('There is no drop callback for dragged element.');
      dragging = null;
      return;
    }



    mouseOriginX = mouseX = event.pageX;
    mouseOriginY = mouseY = event.pageY;

    let box = dragging.getBoundingClientRect();
    draggingDx = (box.x + window.scrollX + box.width/2) - mouseX;
    draggingDy = (box.y + window.scrollY + box.height/2) - mouseY;

    updateTargets();

    document.addEventListener('mousemove', updateMouse);
    document.addEventListener('mouseup', endDrag, {once: true});
    intervalId = setInterval(updateDrag, 16); // a cool 60 fps

    // console.log({
    //   dragging: dragging,
    //   dragType: dragType,
    // })
  }

  function updateDrag() {
    let top = mouseY - mouseOriginY;
    let left = mouseX - mouseOriginX;
    dragging.style.top = `${top}px`;
    dragging.style.left = `${left}px`;

    let dragX = mouseX + draggingDx;
    let dragY = mouseY + draggingDy
    let closest = getClosestTarget(dragX, dragY);

    // console.log({closest: closest, dragType: dragType});

    if(closest === null)
      return;

    if(dragClosest !== null) {
      clearDragClasses(dragClosest.elem);
    }

    if(dragType === 'default') {
      // Not yet implemented

    }else{ // then it's abovebelow
      if(closest.dy > 0) { // then it's below us
        closest.elem.classList.add('is-drag-target-below');
        closest.abovebelow = 'above'; // dragged is ABOVE target
      }else {
        closest.elem.classList.add('is-drag-target-above');
        closest.abovebelow = 'below'; // dragged is BELOW target
      }
    }



    dragClosest = closest;
  }

  function endDrag() {
    updateDrag();
    clearDragClasses(dragClosest.elem);
    dragging.style.top = '0';
    dragging.style.left = '0';
    document.removeEventListener('mousemove', updateMouse);
    clearInterval(intervalId);

    if(dragClosest !== null) {
      dropCallback(dragging, dragClosest);
    }

    dragging = null;
  }

  function updateMouse(event) {
    mouseX = event.pageX;
    mouseY = event.pageY;
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
