

async function getSourceDirs() {
    fetch("/module-admin/get-rec-sources/", { method: "GET" })
    .then(function(response) {
        if (response.ok) {
            return response.json();
        } else {
            return Promise.reject(response);
        }
    })
    .then(function(json) {
        // Populate options to select list.
        var select = byId("anno-select-source-id");
        // Empty.
        while (select.firstChild) {
            select.removeChild(select.firstChild);
        }
        // Add first option.
        var option = document.createElement("option");
        option.textContent = "Please select:";
        option.value = "select";
        select.appendChild(option);
        // Use received json.
        for(var i = 0; i < json.length; i++) {
            var content = json[i];
            var option = document.createElement("option");
            option.textContent = content;
            option.value = content;
            select.appendChild(option);
        }
    })
    .catch(function (err) {
        console.warn("Something went wrong.", err);
    })
};


async function getNightDirs() {
    fetch("/module-admin/get-rec-nights/", { method: "GET" })
    .then(function(response) {
        if (response.ok) {
            return response.json();
        } else {
            return Promise.reject(response);
        }
    })
    .then(function(json) {
        // Populate options to select list.
        var select = byId("anno-select-night-id");
        // Empty.
        while (select.firstChild) {
            select.removeChild(select.firstChild);
        }
        // Add first option.
        var option = document.createElement("option");
        option.textContent = "Please select:";
        option.value = "select";
        select.appendChild(option);
        // Use received json.
        for(var i = 0; i < json.length; i++) {
            var content = json[i];
            var option = document.createElement("option");
            option.textContent = content;
            option.value = content;
            select.appendChild(option);
        }
    })
    .catch(function (err) {
        console.warn("Something went wrong.", err);
    })
};

async function getRecordingInfo() {
    fetch("/module-record/", { method: "GET" })
    .then(function (response) {
        if (response.ok) {
            return response.json();
        } else {
            return Promise.reject(response);
        }
    })
    .then(function (json) {
        byId('hero-body-record-id').innerHTML = html;
        byId("module-record-id").classList.add("is-inverted");
    })
    .catch(function (err) {
        console.warn("Something went wrong.", err);
    })
    // try {
    //     let response = await fetch("/module-admin/get-rec-metadata/");
    //     let rec_info = await response.json();

    //     alert(response)

    // } catch (err) {
    //     alert(`ERROR getEventsDirs: ${err}`);
    //     console.log(err);
    // };
};
