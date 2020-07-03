
var videoID;
function getHttpParam(name) {
    var regexS = "[\\?&]" + name + "=([^&#]*)";
    var regex = new RegExp(regexS);
    var results = regex.exec(window.location.href);
    if (results == null) {
        return 2;
    } else {
        return results[1];
    }
}
window.onload = function() {
    videoID = getHttpParam("videoID");
    $.ajax({
        type:"GET",
        url:"http://202.30.29.170:8000/plus?url=https://www.youtube.com/watch?v=" + videoID,
        success: function(data) {
            console.log(data);
            _temp = data.split("\"");
            document.getElementById("img1").src = "data:image/png;base64," + _temp[3];
            console.log (_temp[3]);
            document.getElementById("img2").src = "data:image/png;base64," + _temp[7];
            console.log (_temp[7]);
            document.getElementById("img3").src = "data:image/png;base64," + _temp[11];
            console.log (_temp[11]);
            document.getElementById("img4").src = "data:image/png;base64," + _temp[15];
            console.log (_temp[15]);
        }
    }); 
}
