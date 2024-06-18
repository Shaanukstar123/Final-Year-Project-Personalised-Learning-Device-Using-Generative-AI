// keyboard.js
const KioskBoard = require('kioskboard');

// Initialize KioskBoard
KioskBoard.init({
    keysArrayOfObjects: null,
    keysJsonUrl: null,
    keysSpecialCharsArrayOfStrings: null,
    keysJsonUrl: 'kioskboard-keys-english.json',
    keysNumpadArrayOfNumbers: null,
    language: 'en',
    theme: 'light',
    autoScroll: true,
    capsLockActive: true,
    allowRealKeyboard: false,
    allowMobileKeyboard: false,
    cssAnimations: true,
    cssAnimationsDuration: 360,
    cssAnimationsStyle: 'slide',
    keysAllowSpacebar: true,
    keysSpacebarText: 'Space',
    keysFontFamily: 'sans-serif',
    keysFontSize: '22px',
    keysFontWeight: 'normal',
    keysIconSize: '25px',
    keysEnterText: 'Enter',
    keysEnterCallback: undefined,
    keysEnterCanClose: true,
});

// Function to run KioskBoard on input elements with the class 'js-virtual-keyboard'
const runKioskBoard = () => {
    KioskBoard.run('.js-virtual-keyboard');
};

module.exports = { runKioskBoard };
