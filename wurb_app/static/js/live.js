
function liveAudioToggleSettings() {
    if ($("#liveaudio-settings-id").hasClass("is-hidden")) {
        // $("#liveaudio-boddy-id").addClass("is-hidden")
        $("#liveaudio-settings-id").removeClass("is-hidden")
        $("#liveaudio-show-settings-text-id").text("Hide settings")
    } else {
        $("#liveaudio-settings-id").addClass("is-hidden")
        // $("#liveaudio-boddy-id").removeClass("is-hidden")
        $("#liveaudio-show-settings-text-id").text("Show settings")
    };
}

function liveVisualToggleSettings() {
    if ($("#livevisual-settings-id").hasClass("is-hidden")) {
        // $("#livevisual-boddy-id").addClass("is-hidden")
        $("#livevisual-settings-id").removeClass("is-hidden")
        $("#livevisual-show-settings-text-id").text("Hide settings")
    } else {
        $("#livevisual-settings-id").addClass("is-hidden")
        // $("#livevisual-boddy-id").removeClass("is-hidden")
        $("#livevisual-show-settings-text-id").text("Show settings")
    };
}
