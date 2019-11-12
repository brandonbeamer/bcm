"use strict"; // defer

// relies on BCM and BCM.PopupMenu namespaces
BCM.CourseItemList = (function(){
  let self = {};

  self.addHeading = function() {
    let
  }

  return self
})();

// Pre-defined popup menus
BCM.CourseItemList.ListElement = (function(){
  let menu = [
    ['Fetch', function(elem){
      BCM.API.get_item_list(BCM.globals.courseId);
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
