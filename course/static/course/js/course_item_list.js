"use strict"; // defer

// relies on PopupMenu, ModalDialog, ServerStatus
[PopupMenu, ModalDialog, ServerStatus, ServerData, ServerPost].forEach(function(e) {
  if(e === undefined) throw Error('Dependencies not met.')
});

var CourseItemList = (function(){
  let self = {};

  async function addHeading(name) {
    let ss = ServerStatus;
    ss.incrementTasks();

    let action = ServerData.heading_create_inline_url

    let response = await ServerPost.postData(action, {'name': name});
    if(!response.ok) {
      ss.error('Server returned a bad response!');
      return;
    }

    let text = await response.text();
    let ul = document.querySelector('.item-list');
    if(!ul) {
      console.error("Couldn't update item list because no #item_list found.");
      ss.decrementTasks();
      return;
    }

    ul.innerHTML = text;

    ss.decrementTasks();
  }

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
