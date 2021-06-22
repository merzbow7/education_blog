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