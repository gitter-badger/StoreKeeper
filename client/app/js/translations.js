angular.module('gettext').run(['gettextCatalog', function (gettextCatalog) {
/* jshint -W100 */
    gettextCatalog.setStrings('hu', {"Auth check":"Bejelentkezés ellenőrzése","Enter search query":"Keresési kifejetés","Error {{status}}":"Hiba {{status}}","LogOut":"Kijelentkezés","Login":"Bejelentkezés","Main":"Főoldal","Password":"Jelszó","Remember me":"Emlékezz rám","Search:":"Keresés:","Sign in":"Bejelentkezés","The user's password is required":"A jelszót kötelező megadni","The user's username is required":"A felhasználónevet kötelező megadni","Username":"Felhasználónév","Welcome {{session.username}}!":"Üdvözöllek {{session.username}}!"});
/* jshint +W100 */
}]);