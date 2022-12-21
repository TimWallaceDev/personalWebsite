//TODO
//make sure habit != reward
//make sure reward != habit
//no duplicate rewards
//no duplicate habits

function progress(){
  let progress = document.createElement("progress");
  progress.max = 5;
  progress.value = 1;
  progress.id = "progress";

  setTimeout(() => {
    progress.value = 2;
  }, 1000)

  


  var menu = document.querySelector("nav");
  menu.append(progress);
}

function betterAlert(messageText){
  let topPad = screen.height / 4;
  let message = messageText;
  console.log("sending alert");
  var main = document.createElement("div");
  main.id = "betterAlert";
  main.style.textAlign = "center";
  main.style.position = "absolute";
  main.style.top = "0";
  main.style.left = "0";
  main.style.width = "100%";
  main.style.height = "100vh"
  main.style.backgroundColor = "rgba(200,200,200,0.8)";
  main.style.justifyContent = "center";
  main.style.boxSizing = "border-box";
  main.style.zIndex = "6";

  var box = document.createElement("div")
  box.style.backgroundColor = "#999";
  box.style.padding = "20px";
  box.style.borderRadius = "5px";
  if (screen.width > 300){
      box.style.width = "300px";
  }
  else {
      box.style.width = screen.width - 5;
  }
  
  box.style.marginRight = "auto";
  box.style.marginLeft = "auto";
  box.style.marginTop =`${topPad}px`;

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

document.addEventListener("DOMContentLoaded", () => {
  //-------------------------------------------------------------------------------------ONLOAD SETUP
  if (!localStorage.getItem("habitNames")) {
    //add palceholder to total saved
    var totalSavings = document.getElementById("totalSavings");
    totalSavings.innerHTML += "0";
    //add placeholder to dashboard
    var mainMessage = document.getElementById("messageDisplay");
    var menuMessage = document.getElementById("habitMessage");
    mainMessage.innerHTML = "Add Bad Habits in the Menu!";
    menuMessage.innerHTML = "Add Bad Habits Using the Form Above!";
    mainMessage.style.padding = "20px";
    //add placeholder to menu
    var menuMessage = document.getElementById("removeHabits");
    menuMessage.innerHTML = "Add habit using the form below!";
  }

  //initialize spent value
  if (!localStorage.getItem("spent")) {
    localStorage.setItem("spent", "0");
  }

  //Image Generation settings
  //get preference
  if (!localStorage.getItem("imagePreference")){
    localStorage.setItem("imagePreference", "auto")
  }

  let autoSwitch = document.getElementById("autoSwitch")
  let genericSwitch = document.getElementById("genericSwitch")

  autoSwitch.addEventListener('change', setImages)
  genericSwitch.addEventListener('change', setImages)

  //Display data
  refreshDisplay()



  //-----------------------------------------------------------------------------------------------------Menu Slider Function
  function openMenu() {
    var menu = document.querySelector("nav");
    var openMenuBtn = document.getElementById("openMenuBtn");
    openMenuBtn.style.display = "none";
    menu.style.width = "100%";
  }

  function closeMenu() {
    var main = document.querySelector("main");
    var menu = document.querySelector("nav");
    var openMenuBtn = document.getElementById("openMenuBtn");
    main.style.width = "100%";
    menu.style.width = "0";
    openMenuBtn.style.display = "block";
    openMenuBtn.addEventListener("click", openMenu);
  }

  //close menu onload
  closeMenu();
  var closeMenuBtn = document.getElementById("closeMenuBtn");
  closeMenuBtn.addEventListener("click", closeMenu);

  //-------------------------------------------------------------------------------------------auto image preference and switch functions

  function setImages(){
    if (localStorage.getItem("imagePreference") == "auto"){
      localStorage.setItem("imagePreference", "generic")
      setSwitches()
    }
    else{
      localStorage.setItem("imagePreference", "auto")
      setSwitches()
    }
  }

  //set switches
  function setSwitches(){
    let autoSwitch = document.getElementById("autoSwitch")
    let genericSwitch = document.getElementById("genericSwitch")
    if (localStorage.getItem("imagePreference") == "auto"){
      autoSwitch.checked = true;
      genericSwitch.checked = false;
    }
    else{
      autoSwitch.checked = false;
      genericSwitch.checked = true;
    }
  }
  setSwitches()

  //------------------------------------------------------------------------------------------ADD HABIT
  //add event listener to submit button
  var submitHabit = document.getElementById("submitHabit");
  submitHabit.addEventListener("click", addHabit);

  function addHabit() {
    //Gather Data from form
    var newHabitName = document.getElementById("habitName").value;
    var newHabitCost = document.getElementById("habitCost").value;
    var newHabitQuitDate = document.getElementById("habitDate").value;
    document.getElementById("messageDisplay").innerHTML = ""
    //TODO
    //check that fields are not empty
    if (newHabitName.length == 0) {
      betterAlert("please enter name of habit");
      return 0;
    }
    if (newHabitCost.length == 0) {
      betterAlert("please enter habit daily cost in dollars");
      return 0;
    }
    if (newHabitQuitDate.length == 0) {
      betterAlert("please enter the date you quit this habit");
      return 0;
    }
    //Make sure habit is not in rewards
    var rewardsListString = localStorage.getItem("rewardsList");
    var rewardsListObj = JSON.parse(rewardsListString);
    if (rewardsListObj){
      for (let i = 0; i < rewardsListObj.length; i++){
        if (rewardsListObj[i] == newHabitName){
          betterAlert("please make sure that habits are not the same as rewards.")
          return 0
        }
      }
    }

    //make sure no duplicate habits
    var habitNames = localStorage.getItem("habitNames");
    var habitObject = JSON.parse(habitNames);
    if (habitObject != null){
      for (let item of habitObject){
        if (item == newHabitName){
          betterAlert("no duplicate habits please. If you wish to update this habit, please delete it and add it again.")
          return 0
        }
      }
    }
    

    //clear out form
    document.getElementById("habitName").value = "";
    document.getElementById("habitCost").value = "";
    document.getElementById("habitDate").value = "";

    //get habit names and add new habit to list
    if (localStorage.getItem("habitNames")) {
      var habitNames = localStorage.getItem("habitNames");
      var habitObject = JSON.parse(habitNames);
      var len = habitObject.length;
    } else {
      var len = 0;
      habitObject = [];
    }

    habitObject[len] = newHabitName;
    localStorage.setItem(newHabitName, newHabitCost + "," + newHabitQuitDate);
    localStorage.setItem("habitNames", JSON.stringify(habitObject));

    //re render the DOM
    refreshDisplay();
  }

  //---------------------------------------------------------------------------------------- add Rewards

  //set event listener for addReward button
  var addRewardBtn = document.getElementById("submitReward");
  addRewardBtn.addEventListener("click", addReward);

  function addReward() {
    //get local storage and make check to see if it is empty
    if (!localStorage.getItem("rewardsList")) {
      var rewards = [];
      localStorage.setItem("rewardsList", JSON.stringify(rewards));
    }
    //if empty, initialize local storage values

    //add new reward
    var rewardName = document.getElementById("rewardName").value;
    var rewardCost = document.getElementById("rewardCost").value;
    var imagePreference = localStorage.getItem("imagePreference");

    //make sure reward field are complete
    if (rewardName.length == 0){
      betterAlert("please enter reward name")
      return 0
    }
    if (rewardCost.length == 0){
      betterAlert("please enter reward cost")
      return 0;
    }
    //make sure reward is not a habit

    if (localStorage.getItem("habitNames")) {
      var habitNames = localStorage.getItem("habitNames");
      var habitObject = JSON.parse(habitNames);
      for (let i = 0; i < habitObject.length; i++){
        if (habitObject[i] == rewardName){
          betterAlert("please make sure that rewards are not the same as Habits.")
          return 0
        }
      }
    }

    //make sure that no duplicate rewards
    //retreive reward obj
    var rewardsListString = localStorage.getItem("rewardsList");
    var rewardsListObj = JSON.parse(rewardsListString);
    for (let item of rewardsListObj){
      if (item == rewardName){
        betterAlert("no duplicates allowed. Please delete the duplicate before trying again.")
        return 0
      }
    }

    progress()
    var currentProgress = document.getElementById("progress");


    //generate image URL
    if (imagePreference == "generic"){
      rewardURL = "https://cdn-icons-png.flaticon.com/512/1426/1426770.png";
      localStorage.setItem(rewardName + "url", rewardURL);
      //retreive reward obj
      var rewardsListString = localStorage.getItem("rewardsList");
      var rewardsListObj = JSON.parse(rewardsListString);

      //append reward obj
      rewardsListObj.push(rewardName);
      localStorage.setItem("rewardsList", JSON.stringify(rewardsListObj));
      localStorage.setItem(rewardName, rewardCost);

      //clear out form TODO
      document.getElementById("rewardName").value = "";
      document.getElementById("rewardCost").value = "";

      //reload
      refreshDisplay();
    }
    else{
      fetch(`https://timwallace.ca/generator/${rewardName}`)
      .then((response) => response.text())
      .then((data) => {
        localStorage.setItem(rewardName + "url", data);
        //retreive reward obj
        var rewardsListString = localStorage.getItem("rewardsList");
        var rewardsListObj = JSON.parse(rewardsListString);

        //append reward obj
        rewardsListObj.push(rewardName);
        localStorage.setItem("rewardsList", JSON.stringify(rewardsListObj));
        localStorage.setItem(rewardName, rewardCost);

        //clear out form TODO
        document.getElementById("rewardName").value = "";
        document.getElementById("rewardCost").value = "";

        //reload
        refreshDisplay();
      });
    }
  }


  //------------------------------------------------------------------------------------refresh Display
  function refreshDisplay() {
    /*--------Display habits // display habits in menu------------ */
    
      //get habit list
      var habitNamesString = localStorage.getItem("habitNames");
      var habitObject = JSON.parse(habitNamesString);
    
      //Clear habit Children from MAIN
      var habitDisplayMain = document.getElementById("habitDisplay");
      while (habitDisplayMain.firstChild) {
        habitDisplayMain.removeChild(habitDisplayMain.lastChild);
      }
      //clear out the children for MENU
      var habitDisplayMenu = document.getElementById("removeHabits");
      while (habitDisplayMenu.firstChild) {
        habitDisplayMenu.removeChild(habitDisplayMenu.lastChild);
      }
    
      //initialize totals
      var totalSaved = 0.0;
      var dailySavings = 0.0;
    
      //Determine how many children
      try {
        var numberOfHabits = habitObject.length;
      } catch {
        var numberOfHabits = 0;
      }
    
      //Add each child back in
      for (i = 0; i < numberOfHabits; i++) {
        /*-------LOOPING FOR MAIN----------- */
        var listel = document.createElement("p");
        listel.className = "habitItem";
        var singleHabitObject = localStorage.getItem(habitObject[i]);
        var habitList = singleHabitObject.split(",");
        var habitCost = parseFloat(habitList[0]);
        var habitDate = Date.parse(habitList[1]);
        var today = Date.now();
        var elapsed = (today - habitDate) / 86400000;
    
        //calculate savings since quit date
        totalSaved += elapsed * habitCost;
        dailySavings += habitCost;
        listel.innerHTML = habitObject[i] + ": $ " + habitCost.toFixed(2) + " per day";
        habitDisplayMain.append(listel);
    
        /*-------LOOPING FOR MENU----------- */
        let delBtn = document.createElement("button");
        delBtn.setAttribute("data-habitName", habitObject[i]);
        delBtn.setAttribute("class", "delBtn");
        delBtn.innerHTML = "X";
        delBtn.addEventListener("click", (event) => {
          var habitNamesString = localStorage.getItem("habitNames");
          var habitObject = JSON.parse(habitNamesString);
          var index = habitObject.indexOf(event.target.dataset.habitname);
          habitToDelete = event.target.dataset.habitname;
          habitObject.splice(index, 1);
          localStorage.setItem("habitNames", JSON.stringify(habitObject));
          localStorage.removeItem(habitToDelete);
    
          refreshDisplay();
        });
    
        var listel = document.createElement("li");
        listel.setAttribute("class", "li-habit");
        //get name of habit
        //cost, date of habit
        listel.append(delBtn);
        listel.append(
          " " +
            habitObject[i] +
            ": $" +
            habitCost +
            "/day | quit since: " +
            habitList[1]
        );
        habitDisplayMenu.append(listel);
      }
      //display current savings
      var currentSavedEl = document.getElementById("totalSavings");
      currentSavedEl.innerHTML = totalSaved.toFixed(2);
      //display daily and yearly savings
      var totalDisplay = document.createElement("p");
      totalDisplay.id = "dailyDisplay";
      var yearlySavings = document.createElement("p");
      yearlySavings.id = "yearlyDisplay";
      var yealyTotal = (dailySavings * 365).toFixed(2);
      yealyTotal = parseFloat(yealyTotal);
      yealyTotal = yealyTotal.toLocaleString();
      totalDisplay.innerHTML = `total daily savings: $<span id="dailySavingsValue">${dailySavings.toFixed(
        2
      )}</span>`;
      yearlySavings.innerHTML = `Yearly Savings: $${yealyTotal}`;
      habitDisplayMain.append(totalDisplay);
      habitDisplayMain.append(yearlySavings);
    
      /*---------------------------------DISPLAY REWARDS-----------------------*/
        //select reward display div
        var rewardsDisplayBox = document.getElementById("removeRewards");
        var rewardsDisplayMain = document.getElementById("rewardsBox");
    
        //check if rewards are empty and add placeholders
        if (!localStorage.getItem("rewardsList")) {
          //fill in placeholders
          const placeholders = document.getElementsByClassName("rewardMessage")
          placeholders[0].innerHTML = "Add Rewards Using the Form Above!";
          placeholders[1].innerHTML = "Add Rewards in the Menu!";
          rewardsListObj = [];
        }
        else if (localStorage.getItem("rewardsList") == "[]"){
          //fill in placeholders
          const placeholders = document.getElementsByClassName("rewardMessage")
          placeholders[0].innerHTML = "Add Rewards Using the Form Above!";
          placeholders[1].innerHTML = "Add Rewards in the Menu!";
          rewardsListObj = [];
        }
    
        //get rewards from local storage
        else {
          var rewardsListStr = localStorage.getItem("rewardsList");
          var rewardsListObj = JSON.parse(rewardsListStr);
        }
        //clear out any children
        while (rewardsDisplayBox.firstChild) {
          rewardsDisplayBox.removeChild(rewardsDisplayBox.lastChild);
        }
        while (rewardsDisplayMain.firstChild) {
          rewardsDisplayMain.removeChild(rewardsDisplayMain.lastChild);
        }

        //add placeholder to balance if no rewards
        if (rewardsListObj.length == 0){
          var balanceBox = document.getElementById("balanceValue");
          balanceBox.innerHTML = "0.00";
        }
    
        //display rewards in Menu
        for (i = 0; i < rewardsListObj.length; i++) {
          var newEl = document.createElement("p");
          var rewardObjStr = localStorage.getItem(rewardsListObj[i]);
          var rewardObj = JSON.parse(rewardObjStr)
          var price = rewardObj;
  
          //set up delete btn
          var delRewardBtn = document.createElement("button");
          delRewardBtn.innerHTML = "X";
          delRewardBtn.setAttribute("data-reward", rewardsListObj[i]);
          delRewardBtn.className = "delBtn"
          delRewardBtn.addEventListener("click", (event) => {
            var rewardNamesString = localStorage.getItem("rewardsList");
            var rewardObject = JSON.parse(rewardNamesString);
            var index = rewardObject.indexOf(event.target.dataset.reward);
            rewardToDelete = event.target.dataset.reward;
            rewardObject.splice(index, 1);
            localStorage.setItem("rewardsList", JSON.stringify(rewardObject));
            localStorage.removeItem(rewardToDelete);
    
            refreshDisplay();
          });
          newEl.append(delRewardBtn);
          newEl.append(rewardsListObj[i] + ": $" + price);
          rewardsDisplayBox.append(newEl);
    
          //total Banked
          var totalSaved = parseFloat(
            document.getElementById("totalSavings").innerHTML
          );
          var balanceBox = document.getElementById("balanceValue");
          var spent = parseInt(localStorage.getItem("spent"));
          var balance = totalSaved - spent;
          balanceBox.innerHTML = balance.toFixed(2);
    
          //main display
          var newMainEl = document.createElement("div");
          var newTextDiv = document.createElement("div");
          newMainEl.className = "rewardBox"
    
          //add claim button
          var newMainBtn = document.createElement("button");
          var itemPrice = parseInt(localStorage.getItem(rewardsListObj[i]));
          if (price <= balance) {
            newMainBtn.style.backgroundColor = "green";
            newMainBtn.innerHTML = "Claim Reward!";
            newMainBtn.setAttribute("data-rewardName", rewardsListObj[i]);
            newMainBtn.setAttribute("data-rewardCost", price);
            newMainBtn.className = "buyBtn available";
          } else {
            newMainBtn.style.backgroundColor = "gray";
            var dailySavings = parseFloat(
              document.getElementById("dailySavingsValue").innerHTML
            );
            var daysLeft = (itemPrice - balance) / dailySavings;
            newMainBtn.disabled = true;
            newMainBtn.innerHTML = `${daysLeft.toFixed(1)} days to earn`;
            newMainBtn.className = "buyBtn locked";
          }
    
          newTextDiv.append(newMainBtn);
          //add reward Name
          var newTextP = document.createElement("p");
          newTextP.innerHTML = " $" + itemPrice + " - " + rewardsListObj[i];
          newTextDiv.append(newTextP)
    
          //append text to main EL
          newMainEl.append(newTextDiv)
    
          //add Image
          var url = localStorage.getItem(rewardsListObj[i] + "url")
          var newImg = document.createElement("img")
          newImg.src = url;
          newImg.style.maxWidth = "150px";
          newMainEl.append(newImg)
    
          //append element finally
          rewardsDisplayMain.append(newMainEl);
        }
    
        let availableBtns = document.querySelectorAll(".available");
    
        //buying action
        for (let i = 0; i < availableBtns.length; i++) {
          availableBtns[i].addEventListener("click", (event) => {
            let cost = parseInt(event.target.dataset.rewardcost);
            let name = event.target.dataset.rewardname;
    
            //add to spent
            let oldSpent = parseInt(localStorage.getItem("spent"));
            let newSpent = oldSpent + cost;
            localStorage.setItem("spent", newSpent);
    
            //remove item from rewards
            var rewardNamesString = localStorage.getItem("rewardsList");
            var rewardObject = JSON.parse(rewardNamesString);
            var index = rewardObject.indexOf(name);
            rewardToDelete = name;
            rewardObject.splice(index, 1);
            localStorage.setItem("rewardsList", JSON.stringify(rewardObject));
            localStorage.removeItem(rewardToDelete);
    
            //TODO add purchased items to spoils
    
            if (localStorage.getItem("spoils")) {
                var treasure = localStorage.getItem("spoils");
                treasure = JSON.parse(treasure);
            }
            else {
                var treasure = [];
            }
            treasure.push(name);
            localStorage.setItem("spoils", JSON.stringify(treasure));
            refreshDisplay();
          });
        }
    
        /*--------------------------------DISPLAY SPOILS-----------------*/
    
        //clear out the div
        let spoilsDiv = document.getElementById("spoilsDiv")
        while (spoilsDiv.lastChild) {
            spoilsDiv.removeChild(spoilsDiv.lastChild)
        }
        if (!localStorage.getItem("spoils")) {
            document.getElementById("spoilsDiv").innerHTML = "No Spoils yet";
            spoilsDiv.style.textAlign = "center";
            spoilsDiv.style.display = "block";
    
        }
        else {
            spoilsDiv.style.display = "flex";
            var spoilsList = JSON.parse(localStorage.getItem("spoils"));
            for (let i = 0; i < spoilsList.length; i++) {
                let spoilContainer = document.createElement("div");
                let spoilBox = document.createElement("p")
                let spoildiv = document.getElementById("spoilsDiv");
                spoilBox.innerHTML = spoilsList[i];
                spoilContainer.append(spoilBox);
    
                //add image
                let img = document.createElement("img")
                img.style.maxWidth = "150px";
                img.src = localStorage.getItem(spoilsList[i] + "url")
                spoilContainer.append(img);
    
                //add container to spoilDiv
                spoilContainer.className = "spoilContainer";
                spoildiv.append(spoilContainer);
    
                //"https://cdn-icons-png.flaticon.com/512/1426/1426770.png"
            }
        }
    }
});
