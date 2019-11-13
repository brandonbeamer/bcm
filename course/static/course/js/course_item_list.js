"use strict"; // defer

// relies on PopupMenu, ModalDialog, ServerStatus
[PopupMenu, ModalDialog, ServerStatus].forEach(function(e) {
  if(e === undefined) throw Error('Dependencies not met.')
});

var CourseItemList = (function(){
  let self = {};

  async function addHeading(name) {
    let ss = BCM.ServerStatus;
    ss.incrementTasks();
    let response = await fetch('/');
    if(!response.ok) {
      ss.error('Server returned a bad response!');
      ss.decrementTasks();
      return;
    }

    let text = await response.text();
    console.log(`RESPONSE: ${text}`);

    ss.decrementTasks();
  }

  self.addHeadingStart = function() {
    BCM.ModalDialog.inputDialog(
      'Add a Heading',
      'Please specify a name for the new heading.',
      function(result) {
        if(result === false)
          return;

        if(result === '') {
          setTimeout(() => BCM.ModalDialog.verifyDialog(
            ':(', 'Headings need to include a non-whitespace character.'
          ), 0)
        }

        setTimeout(() => addHeading(result), 0);
      }
    );
  }

  return self
})();

// Pre-defined popup menus
CourseItemList.ListElement = (function(){
  let menu = [
    ['Fetch', function(elem){
      BCM.API.get_item_list(SERVER_DATA.courseId);
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
