// Copyright 2018 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

'use strict';



// function load(){
//   chrome.tabs.query({
//         active: true,
//         lastFocusedWindow: true
//       }, function (tabs){
//       document.getElementById("queryHeader").innerHTML = tabs[0].url;
//     }
//   );
// }

function alerting(url, query) {

  var pathArray = url.split('en.wikipedia.org')[1];
  // TODO: remove it
  // alert(pathArray + " ## " + query);
  document.getElementById("queryHeader").innerHTML = pathArray;
  document.getElementById("queryText").innerHTML = query;
  // TODO
  // call api function call here
}


changeColor.onclick = function (element) {
  chrome.tabs.query(
  {
    active: true,
    lastFocusedWindow: true
  },function (tabs) 
  {
    chrome.tabs.executeScript(
      {
      code: "window.getSelection().toString();"
    }, 
    function (selection) 
    {
      var query = selection[0];
      chrome.tabs.executeScript(tabs[0].id, 
        {code: alerting(tabs[0].url, query)});
    }
    );
  }
  );
};