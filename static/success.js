// You can get data from the URL (in this case cFields) and use it

const urlParams = new URLSearchParams(window.location.search);
console.log(urlParams);
const pageCode = urlParams.get('cField1');
document.getElementById("pageCode").textContent = 'pageCode: ' + pageCode ;