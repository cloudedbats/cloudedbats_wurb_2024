
function adminToggleSettings() {
    if (byId("adminSettingsId").classList.contains("is-hidden")) {
        byId("adminBodyId").classList.add("is-hidden");
        byId("adminSettingsId").classList.remove("is-hidden");
        byId("adminShowSettingsTextId").textContent = "Hide settings";
    } else {
        byId("adminSettingsId").classList.add("is-hidden");
        byId("adminBodyId").classList.remove("is-hidden");
        byId("adminShowSettingsTextId").textContent = "Show settings";
    };
}

function adminCommand(command) {
    // let selectedValue = byId("recModeSelectId").options[byId("recModeSelectId").selectedIndex].value
    hideDivision(byId("confirmRemoveQ0Id"));
    hideDivision(byId("confirmRemoveNaId"));
    hideDivision(byId("confirmDeleteNightId"));
    if (command == "confirmRemoveQ0") {
        showDivision(byId("confirmRemoveQ0Id"));
    }
    else if (command == "confirmRemoveNa") {
        showDivision(byId("confirmRemoveNaId"));
    }
    else if (command == "confirmDeleteNight") {
        showDivision(byId("confirmDeleteNightId"));
    }
    else {
        var sourceId = byId("adminSelectSourceId").value;
        var nightId = byId("adminSelectNightId").value;
        adminExecuteCommand(sourceId, nightId, command);
    }
}

function adminSourceLoad() {
    getAdminSourceDirs()
}

function adminSourceChanged() {
    var sourceId = byId("adminSelectSourceId").value;
    getAdminNights(sourceId);
}

function adminToggleViewData() {
    alert("adminToggleViewData...");
}

function adminToggleViewMap() {
    alert("adminToggleViewMap...");
}

function adminToggleViewMap() {
    alert("adminToggleViewMap...");
}

function adminNightChanged() {
    adminUpdate()
}

function adminPrevious() {
    optionList = byId("adminSelectNightId");
    optionIndex = optionList.selectedIndex;
    optionList.selectedIndex = optionIndex - 1;
    adminUpdate()
}

function adminNext() {
    optionList = byId("adminSelectNightId");
    optionIndex = optionList.selectedIndex;
    optionList.selectedIndex = optionIndex + 1;
    adminUpdate()
}

function adminUpdate() {
    var sourceId = byId("adminSelectSourceId").value;
    var nightId = byId("adminSelectNightId").value;
    getAdminNightInfo(sourceId, nightId);
}

// function adminGetComments() {
//     var comments = byId("adminCommentsId").value
//     return comments;
// }

// function adminSetComments(comment) {
//     byId("adminCommentsId").value = comment
// }
