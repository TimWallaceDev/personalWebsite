document.addEventListener("DOMContentLoaded", () => 
{   
    console.log("dom ocntent loaded");
    var trigger = document.getElementById("trigger");
    trigger.addEventListener("click", betterAlert);
    trigger.message = "Here is just a little sample of a message. ";
    console.log("Listening...");

    function betterAlert(e){
        let topPad = screen.height / 4
        let message = e.currentTarget.message
        console.log("sending alert")
        var main = document.createElement("div");
        main.id = "betterAlert"
        main.style.textAlign = "center";
        main.style.position = "absolute";
        main.style.top = "0";
        main.style.left = "0";
        main.style.width = "100%";
        main.style.height = "100vh"
        main.style.backgroundColor = "rgba(200,200,200,0.8)";
        main.style.justifyContent = "center";
        main.style.boxSizing = "border-box";

        var box = document.createElement("div")
        box.style.backgroundColor = "#999";
        box.style.padding = "20px";
        box.style.borderRadius = "5px";
        if (screen.width > 300){
            box.style.width = "300px";
        }
        else {
            box.style.width = screen.width - 5
        }
        
        box.style.marginRight = "auto";
        box.style.marginLeft = "auto";
        box.style.marginTop =`${topPad}px`
    
        var messageP = document.createElement("p");
        messageP.innerHTML = message;
    
    
        var closeBtn = document.createElement("button");
        closeBtn.innerHTML = "Close Popup";
        closeBtn.style.border = "none";
        closeBtn.style.borderRadius = "5px";
        closeBtn.addEventListener("click", () => {
            let main = document.getElementById("betterAlert");
            body.removeChild(main);
            console.log("closed");
        })
    
        var body = document.querySelector("body");
    
        box.append(messageP)
        box.append(closeBtn)
        main.append(box)
        body.append(main)
    }
    
})


