
async function getAdminSourceDirs() {
    // fetch("/module-admin/get-rec-sources", { method: "GET" })
    fetch("/annotations/sources", { method: "GET" })
        .then(function (response) {
            if (response.ok) {
                return response.json();
            } else {
                return Promise.reject(response);
            }
        })
        .then(function (json) {
            // Populate options to select list.
            var select = byId("adminSelectSourceId");
            // Empty.
            while (select.firstChild) {
                select.removeChild(select.firstChild);
            }
            // Add first option.
            var option = document.createElement("option");
            option.textContent = "Select:";
            option.value = "select";
            select.appendChild(option);
            // Use received json.
            for (var i = 0; i < json.length; i++) {
                var content = json[i];
                var option = document.createElement("option");
                option.textContent = content.name;
                option.value = content.id;
                select.appendChild(option);
            }
        })
        .catch(function (err) {
            console.warn("Error in javascript fetch: ", err);
        })
};

async function getAdminNights(sourceId) {
    fetch("/annotations/nights?" + new URLSearchParams({
        sourceId: sourceId,
    }), { method: "GET" })
        .then(function (response) {
            if (response.ok) {
                return response.json();
            } else {
                return Promise.reject(response);
            }
        })
        .then(function (json) {
            // Populate options to select list.
            var select = byId("adminSelectNightId");
            // Empty.
            while (select.firstChild) {
                select.removeChild(select.firstChild);
            }
            // Add first option.
            var option = document.createElement("option");
            option.textContent = "Select:";
            option.value = "select";
            select.appendChild(option);
            // Use received json.
            for (var i = 0; i < json.length; i++) {
                var content = json[i];
                var option = document.createElement("option");
                option.textContent = content.id;
                option.value = content.id;
                select.appendChild(option);
            }
        })
        .catch(function (err) {
            console.warn("Error in javascript fetch: ", err);
        })
};

async function getAdminNightInfo(sourceId, nightId) {

    byId("adminMonitoringNightId").textContent = ""
    byId("adminDirPathId").textContent = ""
    byId("adminNumberOfSoundFilesId").textContent = ""
    byId("adminNumberOfQ0Id").textContent = ""
    byId("adminNumberOfNoAssignedId").textContent = ""

    byId("adminPreviousId").disabled = true;
    byId("adminNextId").disabled = true;
    byId("adminUpdateId").disabled = true;

    fetch("/administration/info?" + new URLSearchParams({
        sourceId: sourceId,
        nightId: nightId,
    }), { method: "GET" })
        .then(function (response) {
            if (response.ok) {
                return response.json();
            } else {
                return Promise.reject(response);
            }
        })
        .then(function (json) {

            byId("adminMonitoringNightId").textContent = json.monitoringNight
            byId("adminDirPathId").textContent = json.dirPath
            byId("adminNumberOfSoundFilesId").textContent = json.numberOfSoundFiles
            byId("adminNumberOfQ0Id").textContent = json.numberOfQ0
            byId("adminNumberOfNoAssignedId").textContent = json.numberOfNoAssigned

            byId("adminPreviousId").disabled = false;
            byId("adminNextId").disabled = false;
            byId("adminUpdateId").disabled = false;
        })
        .catch(function (err) {
            console.warn("Error in javascript fetch: ", err);
        })
};

async function adminExecuteCommand(sourceId, nightId, command) {
    fetch("/administration/command?" + new URLSearchParams({
        sourceId: sourceId,
        nightId: nightId,
        command: command,
    }), { method: "POST" })
        .then(function (response) {
            if (response.ok) {
                return response.json();
            } else {
                return Promise.reject(response);
            }
        })
        .then(function (json) {
            if (json.command == "createReport") {
                reportSrc = "/administration/downloads/report?";
                reportSrc += "sourceId=";
                reportSrc += json.sourceId;
                reportSrc += "&nightId=";
                reportSrc += json.nightId;
                // Create temporary element.
                let hidden_a = document.createElement('a');
                hidden_a.setAttribute('href', reportSrc);
                hidden_a.setAttribute('download', json.report_name);
                document.body.appendChild(hidden_a);
                hidden_a.click();
                document.body.removeChild(hidden_a);
            }
        })
        .catch(function (err) {
            console.warn("Error in javascript fetch: ", err);
        })
};
