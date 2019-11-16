"use strict";

// wrapper for inline post requests

[Cookies].forEach(function(e) {
  if(e === undefined) throw Error('Dependencies not met.')
});

var ServerPost = (function(){
  let self = {};

  self.postData = async function(action, object) {

    if(Array.isArray(object)) {
      // post a formset
      console.log('is array');
      return await postArray(action, object);
    }else{
      // post a single form
      return await postObject(action, object);
    }

  }

  async function postArray(action, objects) {
    // object is array
    // will be received by django as formset

    console.log('Posting array:');
    console.log(objects);

    let formdata = new FormData()
    formdata.set('form-TOTAL_FORMS', objects.length);
    formdata.set('form-INITIAL_FORMS', 0);
    formdata.set('form-MIN_NUM_FORMS', 0);
    formdata.set('form-MAX_NUM_FORMS', 1000)

    let formNum = 0;
    for(let object of objects) {
      for(let field in object) {
        if(Array.isArray(object[field])) {
          for(let val of object[field]) {
            formdata.append(`form-${formNum}-${field}`, val);
          }
        }else{
          formdata.set(`form-${formNum}-${field}`, object[field]);
        }
      }
      formNum++;
    }

    return await postFormData(action, formdata);
  }

  async function postObject(action, object) {
    console.log('Posting object:');
    console.log(object);


    let formdata = new FormData();
    formdata.append('csrfmiddlewaretoken', Cookies.get('csrftoken'));
    for(let field in object) {
      if(Array.isArray(object[field])) {
        for(let val of object[field]) {
          formdata.append(field, val);
        }
      }else{
        formdata.set(field, object[field]);
      }
    }

    return await postFormData(action, formdata);
  }

  async function postFormData(action, formdata) {
    console.log('Posting form:');
    console.log(formdata);

    formdata.append('csrfmiddlewaretoken', Cookies.get('csrftoken'));

    let response = await fetch(action, {
      method: 'POST',
      mode: 'same-origin',
      cache: 'no-cache',
      credentials: 'same-origin',
      // headers automatically set
      redirect: 'follow',
      referrer: 'client',
      body: formdata,
    });

    if(!response.ok) {
      console.error('Server returned bad response:');
      console.error(response);
    }

    return response;
  }

  return self;
})();
