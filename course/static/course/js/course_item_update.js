"use strict"; // defer execution

// Custom behavior for CourseItem type select element
// Hides item_content or url_content boxes depending on what is selected

[ServerData, ServerPost].forEach(function(e) {
  if(e === undefined) throw Error('Dependencies not met.')
});

var CourseItemUpdate = (function(){
  let self = {};

  self.updateSelect = function() {
    let sel_elem = document.getElementById('id_content_type');
    let url_div = document.getElementById('id_url_content_div');
    let text_div = document.getElementById('id_text_content_div');
    let url_input = document.getElementById('id_url_content');
    let text_input = document.getElementById('id_text_content');
    let preview_button = document.getElementById('id_preview_button');
    let preview_area = document.getElementById('id_preview_area');
    let preview_container = document.getElementById('id_preview_container');

    let val = sel_elem.value;
    if(val === 'U') { // the code BCM uses for 'url'
      url_div.style.display = 'block';
      text_div.style.display = 'none';
      text_input.disabled = true;
      url_input.disabled = false;
    }else {
      url_div.style.display = 'none';
      text_div.style.display = 'block';
      text_input.disabled = false;
      url_input.disabled = true;
    }

    if(val === 'M') {
      for(let e of document.querySelectorAll('.markdown-only')) {
        e.style.display = '';
      }
      preview_button.disabled = false;
      preview_container.classList.add('empty');
      preview_container.innerHTML = `
        <p>Click the 'Preview' button to see your markdown-rendered content.</p>
      `;
    }else {
      for(let e of document.querySelectorAll('.markdown-only')) {
        e.style.display = 'none';
      }
      preview_button.disabled = true;
    }
  }

  self.getRenderedMarkdown = async function() {
    let text = document.getElementById('id_text_content').value;
    let preview_container = document.getElementById('id_preview_container');
    let action = ServerData.markdown_preview_url;
    let response = await ServerPost.postData(action, {text: text});
    if(!response.ok) {
      console.error('Bad Response');
      return;
    }
    let html = await response.text();
    preview_container.innerHTML = html;
    preview_container.classList.remove('empty');
  }

  self.updateSelect();

  return self;
})();
