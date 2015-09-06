(function (_) {

  angular.module('cooperativa.homepage', ['ngAnimate'])
    
    .factory('HomePageService', ['$http', '$q', '$filter', function ($http, $q, $filter) {

      function homepage() {
        return false;
      }

      function getInfoEmpresa() {
        var deferred = $q.defer();
        var url = "/informacionGeneral/";

        $http.get(url)
          .success(function (data) {
            deferred.resolve(data);
          });
        return deferred.promise;
      }

      return {
        homepage: homepage,
        getInfoEmpresa: getInfoEmpresa
      };

    }])

    //****************************************************
    //                                                   *
    //CONTROLLERS                                        *
    //                                                   *
    //****************************************************
    .controller('HomePageCtrl', ['$scope', '$rootScope', '$filter', '$window', 'HomePageService', 
      function ($scope, $rootScope, $filter, $window, HomePageService) {
      
      //Limpiar todas las variables de session en javascript del sessionStorage.
      $window.sessionStorage.clear();
      
      //Llenar con las variables de informacion general sobre la Empresa
      HomePageService.getInfoEmpresa().then(function (data) {
        console.log(data);
        $window.sessionStorage['empresa'] = data[0]['nombre'];
        $window.sessionStorage['localidadS'] = data[0]['localidadS'];
        $window.sessionStorage['localidadL'] = data[0]['localidadL'];
        $window.sessionStorage['RNC'] = data[0]['rnc'];
        $window.sessionStorage['telefono'] = data[0]['telefono'];

      });


    }]);

})(_);