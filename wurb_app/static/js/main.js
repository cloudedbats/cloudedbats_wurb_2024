
var byId = function (id) {
    return document.getElementById(id);
};

function hideModules() {
    byId("module-record-id").classList.remove("is-inverted");
    byId("module-live-id").classList.remove("is-inverted");
    byId("module-annotations-id").classList.remove("is-inverted");
    byId("module-admin-id").classList.remove("is-inverted");
    byId("hero-body-record-id").classList.add("is-hidden");
    byId("hero-body-live-id").classList.add("is-hidden");
    byId("hero-body-annotations-id").classList.add("is-hidden");
    byId("hero-body-admin-id").classList.add("is-hidden");
    byId("hero-body-about-id").classList.add("is-hidden");
};

function activateModuleRecord() {
    hideModules();
    byId("module-record-id").classList.add("is-inverted");
    byId("hero-body-record-id").classList.remove("is-hidden");
};

function activateModuleLive() {
    hideModules();
    byId("module-live-id").classList.add("is-inverted");
    byId("hero-body-live-id").classList.remove("is-hidden");
};

function activateModuleAnnotations() {
    hideModules()
    byId("module-annotations-id").classList.add("is-inverted");
    byId("hero-body-annotations-id").classList.remove("is-hidden");
};

function activateModuleAdministration() {
    hideModules()
    byId("module-admin-id").classList.add("is-inverted");
    byId("hero-body-admin-id").classList.remove("is-hidden");
};

function activateModuleAbout() {
    hideModules()
    // byId("module-about-id").classList.add("is-inverted");
    byId("hero-body-about-id").classList.remove("is-hidden");
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
            byId('hero-body-record-id').innerHTML = html;
            byId("module-record-id").classList.remove("is-inverted");
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
            byId('hero-body-live-id').innerHTML = html;
            byId("module-live-id").classList.remove("is-inverted");
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
            byId('hero-body-annotations-id').innerHTML = html;
            byId("module-annotations-id").classList.remove("is-inverted");

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
            byId('hero-body-admin-id').innerHTML = html;
            byId("module-admin-id").classList.remove("is-inverted");
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
            byId('hero-body-about-id').innerHTML = html;
        })
        .catch(function (err) {
            console.warn("Something went wrong.", err);
        })
};

// Called from body onLoad.
function fetchModules() {
    setTimeout(fetchAllModules, 1000);
};

function fetchAllModules() {
    fetchModuleRecord();
    fetchModuleLive();
    fetchModuleAnnotations();
    fetchModuleAdministration();
    fetchModuleAbout();
};
