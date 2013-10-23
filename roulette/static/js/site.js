function playDonate() {
  document.getElementById("Donate").style.visibility="hidden";
  document.getElementById("Fun").style.visibility="hidden";
  window.open("{{ auth_url }}", "_blank");
}
function playFun() {
  document.getElementById("Donate").style.visibility="hidden";
  document.getElementById("Fun").style.visibility="hidden";
}
function like() {
  var xmlhttp = new XMLHttpRequest();
  var url = document.getElementsByTagName('iframe')[0].src;
  var title = document.getElementsByTagName('h3')[0].textContent;
  xmlhttp.onreadystatechange=function() {
    if(xmlhttp.readyState == 4 && xmlhttp.status == 200) {
      var li_tag = document.createElement('li');
      li_tag.innerHTML = xmlhttp.responseText;
      document.getElementById('song_list').appendChild(li_tag);
    }
  };
  xmlhttp.open('POST', 'like', true);
  xmlhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");
  xmlhttp.send('url='+url+'&title='+title);
}
function finishSongs() {
  //create the thumbs up buttons for good songs
  location.replace("finish");
}
