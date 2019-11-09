"use strict"; // defer execution

// Custom behavior for CourseItem type select element
// Hides item_content or url_content boxes depending on what is selected

BCM.CourseItemTypeSelect = (function(){
  // Assumes there is only one select element on the page to worry about
  let sel_elem = document.querySelector('select[name=content_type]');
  let url_div = document.querySelector('div._url_content');
  let text_div = document.querySelector('div._text_content');
  if(sel_elem === null) {
    console.log('No content_type select element found!');
  }

  if(url_div === null) {
    console.log('No url container found!');
  }

  if(text_div === null) {
    console.log('No text container found!');
  }

  let update = function() {
    let val = sel_elem.value;
    if(val == 'U') { // the code BCM uses for 'url'
      url_div.style.display = 'block';
      text_div.style.display = 'none';
    }else {
      url_div.style.display = 'none';
      text_div.style.display = 'block';
    }
  }

  sel_elem.addEventListener('change', update);
  update();
})();
