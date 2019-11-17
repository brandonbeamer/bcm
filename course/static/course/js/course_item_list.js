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
    console.log('Posting data:');
    console.log(data);

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
    let action = ServerData.heading_create_inline_url

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
        itemData.is_heading = 'checked';
      itemData.id = item.dataset.itemId;
      itemData.order = order;

      data.push(itemData);
      order++;
    }

    let action = ServerData.item_update_order_inline_url
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

    updateOrder();
  }

  function handleCourseItemHeadingDrop(draggedElement, dropDetails) {
    let headingItems = getHeadingItems(draggedElement);

    if(dropDetails.abovebelow === 'above') {
      dropDetails.elem.before(draggedElement);
    }else{
      dropDetails.elem.after(draggedElement);
    }

    let insertHere = draggedElement;
    for(let item of headingItems) {
      insertHere.after(item);
      insertHere = item;
    }

    updateOrder();
  }

  function getHeadingItems(headingElement) {
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

  async function deleteCourseItem(itemId) {
    let action = ServerData.item_delete_inline_url;

    let elem = document.querySelector(`li.course-item[data-item-id='${itemId}']`);
    elem.classList.add('pending-delete');

    let response = await postData(action, {id: itemId});
    if(!response.ok) {
      elem.classList.remove('pending-delete');
      return;
    }

    elem.remove();
    Draggable.updateHotSpots();
  }

  async function deleteItemHeading(itemId) {
    let action = ServerData.heading_delete_inline_url;

    let elem = document.querySelector(`li.course-item-heading[data-item-id='${itemId}']`);
    elem.classList.add('pending-delete');

    let response = await postData(action, {id: itemId});
    if(!response.ok) {
      elem.classList.remove('pending-delete');
      return;
    }

    elem.remove();
    Draggable.updateHotSpots();
  }

  // ---------------------- public functions ----------------
  self.Menus = {};
  self.Menus.CourseItemMenu = [
      ['Delete', function(popupElem) {
        let item = document.querySelector(`li.course-item[data-item-id='${popupElem.dataset.itemId}']`);
        if(item == null) {
          console.error("Can't find item!")
          return;
        }
        ModalDialog.confirmDialog(
          'Confirm Delete',
          'Are you sure you want to delete this course item?',
          function(result) {
            if(!result) return;

            deleteCourseItem(popupElem.dataset.itemId);
          }
        );

      }]
  ];

  self.Menus.ItemHeadingMenu = [
      ['Delete', function(popupElem) {
        let heading = document.querySelector(`li.course-item-heading[data-item-id='${popupElem.dataset.itemId}']`);
        if(heading == null) {
          console.error("Can't find heading!")
          return;
        }
        let items = getHeadingItems(heading);
        ModalDialog.confirmDialog(
          'Confirm Delete',
          `You are about to permanently delete a course heading as well as ${items.length} item(s) under it. Are you sure about this?`,
          function(result) {
            if(!result) return;

            for(let item of items) {
              deleteCourseItem(item.dataset.itemId);
            }
            deleteItemHeading(heading.dataset.itemId);
          }
        );
      }]
  ];

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
