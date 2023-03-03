

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

