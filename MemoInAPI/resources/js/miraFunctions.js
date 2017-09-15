//var root = 'https://jsonplaceholder.typicode.com';
var person;
var addy = 'http://10.0.0.246:8000/'
var first = false;
function myFunction() {
    msg = $('#m').val();
    nme = $('#name').val();
    var str = '{"name": "';
    str += person;
    str +='", "message":"';
    str +=msg;
    str += '"}';
    console.log(msg);
    console.log(nme);
    console.log(str);
    if (msg !== "") {
        //$('<li>').text(msg).appendTo( "#messages" );
    }
    $('#m').val('');
    var root = 'http://172.31.81.254:8000/';
    var req = new FormData();
    req.append('name', 'joonching');
    req.append('message', 'work baby work');
    //"{'name': 'joonching', 'message':'work'}",
    $.ajax({
        url: root,
        method: "POST",
        data: str,
        //dataType: "json",
        //processData: false,
        headers: {"Content-Type":"text/plain"},
        ///contentType: 'application/json',
    }).then(function(data) {
        $("#messages").empty();
//        window.scroll(0, document.body.scrollHeight);
        onLoadFunction();
//        window.scroll(0, document.body.scrollHeight);
//        if(($(window).scrollTop() + $(window).height() == $(document).height())) {
//            $('html, body').animate({scrollTop: $("messages").offset().top - $("#messages").height() - $(window).height()}, 2000)
//        };
//        
    });
    return false;
}

function onLoadFunction() {
    //var root = 'https://jsonplaceholder.typicode.com';
    var root = 'http://172.31.81.254:8000/';
	alert(document.url);
    $.ajax({
        url: root,  //+ '/posts/1',
        contentType: 'text/plain',
        method: 'GET',
    }).then(function(data) {
        var str = JSON.stringify(data, null, '\t');
        var parsed_data = JSON.parse(data);
        console.log(parsed_data.length);
       // console.log(data);
        msg = $('#m').val();
        //$('#messages').append($('<li>').text(msg));
        var count;
        for(count = parsed_data.length-1; count > 0; count--)
        {
            var date = new Date(parsed_data[count].time.$date);
            console.log(date.toLocaleString());
          $('<li>').html(parsed_data[count].name.bold() 
            +": " +parsed_data[count].message 
            + "<br><br><br><p style=\"text-indent: 410px\"><font size = \"1\">Date:</font> " 
            + date.toLocaleString().fontsize(1)).appendTo( "#messages" );  
        }
        $('<li>').html(parsed_data[count].name.bold() +": " +parsed_data[count].message).appendTo( "#messages" );  
    });
    
    return false;
}

$(document).ready( function () {
document.write('hello');
person = prompt("Please enter your name", "Your Name Here");
    onLoadFunction();

});


                  
