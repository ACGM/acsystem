(function () {

  angular.module('cooperativa.inventario', [])

    .filter('posteo', function() {
      return function (input) {
        if (!input) return "";

        input = input
                .replace('N', false)
                .replace('S', true);
        return input;
      }
    })    

    .factory('InventarioService', ['$http', '$q', '$filter', function ($http, $q, $filter) {

      //Llenar el listado de entradas de inventario
      function all() {
        var deferred = $q.defer();

        $http.get('/api/inventario/?format=json')
          .success(function (data) {
            deferred.resolve(data);
          });

        return deferred.promise;
      }

      //Listado de suplidores
      function suplidores() {
        var deferred = $q.defer();

        $http.get('/api/suplidor/?format=json')
          .success(function (data) {
            deferred.resolve(data);
          });

        return deferred.promise;
      }

      //Buscar un numero de documento en especifico.
      function byNoDoc(NoDoc) {
        var deferred = $q.defer();

        all().then(function (data) {
          var result = data.filter(function (documento) {
            return documento.id == NoDoc;
          });

          if(result.length > 0) {
            deferred.resolve(result);
          } else {
            deferred.reject();
          }
        });

        return deferred.promise;
      }

      //Buscar por tipo de posteo
      function byPosteo(valor){
        var deferred = $q.defer();

        all().then(function (data) {
          var results = data.filter(function (registros) {
            return registros.posteo == valor;
          });

          if(results.length > 0) {
            deferred.resolve(results);
          } else {
            deferred.reject();
          }
        });

        return deferred.promise;
      }

      return {
        all: all,
        byPosteo: byPosteo,
        byNoDoc: byNoDoc,
        suplidores: suplidores
      };

    }])


    .controller('ListadoEntradaInvCtrl', ['$scope','$http', 'InventarioService', function ($scope, $http, InventarioService) {
      $scope.showLEI = true;
      $scope.entradas = {};
      $scope.entradasSeleccionadas = [];
      $scope.reg = [];
      $scope.valoresChk = [];

      $scope.regAll = false;

      //Traer suplidores
      $scope.getSuplidor = function(suplidor) {
        InventarioService.suplidores().then(function (data) {
          $scope.suplidores = data;

        });

      }

      //Listado de todas las entradas de inventario
      $scope.listadoEntradas = function() {
        $scope.entradasSeleccionadas = [];
        $scope.valoresChk = [];
        $scope.regAll = false;

        InventarioService.all().then(function (data) {
          $scope.entradas = data.reverse();

          if(data.length > 0) {
            $scope.verTodos = 'ver-todos-ei';

            var i = 0;
            data.forEach(function (data) {
              $scope.valoresChk[i] = false;
              i++;
            });

          }
        });
      }

      //Buscar una entrada de inventario en especifico
      $scope.filtrarPorNoDoc = function(NoDoc) {
        InventarioService.byNoDoc(NoDoc).then(function (data) {
          $scope.entradas = data;

          if(data.length > 0) {
            $scope.verTodos = '';
          }
        });
      }

      //Filtrar las entradas de inventario por posteo (SI/NO)
      $scope.filtrarPosteo = function() {
        $scope.entradasSeleccionadas = [];
        $scope.valoresChk = [];
        $scope.regAll = false;

        if($scope.posteof != '*') {
          InventarioService.byPosteo($scope.posteof).then(function (data) {
            $scope.entradas = data.reverse();

            if(data.length > 0){
              $scope.verTodos = '';
            }
        });
        } else {
          $scope.listadoEntradas();

        }        
      }


      // Mostrar/Ocultar panel de Listado de Entrada Inventario
      $scope.toggleLEI = function() {
        $scope.showLEI = !$scope.showLEI;
      }


      //Cuando se le de click al checkbox del header.
      $scope.seleccionAll = function() {

        $scope.entradas.forEach(function (data) {
          if (data.posteo == 'N') {
            if ($scope.regAll === true){

              $scope.valoresChk[data.id] = true;
              $scope.entradasSeleccionadas.push(data);
            }
            else{

              $scope.valoresChk[data.id] = false;
              $scope.entradasSeleccionadas.splice(data);
            }
          }

        });
      }

      
      //Cuando se le de click a un checkbox de la lista
      $scope.selectedReg = function(iReg) {
        
        index = $scope.entradas.indexOf(iReg);

        if ($scope.reg[$scope.entradas[index].id] === true){
          $scope.entradasSeleccionadas.push($scope.entradas[index]);
        }
        else{
          $scope.entradasSeleccionadas.splice($scope.entradasSeleccionadas[index],1);
        }
      }


      $scope.postear = function(){

      }

    }])



    .controller('EntradaInvCtrl', ['$scope', function ($scope) {
      $scope.showEI = true;

      // Mostrar/Ocultar panel de Entrada de Inventario
      $scope.toggleEI = function() {
        $scope.showEI = !$scope.showEI;
      }

    }]);

})();