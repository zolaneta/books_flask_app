/**
 * Created by bot on 6/24/16.
 */



  function fun() {
  alert("we have fun");
}

  function thanks(reason){
                alert("Thank You " +  reason)
            }


function disapear(){
    document.getElementById("top2").style.visibility = "hidden";
}

function show(){
    document.getElementById("top2").style.visibility = "visible";
}

///setTimeout(disapear, 7000);
///setTimeout(show, 8000);

setInterval("disapear()",  1000);
setInterval("show()",  1100);