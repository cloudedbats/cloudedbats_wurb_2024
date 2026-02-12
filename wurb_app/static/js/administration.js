
var adminSelectedSourceValue = "";
var adminSelectedNightValue = "";

var leafletMap = null;

function initLeafletMap() {
    if (leafletMap === null) {
        leafletMap = new L.Map('leafletMapId');
        var osmUrl = 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
        var osmAttrib = 'Map data © <a href="http://openstreetmap.org">OpenStreetMap</a> contributors';
        var osm = new L.TileLayer(osmUrl, { minZoom: 4, maxZoom: 16, attribution: osmAttrib });
        leafletMap.setView(new L.LatLng(57.66194, 12.63896), 9);
        leafletMap.addLayer(osm);
    }
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
    if (byId("adminViewDataId").hidden == true) {
        byId("adminViewDataButtonId").classList.add("is-inverted");
        byId("adminViewDataId").hidden = false;
    } else {
        byId("adminViewDataButtonId").classList.remove("is-inverted");
        byId("adminViewDataId").hidden = true;
    };
}

function adminToggleViewActivity() {
    if (byId("adminViewActivityId").hidden == true) {
        byId("adminViewActivityButtonId").classList.add("is-inverted");
        byId("adminViewActivityId").hidden = false;



        getActivityData(adminSelectedSourceValue, adminSelectedNightValue);



    } else {
        byId("adminViewActivityButtonId").classList.remove("is-inverted");
        byId("adminViewActivityId").hidden = true;
    };
}

function adminToggleViewMap() {
    if (byId("adminViewMapId").hidden == true) {
        byId("adminViewMapButtonId").classList.add("is-inverted");
        byId("adminViewMapId").hidden = false;

        initLeafletMap();

    } else {
        byId("adminViewMapButtonId").classList.remove("is-inverted");
        byId("adminViewMapId").hidden = true;
    };
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
