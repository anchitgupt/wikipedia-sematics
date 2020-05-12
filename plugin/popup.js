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

  var pathArray = url.split('en.wikipedia.org/wiki/')[1];
  // TODO: remove it
  // alert(pathArray + " ## " + query);
  if (pathArray.split('#').length > 1) pathArray = pathArray.split('#')[0]

  document.getElementById("queryHeader").innerHTML = pathArray;
  document.getElementById("queryText").innerHTML = query;
  // TODO
  // call api function call here
  var myHeaders = new Headers();
  myHeaders.append("Content-Type", "application/json");

  var raw = JSON.stringify({
    "pageName": pathArray,
    "queryText": query
  });

  var requestOptions = {
    method: 'POST',
    headers: myHeaders,
    body: raw,
    redirect: 'follow'
  };

  fetch("http://127.0.0.1:5000/", requestOptions)
    .then(response => response.text())
    .then(result => console.log('Result: ' + result))
    .catch(error => console.log('error', error));

}


changeColor.onclick = function (element) {
  chrome.tabs.query({
    active: true,
    lastFocusedWindow: true
  }, function (tabs) {
    chrome.tabs.executeScript({
        code: "window.getSelection().toString();"
      },
      function (selection) {
        var query = selection[0];
        chrome.tabs.executeScript(tabs[0].id, {
          code: alerting(tabs[0].url, query)
        });
      }
    );
  });
};