document.addEventListener("DOMContentLoaded",function(){
    let oneway = document.querySelector("#oneway")
    let round = document.querySelector("#round")
    let todate = document.querySelector("#todate")
    oneway.onclick = function(){        
        todate.disabled = true;
    }
    round.onclick = function(){
        todate.disabled = false;
    } 
})
