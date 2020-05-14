
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
function showresult(result) {
  console.log(result);
  result = JSON.parse(result)
  console.log(result["status"]);
  if (result.status === "OK") {
    var row = "";
    var keys = Object.keys(result.result)
    for (var x in keys) {
      var data = ""
      for (var y in result.result[keys[x]]) {
        data += result.result[keys[x]][y];
      }
      console.log(x, data);
      if (data === "No sentences found in the cited document" || data === "No data To handle") {
        row += '<tr id="' + keys[x] + '">' +
          '<td>' +
          '<div class="w3-card w3-hover-shadow w3-margin w3-row-padding">' +
          "Cite : [" + keys[x] + "]" +
          '<p class="w3-red">' +
          data +
          '</p>' +
          '</div></td>' +
          '</tr></hr>';
      } else {
        row += '<tr id="' + keys[x] + '">' +
          '<td>' +
          '<div class="w3-card w3-hover-shadow w3-margin w3-row-padding">' +
          "Cite : [" + keys[x] + "]" +
          '<p>' +
          data +
          '</p>' +
          '</div></td>' +
          '</tr></hr>';
      }
    }
    document.getElementById('resultText')
      .innerHTML = row;
  } else {
    // TODO: Add messages
    document.getElementById('resultText')
      .innerHTML = '<h5 class="w3-red">Internal Error<h5>';
  }
}




function alerting(url, query) {

  var pathArray = url.split('en.wikipedia.org/wiki/')[1];
  // TODO: remove it
  // alert(pathArray + " ## " + query);
  if (pathArray.split('#').length > 1) pathArray = pathArray.split('#')[0]

  document.getElementById("queryHeader").innerHTML = '<strong>Document: </strong>: ' + pathArray;
  document.getElementById("queryText").innerHTML = '<strong>Query</strong>: '+ query;
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
    .then(result => showresult(result))
    .catch(error => console.log('error', error));

}


changeColor.onclick = function (element) {

  document.getElementById("head").setAttribute("style", "visibility: visible;");
  document.getElementById("tail").setAttribute("style", "visibility: visible;");

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