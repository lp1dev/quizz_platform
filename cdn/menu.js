(function () {
    window.menu = {}

    window.menu.init = () => {
        window.menu.icon = document.querySelector("#hamburger-icon")
        window.menu.menu = document.querySelector("#menu")

        window.menu.menu.style.display = "none"

        window.menu.icon.onclick = (e) => {
            window.menu.menu.style.display = window.menu.menu.style.display == "none" ? "block" : "none"
            console.log(e)
        }
        return true;
    
    }
})();