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
    let next = draggedElement.nextElementSibling;

    if(dropDetails.abovebelow === 'above') {
      dropDetails.elem.before(draggedElement);
    }else{
      dropDetails.elem.after(draggedElement);
    }


    while(next != null && next.classList.contains('course-item')) {
        let moveThis = next;
        next = next.nextElementSibling;

        draggedElement.after(moveThis);
        draggedElement = draggedElement.nextElementSibling;
    }

    updateOrder();
  }

  // ---------------------- public functions ----------------

  self.addHeadingStart = function() {
    ModalDialog.inputDialog(
      'Add a Heading',
      'Please specify a name for the new heading.',
      function(result) {
        if(result === false)
          return;

        if(result === '') {
          setTimeout(() => ModalDialog.verifyDialog(
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

// Pre-defined popup menus
CourseItemList.ListElement = (function(){
  let menu = [
    ['Fetch', function(elem){
      // BCM.API.get_item_list(SERVER_DATA.courseId);
    }],
    ['Edit', function(elem){
      window.location.href = elem.dataset.editUrl
    }],
    ['Toggle Visibility', function(){console.log('Clicked Toggle!')}],
    '-',
    ['Delete', function(){console.log('Clicked Delete :o')}]
  ]

  let self = {
    'menu': menu
  };

  return self;
})();
