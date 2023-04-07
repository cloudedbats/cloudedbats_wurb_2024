
function byId(id) {
    return document.getElementById(id);
};

function hideModules() {
    byId("moduleRecordId").classList.remove("is-inverted");
    byId("moduleLiveId").classList.remove("is-inverted");
    byId("moduleAnnotationsId").classList.remove("is-inverted");
    byId("moduleAdminId").classList.remove("is-inverted");
    byId("heroBodyRecordId").classList.add("is-hidden");
    byId("heroBodyLiveId").classList.add("is-hidden");
    byId("heroBodyAnnotationsId").classList.add("is-hidden");
    byId("heroBodyAdminId").classList.add("is-hidden");
    byId("heroBodyAboutId").classList.add("is-hidden");
};

function activateModuleRecord() {
    hideModules();
    byId("moduleRecordId").classList.add("is-inverted");
    byId("heroBodyRecordId").classList.remove("is-hidden");
};

function activateModuleLive() {
    hideModules();
    byId("moduleLiveId").classList.add("is-inverted");
    byId("heroBodyLiveId").classList.remove("is-hidden");
};

function activateModuleAnnotations() {
    hideModules()
    byId("moduleAnnotationsId").classList.add("is-inverted");
    byId("heroBodyAnnotationsId").classList.remove("is-hidden");
};

function activateModuleAdministration() {
    hideModules()
    byId("moduleAdminId").classList.add("is-inverted");
    byId("heroBodyAdminId").classList.remove("is-hidden");
};

function activateModuleAbout() {
    hideModules()
    // byId("moduleAdminId").classList.add("is-inverted");
    byId("heroBodyAboutId").classList.remove("is-hidden");
};

function fetchModuleRecord() {
    hideModules()
    fetch("/pages/record", { method: "GET" })
        .then(function (response) {
            if (response.ok) {
                return response.text();
            } else {
                return Promise.reject(response);
            }
        })
        .then(function (html) {
            byId("heroBodyRecordId").innerHTML = html;
            byId("moduleRecordId").classList.remove("is-inverted");



            activateModuleRecord()




        })
        .catch(function (err) {
            console.warn("Something went wrong.", err);
        })
};

function fetchModuleLive() {
    hideModules()
    fetch("/pages/live", { method: "GET" })
        .then(function (response) {
            if (response.ok) {
                return response.text();
            } else {
                return Promise.reject(response);
            }
        })
        .then(function (html) {
            byId("heroBodyLiveId").innerHTML = html;
            byId("moduleLiveId").classList.remove("is-inverted");
        })
        .catch(function (err) {
            console.warn("Something went wrong.", err);
        })
};

function fetchModuleAnnotations() {
    hideModules()
    fetch("/pages/annotations", { method: "GET" })
        .then(function (response) {
            if (response.ok) {
                return response.text();
            } else {
                return Promise.reject(response);
            }
        })
        .then(function (html) {
            byId("heroBodyAnnotationsId").innerHTML = html;
            byId("moduleAnnotationsId").classList.remove("is-inverted");

            annoSourceLoad()

        })
        .catch(function (err) {
            console.warn("Something went wrong.", err);
        })
};

function fetchModuleAdministration() {
    hideModules()
    fetch("/pages/admin", { method: "GET" })
        .then(function (response) {
            if (response.ok) {
                return response.text();
            } else {
                return Promise.reject(response);
            }
        })
        .then(function (html) {
            byId("heroBodyAdminId").innerHTML = html;
            byId("moduleAdminId").classList.remove("is-inverted");
        })
        .catch(function (err) {
            console.warn("Something went wrong.", err);
        })
};

function fetchModuleAbout() {
    hideModules()
    fetch("/pages/about", { method: "GET" })
        .then(function (response) {
            if (response.ok) {
                return response.text();
            } else {
                return Promise.reject(response);
            }
        })
        .then(function (html) {
            byId("heroBodyAboutId").innerHTML = html;
        })
        .catch(function (err) {
            console.warn("Something went wrong.", err);
        })
};

// Called from body onLoad.
function fetchModules() {
    setTimeout(fetchAllModules, 1000);
    // setTimeout(loadWebsocket, 1500);
};

function fetchAllModules() {
    fetchModuleRecord();
    fetchModuleLive();
    fetchModuleAnnotations();
    fetchModuleAdministration();
    fetchModuleAbout();

    setTimeout(loadWebsocket, 5000);
};

function loadWebsocket() {

    audioFeedbackSliders();

    var ws_url = (window.location.protocol === "https:") ? "wss://" : "ws://"
    ws_url += window.location.host // Note: Host includes port.
    ws_url += "/record/ws";
    startWebsocket(ws_url);
    //alert("Onload done...")
}
