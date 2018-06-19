$(document).ready(function(){

    // load 10 initial tweets on the page load
    url = "/get_list/?start=0&limit=10"; 
    console.log("initial url:   "+ url)

    $.get(url, function(data, status){
        $("ul").append(data);
    });
    
    // function to load more tweets on button click 
    $("input").click(function(){
        start = $("ul li").length +1;
        limit = 5;
        url = "/get_list/?start=" + start + "&limit=" + limit; 

        console.log("url:   "+ url)
        $.get(url, function(data, status){
            $("ul").append(data);
        });
    });

});
