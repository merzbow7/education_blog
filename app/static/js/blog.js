function makeFriendship(_url, user) {
    let action;
    if (this.classList.contains("btn-success")) {
        action = "append";
    } else {
        action = "remove";
    }
    let url = new URL(_url), params = {recipient: user, action: action};
    Object.keys(params).forEach(key => url.searchParams.append(key, params[key]));
    fetch(url)
        .then(response => response.json())
        .then(data => console.log(data));
    this.classList.toggle("btn-success");
    this.classList.toggle("btn-danger");
    this.classList.toggle("bi-person-dash");
    this.classList.toggle("bi-person-plus");
}

function makeSpinner() {
    return '<div className="spinner-border text-warning" role="status"><span className="visually-hidden">Loading...</span></div>'

}

function sleep(miliseconds) {
    let currentTime = new Date().getTime();
    while (currentTime + miliseconds >= new Date().getTime()) {
    }
}


function getPopover() {
    if (!this.popper) {
        let url = "/popover/" + this.textContent;
        fetch(url)
            .then(response => response.text())
            .then(data => {
                let template = "<div class='popover-body p-0' role='tooltip'><div class='popover-body'></div></div>"
                let config = {html: true, content: data, template: template};
                this.popper = new bootstrap.Popover(this, config);
                this.popper.show();
                popperTime();
            });
    } else {
        this.popper.show()
        popperTime();
    }
}


function popperTime() {
    let time = document.querySelector('p.mb-2 span.ms-4 span.flask-moment');
    if (time) {
        time.textContent = moment(time.textContent, "YYYY-MM-DDThh:mm:ssZ").fromNow()
    }

}

function hidePopover() {
    this.popper?.hide()
}

let popoverTriggerList = Array.from(document.querySelectorAll('[data-bs-toggle="popover"]'))
popoverTriggerList.map(function (node) {
    node.onmouseenter = getPopover;
    node.onmouseleave = hidePopover;
})




