
var adminSelectedSourceValue = "";
var adminSelectedNightValue = "";

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

function adminSourceLoad() {
    getAdminSourceDirs()
}

function adminSourceChanged() {
    adminSelectedSourceValue = byId("adminSelectSourceId").value;
    adminSelectedNightValue = "";
    var select = byId("adminSelectNightId");
    while (select.firstChild) {
        select.removeChild(select.firstChild);
    }
    getAdminNights(adminSelectedSourceValue);

}

function adminNightChanged() {
    adminSelectedSourceValue = byId("adminSelectSourceId").value;
    adminSelectedNightValue = byId("adminSelectNightId").value;
    getAdminNightInfo(adminSelectedSourceValue, adminSelectedNightValue)
}

function adminUpdate() {
    adminSelectedSourceValue = byId("adminSelectSourceId").value;
    getAdminNights(adminSelectedSourceValue);
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

function adminPrevious() {
    optionList = byId("adminSelectNightId");
    optionIndex = optionList.selectedIndex;
    if (optionIndex > 1) {
        optionList.selectedIndex = optionIndex - 1;
    }
    adminNightChanged()
}

function adminNext() {
    optionList = byId("adminSelectNightId");
    optionIndex = optionList.selectedIndex;
    if (optionIndex < optionList.options.length - 1) {
        optionList.selectedIndex = optionIndex + 1;
    }
    adminNightChanged()
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

        adminUpdate()
    }

}
