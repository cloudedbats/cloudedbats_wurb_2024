
function liveAudioToggleSettings() {
    if (byId("liveaudio-settings-id").classList.contains("is-hidden")) {
        byId("liveaudio-settings-id").classList.remove("is-hidden")
        byId("liveaudio-show-settings-text-id").textContent = "Hide settings"
    } else {
        byId("liveaudio-settings-id").classList.add("is-hidden")
        byId("liveaudio-show-settings-text-id").textContent = "Show settings"
    };
}

function liveVisualToggleSettings() {
    if (byId("livevisual-settings-id").classList.contains("is-hidden")) {
        byId("livevisual-settings-id").classList.remove("is-hidden")
        byId("livevisual-show-settings-text-id").textContent = "Hide settings"
    } else {
        byId("livevisual-settings-id").classList.add("is-hidden")
        byId("livevisual-show-settings-text-id").textContent = "Show settings"
    };
}
