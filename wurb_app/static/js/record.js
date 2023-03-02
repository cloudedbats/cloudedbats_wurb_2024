

function recToggleSettings() {
    if (byId("rec-settings-id").classList.contains("is-hidden")) {
        byId("rec-body-id").classList.add("is-hidden");
        byId("rec-settings-id").classList.remove("is-hidden");
        byId("rec-settings-text-id").textContent = "Hide settings";
    } else {
        byId("rec-settings-id").classList.add("is-hidden");
        byId("rec-body-id").classList.remove("is-hidden");
        byId("rec-settings-text-id").textContent = "Show settings";
    };
}

function geoToggleSettings() {
    if (byId("geo-settings-id").classList.contains("is-hidden")) {
        byId("geo-body-id").classList.add("is-hidden");
        byId("geo-settings-id").classList.remove("is-hidden");
        byId("geo-settings-text-id").textContent = "Hide settings";
    } else {
        byId("geo-settings-id").classList.add("is-hidden");
        byId("geo-body-id").classList.remove("is-hidden");
        byId("geo-settings-text-id").textContent = "Show settings";
    };
}

