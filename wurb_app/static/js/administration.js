

function adminToggleSettings() {
    if (byId("admin-settings-id").classList.contains("is-hidden")) {
        byId("admin-body-id").classList.add("is-hidden");
        byId("admin-settings-id").classList.remove("is-hidden");
        byId("admin-show-settings-text-id").textContent = "Hide settings";
    } else {
        byId("admin-settings-id").classList.add("is-hidden");
        byId("admin-body-id").classList.remove("is-hidden");
        byId("admin-show-settings-text-id").textContent = "Show settings";
    };
}

