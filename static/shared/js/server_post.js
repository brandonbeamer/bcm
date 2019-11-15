"use strict";

// wrapper for inline post requests

[Cookies].forEach(function(e) {
  if(e === undefined) throw Error('Dependencies not met.')
});

var ServerPost = (function(){
  let self = {};

  self.postData = async function(action, object) {
    let formdata = new FormData();
    formdata.append('csrfmiddlewaretoken', Cookies.get('csrftoken'));
    for(let field in object) {
      if(Array.isArray(object[field])) {
        for(let val of object[field]) {
          formdata.append(field, val);
        }
      }else{
        formdata.append(field, object[field]);
      }
    }

    console.log(formdata);

    return await fetch(action, {
      method: 'POST',
      mode: 'same-origin',
      cache: 'no-cache',
      credentials: 'same-origin',
      // headers automatically set
      redirect: 'follow',
      referrer: 'client',
      body: formdata,
    });
  };

  return self;
})();
