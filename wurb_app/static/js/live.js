
function liveAudioToggleSettings() {
    if (byId("liveaudioSettingsId").classList.contains("is-hidden")) {
        byId("liveaudioSettingsId").classList.remove("is-hidden")
        byId("liveaudioShowSettingsTextId").textContent = "Hide settings"
    } else {
        byId("liveaudioSettingsId").classList.add("is-hidden")
        byId("liveaudioShowSettingsTextId").textContent = "Show settings"
    };
}

function liveVisualToggleSettings() {
    if (byId("livevisualSettingsId").classList.contains("is-hidden")) {
        byId("livevisualSettingsId").classList.remove("is-hidden")
        byId("livevisualShowSettingsTextId").textContent = "Hide settings"
    } else {
        byId("livevisualSettingsId").classList.add("is-hidden")
        byId("livevisualShowSettingsTextId").textContent = "Show settings"
    };
}
