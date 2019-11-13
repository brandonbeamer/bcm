"use strict";
// defer execution

// How to Use:
// Drawer drawers are just elements whose display:none-ness is toggled by a button
// somewhere else.

// Each drawer has a 'toggle' element and a 'drawer' element.
// * Assign the toggle element the class .drawer-toggle.
// * Assign the drawer element the class .drawer-drawer.
// * Link toggles to their drawers by setting there data-drawer-id attribute to the
//   same value.
// * Elements which match [data-drawer-id=___] .drawer-expanded-only will be hidden while
//   the drawer is collapsed.
// * Elements which match [data-drawer-id=___] .drawer-collapsed-only will
//   be hidden while the drawer is expanded.

var Drawer = (function(){
  // Find all the drawers

  let toggle = function(drawer, exp_only, col_only) {
    if(drawer.classList.contains('is-hidden')) {
      // drawer is collapsed
      drawer.classList.remove('is-hidden');

      for(let exp of exp_only)
        exp.classList.remove('is-hidden');
      for(let col of col_only)
        col.classList.add('is-hidden');
    }else{
      // drawer is expanded
      drawer.classList.add('is-hidden');

      for(let exp of exp_only)
        exp.classList.add('is-hidden');
      for(let col of col_only)
        col.classList.remove('is-hidden');
    }
  }


  let toggle_elems = document.querySelectorAll(".drawer-toggle");
  for(let toggle_elem of toggle_elems) {
    let id = toggle_elem.dataset.drawerId;
    let drawer = document.querySelector("[data-drawer-id="+id+"].drawer");
    let col_only = document.querySelectorAll("[data-drawer-id="+id+"] .drawer-collapsed-only");
    let exp_only  = document.querySelectorAll("[data-drawer-id="+id+"] .drawer-expanded-only");

    drawer.classList.add('is-hidden');
    for(let exp of exp_only) {
      exp.classList.add('is-hidden');
    }

    toggle_elem.addEventListener('click', function(){toggle(drawer, exp_only, col_only)});
  }

  let self = {};
  return self;
})();
