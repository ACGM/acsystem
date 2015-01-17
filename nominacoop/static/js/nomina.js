(function (_) {

  angular.module('cooperativa.nomina', ['ngAnimate'])
    
    .factory('NominaService', ['$http', '$q', '$filter', function ($http, $q, $filter) {

      // Retornar las nominas generadas
      function nominasGeneradas() {
        var deferred = $q.defer();

        $http.get('/api/nominasgeneradas/?format=json')
          .success(function (data) {
            deferred.resolve(data);
          });

          return deferred.promise;
      }

      // Retornar los tipos de nominas
      function tiposNominas() {
        var deferred = $q.defer();

        $http.get('/api/tiposnomina/?format=json')
          .success(function (data) {
            deferred.resolve(data);
          });

          return deferred.promise;
      }


      //Generar nomina (parametros: Fecha y Tipo de Nomina [y Nota])
      function generaNomina(fecha, tipo, quincena, nota) {
        var deferred = $q.defer();

        $http.post('/nomina/generar/', JSON.stringify({'fechaNomina': fecha, 'tipoNomina': tipo, 'quincena': quincena, 'nota': nota})).
          success(function (data) {
            deferred.resolve(data);
          }).
          error(function (data) {
            deferred.resolve(data);
          });

        return deferred.promise;

      }

      return {
        nominasGeneradas: nominasGeneradas,
        generaNomina: generaNomina,
        tiposNominas: tiposNominas
      };

    }])

    //****************************************************
    //CONTROLLERS                                        *
    //****************************************************
    .controller('GeneraNominaCtrl', ['$scope', 'NominaService', function ($scope, NominaService) {
      $scope.showGN = true;
      $scope.nominaH = {};

      // Mostrar/Ocultar panel de Generar Nomina
      $scope.toggleGN = function() {
        $scope.showGN = !$scope.showGN;
      }

      //Generar la nomina
      $scope.generarNomina = function() {
        try {
          if ($scope.FormGeneraNomina.$valid) {
            var fecha = $scope.nominaH.fechaNomina;
            var tipo = $scope.nominaH.tipoNomina;
            var nota = $scope.nominaH.nota != undefined? $scope.nominaH.nota : '';
            var quincena = 0;

            if (quincena =0) {
              quincena =1;
            }
            
            NominaService.generaNomina(fecha,tipo,quincena,nota).then(function (data) {
              console.log(data);
            });
          } else {
            throw "Verifique que ha completado toda la información requerida.";

          }

        } catch (e) {
          console.log(e);
        }
      }

      $scope.tiposNominas = function() {
        NominaService.tiposNominas().then(function (data) {
          $scope.tiposN = data;
        });
      }

    }])



    .controller('ConsultarNominaCtrl', ['$scope', 'NominaService', function ($scope, NominaService) {
      $scope.showCN = true;

      // Mostrar/Ocultar panel de Consultar Nomina
      $scope.toggleCN = function() {
        $scope.showCN = !$scope.showCN;
      }


      // Todas las nominas generadas
      $scope.getNominasGeneradas = function() {
        NominaService.nominasGeneradas().then(function (data) {
          $scope.nominas = data;
        });
      }

    }])

    .controller('DetalleNominaCtrl', ['$scope', function ($scope) {
      

    }])

})(_);