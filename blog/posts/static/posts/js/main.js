window.onload = function(){
    // selectors
    const drawerClose = document.querySelector('.drawer-close-symbol');
    const drawerContainer = document.querySelector('.drawer-container');
    const drawerBtn = document.getElementsByClassName('drawer-btn');
    const drawerOverlay = document.querySelector('.drawer-overlay');

    // by default events
    drawerContainer.hidden=true;
    drawerOverlay.hidden=true;

    // event listener   
    drawerClose.addEventListener('click', toggleDrawer);
    drawerBtn[0].addEventListener('click', toggleDrawer);
    drawerBtn[1].addEventListener('click', toggleDrawer);
    drawerOverlay.addEventListener('click', toggleDrawer)

    // functions
    function toggleDrawer(event){
        let clickedOn = event.target.classList[0];
        // console.log(clickedOn);
        if(clickedOn === "drawer-close-symbol"){
            drawerContainer.hidden=true;
            drawerOverlay.hidden = true;
        }
        if(clickedOn === "drawer-btn"){
            drawerContainer.hidden=false;
            drawerOverlay.hidden = false;

        }
        if(clickedOn === "drawer-overlay"){
            drawerContainer.hidden=true;
            drawerOverlay.hidden=true;
        }
    }
}