import 'bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'jquery-ui-dist/jquery-ui.css';
import generateUUID from './lib';
import mainMenuEvents from './main_menu';
import showModalForm, {switchModalForm, showChangePassErrors} from './form';

require('jquery-ui');

const addEvents = () => {

    mainMenuEvents();

}


$(window).on("load", () => {

    const selectedURI = sessionStorage.getItem('selectedURI');
    if (selectedURI) {
        const mainMenuItems = document.getElementsByClassName('main__menu__item');
        for (var i=0; i < mainMenuItems.length; i++) {
            if (mainMenuItems[i].getAttribute('data-url') == selectedURI) {
                mainMenuItems[i].classList.add('main__menu__item--selected');
                continue;
            }
            if (mainMenuItems[i].classList.contains('main__menu__item--selected')) {
                mainMenuItems[i].classList.remove('main__menu__item--selected');    
            }
        }
    }

});


$(document).ready(() => {

    // login
    const mainAuthForm = 'registration-form';
    showModalForm(mainAuthForm, generateUUID());
    switchModalForm('entry', mainAuthForm, generateUUID());
    switchModalForm('register', mainAuthForm, generateUUID());

    // change pass
    showChangePassErrors();

    // events
    addEvents();
})


import '../scss/main.scss';
import '../scss/index.scss';
