(function (_) {

  angular.module('cooperativa.inventarioRPT',['ngAnimate'])

    .factory('InventarioServiceRPT', ['$http', '$q', '$filter', function ($http, $q, $filter) {

      //Llenar el listado de entradas de inventario
      function all() {
        var deferred = $q.defer();

        $http.get('/api/inventario/?format=json')
          .success(function (data) {
            deferred.resolve(data);
          });

        return deferred.promise;
      }

      

      return {
        all : all
      };

    }])


    //****************************************************
    //CONTROLLERS                                        *
    //****************************************************
    .controller('RPTEntradaSalidaArticuloCtrl', ['$scope', '$filter', 'InventarioServiceRPT', function ($scope, $filter, InventarioServiceRPT) {
      console.log('ENTRO AL CONTROLADOR SIN PROBLEMA ALGUNO.')

    }]);

})(_);  