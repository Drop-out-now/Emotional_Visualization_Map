const xhr = new XMLHttpRequest();
xhr.open('GET', 'http://127.0.0.1:3000',true);
xhr.setRequestHeader('Access-Control-Allow-Origin', 'http://127.0.0.1:3000');
xhr.onload = () => {
    if (xhr.status === 200) {
        document.getElementById("test").value = xhr.responseText;    
    }
};

setInterval(
  () => {
    xhr.send();
  }
,10000);