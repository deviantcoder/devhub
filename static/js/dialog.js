; (function () {
    const modal = new bootstrap.Modal(document.getElementById("modal"))

    htmx.on("htmx:afterSwap", (e) => {
        if (e.detail.target.id == "dialog") {
            modal.show()
        }
    })

    htmx.on("htmx:beforeSwap", (e) => {
        if (e.detail.target.id == "dialog" && !e.detail.xhr.response) {
            modal.hide()
            e.detail.shouldSwap = false
        }
    })

    htmx.on("hidden.bs.modal", () => {
        document.getElementById("dialog").innerHTML = ""
    })
})()

; (function () {
    const modal = new bootstrap.Modal(document.getElementById("projectModal"))

    htmx.on("htmx:afterSwap", (e) => {
        if (e.detail.target.id == "projectDialog") {
            modal.show()
        }
    })

    htmx.on("htmx:beforeSwap", (e) => {
        if (e.detail.target.id == "projectDialog" && !e.detail.xhr.response) {
            modal.hide()
            e.detail.shouldSwap = false
        }
    })

    htmx.on("hidden.bs.modal", () => {
        document.getElementById("projectDialog").innerHTML = ""
    })
})()