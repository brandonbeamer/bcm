"use strict"; // defer

// relies on BCM and BCM.PopupMenu namespaces

// Pre-defined popup menus
BCM.CourseItemListElement = (function(){
  let menu = [
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
