function openNav() {
    document.getElementById("mySidenav").style.width = "350px";
    if (window.innerWidth >= 1000) {
        document.getElementById("main").style.paddingLeft = "350px";
        document.getElementById("menu_btn").style.transform = 'rotate('  + 180 + 'deg)';
    }
    else {
        document.body.style.overflowY = "hidden";
        document.getElementById("menu_btn").style.display = "none";
    }
    isOpen = true
}

function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
    if (window.innerWidth <= 1000) {
        document.getElementById("main").style.paddingLeft = "5";
    }
    else {
        document.getElementById("menu_btn").style.transform = 'rotate(' + 0+ 'deg)';
        document.getElementById("main").style.paddingLeft = "0";
    }
    document.getElementById("menu_btn").style.display = "block";
    document.body.style.overflowY = "scroll";
    isOpen = false
}

//Двойное нажатие (Больше не используется)
let isOpen = false
function navHandler() {
    if (!isOpen) {
        openNav();
    }
    else {
        closeNav();
    }
}