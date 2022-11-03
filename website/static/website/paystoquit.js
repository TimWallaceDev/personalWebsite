document.addEventListener("DOMContentLoaded", () => {
  //ONLOAD SETUP
  if (!localStorage.getItem("habitNames")) {
    //add palceholder to total saved
    var totalSavings = document.getElementById("totalSavings");
    totalSavings.innerHTML += "0";
    //add placeholder to dashboard
    var mainMessage = document.getElementById("messageDisplay");
    var menuMessage = document.getElementById("habitMessage");
    mainMessage.innerHTML = "Add Rewards in the Menu!";
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

  //Menu Slider Function
  function openMenu() {
    console.log("opened Menu")
    var menu = document.querySelector("nav");
    var openMenuBtn = document.getElementById("openMenuBtn");
    openMenuBtn.style.display = "none";
    menu.style.width = "100%";
  }

  function closeMenu() {
    console.log("closed Menu")
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

  //Image Generation settings
  //get preference
  if (!localStorage.getItem("imagePreference")){
    localStorage.setItem("imagePreference", "auto")
  }
  console.log(localStorage.getItem("imagePreference"))

  let autoSwitch = document.getElementById("autoSwitch")
  let genericSwitch = document.getElementById("genericSwitch")

  autoSwitch.addEventListener('change', setImages)
  genericSwitch.addEventListener('change', setImages)

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

  //ADD HABIT
  //add event listener to submit button
  var submitHabit = document.getElementById("submitHabit");
  submitHabit.addEventListener("click", addHabit);

  function addHabit() {
    console.log("addedhabit")
    //Gather Data from form
    var newHabitName = document.getElementById("habitName").value;
    var newHabitCost = document.getElementById("habitCost").value;
    var newHabitQuitDate = document.getElementById("habitDate").value;
    //TODO
    //check that fields are not empty
    if (newHabitName.length == 0) {
      alert("please enter name of habit");
      return 0;
    }
    if (newHabitCost.length == 0) {
      alert("please enter habit daily cost in dollars");
      return 0;
    }
    if (newHabitQuitDate.length == 0) {
      alert("please enter the date you quit this habit");
      return 0;
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
    displayHabits();
  }

  //Display Habits
  function displayHabits() {
    console.log("displayedHabits")
    //get habit list
    var habitNamesString = localStorage.getItem("habitNames");
    var habitObject = JSON.parse(habitNamesString);

    //Clear habit Children from DOM
    var habitDisplay = document.getElementById("habitDisplay");
    while (habitDisplay.firstChild) {
      habitDisplay.removeChild(habitDisplay.lastChild);
    }

    //initialize totals
    var totalSaved = 0.0;
    var dailySavings = 0.0;

    //Add each child back in
    try {
      var numberOfHabits = habitObject.length;
    } catch {
      var numberOfHabits = 0;
    }

    for (i = 0; i < numberOfHabits; i++) {
      //create Parent element for habit
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
      listel.innerHTML = habitObject[i] + ": $ " + habitCost + " per day";
      habitDisplay.append(listel);
    }
    //display current savings
    var currentSavedEl = document.getElementById("totalSavings");
    totalSaved = totalSaved.toFixed(2);
    totalSaved = parseFloat(totalSaved);
    totalSaved = totalSaved.toLocaleString();
    currentSavedEl.innerHTML = totalSaved;
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
    habitDisplay.append(totalDisplay);
    habitDisplay.append(yearlySavings);
    displayHabitsInMenu()
  }

  //DISPLAY HABIT IN MENU
  function displayHabitsInMenu() {
    console.log("displayedhabitsinMenu")
    //get habit list
    var habitNamesString = localStorage.getItem("habitNames");
    habitObject = JSON.parse(habitNamesString);
    //clear out the DOM for refresh
    var habitDisplay = document.getElementById("removeHabits");
    while (habitDisplay.firstChild) {
      habitDisplay.removeChild(habitDisplay.lastChild);
    }
    //add all habits back into DOM
    try {
      var numberOfHabits = habitObject.length;
    } catch {
      var numberOfHabits = 0;
    }
    for (i = 0; i < numberOfHabits; i++) {
      //Set delete button to remove habit

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

        displayHabits();
      });

      var listel = document.createElement("li");
      listel.setAttribute("class", "li-habit");
      //get name of habit
      //cost, date of habit
      var singleHabitObject = localStorage.getItem(habitObject[i]);
      var habitList = singleHabitObject.split(",");
      var habitCost = habitList[0];
      var habitDate = habitList[1];
      listel.append(delBtn);
      listel.append(
        " " +
          habitObject[i] +
          ": $" +
          habitCost +
          "/day | quit since: " +
          habitDate
      );
      habitDisplay.append(listel);
    }
    displayRewards()
  }

  displayHabits();

  //Rewards

  //set event listener for addReward button
  var addRewardBtn = document.getElementById("submitReward");
  addRewardBtn.addEventListener("click", addReward);

  function addReward() {
    console.log("rewardAdded")
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

    //make sure rewward field are complete
    if (rewardName.length == 0){
      alert("please enter reward name")
      return 0
    }
    if (rewardCost.length == 0){
      alert("please enter reward cost")
      return 0;
    }

    if (imagePreference == "generic"){
      rewardURL = "https://cdn-icons-png.flaticon.com/512/1426/1426770.png";
    }
    else{
      let token = document.querySelector('input[name="csrfmiddlewaretoken"]')
      console.log(token)
      
      console.log(token.value)
      console.log("token ^^^^^")
      fetch("http://127.0.0.1:8000/generator", {
        method: "post",
        keyword: rewardName,
        csrfmiddlewaretoken: token,
      })
      .then((response) => response.json())
      .then((data) => console.log(data));
      rewardURL = "https://cdn-icons-png.flaticon.com/512/1426/1426770.png";
    }

    console.log(rewardURL)

    //retreive reward obj
    var rewardsListString = localStorage.getItem("rewardsList");
    var rewardsListObj = JSON.parse(rewardsListString);

    //append reward obj
    rewardsListObj.push(rewardName);
    localStorage.setItem("rewardsList", JSON.stringify(rewardsListObj));
    localStorage.setItem(rewardName, rewardCost);
    localStorage.setItem(rewardName + "url", rewardURL);
    //console.log(localStorage.getItem(rewardName))

    //clear out form TODO
    document.getElementById("rewardName").value = "";
    document.getElementById("rewardCost").value = "";

    //reload
    displayRewards();
  }

  function displayRewards() {
    console.log("rewards displayed")
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

        displayRewards();
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
      console.log("url" + url)
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

        displayRewards();

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
        console.log("nice buy")
        displayRewards();
      });
    }
    displaySpoils()
  }

  function displaySpoils() {
    console.log("displayedSpoils")

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
