//gallery.js
var http = new XMLHttpRequest();
var url = '/delete/';
var params = '';

window.addEventListener("DOMContentLoaded", () => {
    // Fullscreen Image
    var imgs = document.querySelectorAll(".gallery-item img");
    if (imgs.length>0) { for (let img of imgs) {
        img.onclick = () => img.classList.toggle("full");
    }}
    // Delete Image
    var links = document.querySelectorAll(".gallery-item label span");
    if (links.length>0) { for (let link of links) {
        link.onclick = () => {
            console.log(link.getAttribute('data-uid'))
            var result = confirm("Want to delete?");
            if (result) {
                curr_click = link.getAttribute('data-uid');
              
                http.open('POST', url + curr_click, true);
                http.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
                http.onreadystatechange = function() {//Call a function when the state changes.
                    if(http.readyState == 4 && http.status == 200) {
                        // http.responseText will be anything that the server return
                        console.log(http.responseText);
                    }
                }
                http.send(params);
            }
        }
    }}
});


