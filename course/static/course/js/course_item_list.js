"use strict"; // defer

// relies on PopupMenu, ModalDialog, ServerStatus
[PopupMenu, ModalDialog, ServerStatus, ServerData, ServerPost, Draggable].forEach(function(e) {
  if(e === undefined) throw Error('Dependencies not met.')
});

var CourseItemList = (function(){
  let self = {};

  // ------------------- Private stuff -----------------------

  // For dragging items
  Draggable.registerDropCallback('course-item', handleCourseItemDrop);
  Draggable.registerDropCallback('course-item-heading', handleCourseItemHeadingDrop);

  async function postData(action, data) {
    // console.log('Posting data:');
    // console.log(data);

    let ss = ServerStatus;
    ss.incrementTasks();

    let response = await ServerPost.postData(action, data);

    if(!response.ok) {
      ss.error('Server returned a bad response!');
    }

    ss.decrementTasks();
    return response;
  }

  async function addHeading(name) {
    let action = ServerData.course_item_heading_create_inline_url

    let response = await postData(action, {'name': name});
    if(!response.ok) return;

    let text = await response.text();
    let ul = document.querySelector('.item-list');
    if(!ul) {
      console.error("Couldn't update item list because no #item_list found.");
      ss.decrementTasks();
      return;
    }

    ul.innerHTML = text;
    Draggable.updateHotSpots();
  }

  async function updateOrder() {
    let items = document.querySelectorAll('.item-list li');
    let order = 1;
    let data = [];
    for(let item of items) {
      let itemData = {};
      if(item.classList.contains('course-item-heading'))
        itemData.is_heading = 'on';
      itemData.id = item.dataset.itemId;
      itemData.order = order;

      data.push(itemData);
      order++;

    }
    let action = ServerData.course_item_order_update_inline_url
    let response = await postData(action, data);
    if(!response.ok) {
      ServerStatus.error("Couldn't update item order :(");
      return;
    }

    // if response.ok, then silence

  }

  function handleCourseItemDrop(draggedElement, dropDetails) {
    // dropDetails is an object with .elem, .dx, .dy, and .dist
    // if drag-type is 'abovebelow', then dropDetails.abovebelow will be either 'above' or 'below'
    //   'above' indicating that draggedElement was dropped above the target element.

    if(dropDetails.abovebelow === 'above') {
      dropDetails.elem.before(draggedElement);
    }else{
      dropDetails.elem.after(draggedElement);
    }

    let headingElem = getHeadingOfItem(draggedElement);
    updateOrder();

    if(headingElem == null) return;

    let headingVisible = !headingElem.classList.contains('not-visible');
    let itemVisible = !draggedElement.classList.contains('not-visible');

    if(headingVisible != itemVisible) {
      if(itemVisible) {
        // if item is visible, make heading visible too
        updateCourseItemHeadingVisible(headingElem, true, true);
      }
    }
  }

  function handleCourseItemHeadingDrop(draggedElement, dropDetails) {
    let headingItems = getItemsUnderHeading(draggedElement);

    if(dropDetails.abovebelow === 'above') {
      dropDetails.elem.before(draggedElement);
    }else{
      getLastElementUnderHeading(dropDetails.elem).after(draggedElement);
    }

    let insertHere = draggedElement;
    for(let item of headingItems) {
      insertHere.after(item);
      insertHere = item;
    }

    updateOrder();
  }

  function isVisible(elem) {
    return elem.dataset.itemVisibility === 'visible';
  }

  function getHeadingOfItem(itemElem) {
    let e = itemElem;
    while(e != null && !e.classList.contains('course-item-heading')) {
      e = e.previousElementSibling;
    }

    return e; // will either be null/undef or a heading
  }

  function getItemsUnderHeading(headingElement) {
    if(!headingElement.classList.contains('course-item-heading')) {
      console.error(`${headingElement} is not a heading.`);
      return;
    }
    let next = headingElement.nextElementSibling;
    let items = [];
    while(next != null && next.classList.contains('course-item')) {
      items.push(next);
      next = next.nextElementSibling;
    }

    return items;
  }

  function getLastElementUnderHeading(headingElement) {
    // returns the last "child" of heading or the heading if there are no children
    let e = headingElement;
    while(e.nextElementSibling != null && e.nextElementSibling.classList.contains('course-item')) {
      e = e.nextElementSibling;
    }
    return e;
  }

  async function deleteCourseItem(elem) {
    let action = ServerData.course_item_delete_inline_url;
    elem.classList.add('pending-delete');

    let response = await postData(action, {id: elem.dataset.itemId});
    if(!response.ok) {
      elem.classList.remove('pending-delete');
      return;
    }

    elem.remove();
    Draggable.updateHotSpots();
  }

  async function deleteManyCourseItems(itemArray) {
    let action = ServerData.course_item_delete_set_inline_url;
    for(let e of itemArray){
      e.classList.add('pending-delete');
    }

    let response = await postData(action, itemArray.map(function(elem){return {'id': elem.dataset.itemId}}));
    if(!response.ok) {
      for(let elem of itemArray) {
        elem.classList.remove('pending-delete');
      }

      return;
    }

    for(let elem of itemArray) {
      elem.remove();
    }
    Draggable.updateHotSpots();
  }

  async function deleteCourseItemHeading(elem) {
    let action = ServerData.course_item_heading_delete_inline_url;

    elem.classList.add('pending-delete');

    let response = await postData(action, {id: elem.dataset.itemId});
    if(!response.ok) {
      elem.classList.remove('pending-delete');
      return;
    }

    elem.remove();
    Draggable.updateHotSpots();
  }

  async function updateCourseItemVisible(elem, visible) {
    if(isVisible(elem) === visible) return;

    let action = ServerData.course_item_visible_update_inline_url;

    let data = {id: elem.dataset.itemId};
    if(visible) data['visible'] = 'on';

    let response = await postData(action, data);
    if(!response.ok) return;
    let newHTML = await response.text();
    let template = document.createElement('template');
    template.innerHTML = newHTML.trim();
    elem.replaceWith(template.content.firstChild);
    Draggable.updateHotSpots();
  }

  async function updateCourseItemHeadingVisible(headingElem, visible) {
    if(isVisible(headingElem) === visible) return;
    let headingAction = ServerData.course_item_heading_visible_update_inline_url
    let headingData = {id: headingElem.dataset.itemId};
    if(visible) headingData['visible'] = 'on';

    let response = await postData(headingAction, headingData);
    if(!response.ok) return;
    let newHTML = await response.text();
    let template = document.createElement('template');
    template.innerHTML = newHTML.trim();
    headingElem.replaceWith(template.content.firstChild);
    Draggable.updateHotSpots();
  }

  // ---------------------- public functions ----------------
  self.Menus = {};
  self.Menus.getCourseItemMenu = function(elem) {
    let menu = [];
    if(isVisible(elem)) {
      menu.push(['Hide', function() {
        updateCourseItemVisible(elem, false);
      }]);
    }else{
      menu.push(['Show', function() {
        updateCourseItemVisible(elem, true);
        updateCourseItemHeadingVisible(getHeadingOfItem(elem), true);
      }]);
    }
    menu.push(['-']);
    menu.push(['Delete', () =>ModalDialog.confirmDialog(
      'Confirm Delete',
      'Are you sure you want to delete this course item?',
      () => deleteCourseItem(elem)
    )]);
    return menu;
  };

  self.Menus.getCourseItemHeadingMenu = function(elem) {
    let menu = [];
    if(isVisible(elem)) {
      menu.push(['Hide', function() {
        updateCourseItemHeadingVisible(elem, false);
        let items = getItemsUnderHeading(elem);
        for(let item of items) {
          updateCourseItemVisible(item, false);
        }
      }]);
    }else {
      menu.push(['Show', function() {
        updateCourseItemHeadingVisible(elem, true);
        let items = getItemsUnderHeading(elem);
        for(let item of items) {
          updateCourseItemVisible(item, true);
        }
      }]);
    }
    menu.push(['-']);
    menu.push(['Delete', () => {
      let items = getItemsUnderHeading(elem);
      ModalDialog.confirmDialog(
        'Confirm Delete',
        `You are about to permanently delete a course heading as well as ${items.length} item(s) under it. Are you sure about this?`,
        () => {
          deleteManyCourseItems(items);
          deleteCourseItemHeading(elem);
        })
      }]);
    return menu;
  }


  self.addHeadingStart = function() {
    ModalDialog.inputDialog(
      'Add a Heading',
      'Please specify a name for the new heading.',
      function(result) {
        if(result === false)
          return;

        if(result === '') {
          setTimeout(() => ModalDialog.confirmDialog(
            ':(', 'Headings need to include a non-whitespace character.'
          ), 0)
        }
        addHeading(result);
        // setTimeout(() => addHeading(result), 0);
      }
    );
  }

  return self
})();
