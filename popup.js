// Copyright 2018 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

'use strict';



function alerting(url){
  
  var pathArray = url.split('en.wikipedia.org')[1];
  // TODO: remove it
  alert(pathArray);
  // TODO
  // call api function call here
}


changeColor.onclick = function(element) {
  
  chrome.tabs.query({
        active: true,
        lastFocusedWindow: true
      }, function (tabs) {

    chrome.tabs.executeScript(
        tabs[0].id,
        {
          // code: 'alert("' + tabs[0].id + "##" + tabs[0].url + '")'
          code: alerting(tabs[0].url)
        }
          );
  });
};
